from django.test import TestCase, Client
from unittest.mock import patch
from drive.utils.google_auth import get_flow, save_credentials, load_credentials
import io

class DriveApiTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.valid_credentials = {
            "token": "mock_token",
            "refresh_token": "mock_refresh_token",
            "token_uri": "https://oauth2.googleapis.com/token",
            "client_id": "mock_client_id",
            "client_secret": "mock_client_secret",
            "scopes": ["https://www.googleapis.com/auth/drive"]
        }

    @patch("drive.utils.google_auth.get_flow")
    def test_login_redirect(self, mock_get_flow):
        """Test login redirects to Google OAuth"""
        mock_get_flow.return_value.authorization_url.return_value = ("http://example.com/oauth", "state")
        response = self.client.get("/drive/login/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("example.com", response["Location"])


    @patch("drive.utils.google_auth.get_flow")
    @patch("drive.utils.google_auth.save_credentials")
    def test_callback_success(self, mock_save_credentials, mock_get_flow):
        """Test successful OAuth callback"""
        mock_flow = mock_get_flow.return_value
        mock_flow.fetch_token.return_value = self.valid_credentials
        mock_flow.credentials = self.valid_credentials
        response = self.client.get("/drive/callback/?code=mock_code")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "Authentication successful. Access token saved."})

    @patch("drive.utils.google_auth.load_credentials")
    @patch("googleapiclient.discovery.build")
    def test_list_files(self, mock_build, mock_load_credentials):
        """Test listing files in Google Drive"""
        mock_load_credentials.return_value = self.valid_credentials
        mock_service = mock_build.return_value
        mock_service.files.return_value.list.return_value.execute.return_value = {
            "files": [{"id": "1", "name": "example.txt", "mimeType": "text/plain"}]
        }
        response = self.client.get("/drive/list/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {
            "files": [{"id": "1", "name": "example.txt", "mimeType": "text/plain"}]
        })

    @patch("drive.utils.google_auth.load_credentials")
    @patch("googleapiclient.discovery.build")
    def test_upload_file(self, mock_build, mock_load_credentials):
        """Test uploading a file to Google Drive"""
        mock_load_credentials.return_value = self.valid_credentials
        mock_service = mock_build.return_value
        mock_service.files.return_value.create.return_value.execute.return_value = {"id": "1"}
        file = io.BytesIO(b"Mock file content")
        file.name = "mock_file.txt"
        response = self.client.post("/drive/upload/", {"file": file}, format="multipart")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "File uploaded successfully.", "fileId": "1"})


    @patch("drive.utils.google_auth.load_credentials")
    @patch("googleapiclient.discovery.build")
    def test_download_file(self, mock_build, mock_load_credentials):
        """Test downloading a file from Google Drive"""
        mock_load_credentials.return_value = self.valid_credentials
        mock_service = mock_build.return_value
        mock_request = mock_service.files.return_value.get_media.return_value
        mock_request.execute.return_value = b"Mock file content"
        response = self.client.get("/drive/download/1/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"Mock file content")


    @patch("drive.utils.google_auth.load_credentials")
    @patch("googleapiclient.discovery.build")
    def test_delete_file(self, mock_build, mock_load_credentials):
        """Test deleting a file from Google Drive"""
        mock_load_credentials.return_value = self.valid_credentials
        mock_service = mock_build.return_value
        mock_service.files.return_value.delete.return_value.execute.return_value = {}
        response = self.client.delete("/drive/delete/1/")
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {"message": "File deleted successfully."})
