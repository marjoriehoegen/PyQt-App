# PyQt-App

App made with PyQt and Flask to login and upload files.

Features:
- Login with hardcoded username/password.
-- username = username
-- password = password
- Upload files to /uploads directory.
- Option to cancel upload.
- App always available on the system tray.
-- To close app: right-click on system tray icon and select "Exit".

Upload progress bar and estimated time remaining were not implemented.


## Installation

To install required libraries use the 'requirement.txt':

```python
pip install -r requirements.txt
```

## Usage

To run the application, first start the server:

```python
python server.py
```

Then, execute the main app:
```python
python main.py
```

Use the default username and password to login.
You can test the upload feature with the "example.txt" file.