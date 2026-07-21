@echo off
cd /d "%~dp0"
echo === Reparar droplet Piaget (distutils/setuptools) ===
C:\Users\ASUS\Envs\Neo\Scripts\python.exe -m pip install paramiko -q
C:\Users\ASUS\Envs\Neo\Scripts\python.exe _fix_droplet.py
echo.
echo Abre: http://67.205.138.3/login/
pause
