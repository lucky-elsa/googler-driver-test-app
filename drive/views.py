from django.shortcuts import redirect, render
from drive.utils.google_auth import get_flow, save_credentials, load_credentials
from googleapiclient.discovery import build
from django.shortcuts import render
from drive.utils.google_auth import load_credentials
from django.http import FileResponse
from googleapiclient.http import MediaFileUpload
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import io
from googleapiclient.http import MediaIoBaseDownload




def login(request):
    """Redirect user to Google's OAuth 2.0 login page"""
    flow = get_flow()
    auth_url, _ = flow.authorization_url(prompt='consent')
    return redirect(auth_url)

def callback(request):
    """Handle OAuth 2.0 callback and save credentials"""
    try:
        flow = get_flow()
        flow.fetch_token(authorization_response=request.build_absolute_uri())
        credentials = flow.credentials
        save_credentials(credentials)
        return JsonResponse({"message": "Authentication successful. Access token saved."})
    except Exception as e:
        return JsonResponse({"error": f"Invalid OAuth callback or token. Details: {str(e)}"})




def list_files(request):
    """List files in Google Drive"""
    credentials = load_credentials()
    if not credentials:
        return JsonResponse({"error": "User not authenticated. Please log in."})

    try:
        service = build('drive', 'v3', credentials=credentials)
        results = service.files().list(fields="files(id, name, mimeType, modifiedTime)").execute()
        files = results.get('files', [])
        return JsonResponse({"files": files})
    except Exception as e:
        return JsonResponse({"error": f"Failed to list files. Details: {str(e)}"})

@csrf_exempt
def upload_file(request):
    """Upload a file to Google Drive"""
    if request.method != 'POST':
        return JsonResponse({"error": "Invalid request method. Use POST."})

    credentials = load_credentials()
    if not credentials:
        return JsonResponse({"error": "User not authenticated. Please log in."})

    try:
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({"error": "No file provided."})

        service = build('drive', 'v3', credentials=credentials)
        file_metadata = {'name': file.name}
        media = MediaFileUpload(file.temporary_file_path(), resumable=True)
        uploaded_file = service.files().create(body=file_metadata, media_body=media).execute()
        return JsonResponse({"message": "File uploaded successfully.", "fileId": uploaded_file.get("id")})
    except Exception as e:
        return JsonResponse({"error": f"Failed to upload file. Details: {str(e)}"})



def download_file(request, file_id):
    """Download a file from Google Drive"""
    credentials = load_credentials()
    if not credentials:
        return JsonResponse({"error": "User not authenticated. Please log in."})

    try:
        service = build('drive', 'v3', credentials=credentials)
        request_file = service.files().get_media(fileId=file_id)
        buffer = io.BytesIO()
        downloader = MediaIoBaseDownload(buffer, request_file)
        done = False
        while not done:
            status, done = downloader.next_chunk()

        buffer.seek(0)
        response = FileResponse(buffer, as_attachment=True, filename=f"{file_id}.download")
        return response
    except Exception as e:
        return JsonResponse({"error": f"Failed to download file. Details: {str(e)}"})


def delete_file(request, file_id):
    """Delete a file from Google Drive"""
    credentials = load_credentials()
    if not credentials:
        return JsonResponse({"error": "User not authenticated. Please log in."})

    try:
        service = build('drive', 'v3', credentials=credentials)
        service.files().delete(fileId=file_id).execute()
        return JsonResponse({"message": "File deleted successfully."})
    except Exception as e:
        return JsonResponse({"error": f"Failed to delete file. Details: {str(e)}"})
