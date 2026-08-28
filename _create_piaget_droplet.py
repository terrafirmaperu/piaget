"""Diagnose DO droplets and create a new Piaget droplet if needed. No token prints."""
from __future__ import print_function

import json
import os
import re
import ssl
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.abspath(__file__))
PERMISOS = os.path.join(
    os.path.dirname(ROOT),
    "TERRAFIRMA",
    "factora-master",
    "factora-master",
    "app",
    "permisos.txt",
)
ENV_DEPLOY = os.path.join(ROOT, ".env.deploy")
OUT = os.path.join(ROOT, "_tmp_do_work.txt")
CTX = ssl.create_default_context()


def log(msg):
    line = str(msg)
    print(line)
    with open(OUT, "a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def load_env(path):
    data = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, _, v = line.partition("=")
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def token_do():
    text = open(PERMISOS, encoding="utf-8").read()
    m = re.search(r"token DigitalOcean:\s*(\S+)", text)
    if not m:
        raise SystemExit("No DO token")
    return m.group(1).strip()


def api(method, path, token, body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.digitalocean.com/v2" + path,
        data=data,
        method=method,
        headers={
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60, context=CTX) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            parsed = json.loads(raw)
        except Exception:
            parsed = {"raw": raw[:2000]}
        return exc.code, parsed


def public_ip(droplet):
    for n in droplet.get("networks", {}).get("v4", []):
        if n.get("type") == "public":
            return n.get("ip_address")
    return ""


def main():
    open(OUT, "w", encoding="utf-8").write("")
    token = token_do()
    cfg = load_env(ENV_DEPLOY)
    old_ip = cfg.get("DROPLET_IP", "")
    password = cfg["DROPLET_PASSWORD"]

    code, acct = api("GET", "/account", token)
    log("ACCOUNT_HTTP {}".format(code))
    if code != 200:
        log("ACCOUNT_ERR {}".format(acct))
        raise SystemExit(1)
    account = acct.get("account", {})
    log(
        "ACCOUNT {} status={} droplet_limit={}".format(
            account.get("email"),
            account.get("status"),
            account.get("droplet_limit"),
        )
    )

    code, data = api("GET", "/droplets?per_page=100", token)
    droplets = data.get("droplets", [])
    log("DROPLETS count={}".format(len(droplets)))
    found_old = None
    found_piaget = None
    for d in droplets:
        ip = public_ip(d)
        log(
            "DROPLET id={} name={} status={} region={} size={} ip={}".format(
                d["id"],
                d["name"],
                d["status"],
                d["region"]["slug"],
                d.get("size_slug"),
                ip,
            )
        )
        if ip == old_ip:
            found_old = d
        if d["name"] in ("piaget", "jean-piaget", "jean-piaget-ia"):
            found_piaget = d

    code, keys_data = api("GET", "/account/keys", token)
    keys = keys_data.get("ssh_keys", [])
    log("SSH_KEYS count={}".format(len(keys)))
    key_ids = [k["id"] for k in keys]
    for k in keys:
        log("SSH_KEY id={} name={}".format(k["id"], k["name"]))

    if found_old:
        log("OLD_DROPLET_FOUND id={} status={}".format(found_old["id"], found_old["status"]))
        if found_old["status"] != "active":
            log("POWERING_ON old droplet")
            api("POST", "/droplets/{}/actions".format(found_old["id"]), token, {"type": "power_on"})
    else:
        log("OLD_DROPLET_NOT_IN_ACCOUNT ip={}".format(old_ip))

    target = found_piaget
    created = False
    if target and target.get("status") == "active" and public_ip(target):
        log("REUSING_PIAGET_DROPLET id={} ip={}".format(target["id"], public_ip(target)))
    else:
        quoted = json.dumps(password)
        user_data = (
            "#cloud-config\n"
            "disable_root: false\n"
            "ssh_pwauth: true\n"
            "chpasswd:\n"
            "  expire: false\n"
            "  users:\n"
            "    - name: root\n"
            "      password: {quoted}\n"
            "      type: text\n"
            "runcmd:\n"
            "  - sed -i 's/^#\\?PasswordAuthentication.*/PasswordAuthentication yes/' /etc/ssh/sshd_config\n"
            "  - sed -i 's/^#\\?PermitRootLogin.*/PermitRootLogin yes/' /etc/ssh/sshd_config\n"
            "  - systemctl restart ssh || systemctl restart sshd || true\n"
        ).format(quoted=quoted)

        body = {
            "name": "piaget",
            "region": "nyc3",
            "size": "s-1vcpu-1gb",
            "image": "ubuntu-24-04-x64",
            "backups": False,
            "ipv6": False,
            "monitoring": True,
            "tags": ["piaget", "jean-piaget"],
            "user_data": user_data,
        }
        if key_ids:
            body["ssh_keys"] = key_ids

        log("CREATING_DROPLET name=piaget region=nyc3 size=s-1vcpu-1gb")
        code, created_data = api("POST", "/droplets", token, body)
        log("CREATE_HTTP {}".format(code))
        if code not in (201, 202):
            log("CREATE_ERR {}".format(created_data))
            raise SystemExit(2)
        target = created_data["droplet"]
        created = True
        log("CREATED_ID {}".format(target["id"]))

        for i in range(36):
            time.sleep(5)
            code, got = api("GET", "/droplets/{}".format(target["id"]), token)
            target = got.get("droplet") or target
            ip = public_ip(target)
            log("WAIT {} status={} ip={}".format(i + 1, target.get("status"), ip))
            if target.get("status") == "active" and ip:
                break
        else:
            log("DROPLET_NOT_READY")
            raise SystemExit(3)

    ip = public_ip(target)
    log("TARGET_IP {}".format(ip))
    log("CREATED {}".format("yes" if created else "no"))

    if created:
        log("WAITING_CLOUD_INIT 45s")
        time.sleep(45)

    lines = open(ENV_DEPLOY, encoding="utf-8").read().splitlines()
    new_lines = []
    replaced = False
    for line in lines:
        if line.startswith("DROPLET_IP="):
            new_lines.append("DROPLET_IP={}".format(ip))
            replaced = True
        else:
            new_lines.append(line)
    if not replaced:
        new_lines.append("DROPLET_IP={}".format(ip))
    open(ENV_DEPLOY, "w", encoding="utf-8").write("\n".join(new_lines) + "\n")
    log("UPDATED_ENV_DEPLOY")
    log("DONE")


if __name__ == "__main__":
    main()
