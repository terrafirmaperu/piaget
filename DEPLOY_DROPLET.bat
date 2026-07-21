@echo off
cd /d "%~dp0"
echo === Deploy Piaget (push + droplet) ===
C:\Users\ASUS\Envs\Neo\Scripts\python.exe -m pip install paramiko -q
C:\Users\ASUS\Envs\Neo\Scripts\python.exe _push_and_deploy.py
if errorlevel 1 (
  echo Fallo push/deploy. Reintentando solo SFTP...
  C:\Users\ASUS\Envs\Neo\Scripts\python.exe _deploy_droplet.py
)
echo.
echo Web: http://67.205.138.3/
echo Demo: http://67.205.138.3/demo/
echo Login alumno: http://67.205.138.3/sin-limites/ingresar/
pause
