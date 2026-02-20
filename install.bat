@echo off
echo =================================
echo Setting up Automation Framework
echo =================================

cd /d %~dp0

echo Creating virtual environment...
python -m venv .venv

echo Activating virtual environment...
call .venv\Scripts\activate

echo Installing Python packages...
pip install -r requirements.txt

IF %ERRORLEVEL% NEQ 0 (
    echo Package installation failed!

    exit /b %ERRORLEVEL%
)

echo Installing Playwright browsers...
python -m playwright install

IF %ERRORLEVEL% NEQ 0 (
    echo Playwright browser installation failed!

    exit /b %ERRORLEVEL%
)

echo Setup completed successfully!
