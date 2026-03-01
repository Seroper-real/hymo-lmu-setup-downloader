@echo off
REM ==============================================
REM Script per creare l'exe di TrackTitan Downloader
REM ==============================================

REM Imposta il nome dell'exe
SET EXE_NAME=hymo-lmu-setup-downloader

REM Pulizia cartelle build precedenti
IF EXIST build rmdir /s /q build
IF EXIST dist rmdir /s /q dist
IF EXIST %EXE_NAME%.spec del /f /q %EXE_NAME%.spec

REM Crea l'exe con PyInstaller
pyinstaller --onefile --name %EXE_NAME% --paths=src src\main.py

REM Copia eventuali file esterni nella cartella dist
xcopy /Y config\config.json dist\config\
xcopy /Y config\tracks.json dist\config\
copy /Y .env.sample dist\.env

REM Pulizia
IF EXIST build rmdir /s /q build
IF EXIST %EXE_NAME%.spec del /f /q %EXE_NAME%.spec

echo.
echo ===============================
echo Build completata! Esegui da dist\%EXE_NAME%.exe
echo ===============================
pause
