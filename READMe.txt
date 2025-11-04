This puspose of this repository is to store all the assignment that are given in the Computational Physics Lab and it's solution 

1) utils.py will contains all the method and classes  that are developed for solving the assignments 

2) Each folder Assignment_* will contains all the files e.g question , input files and main script related to that assignment  

# Google Classroom Automation – Download Student Submissions

This project allows you to interact with Google Classroom using the Google Classroom API.
Specifically, it enables teachers to list courses, list assignments, and download student submissions (attachments) for a given course and assignment.

All submissions are automatically downloaded into organized folders:
- Each course has its own folder.
- Inside it, each student gets a subfolder containing their submitted files.

------------------------------------------------------------
## Requirements

1. Python 3.8+
   Ensure Python is installed and added to your system PATH.
   You can verify this using:
   python3 --version

2. Install Required Libraries
   Install all dependencies using the following command:
   pip install -r requirements.txt

   Typical dependencies include:
   google-api-python-client
   google-auth
   google-auth-oauthlib
   google-auth-httplib2
   requests

------------------------------------------------------------
## Setting Up Credentials

To access the Google Classroom and Drive APIs, you must obtain credentials for your Google account.

Step 1. Create a Google Cloud Project
-------------------------------------
1. Visit the Google Cloud Console: https://console.cloud.google.com/
2. Click “Select a Project” → “New Project” and give it a name.
3. After creation, make sure it’s selected (check the top bar).

Step 2. Enable Required APIs
-----------------------------
You must enable both:
- Google Classroom API
- Google Drive API

To enable each:
1. Go to APIs & Services → Library in Google Cloud Console.
2. Search for “Google Classroom API” → click Enable.
3. Do the same for “Google Drive API”.

Step 3. Create OAuth Client ID Credentials
-------------------------------------------
1. In APIs & Services → Credentials, click Create Credentials → OAuth client ID.
2. Choose “Desktop App” as the application type.
3. Download the credentials file — it will be named something like:
   classroom_credentials.json
4. Place this file in your project folder, and rename it to:
   classroom_credentials.json

------------------------------------------------------------
## Running the Script

Once everything is set up, run the script:
python download_student_submission.py

What the script does:
1. Lists all available Google Classroom courses.
2. Prompts you to select a course ID.
3. Lists all assignments for that course.
4. Prompts you to select an assignment ID.
5. Downloads all submitted files for that assignment into structured folders.

------------------------------------------------------------
## Folder Structure

After execution, you’ll get a directory structure like this:

downloads/
└── CourseName_AssignmentID/
    ├── Student1_Name/
    │   ├── file1.pdf
    │   └── file2.docx
    ├── Student2_Name/
    │   └── project.zip
    └── ...

Each student’s submission files are placed in their own folder, named after them.

------------------------------------------------------------
## Notes

- When you run the script for the first time, a browser window will open asking for Google account authorization.
- A token.json file will be created automatically — this stores your access token so you won’t have to log in every time.
- If access issues occur, delete token.json and re-run the script to reauthorize.
- The script uses read-only permissions, so it will not modify anything in your Classroom or Drive.

------------------------------------------------------------
## References

- Google Classroom API Quickstart:
  https://developers.google.com/workspace/classroom/quickstart/python

- Google Drive API Quickstart:
  https://developers.google.com/drive/api/quickstart/python

