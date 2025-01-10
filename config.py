import os
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# 加載環境變數
load_dotenv()

# DOMjudge 配置
JUDGE_URL = os.getenv("JUDGE_URL")
JUDGE_USERNAME = os.getenv("JUDGE_USERNAME")
JUDGE_PASSWORD = os.getenv("JUDGE_PASSWORD")
AUTH = (JUDGE_USERNAME, JUDGE_PASSWORD)

# Google Sheets 配置
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLESHEET_KEY_PATH")
GOOGLE_SHEET_ID = os.getenv("GOOGLESHEET_ID")

# 初始化 Google Sheets API 客戶端
credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)
