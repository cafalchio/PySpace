from google.oauth2.service_account import Credentials
import gspread

class Sheet:
    def __init__(self):
        """Get the google sheet"""
        SCOPE = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        CREDS = Credentials.from_service_account_file("creds.json")
        SCOPRED_CREDS = CREDS.with_scopes(SCOPE)
        GSPREAD_CLIENT = gspread.authorize(SCOPRED_CREDS)
        SHEET = GSPREAD_CLIENT.open("space_game")
        self.records = SHEET.worksheet("records")

    def get_records(self):
        """Get records from google sheet
        Return a list of record lists
        """
        return self.records.get_all_values()

    def update_records(self, record):
        """Update records in google sheet

        Input:
            record(list): list of records [name, score]
        """
        self.records.append_row(record)
        return "Records updated"

    def get_scores(self):
        """Get scores from google sheet
        Return a list of scores
        """
        data = self.get_records()
        return [int(row[1]) for row in data][0:7]
