@echo off
echo ================================
echo Running Pytest with Allure
echo ================================
REM Go to project root (this bat file location)
cd /d "%~dp0"

echo Current directory:
cd

echo Cleaning screenshots folder...
if exist screenshots (
    del /q screenshots\*
)

echo Cleaning old Allure report...
if exist allure-report (
    rmdir /s /q allure-report
)

REM Run pytest and generate allure results
echo off Running Pytest...
echo off .venv\Scripts\python -m pytest -v --alluredir=tests\allure-results

echo Generating Single File Allure Report...
call "%~dp0allure\bin\allure.bat" generate tests\allure-results --clean --single-file -o tests\allure-report

IF %ERRORLEVEL% NEQ 0 (
    echo Allure report generation failed!

    exit /b %ERRORLEVEL%
)





