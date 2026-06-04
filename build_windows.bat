@echo off
REM ============================================
REM  Build AWWA Lunch Project Windows EXE
REM ============================================
REM  Prerequisites (run once):
REM    pip install pyinstaller
REM    pip install -r requirements.txt
REM ============================================

echo ====================================
echo  Building AWWA Lunch Project EXE...
echo ====================================

pip install pyinstaller
pyinstaller build_exe.spec --clean --noconfirm

echo.
echo ====================================
if exist "dist\AWWA_Lunch_Project.exe" (
    echo  BUILD SUCCESS!
    echo  EXE location: dist\AWWA_Lunch_Project.exe
    echo.
    echo  To distribute, copy these together:
    echo    - dist\AWWA_Lunch_Project.exe
    echo    - canteen.db  (will be created on first run if missing)
    echo.
    echo  Backups are saved in a "backups" folder
    echo  next to the .exe file.
) else (
    echo  BUILD FAILED. Check errors above.
)
echo ====================================
pause
