import json

from google.oauth2 import service_account
from googleapiclient.discovery import build

from fms.settings import GOOGLE_DRIVE_FOLDER_ID, GOOGLE_SHEETS_CREDS


class GoogleSheetsClient:
    def __init__(self):
        SCOPES = ["https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/spreadsheets"]
        creds = service_account.Credentials.from_service_account_info(json.loads(GOOGLE_SHEETS_CREDS), scopes=SCOPES)
        self.creds = creds

    def create_sheet(self, sheet_title):
        drive_service = build("drive", "v3", credentials=self.creds)
        sheet_metadata = {
            "name": sheet_title,
            "parents": [GOOGLE_DRIVE_FOLDER_ID],
            "mimeType": "application/vnd.google-apps.spreadsheet",
        }
        sheet = drive_service.files().create(body=sheet_metadata).execute()
        return sheet.get("id")

    def add_row(self, spreadsheet_id, row_number, row_values):
        service = build("sheets", "v4", credentials=self.creds)

        update_request = {
            "updateCells": {
                "rows": [{"values": [{"userEnteredValue": {"stringValue": value}} for value in row_values]}],
                "range": {
                    "sheetId": 0,
                    "startRowIndex": row_number - 1,
                    "endRowIndex": row_number,
                    "startColumnIndex": 0,
                    "endColumnIndex": len(row_values),
                },
                "fields": "userEnteredValue",
            }
        }
        service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id, body={"requests": [update_request]}).execute()


google_sheets_client = GoogleSheetsClient()
