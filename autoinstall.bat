@echo off
chcp 65001 >nul
title Compiling Proxy Checker to .exe
color 0A
echo ==========================================
echo      Compiling Proxy Checker to .exe
echo ==========================================
echo.

rem Check if pyinstaller is installed, and install if not
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

rem Download the icon
echo Downloading the icon...
powershell -Command "Invoke-WebRequest -Uri 'https://icon-icons.com/downloadimage.php?id=72284&root=930/ICO/512/&file=server_icon-icons.com_72284.ico' -OutFile 'server_icon.ico'"

rem Compile Python script to .exe with icon
echo Compiling script to .exe...
pyinstaller --onefile --icon=server_icon.ico main.py

rem Check if compilation was successful and move the .exe file
if exist "dist\\main.exe" (
    echo Moving .exe to current directory...
    move "dist\\main.exe" "%cd%"
) else (
    echo Compilation failed!
    exit /b 1
)

rem Clean up temporary files
echo Cleaning up temporary files...
rmdir /S /Q dist
rmdir /S /Q build
del main.spec

echo.
echo Compilation completed successfully!
pause
@echo off
chcp 65001 >nul
title Compiling Proxy Checker to .exe
color 0A
echo ==========================================
echo      Compiling Proxy Checker to .exe
echo ==========================================
echo.

rem Check if pyinstaller is installed, and install if not
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing pyinstaller...
    pip install pyinstaller
)

rem Download the icon
echo Downloading the icon...
powershell -Command "Invoke-WebRequest -Uri 'https://icon-icons.com/downloadimage.php?id=72284&root=930/ICO/512/&file=server_icon-icons.com_72284.ico' -OutFile 'server_icon.ico'"

rem Compile Python script to .exe with icon
echo Compiling script to .exe...
pyinstaller --onefile --icon=server_icon.ico main.py

rem Check if compilation was successful and move the .exe file
if exist "dist\\main.exe" (
    echo Moving .exe to current directory...
    move "dist\\main.exe" "%cd%"
) else (
    echo Compilation failed!
    exit /b 1
)

rem Clean up temporary files
echo Cleaning up temporary files...
rmdir /S /Q dist
rmdir /S /Q build
del main.spec

echo.
echo Compilation completed successfully!
pause
