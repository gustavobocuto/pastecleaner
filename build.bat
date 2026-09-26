@echo off
pip install -r requirements.txt
pip install pyinstaller
pyinstaller --onefile --windowed --name PastaCleaner main.py
echo.
echo Pronto. O executavel esta em dist\PastaCleaner.exe
pause
