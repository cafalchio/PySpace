""" Access data from google sheets using Sheets class """
from google.oauth2.service_account import Credentials
import gspread


class Sheet:
    """ Manages the data from the google sheet. """

    def __init__(self):
        """Get the google sheet"""
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive",
        ]

        creds = Credentials.from_service_account_file("creds.json")
        scoped_creds = creds.with_scopes(scope)
        gspread_client = gspread.authorize(scoped_creds)
        g_sheets = gspread_client.open("space_game")
        self.sheet = g_sheets.worksheet("records")
        self.data = self.sheet.get_all_values()

    def update_records(self, record):
        """Update records in google sheet

        Input:
            record(list): list of records [name, score]
        """
        msg = ""
        data = self.get_scores()
        idx = data.index(min(data))
        self.sheet.update_cell(idx + 1, 1, record[0]) # name
        self.sheet.update_cell(idx + 1, 2, record[1]) # value
        msg = "Records updated"
        return msg

    def get_scores(self):
        """Get scores from google sheet
        Return a list of scores sorted
        """
        data = sorted([int(row[1]) for row in self.data])
        return data
