import pandas as pd

class CsvReader:
    def __init__(self, file_path):
        self._csv_file = pd.read_csv(file_path) 
    
    def csv_to_html(self):
        html_res = self._csv_file.to_html(index=False)
        return html_res

    def set_csv(self, csv_path):
        self._csv_file = pd.read_csv(csv_path)

    def get_csv(self):
        return self._csv_file

    def get_columns(self):
        return self._csv_file.columns.tolist()
    
    def sel_columns(self, columns):
        self._csv_file = self._csv_file[columns]
        return self._csv_file.to_html(index=False)

    def index_sort(self):
       self._csv_file.sort_index(ascending=False)
