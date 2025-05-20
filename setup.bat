## Creating a Windows Version of the Setup Script

For your template to be fully cross-platform, you'll need a `setup.bat` file that performs the same functions as your bash script but works on Windows. Here's how you could create one:

```batch
@echo off
echo Django AllAuth Project Setup

echo What's the name of your new project?
set /p PROJECT_NAME=

echo Creating project directory...
mkdir %PROJECT_NAME%
xcopy /s /e /q /y . %PROJECT_NAME%\ > nul
cd %PROJECT_NAME%

echo Creating virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Generating secret key...
for /f "delims=" %%i in ('python -c "import secrets; print(secrets.token_urlsafe(50))"') do set SECRET_KEY=%%i

echo Creating env.py file...
copy env.py.example env.py > nul
powershell -Command "(gc env.py) -replace 'generate-a-new-secure-key-here', '%SECRET_KEY%' | Out-File -encoding ASCII env.py"

echo Running migrations...
python manage.py migrate

echo Creating superuser...
python manage.py createsuperuser

echo Setting up site object...
python -c "from django.contrib.sites.models import Site; Site.objects.update_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'Development'})"

echo.
echo Setup complete! Your project is ready.
echo Run the server with: python manage.py runserver