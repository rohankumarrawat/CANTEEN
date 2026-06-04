@echo off
title Canteen Management System
echo =========================================
echo   Canteen Inventory ^& Sales System
echo =========================================
echo.
echo Installing dependencies (first time only)...
pip install customtkinter pillow -q
echo.
echo Launching application...
python app.py
pause
