@echo off
setlocal
set PY=C:\Users\ASUS\Envs\Neo\Scripts\python.exe
cd /d "%~dp0"
echo Creando usuario inscrito de prueba...
"%PY%" manage.py ensure_alumno
echo.
echo En Sin limites usa:
echo   Usuario: alumno
echo   Contraseña: Alumno123
echo.
pause
