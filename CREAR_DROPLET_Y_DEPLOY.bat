@echo off
cd /d "%~dp0"
echo === Crear droplet Piaget + push GitHub + deploy ===
C:\Users\ASUS\Envs\Neo\Scripts\python.exe -m pip install paramiko -q
C:\Users\ASUS\Envs\Neo\Scripts\python.exe _create_piaget_droplet.py
if errorlevel 1 (
  echo Fallo al crear/ubicar el droplet. Revisa _tmp_do_work.txt
  pause
  exit /b 1
)
C:\Users\ASUS\Envs\Neo\Scripts\python.exe _push_and_deploy.py
if errorlevel 1 (
  echo Fallo push/deploy. Reintentando solo SFTP...
  C:\Users\ASUS\Envs\Neo\Scripts\python.exe _deploy_droplet.py
)
echo.
echo Listo. La IP nueva esta en .env.deploy y en _tmp_do_work.txt
pause
