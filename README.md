# python-http
Python flask application to view csv spreadsheets.

## Change database path!

open `app/models.py`, find `conn_path` variable and type path to `app.db` file.

## Run application
1. Make and run python virtualenv:
```
$ python -m venv venv
$ source venv/bin/activate
```
2. Install all needed libs:
```
$ pip install -r requirements.txt
```
3. Run flask application on your localhost, make sure you are in the venv:
```
$ python run.py
```
4. Open `http://localhost:5000/` in your browser.
