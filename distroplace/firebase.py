
import os
import firebase_admin
from firebase_admin import credentials, auth
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# Use the path to your service account key JSON file
cred = credentials.Certificate(os.path.join(
    BASE_DIR, 'firebase_admin.json'))
firebase_admin.initialize_app(cred)
