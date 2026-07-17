"""One-shot GitHub push helper. Not committed to repo."""
import os
import re
import subprocess
import sys

PROJECT_DIR = r"C:\Users\ASUS\Desktop\sistemas\piayetIa"
PERMISOS = r"C:\Users\ASUS\Desktop\sistemas\TERRAFIRMA\factora-master\factora-master\app\permisos.txt"
REPO_URL = "https://github.com/terrafirmaperu/piaget.git"
STATUS_FILE = os.path.join(PROJECT_DIR, "push_status.txt")
LOG_FILE = os.path.join(PROJECT_DIR, "push_run.log")


def log(msg: str) -> None:
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")


def run(cmd: list[str], cwd: str | None = None) -> subprocess.CompletedProcess:
    result = subprocess.run(
        cmd,
        cwd=cwd or PROJECT_DIR,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    log(f"$ {' '.join(cmd)}")
    if result.stdout:
        log(result.stdout.rstrip())
    if result.stderr:
        log(result.stderr.rstrip())
    return result


def read_token() -> str:
    with open(PERMISOS, encoding="utf-8") as f:
        for line in f:
            m = re.match(r"^token GitHub:\s*(.+)$", line.strip())
            if m:
                return m.group(1).strip()
    raise RuntimeError("GitHub token not found in permisos.txt")


def write_status(ok: bool, commit: str = "", method: str = "", error: str = "") -> None:
    lines = ["OK" if ok else "FAIL", f"URL: {REPO_URL}"]
    if commit:
        lines.append(f"Commit: {commit}")
    if method:
        lines.append(f"Method: {method}")
    if error:
        lines.append(f"Error: {error}")
    with open(STATUS_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def main() -> int:
    os.chdir(PROJECT_DIR)
    open(LOG_FILE, "w", encoding="utf-8").close()

    try:
        token = read_token()
        log("Token loaded (redacted)")

        if not os.path.isdir(".git"):
            run(["git", "init"])

        run(["git", "config", "--local", "user.name", "Neo"])
        run(["git", "config", "--local", "user.email", "neo@jeanpiaget.ia"])

        branch = run(["git", "rev-parse", "--abbrev-ref", "HEAD"])
        if branch.returncode != 0 or branch.stdout.strip() in ("", "HEAD"):
            run(["git", "checkout", "-B", "main"])
        elif branch.stdout.strip() != "main":
            run(["git", "checkout", "-B", "main"])

        run(["git", "add", "-A"])
        status = run(["git", "status", "--porcelain"])
        if status.stdout.strip():
            run(["git", "commit", "-m", "Initial commit: Django Jean Piaget project"])

        commit_hash = run(["git", "rev-parse", "HEAD"]).stdout.strip()
        auth_url = f"https://x-access-token:{token}@github.com/terrafirmaperu/piaget.git"

        remote = run(["git", "remote", "get-url", "origin"])
        if remote.returncode == 0:
            run(["git", "remote", "set-url", "origin", auth_url])
        else:
            run(["git", "remote", "add", "origin", auth_url])

        run(["git", "fetch", "origin"])
        remote_main = run(["git", "ls-remote", "--heads", "origin", "main"])
        push_ok = False
        method = ""

        if remote_main.stdout.strip():
            push = run(["git", "push", "-u", "origin", "main"])
            if push.returncode == 0:
                push_ok = True
                method = "direct"
            else:
                run(["git", "fetch", "origin", "main"])
                tree = run(["git", "ls-tree", "-r", "--name-only", "origin/main"])
                files = [x for x in tree.stdout.splitlines() if x.strip()]
                only_readme = len(files) <= 2 and "README.md" in files
                log(f"Remote files: {files!r}, only_readme={only_readme}")

                if only_readme:
                    force = run(["git", "push", "-u", "origin", "main", "--force"])
                    if force.returncode == 0:
                        push_ok = True
                        method = "force (README only)"
                else:
                    rebase = run(["git", "pull", "--rebase", "origin", "main"])
                    if rebase.returncode == 0:
                        push2 = run(["git", "push", "-u", "origin", "main"])
                        if push2.returncode == 0:
                            push_ok = True
                            method = "rebase then push"
        else:
            push = run(["git", "push", "-u", "origin", "main"])
            if push.returncode == 0:
                push_ok = True
                method = "initial push"

        run(["git", "remote", "set-url", "origin", REPO_URL])

        if not push_ok:
            raise RuntimeError("Push failed - see push_run.log")

        write_status(True, commit_hash, method)
        log(f"SUCCESS {method}")
        return 0
    except Exception as exc:
        log(f"ERROR: {exc}")
        write_status(False, error=str(exc))
        return 1


if __name__ == "__main__":
    sys.exit(main())
