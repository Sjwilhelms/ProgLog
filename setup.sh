#!/bin/bash

# Clone the project
echo "What's the name of your new project?"
read PROJECT_NAME

# Create a new directory
mkdir -p $PROJECT_NAME
cp -r config templates static apps $PROJECT_NAME/

# Create virtual environment
cd $PROJECT_NAME
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate a new secret key
SECRET_KEY=$(python -c "import secrets; print(secrets.token_urlsafe(50))")

# Create env.py
cat > env.py << EOF
import os

# Environment settings
os.environ.setdefault("DJANGO_ENVIRONMENT", "development")
os.environ.setdefault("SECRET_KEY", "${SECRET_KEY}")
os.environ.setdefault("DEBUG", "True")

# Database settings (if using PostgreSQL)
# os.environ.setdefault("DB_ENGINE", "django.db.backends.postgresql")
# os.environ.setdefault("DB_NAME", "${PROJECT_NAME}")
# os.environ.setdefault("DB_USER", "postgres")
# os.environ.setdefault("DB_PASSWORD", "")
# os.environ.setdefault("DB_HOST", "localhost")
# os.environ.setdefault("DB_PORT", "5432")
EOF

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Set up the site in the database
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.update_or_create(id=1, defaults={'domain': 'localhost:8000', 'name': 'Development'})"

echo "Setup complete! Your project is ready."
echo "Run the server with: python manage.py runserver"