import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings

# In a real production scenario with multiple tokens or changing tokens,
# you would store the refresh token in the DB or a secure Vault.
# For this implementation, we read from env and handle auth codes.

CLIENT_SECRETS_FILE = os.getenv('YOUTUBE_CLIENT_SECRETS_FILE', 'client_secrets.json')
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
REDIRECT_URI = os.getenv('YOUTUBE_REDIRECT_URI', 'http://localhost:8000/api/auth/youtube/callback/')

class YouTubeService:
    @staticmethod
    def get_auth_url():
        import urllib.parse
        params = {
            'client_id': os.getenv("YOUTUBE_CLIENT_ID"),
            'redirect_uri': REDIRECT_URI,
            'response_type': 'code',
            'scope': 'https://www.googleapis.com/auth/youtube.upload',
            'access_type': 'offline',
            'prompt': 'consent'
        }
        return "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(params)

    @staticmethod
    def get_tokens(auth_code):
        import json
        import urllib.request
        import urllib.parse

        data = {
            'code': auth_code,
            'client_id': os.getenv("YOUTUBE_CLIENT_ID"),
            'client_secret': os.getenv("YOUTUBE_CLIENT_SECRET"),
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code'
        }
        data_encoded = urllib.parse.urlencode(data).encode('utf-8')
        req = urllib.request.Request('https://oauth2.googleapis.com/token', data=data_encoded)
        
        try:
            with urllib.request.urlopen(req) as response:
                return json.loads(response.read().decode())
        except urllib.error.HTTPError as e:
            raise Exception(f"Failed to fetch tokens: {e.read().decode()}")

    @staticmethod
    def get_authenticated_service():
        refresh_token = os.getenv('YOUTUBE_REFRESH_TOKEN')
        if not refresh_token:
            raise Exception("YOUTUBE_REFRESH_TOKEN not set in environment.")

        credentials = Credentials(
            token=None,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=os.getenv("YOUTUBE_CLIENT_ID"),
            client_secret=os.getenv("YOUTUBE_CLIENT_SECRET"),
            scopes=SCOPES
        )

        youtube = build('youtube', 'v3', credentials=credentials)
        return youtube

    @staticmethod
    def upload_video(file_path, title, description=""):
        youtube = YouTubeService.get_authenticated_service()
        
        body = {
            'snippet': {
                'title': title,
                'description': description,
                'categoryId': '27' # Education
            },
            'status': {
                'privacyStatus': 'unlisted',
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=media
        )

        response = None
        while response is None:
            status, response = request.next_chunk()
            
        return response['id']
