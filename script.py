import requests, csv, time, os, subprocess, shutil, math, threading, json, platform
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import re

MAX_REPOS       = 2       
MAX_WORKERS     = 2
JAVA_MEM        = "4g"
GIT_TIMEOUT_SEC = 900
CK_TIMEOUT_SEC  = 1800
DELETE_REPO_AFTER = True
IGNORE_DIRS     = ["build/", "target/", ".git/"]

WORKDIR   = Path("work")
REPOS_DIR = WORKDIR / "repos"
CK_OUT_DIR = WORKDIR / "ck_out"
REPOS_DIR.mkdir(parents=True, exist_ok=True)
CK_OUT_DIR.mkdir(parents=True, exist_ok=True)

RESULTS_CSV = Path("ck_summary.csv")
CHECKPOINT  = Path("ck_progress.jsonl")


def resolve_ck_jar() -> str:
    env = os.getenv("CK_JAR")
    if env and Path(env).exists():
        return str(Path(env).resolve())
    roots = [
        Path(__file__).resolve().parent,
        Path.cwd(),
        Path.home() / "Downloads",
        Path.home() / "Documents",
        Path.home() / "Desktop",
    ]
    for root in roots:
        if root.exists():
            for p in root.rglob("ck-*-jar-with-dependencies.jar"):
                return str(p.resolve())
    raise FileNotFoundError(
        "JAR do CK não encontrado. Defina CK_JAR ou coloque o arquivo "
        "ck-*-jar-with-dependencies.jar em: pasta do script, CWD, Downloads, Documents ou Desktop."
    )

def resolve_java_paths(preferred_version: str = "17"):
    system = platform.system().lower()

    def valid(home: Path):
        exe = "java.exe" if system == "windows" else "java"
        jbin = home / "bin" / exe
        return str(jbin) if jbin.exists() else None

    jhome_env = os.getenv("JAVA_HOME")
    if jhome_env:
        jhome = Path(jhome_env).resolve()
        jbin = valid(jhome)
        if jbin:
            return str(jhome), jbin

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
        for base in [Path("/usr/lib/jvm"), Path("/usr/java")]:
            if base.exists():
                for pat in (f"java-{preferred_version}*", f"jdk-{preferred_version}*"):
                    candidates.extend(base.glob(pat))

    else:  # windows
        try:
            out = subprocess.run(["where", "java"], capture_output=True, text=True,
                                 check=False, timeout=4, shell=True)
            if out.returncode == 0:
                for line in out.stdout.splitlines():
                    p = Path(line.strip()).resolve()
                    candidates.append(p.parent.parent)
        except Exception:
            pass
        for env in ("ProgramFiles", "ProgramW6432", "ProgramFiles(x86)"):
            pf = os.environ.get(env)
            if pf:
                candidates.extend(Path(pf).glob(f"Java/jdk-{preferred_version}*"))

    for home in candidates:
        jbin = valid(home)
        if jbin:
            return str(home), jbin

    which = shutil.which("java")
    if which:
        home = Path(which).resolve().parent.parent
        return str(home), which

    raise RuntimeError("Java não encontrado. Instale JDK 17 ou defina JAVA_HOME.")

CK_JAR = resolve_ck_jar()
JAVA_HOME_RESOLVED, JAVA_BIN = resolve_java_paths()

ENV = os.environ.copy()
if JAVA_HOME_RESOLVED:
    ENV["JAVA_HOME"] = JAVA_HOME_RESOLVED
    ENV["PATH"] = str(Path(JAVA_HOME_RESOLVED) / "bin") + os.pathsep + ENV.get("PATH", "")

def safe_name(full_name: str) -> str:
    return full_name.replace("/", "__")

def run(cmd, cwd=None, timeout=None):
    return subprocess.run(cmd, cwd=cwd, check=False, capture_output=True, text=True, env=ENV, timeout=timeout)

IGNORE_BASENAMES = {d.strip("/").lower() for d in IGNORE_DIRS}
def count_java_files(root: Path) -> int:
    cnt = 0
    for p in root.rglob("*.java"):
        if any(seg.lower() in IGNORE_BASENAMES for seg in p.parts):
            continue
        cnt += 1
    return cnt

def resolve_ck_paths(out_dir: Path, repo_name: str):
    class_a  = out_dir / "class.csv"
    method_a = out_dir / "method.csv"
    pref = safe_name(repo_name)
    class_b  = CK_OUT_DIR / f"{pref}class.csv"
    method_b = CK_OUT_DIR / f"{pref}method.csv"

    if class_b.exists() and not class_a.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(class_b), str(class_a))
    if method_b.exists() and not method_a.exists():
        out_dir.mkdir(parents=True, exist_ok=True)
        shutil.move(str(method_b), str(method_a))

    return class_a, method_a

GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
if not GITHUB_TOKEN:
    raise Exception('Defina GITHUB_TOKEN (ex.: export GITHUB_TOKEN=seu_token)')
HEADERS = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {GITHUB_TOKEN}"}

def gh_get(url, max_retries=5, timeout=60):
    delay = 5
    for _ in range(max_retries):
        r = requests.get(url, headers=HEADERS, timeout=timeout)
        if r.status_code == 200:
            return r.json()
        if r.status_code == 403 and "rate limit" in r.text.lower():
            reset = r.headers.get("X-RateLimit-Reset")
            if reset:
                sleep_for = max(0, int(reset) - int(time.time()) + 1)
                print(f"[rate-limit] aguardando {sleep_for}s…")
                time.sleep(sleep_for); continue
        time.sleep(delay); delay = min(delay * 2, 60)
    r.raise_for_status()
    return r.json()

def count_releases(owner_repo: str) -> int | None:
    url = f"https://api.github.com/repos/{owner_repo}/releases?per_page=1&page=1"
    r = requests.get(url, headers=HEADERS, timeout=60)
    if r.status_code != 200:
        return None
    body_count = len(r.json()) if r.headers.get("Content-Type","").startswith("application/json") else 0
    link = r.headers.get("Link", "")
    if 'rel="last"' in link:
        m = re.search(r'[?&]page=(\d+)>;\s*rel="last"', link)
        if m:
            return int(m.group(1))
    return body_count

# ============== OUTPUT THREAD-SAFE ==============
write_lock = threading.Lock()

def append_result(row: dict):
    with write_lock:
        file_exists = RESULTS_CSV.exists()
        fields = ["name","stars","age_years","num_releases","java_files","classes","methods",
                  "loc_total","cbo_avg","dit_avg","lcom_avg","avg_wmc","url","clone_url","created_at","note"]
        with RESULTS_CSV.open("a", newline='', encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            if not file_exists: w.writeheader()
            w.writerow(row)
        with CHECKPOINT.open("a", encoding="utf-8") as ck:
            ck.write(json.dumps({"name": row["name"], "note": row.get("note")}) + "\n")

def already_done() -> set:
    done = set()
    if RESULTS_CSV.exists():
        with RESULTS_CSV.open("r", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                done.add(row["name"])
    return done

# ============== BUSCAR REPOS ==============
repositories = []
for page in range(1, 11):
    data = gh_get(f"https://api.github.com/search/repositories?q=language:Java&sort=stars&order=desc&per_page=100&page={page}")
    if 'items' not in data: break
    for repo in data['items']:
        created_at = repo["created_at"]
        num_releases = count_releases(repo["full_name"])
        age_years = (datetime.now() - datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")).days / 365
        repositories.append({
            "name": repo["full_name"],
            "stars": repo["stargazers_count"],
            "url": repo["html_url"],
            "clone_url": repo["clone_url"],
            "created_at": created_at,
            "age_years": round(age_years, 2),
            "num_releases": num_releases, 
        })
        if len(repositories) >= MAX_REPOS: break
    if len(repositories) >= MAX_REPOS: break

DONE = already_done()

def process_repo(repo):
    name = repo["name"]
    if name in DONE:
        print(f"[skip] {name}"); return

    local_dir = REPOS_DIR / safe_name(name)
    if local_dir.exists(): shutil.rmtree(local_dir, ignore_errors=True)

    print(f"[clone] {name}")
    try:
        r = run(["git","clone","--depth","1", repo["clone_url"], str(local_dir)], timeout=GIT_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"git_timeout"})
        return
    if r.returncode != 0:
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"git_clone_failed"})
        return

    java_files = count_java_files(local_dir)
    if java_files == 0:
        append_result({**repo,"java_files":0,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"no_java_files"})
        if DELETE_REPO_AFTER: shutil.rmtree(local_dir, ignore_errors=True)
        return

    out_dir = CK_OUT_DIR / safe_name(name)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[ck] {name} (java_files={java_files})")
    try:
        r = run([JAVA_BIN, f"-Xmx{JAVA_MEM}", "-jar", CK_JAR,
                 str(local_dir), "true", "0", "false", str(out_dir)], timeout=CK_TIMEOUT_SEC)
    except subprocess.TimeoutExpired:
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"ck_timeout"})
        if DELETE_REPO_AFTER: shutil.rmtree(local_dir, ignore_errors=True)
        return
    if r.returncode != 0:
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"ck_failed"})
        if DELETE_REPO_AFTER: shutil.rmtree(local_dir, ignore_errors=True)
        return

    class_csv, method_csv = resolve_ck_paths(out_dir, name)
    if not class_csv.exists():
        append_result({**repo,"java_files":java_files,"classes":0,"methods":0,"loc_total":0,
                       "cbo_avg":None,"dit_avg":None,"lcom_avg":None,"avg_wmc":None,"note":"no_class_csv"})
        if DELETE_REPO_AFTER: shutil.rmtree(local_dir, ignore_errors=True)
        return

    classes = methods = 0
    avg_wmc = None
    loc_total = 0.0
    cbo_vals, dit_vals, lcom_vals = [], [], []

    with class_csv.open(newline='', encoding="utf-8", errors="ignore") as f:
        rows = list(csv.DictReader(f))
        classes = len(rows)
        if rows:
            keymap = {k.lower(): k for k in rows[0].keys()}

            def num(r, key):
                k = keymap.get(key.lower())
                if not k: return None
                val = r.get(k)
                if val in (None,''): return None
                try: v = float(val)
                except Exception: return None
                return v if math.isfinite(v) else None

            def num_any(r, keys):
                for k in keys:
                    v = num(r, k)
                    if v is not None: return v
                return None

            wmc_vals = [v for v in (num(r,"wmc") for r in rows) if v is not None]
            if wmc_vals: avg_wmc = round(sum(wmc_vals)/len(wmc_vals), 2)

            for rr in rows:
                v = num(rr,"loc");  loc_total += (v or 0.0)
                v = num(rr,"cbo");  cbo_vals.append(v) if v is not None else None
                v = num(rr,"dit");  dit_vals.append(v) if v is not None else None
                v = num_any(rr,["lcom","lcom*"]); lcom_vals.append(v) if v is not None else None

    if method_csv.exists():
        with method_csv.open(newline='', encoding="utf-8", errors="ignore") as f:
            methods = sum(1 for _ in csv.DictReader(f))

    append_result({
        **repo,
        "java_files": java_files,
        "classes": classes,
        "methods": methods,
        "loc_total": int(loc_total),
        "cbo_avg": round(sum(cbo_vals)/len(cbo_vals), 2) if cbo_vals else None,
        "dit_avg": round(sum(dit_vals)/len(dit_vals), 2) if dit_vals else None,
        "lcom_avg": round(sum(lcom_vals)/len(lcom_vals), 2) if lcom_vals else None,
        "avg_wmc": avg_wmc,
        "note": None
    })

    if DELETE_REPO_AFTER:
        shutil.rmtree(local_dir, ignore_errors=True)

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futs = [ex.submit(process_repo, repo) for repo in repositories]
    for _ in as_completed(futs):
        pass

print("\nOK!")