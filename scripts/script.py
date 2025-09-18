import requests, csv, time, os, subprocess, shutil, math, threading, json, platform
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

# Configurações principais do script
MAX_REPOS       = 1000       # Quantidade máxima de repositórios para analisar
MAX_WORKERS     = 2          # Número de threads para processamento paralelo (limitado para evitar rate limiting)
JAVA_MEM        = "4g"       # Memória alocada para a JVM ao executar o CK
GIT_TIMEOUT_SEC = 900        # Timeout para operações de git clone (15 minutos)
CK_TIMEOUT_SEC  = 1800       # Timeout para execução do CK (30 minutos)
DELETE_REPO_AFTER = True     # Remove repositórios locais após análise para economizar espaço
IGNORE_DIRS     = ["build/", "target/", ".git/"]  # Diretórios que devem ser ignorados na análise

# Estrutura de diretórios para organizar os dados coletados
WORKDIR   = Path("work")                    # Diretório principal de trabalho
REPOS_DIR = WORKDIR / "repos"               # Onde os repositórios clonados serão armazenados
CK_OUT_DIR = WORKDIR / "ck_out"            # Onde os resultados do CK serão salvos
REPOS_DIR.mkdir(parents=True, exist_ok=True)    # Cria os diretórios se não existirem
CK_OUT_DIR.mkdir(parents=True, exist_ok=True)

# Arquivos de saída e controle
RESULTS_CSV = Path("ck_summary.csv")        # Arquivo final com todas as métricas coletadas
CHECKPOINT  = Path("ck_progress.jsonl")     # Log de progresso para permitir retomada em caso de interrupção


def resolve_ck_jar() -> str:
    # Verifica primeiro se o usuário definiu explicitamente onde está o JAR
    env = os.getenv("CK_JAR")
    if env and Path(env).exists():
        return str(Path(env).resolve())
    
    # Lista de diretórios onde é comum encontrar o arquivo JAR
    roots = [
        Path(__file__).resolve().parent,    # Mesmo diretório do script
        Path.cwd(),                         # Diretório atual de trabalho
        Path.home() / "Downloads",          # Downloads do usuário
        Path.home() / "Documents",          # Documentos do usuário
        Path.home() / "Desktop",            # Desktop do usuário
    ]
    
    # Busca recursiva pelo arquivo JAR em cada diretório
    for root in roots:
        if root.exists():
            for p in root.rglob("ck-*-jar-with-dependencies.jar"):
                return str(p.resolve())
    
    # Se não encontrou o JAR em lugar nenhum, falha com uma mensagem explicativa
    raise FileNotFoundError(
        "JAR do CK não encontrado. Defina CK_JAR ou coloque o arquivo "
        "ck-*-jar-with-dependencies.jar em: pasta do script, CWD, Downloads, Documents ou Desktop."
    )

def resolve_java_paths(preferred_version: str = "17"):
    # Obtém o sistema operacional atual em letras minúsculas
    system = platform.system().lower()

    def valid(home: Path):
        # Define o nome do executável do Java conforme o sistema operacional
        exe = "java.exe" if system == "windows" else "java"
        # Monta o caminho completo para o executável dentro do diretório 'bin' da instalação Java
        jbin = home / "bin" / exe
        # Retorna o caminho como string se o executável existir, senão retorna None
        return str(jbin) if jbin.exists() else None

    # Primeiro tenta usar JAVA_HOME se estiver definido
    jhome_env = os.getenv("JAVA_HOME")
    if jhome_env:
        jhome = Path(jhome_env).resolve()
        jbin = valid(jhome)
        if jbin:
            return str(jhome), jbin

    # Lista de candidatos a instalação Java, específica por SO
    candidates = []

    if system == "darwin":  # macOS
        try:
            out = subprocess.run(
                ["/usr/libexec/java_home", "-v", preferred_version],
                capture_output=True, text=True, check=False, timeout=4
            )
            if out.returncode == 0 and out.stdout.strip():
                candidates.append(Path(out.stdout.strip()))
        except Exception:
            pass
        
        # Também verifica instalações via Homebrew
        try:
            out = subprocess.run(
                ["brew", "--prefix", f"openjdk@{preferred_version}"],
                capture_output=True, text=True, check=False, timeout=4
            )
            if out.returncode == 0 and out.stdout.strip():
                candidates.append(Path(out.stdout.strip()) / "libexec/openjdk.jdk/Contents/Home")
        except Exception:
            pass

    elif system == "linux":
        # No Linux, verifica o Java no PATH e o sistema alternatives
        which = shutil.which("java")
        if which:
            candidates.append(Path(which).resolve().parent.parent)

        try:
            out = subprocess.run(
                ["update-alternatives", "--list", "java"],
                capture_output=True, text=True, check=False, timeout=4
            )
            if out.returncode == 0:
                for line in out.stdout.splitlines():
                    p = Path(line.strip()).resolve()
                    candidates.append(p.parent.parent)
        except Exception:
            pass
            
        # Diretórios padrão de instalação Java no Linux
        for base in [Path("/usr/lib/jvm"), Path("/usr/java")]:
            if base.exists():
                for pat in (f"java-{preferred_version}*", f"jdk-{preferred_version}*"):
                    candidates.extend(base.glob(pat))

    else:  # Windows
        # No Windows, usa o comando 'where' para localizar java.exe
        try:
            out = subprocess.run(["where", "java"], capture_output=True, text=True,
                                 check=False, timeout=4, shell=True)
            if out.returncode == 0:
                for line in out.stdout.splitlines():
                    p = Path(line.strip()).resolve()
                    candidates.append(p.parent.parent)
        except Exception:
            pass
            
        # Verifica diretórios padrão do Windows
        for env in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
            pf = os.environ.get(env)
            if pf:
                candidates.extend(Path(pf).glob(f"Java/jdk-{preferred_version}*"))

    # Testa cada candidato para ver se é uma instalação válida
    for home in candidates:
        jbin = valid(home)
        if jbin:
            return str(home), jbin

    # Como último recurso, usa o Java do PATH se disponível
    which = shutil.which("java")
    if which:
        home = Path(which).resolve().parent.parent
        return str(home), which

    # Se chegou até aqui, não encontrou Java instalado
    raise RuntimeError("Java não encontrado. Instale JDK 17 ou defina JAVA_HOME.")

# Inicialização das dependências principais
# Aqui localizamos e configuramos as ferramentas necessárias antes de começar o processamento
CK_JAR = resolve_ck_jar()                           # Localiza o arquivo JAR da ferramenta CK
JAVA_HOME_RESOLVED, JAVA_BIN = resolve_java_paths() # Localiza a instalação do Java

# Configuração do ambiente de execução
ENV = os.environ.copy()
if JAVA_HOME_RESOLVED:
    ENV["JAVA_HOME"] = JAVA_HOME_RESOLVED
    ENV["PATH"] = str(Path(JAVA_HOME_RESOLVED) / "bin") + os.pathsep + ENV.get("PATH", "")

def safe_name(full_name: str) -> str:
    return full_name.replace("/", "__")

def run(cmd, cwd=None, timeout=None):
    #Função auxiliar para executar comandos de sistema . Centraliza a configuração de ambiente e tratamento de erros para subprocessos.
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True, env=ENV, timeout=timeout)

# Preparação para filtragem de diretórios
# Converto a lista de diretórios a ignorar para um conjunto de nomes em lowercase
# Isso torna a verificação mais eficiente e case-insensitive
IGNORE_BASENAMES = {d.strip("/").lower() for d in IGNORE_DIRS}

def count_java_files(root: Path) -> int:
    #Conta recursivamente o número de arquivos .java em um diretório, excluindo diretórios que sabemos que contêm código gerado ou irrelevante.
    #Esta função é importante para avaliar se vale a pena analisar um repositório e também serve como métrica de tamanho do projeto.

    cnt = 0
    for p in root.rglob("*.java"):  # Busca recursiva por todos os arquivos .java
        # Verifica se alguma parte do caminho está na lista de diretórios ignorados
        if any(seg.lower() in IGNORE_BASENAMES for seg in p.parts):
            continue
        cnt += 1
    return cnt

def loc_breakdown(root: Path) -> dict:
    #Calcula métricas detalhadas de linhas de código (LOC) para arquivos Java.
    # Esta função implementa um parser simples para distinguir entre:
    # - Linhas de código executável
    # - Linhas de comentário
    # - Linhas em branco

    totals = {"loc_total_src": 0, "loc_code": 0, "loc_comment": 0, "loc_blank": 0, "comment_pct": None}

    def ignored(p: Path) -> bool:
        #Verifica se um arquivo deve ser ignorado baseado em seu caminho
        return any(seg.lower() in IGNORE_BASENAMES for seg in p.parts)

    # Processa cada arquivo .java no diretório
    for file in root.rglob("*.java"):
        if ignored(file): 
            continue
        try:
            with file.open("r", encoding="utf-8", errors="ignore") as f:
                in_block = False  # Controla se estamos dentro de um comentário de bloco /* */
                
                # Analisa o arquivo linha por linha
                for line in f:
                    totals["loc_total_src"] += 1
                    
                    # Linha vazia
                    if not line.strip():
                        totals["loc_blank"] += 1
                        continue

                    # Parser simples para distinguir código de comentários
                    i = 0
                    n = len(line)
                    in_string = False      # Dentro de uma string "..."
                    in_char = False        # Dentro de um literal de caractere '...'
                    escape = False         # Próximo caractere está escaped com \

                    has_code = False           # Se a linha contém código executável
                    has_comment_token = False  # Se a linha contém tokens de comentário

                    # Percorre cada caractere da linha
                    while i < n:
                        ch = line[i]
                        nxt = line[i+1] if i+1 < n else ""

                        # Estados para lidar com strings e escapes
                        if in_string:
                            if escape: 
                                escape = False
                            elif ch == "\\":
                                escape = True
                            elif ch == '"':
                                in_string = False
                            i += 1
                            continue

                        if in_char:
                            if escape: 
                                escape = False
                            elif ch == "\\":
                                escape = True
                            elif ch == "'":
                                in_char = False
                            i += 1
                            continue

                        # Se estamos em comentário de bloco, procura pelo fim */
                        if in_block:
                            has_comment_token = True
                            if ch == "*" and nxt == "/":
                                in_block = False
                                i += 2
                                continue
                            i += 1
                            continue

                        # Detecta início de comentários
                        if ch == "/" and nxt == "/":
                            has_comment_token = True
                            break  # Resto da linha é comentário
                        if ch == "/" and nxt == "*":
                            has_comment_token = True
                            in_block = True
                            i += 2
                            continue
                            
                        # Detecta início de strings
                        if ch == '"':
                            in_string = True
                            i += 1
                            continue
                        if ch == "'":
                            in_char = True
                            i += 1
                            continue
                            
                        # Se chegou aqui e não é espaço, é código
                        if not ch.isspace():
                            has_code = True
                        i += 1

                    # Classifica a linha baseado no que encontramos
                    if has_code:
                        totals["loc_code"] += 1
                    elif has_comment_token or in_block:
                        totals["loc_comment"] += 1
                    else:
                        totals["loc_blank"] += 1
                        
        except Exception:
            # Se der erro ao ler um arquivo, pula
            continue

    # Calcula percentual de comentários
    tot = totals["loc_total_src"]
    if tot > 0:
        totals["comment_pct"] = round(100.0 * totals["loc_comment"] / tot, 2)
    return totals


def resolve_ck_paths(out_dir: Path, repo_name: str):
    # A ferramenta CK às vezes gera arquivos com nomes diferentes dependendo da versão. Esta função padroniza os nomes dos arquivos de saída para facilitar o processamento.

    class_a  = out_dir / "class.csv"
    method_a = out_dir / "method.csv"
    
    # Nomes alternativos que o CK pode usar
    pref = safe_name(repo_name)
    class_b  = CK_OUT_DIR / f"{pref}class.csv"
    method_b = CK_OUT_DIR / f"{pref}method.csv"

    # Move os arquivos para os nomes padronizados se necessário
    if class_b.exists() and not class_a.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(class_b), str(class_a))
    if method_b.exists() and not method_a.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(method_b), str(method_a))

    return class_a, method_a

# Configuração da API do GitHub
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise Exception('Defina a variável de ambiente GITHUB_TOKEN')
HEADERS = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"}

def gh_get(url, max_retries=5, timeout=60):
    #Função para fazer requisições à API do GitHub com tratamento de rate limiting.
    
    delay = 5  # Delay inicial entre tentativas
    
    for _ in range(max_retries):
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        
        # Sucesso, retorna os dados
        if r.status_code == 200:
            return r.json()
            
        # Rate limit atingido, espera até poder tentar novamente
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = r.headers.get("X-RateLimit-Reset")
            if reset:
                # Calcula quanto tempo falta para o reset do rate limit
                sleep_for = max(0, int(reset) - int(time.time()) + 1)
                print(f"[rate-limit] aguardando {sleep_for}s…")
                time.sleep(sleep_for)
                continue
                
        # Outros erros, tenta novamente após delay
        time.sleep(delay)
        delay = min(delay * 2, 60)  # Backoff exponencial limitado a 60s
    
    # Se todas as tentativas falharam, exceção
    r.raise_for_status()
    return r.json()

def count_releases(owner_repo: str) -> int | None:
    #Conta o número de releases de um repositório GitHub.
    
    url = f"https://api.github.com/repos/{owner_repo}/releases?per_page=1&page=1"
    r = requests.get(url, headers=HEADERS, timeout=60)
    
    if r.status_code != 200:
        return None
    
    # Se não há releases, o array estará vazio
    body_count = len(r.json()) if r.headers.get("Content-Type","").startswith("application/json") else 0
    
    # Verifica se há mais páginas através do cabeçalho Link
    link = r.headers.get("Link", "")
    if 'rel="last"' in link:
        # Extrai o número da última página para saber quantas releases existem
        m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', link)
        if m:
            return int(m.group(1))
    
    return body_count

# Thread safety para escrita concorrente
# Como processamos múltiplos repositórios em paralelo, foi preciso garantir que
# apenas uma thread escreva no arquivo CSV por vez para evitar erros
write_lock = threading.Lock()

def append_result(row: dict):
    #Adiciona uma linha de resultados ao arquivo CSV de forma thread-safe.
    #Esta função também mantém um checkpoint em formato JSONL para poder retomar o processamento em caso de interrupção do script.

    with write_lock:  # Garante que apenas uma thread escreva por vez
        file_exists = RESULTS_CSV.exists()
        
        # Define todas as colunas que serão incluídas no CSV final
        fields = [
            "name","stars","age_years","num_releases","java_files",
            "classes","methods",
            "loc_total",
            "loc_total_src","loc_code","loc_comment","loc_blank","comment_pct",
            "cbo_avg","dit_avg","lcom_avg","avg_wmc",
            "url","clone_url","created_at","note"
        ]

        # Escreve no arquivo CSV
        with RESULTS_CSV.open("a", newline='', encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            if not file_exists: 
                w.writeheader()  # Escreve cabeçalho apenas na primeira vez
            w.writerow(row)
            
        # Mantém checkpoint para poder retomar processamento
        with CHECKPOINT.open("a", encoding="utf-8") as ck:
            ck.write(json.dumps({"name": row["name"], "note": row.get("note")}) + "\n")

def already_done() -> set:
    #Verifica quais repositórios já foram processados anteriormente.
    #Isso permite retomar o processamento de onde parou em caso de interrupção, sem ter que recomeçar do zero.

    done = set()
    if RESULTS_CSV.exists():
        with RESULTS_CSV.open("r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["name"])
    return done

# Fase 1: Coleta de repositórios populares, pegamos os repositórios Java mais populares do GitHub ordenados por número de estrelas
# Uso paginação para coletar até MAX_REPOS repositórios
print("Coletando repositórios da API do GitHub...")
repositories_basic = []

for page in range(1, 11):  # Máximo 10 páginas (1000 repositórios)
    data = gh_get(f"https://api.github.com/search/repositories?q=language:Java&sort=stars&order=desc&per_page=100&page={page}")
    
    if 'items' not in data: 
        break
    
    for repo in data['items']:
        repositories_basic.append({
            "name": repo["full_name"],           # Nome do repositório 
            "stars": repo["stargazers_count"],   # Número de estrelas
            "url": repo["html_url"],             # URL para visualizar no GitHub
            "clone_url": repo["clone_url"],      # URL para clonar o repositório
            "created_at": repo["created_at"],    # Data de criação
        })
        
        if len(repositories_basic) >= MAX_REPOS: 
            break
    
    if len(repositories_basic) >= MAX_REPOS: 
        break

print(f"Coletados {len(repositories_basic)} repositórios básicos")


# Fase 2: Enriquecimento dos dados
# Para cada repositório, calculamos informações adicionais que podem ser interessantes
# para a análise, como idade do projeto e número de releases
print("Processando informações adicionais...")
repositories = []

for repo in repositories_basic:
    created_at = repo["created_at"]
    num_releases = count_releases(repo["name"])
    
    # Calcula a idade do projeto em anos
    age_years = (datetime.now() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days / 365
    
    repositories.append({
        "name": repo["name"],
        "stars": repo["stars"],
        "url": repo["url"],
        "clone_url": repo["clone_url"],
        "created_at": created_at,
        "age_years": round(age_years, 2),     # Idade em anos com 2 casas decimais
        "num_releases": num_releases,         # Número de releases publicadas
    })

print(f"Processamento completo: {len(repositories)} repositórios prontos para análise")

# Verifica quais repositórios já foram processados (para permitir retomada)
DONE = already_done()

def process_repo(repo):
        # Função principal que processa um único repositório.
        #
        # Esta função implementa todo o pipeline de análise:
        # 1. Clone do repositório
        # 2. Contagem de arquivos Java
        # 3. Análise de linhas de código
        # 4. Execução da ferramenta CK para métricas
        # 5. Processamento dos resultados
        # 6. Limpeza dos arquivos temporários
    
    name = repo["name"]
    
    # Pula repositórios já processados
    if name in DONE:
        print(f"[skip] {name}")
        return

    # Prepara diretório local para o clone
    local_dir = REPOS_DIR / safe_name(name)
    if local_dir.exists(): 
        shutil.rmtree(local_dir, ignore_errors=True)

    # Etapa 1: Clone do repositório
    print(f"[clone] {name}")
    try:
        # Clone shallow (apenas último commit) 
        r = run(["git","clone","--depth","1", repo["clone_url"], str(local_dir)], timeout=GIT_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        # Se o clone demorar demais, registra timeout e segue para o próximo
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0,
                       **{"loc_total_src": 0, "loc_code": 0, "loc_comment": 0, "loc_blank": 0, "comment_pct": None},
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"git_timeout"})
        return
        
    if r.returncode != 0:
        # Clone falhou por algum motivo (repositório privado, deletado, etc)
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0,
                        **{"loc_total_src": 0, "loc_code": 0, "loc_comment": 0, "loc_blank": 0, "comment_pct": None},
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"git_clone_failed"})
        return

    # Etapa 2: Conta arquivos Java
    java_files = count_java_files(local_dir)

    # Se não tem arquivos Java, não há o que analisar
    if java_files == 0:
        breakdown = {"loc_total_src": 0, "loc_code": 0, "loc_comment": 0, "loc_blank": 0, "comment_pct": None}
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0, **breakdown,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"no_java_files"})
        if DELETE_REPO_AFTER: 
            shutil.rmtree(local_dir, ignore_errors=True)
        return
    
    # Etapa 3: Análise detalhada de linhas de código
    try:
        breakdown = loc_breakdown(local_dir)
    except Exception:
        # Se der erro na análise LOC, usa valores nulos
        breakdown = {"loc_total_src": None, "loc_code": None, "loc_comment": None, "loc_blank": None, "comment_pct": None}
    
    # Etapa 4: Execução da ferramenta CK
    out_dir = CK_OUT_DIR / safe_name(name)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[ck] {name} (java_files={java_files})")
    try:
        # Executa o CK com configurações otimizadas
        r = run([JAVA_BIN, f"-Xmx{JAVA_MEM}", "-jar", CK_JAR,
                 str(local_dir), "true", "0", "false", str(out_dir)], timeout=CK_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        # CK demorou demais, pode acontecer com projetos muito grandes
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                          **breakdown,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"ck_timeout"})
        if DELETE_REPO_AFTER: 
            shutil.rmtree(local_dir, ignore_errors=True)
        return
        
    if r.returncode != 0:
        # CK falhou, pode ser por problema na JVM ou código inválido
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                          **breakdown,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"ck_failed"})
        if DELETE_REPO_AFTER: 
            shutil.rmtree(local_dir, ignore_errors=True)
        return

    # Etapa 5: Processamento dos resultados do CK
    class_csv, method_csv = resolve_ck_paths(out_dir, name)
    
    if not class_csv.exists():
        # CK executou mas não gerou o arquivo esperado
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                        **breakdown,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"no_class_csv"})
        if DELETE_REPO_AFTER: 
            shutil.rmtree(local_dir, ignore_errors=True)
        return

    # Inicialização das variáveis para coletar métricas
    classes = methods = 0
    avg_wmc = None
    loc_total = 0.0
    cbo_vals, dit_vals, lcom_vals = [], [], []

    # Processa o arquivo de métricas de classe
    with class_csv.open(newline='', encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f))
        classes = len(rows)
        
        if rows:
            # Cria mapeamento case-insensitive das colunas
            # Isso é necessário porque diferentes versões do CK podem usar casing diferente
            keymap = {k.lower(): k for k in rows[0].keys()}

            def num(r, key):
                """Extrai um valor numérico de uma linha, tratando casos especiais"""
                k = keymap.get(key.lower())
                if not k: return None
                val = r.get(k)
                if val in (None,''): return None
                try: 
                    v = float(val)
                except Exception: 
                    return None
                # Filtra valores infinitos que podem ocorrer em divisões por zero
                return v if math.isfinite(v) else None

            def num_any(r, keys):
                """Tenta extrair um valor de qualquer uma das chaves fornecidas"""
                for k in keys:
                    v = num(r, k)
                    if v is not None: return v
                return None

            # Coleta métricas WMC
            wmc_vals = [v for v in (num(r,"wmc") for r in rows) if v is not None]
            if wmc_vals: 
                avg_wmc = round(sum(wmc_vals)/len(wmc_vals), 2)

            # Coleta outras métricas para cada classe
            for rr in rows:
                v = num(rr,"loc");  loc_total += (v or 0.0)           # Lines of Code
                v = num(rr,"cbo");  cbo_vals.append(v) if v is not None else None     # Coupling Between Objects
                v = num(rr,"dit");  dit_vals.append(v) if v is not None else None     # Depth of Inheritance Tree
                v = num_any(rr,["lcom","lcom*"]); lcom_vals.append(v) if v is not None else None  # Lack of Cohesion

    # Conta métodos se o arquivo existir
    if method_csv.exists():
        with method_csv.open(newline='', encoding="utf-8", errors="ignore") as f:
            methods = sum(1 for _ in csv.DictReader(f))

    # Registra resultado final com todas as métricas coletadas
    append_result({
        **repo,
        "java_files": java_files,
        "classes": classes,
        "methods": methods,
        "loc_total": int(loc_total),
        **breakdown,
        "cbo_avg": round(sum(cbo_vals)/len(cbo_vals), 2) if cbo_vals else None,
        "dit_avg": round(sum(dit_vals)/len(dit_vals), 2) if dit_vals else None,
        "lcom_avg": round(sum(lcom_vals)/len(lcom_vals), 2) if lcom_vals else None,
        "avg_wmc": avg_wmc,
        "note": None  
    })

    # Etapa 6: Limpeza
    if DELETE_REPO_AFTER:
        shutil.rmtree(local_dir, ignore_errors=True)

# Fase 3: Processamento paralelo dos repositórios
# Utilizo ThreadPoolExecutor para processar múltiplos repositórios simultaneamente
# O número de workers é limitado para evitar sobrecarregar a API do GitHub e o sistema
print("\nIniciando processamento paralelo...")

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    # Submete uma tarefa para cada repositório
    futs = [ex.submit(process_repo, repo) for repo in repositories]
    
    # Aguarda todas as tarefas completarem
    for _ in as_completed(futs):
        pass  # O resultado já é tratado dentro de process_repo()

print("\nOK!")
