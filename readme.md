# ProgLog

## or Tracking Calorie Inputs and Outputs

### Conceit

Modern people can face historically atypical circumstances: ready access to calories combined with a sedentary lifestyle.  

Someone once told me that diets don't work. That I need to find a way I can live for decades to come. 

Counting calories can be a powerful means for making what one eats and drinks more intentional, making maintaining, losing, or gaining weight easier.  

"And if you gaze long into an abyss, the abyss also gazes into you" - Friedrich Nietzsche

### MVP

This project intends to combine the recording and monitoring of calorie input and output in a simple web application.  

"That which is measured improves. That which is measured and reported improves exponentially." - Karl Pearsons

### Future Editions

A second iteration would extend this functionality to track exercise performance over time.

Future iterations could extend this functionality to track smoking, drinking, recreational/medicinal drug use and hours worked for the purposes of overall self knowledge.

"No phenomenon is a real phenomenon until it is an observed phenomenon" - John Archibald Wheeler

### Disclaimer

This project is for training and education purposes only and is not intended for medical/scientific use.  










## This project was made with Django AllAuth Project Template

https://github.com/Sjwilhelms/setupProject

A robust Django starter project with django-allauth integration, ready for rapid development.

## Features

- User authentication (signup, login, password reset)
- Social authentication (optional)
- Environment-based settings (development/production)
- Bootstrap 5 integration
- Static files configuration
- Ready-to-use templates

## Getting Started

### 1. Clone this repository

```bash
git clone https://github.com/yourusername/django-all-auth.git your-project-name
cd your-project-name
```

### 2. Create a virtual environment

In VS code you will need to use this code before you can set up the virtual environment

```bash
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Copy env.example and modify

```bash
cp env.py.example env.py
# Edit env.py with your settings
```

### 5. Run migrations

```bash
python manage.py migrate
```

### 6. Create a superuser

```bash
python manage.py createsuperuser
```

### 6.1 Creating Static Directories

The project expects certain static directories to exist. Create them using:

```bash
# Create static directories
mkdir -p static/css static/js static/images

# Create basic files
echo "/* Custom styles */" > static/css/style.css
echo "// Project scripts" > static/js/main.js
```

### 7. Create a site object

```bash
python manage.py shell
```

```bash
from django.contrib.sites.models import Site
Site.objects.update_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'Development'})
exit()
```

### 8. Run the server

```bash
python manage.py runserver
```

### 9. Comprehensive gitignore included

With a mind to keeping your SECRET_KEY's secure

### 10. Use the Included Setup Script (Recommended)

This template includes a setup script to automate the initial configuration of new projects:

```bash
# Make the script executable (Unix/Linux/Mac)
chmod +x setup.sh

# Run the setup script
./setup.sh
```

**For Windows:**
```bash
# Run the Windows setup script
setup.bat
```

### 11. Use the Included Rename Project Script (Recommended)

You will likely need to rename your project after creation, use the included script:

```bash
python rename_project.py old_project_name new_project_name
```

### Repository Management

#### Update Repository URL

This template includes scripts to easily update your Git remote repository URL:

**For Windows:**
```bash
.\update_remote.bat https://github.com/username/your-repo-name.git
```

**For UNIX/Linux:**
```bash
.\update_remote.py https://github.com/username/your-repo-name.git
```