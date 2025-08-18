import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get port from environment variable
port = os.getenv('PORT', '8000')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoProject.settings')
django.setup()

# Run the server
if __name__ == '__main__':
    from django.core.management import execute_from_command_line
    execute_from_command_line(['manage.py', 'runserver', f'0.0.0.0:{port}'])