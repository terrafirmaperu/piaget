"""
Reparación rápida del droplet (distutils + migrate + gunicorn + nginx).
  C:\\Users\\ASUS\\Envs\\Neo\\Scripts\\python.exe _fix_droplet.py
"""
import os
import re
import sys
import time

ROOT = os.path.dirname(os.path.abspath(__file__))
os.chdir(ROOT)
APP_DIR = '/var/www/piaget/app'
ENV_DEPLOY = os.path.join(ROOT, '.env.deploy')


def load_env_file(path):
    data = {}
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, _, v = line.partition('=')
            data[k.strip()] = v.strip().strip('"').strip("'")
    return data


def main():
    try:
        import paramiko
    except ImportError:
        os.system('"{}" -m pip install paramiko'.format(sys.executable))
        import paramiko

    cfg = load_env_file(ENV_DEPLOY)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    print('Conectando...')
    client.connect(
        cfg['DROPLET_IP'],
        username=cfg.get('DROPLET_USER', 'root'),
        password=cfg['DROPLET_PASSWORD'],
        timeout=60,
        allow_agent=False,
        look_for_keys=False,
    )

    def run(cmd, check=True, timeout=900):
        print('>>', cmd[:120] + ('...' if len(cmd) > 120 else ''))
        _i, out, err = client.exec_command(cmd, timeout=timeout, get_pty=True)
        text = (out.read() + err.read()).decode('utf-8', errors='replace')
        code = out.channel.recv_exit_status()
        if text.strip():
            print(text[-3000:] if len(text) > 3000 else text)
        if check and code != 0:
            raise SystemExit('falló ({})'.format(code))
        return code

    # Subir requirements actualizado
    sftp = client.open_sftp()
    sftp.put(os.path.join(ROOT, 'requirements.txt'), APP_DIR + '/requirements.txt')
    sftp.put(
        os.path.join(ROOT, 'deploy', 'digitalocean', 'nginx', 'piaget.conf'),
        '/etc/nginx/sites-available/piaget',
    )
    sftp.put(
        os.path.join(ROOT, 'deploy', 'digitalocean', 'systemd', 'piaget.service'),
        '/etc/systemd/system/piaget.service',
    )
    sftp.close()

    run('apt-get install -y python3-setuptools')
    run('rm -f /etc/nginx/sites-enabled/default')
    run('ln -sfn /etc/nginx/sites-available/piaget /etc/nginx/sites-enabled/piaget')
    run('chown -R www-data:www-data /var/www/piaget')

    run(
        "sudo -u www-data bash -lc '"
        "cd {app} && source venv/bin/activate && "
        "set -a && source .env && set +a && "
        "pip install --upgrade pip setuptools && "
        "pip install -r requirements.txt && "
        "python manage.py migrate --noinput && "
        "python manage.py collectstatic --noinput && "
        "python manage.py ensure_neo && "
        "python manage.py ensure_alumno || true"
        "'".format(app=APP_DIR),
        timeout=1200,
    )

    run('systemctl daemon-reload')
    run('systemctl enable piaget')
    run('systemctl restart piaget')
    run('nginx -t')
    run('systemctl reload nginx')
    time.sleep(2)
    run('systemctl is-active piaget', check=False)
    run('curl -sI http://127.0.0.1/login/ | head -n 15', check=False)
    run('curl -s http://127.0.0.1/ | head -n 25', check=False)
    client.close()
    print('FIX OK — prueba http://{}/login/'.format(cfg['DROPLET_IP']))
    with open(os.path.join(ROOT, 'deploy_status.txt'), 'w', encoding='utf-8') as fh:
        fh.write('OK\nhttp://{}/\n'.format(cfg['DROPLET_IP']))


if __name__ == '__main__':
    main()
