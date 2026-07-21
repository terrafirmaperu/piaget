@echo off
setlocal
set PY=C:\Users\ASUS\Envs\Neo\Scripts\python.exe

echo Usando: %PY%
"%PY%" -c "import sys; print(sys.executable); print(sys.version)"
echo.
echo Instalando dependencias...
"%PY%" -m pip install --upgrade pip
"%PY%" -m pip install -r "%~dp0requirements.txt"
echo.
echo Verificando whitenoise...
"%PY%" -c "import whitenoise; print('whitenoise OK', whitenoise.__version__)"
if errorlevel 1 (
  echo FALLO: whitenoise no se pudo importar.
  pause
  exit /b 1
)
echo.
echo Listo. Ahora en la misma terminal activa Neo y corre:
echo   python manage.py runserver
echo.
pause
