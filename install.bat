@echo off
echo =================================
echo Setting up Automation Framework
echo =================================

echo Installing Python packages...
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo Package installation failed!
    pause
    exit /b %ERRORLEVEL%
)

echo Installing Playwright browsers...
python -m playwright install

IF %ERRORLEVEL% NEQ 0 (
    echo Playwright browser installation failed!
    pause
    exit /b %ERRORLEVEL%
)

echo Setup completed successfully!
pause