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

echo Running Pytest...
pytest -v --alluredir=tests\allure-results

echo Generating Allure HTML report...
.\allure\bin\allure.bat generate tests\allure-results --clean -o allure-report

echo Opening Allure Report...
.\allure\bin\allure.bat open allure-report


