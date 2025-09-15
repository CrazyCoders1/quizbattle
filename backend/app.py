#!/usr/bin/env python3
"""
Main application entry point for Render deployment with psycopg3 support
"""
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Set environment variables for psycopg3 and Flask-Migrate compatibility
os.environ.setdefault('FLASK_APP', 'app.py')

from app import create_app

# Create the Flask app instance with psycopg3 support
app = create_app()

# Ensure database URL is compatible with psycopg3
with app.app_context():
    database_url = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    if database_url.startswith('postgres://'):
        # Convert postgres:// to postgresql:// for psycopg3
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
        print(f"✅ Updated database URL for psycopg3 compatibility")
    
    print(f"🗄️ Database URI configured: {database_url[:50]}...")

if __name__ == '__main__':
    # Get port from environment variable (Render provides this)
    port = int(os.environ.get('PORT', 10000))
    
    print(f"🚀 Starting QuizBattle server on port {port} with Python {sys.version[:5]}")
    print(f"🔧 Environment: {os.environ.get('FLASK_ENV', 'production')}")
    
    # Run the app
    app.run(host='0.0.0.0', port=port, debug=False)
