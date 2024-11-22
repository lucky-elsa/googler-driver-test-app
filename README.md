Google Drive Integration App
Overview
This is a Django application that integrates with Google Drive using OAuth 2.0. The app allows users to:

Authenticate using Google OAuth.
List files in their Google Drive.
Upload files to Google Drive.
Download files from Google Drive.
Delete files from Google Drive.


Features
Login: Authenticate with Google OAuth 2.0.
List Files: View files in Google Drive with details like name, type, and modification date.
Upload Files: Upload files from your local system to Google Drive.
Download Files: Download files from Google Drive to your local system.
Delete Files: Delete files from Google Drive.

Prerequisites
Python 3.8 or higher
Django 4.0 or higher
Google Cloud account
pip for package management


Set Up a Virtual Environment

python -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate     # For Windows


Install Dependencies

pip install -r requirements.txt


SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8000/drive/callback/




Google Drive Integration App
Overview
This is a Django application that integrates with Google Drive using OAuth 2.0. The app allows users to:

Authenticate using Google OAuth.
List files in their Google Drive.
Upload files to Google Drive.
Download files from Google Drive.
Delete files from Google Drive.
Features
Login: Authenticate with Google OAuth 2.0.
List Files: View files in Google Drive with details like name, type, and modification date.
Upload Files: Upload files from your local system to Google Drive.
Download Files: Download files from Google Drive to your local system.
Delete Files: Delete files from Google Drive.
Prerequisites
Python 3.8 or higher
Django 4.0 or higher
Google Cloud account
pip for package management
Installation
1. Clone the Repository
git clone https://github.com/your-username/google-drive-integration.git
cd google-drive-integration
2. Set Up a Virtual Environment

python -m venv env
source env/bin/activate  # For Linux/macOS
env\Scripts\activate     # For Windows
3. Install Dependencies

pip install -r requirements.txt
4. Configure Environment Variables
Create a .env file in the root directory with the following content:


SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
REDIRECT_URI=http://localhost:8000/drive/callback/

Google Cloud Setup
1. Enable Google Drive API
Go to the Google Cloud Console.
Create a new project or select an existing project.
Navigate to APIs & Services > Library.
Search for Google Drive API and enable it.
2. Create OAuth Credentials
Navigate to APIs & Services > Credentials.
Click on Create Credentials > OAuth 2.0 Client IDs.
Select Web Application as the application type.
Add the following in Authorized redirect URIs:
http://localhost:8000/drive/callback/
Download the credentials.json file and place it in the root directory of your project.

Usage

python manage.py runserver


API Endpoints

GET http://localhost:8000/drive/login/
GET http://localhost:8000/drive/list/
POST http://localhost:8000/drive/upload/
GET http://localhost:8000/drive/download/<file_id>/
DELETE http://localhost:8000/drive/delete/<file_id>/


Testing

python manage.py test
