import pandas as pd

class CsvReader:
    def __init__(self):
        self._csv_file = ""
    
    def csv_to_html(self, csv_path):
        self._csv_file = pd.read_csv(csv_path)

        html_res = self._csv_file.to_html()

        return html_res

    def set_csv(self, csv_path):
        self._csv_file = pd.read_csv(csv_path)

    def get_csv(self):
        return self._csv_file

