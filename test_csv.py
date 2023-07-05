from app.csv_reader import CsvReader

reader = CsvReader()

csv_html_tbl = reader.csv_to_html('test.csv')

with open('html.html', 'w', encoding='UTF-8') as file:
    file.write(csv_html_tbl)
