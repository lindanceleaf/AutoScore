""" 此程式用來自動寫入學生資料(姓名、學號) """

from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
import os
from dotenv import load_dotenv

os.environ.pop("GOOGLESHEET_KEY_PATH", None)
os.environ.pop("GOOGLESHEET_ID", None)
load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = os.getenv("GOOGLESHEET_KEY_PATH")

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('sheets', 'v4', credentials=credentials)

googleSheetId = os.getenv("GOOGLESHEET_ID")

""" 填入從 eCourse2 下載的學生資料 及 對應的試算表名稱(底下的名字) """
csvFile = ['courseid_27547_participants.csv', 'courseid_27550_participants.csv', 'courseid_27551_participants.csv']
mapTable = ['程式設計總成績', '程式設計實習(二)總成績', '程式設計實習(四)總成績']

for file, table in zip(csvFile, mapTable):
    with open(file, 'r', encoding = 'utf-8') as f:
        lines = f.readlines()[1:]
        stu_list = [] 
        for line in lines:
            data = line.split(',')
            name = data[0]
            student_id = data[1]
            stu_list.append((name, student_id))
        
        body = {
            'values': stu_list
        }

        WRITE_RANGE = table + '!A3'
        
        response = service.spreadsheets().values().update(
            spreadsheetId=googleSheetId,
            range=WRITE_RANGE,
            valueInputOption='RAW',
            body=body
        ).execute()