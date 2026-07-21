@echo off
set SRC=%USERPROFILE%\.cursor\projects\c-Users-ASUS-Desktop-sistemas-piayetIa\assets\alumna-huancavelicana.png
set DST=%~dp0static\img\website\alumna-huancavelicana.png
if not exist "%SRC%" (
  echo No se encontro: %SRC%
  pause
  exit /b 1
)
mkdir "%~dp0static\img\website" 2>nul
copy /Y "%SRC%" "%DST%"
echo Copiado a %DST%
pause
