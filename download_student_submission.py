import re
import requests
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
import io, os
# Required scopes
SCOPES = [
    "https://www.googleapis.com/auth/classroom.courses.readonly",
    "https://www.googleapis.com/auth/classroom.announcements.readonly",
    "https://www.googleapis.com/auth/classroom.student-submissions.students.readonly",
    "https://www.googleapis.com/auth/classroom.rosters.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

def get_service(api_name, api_version, scopes):
    creds = None
    if os.path.exists("APICredentials/token.json"):
        creds = Credentials.from_authorized_user_file("APICredentials/token.json", scopes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "APICredentials/classroom_credentials.json", scopes)
            creds = flow.run_local_server(port=0)
        with open("APICredentials/token.json", "w") as token:
            token.write(creds.to_json())
    service = build(api_name, api_version, credentials=creds)
    return service, creds


def sanitize_name(name):
    return re.sub(r'\s+', '_', name.strip())


def list_courses(service):
    results = service.courses().list().execute()
    courses = results.get("courses", [])
    if not courses:
        print("No courses found.")
        return []
    print("\nAvailable Courses:")
    for c in courses:
        print(f"{c['id']} - {c['name']}")
    return courses


def list_assignments(service, course_id):
    results = service.courses().courseWork().list(courseId=course_id).execute()
    courseworks = results.get("courseWork", [])
    assgn_dict = {}
    if not courseworks:
        print("No assignments found.")
        return []
    print("\nAvailable Assignments:")
    for work in courseworks:
        assgn_dict[work['id']] = sanitize_name( work['title'])
        print(f"{work['id']} - {work['title']}")
    return assgn_dict

def download_file(drive_service, creds, file_id, save_path):
    try:
        request = drive_service.files().get_media(fileId=file_id)
        fh = io.FileIO(save_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while not done:
            status, done = downloader.next_chunk()
            if status:
                print(f"  ⬇️ Downloading {os.path.basename(save_path)} ({int(status.progress() * 100)}%)")

        fh.close()
        print(f"  ✅ Saved: {os.path.basename(save_path)}")

    except Exception as e:
        print(f"  ⚠️ Error downloading file {file_id}: {e}")

def get_all_students(service, course_id):  # 🔧 FIX: handle pagination
    all_students = []
    page_token = None
    while True:
        response = service.courses().students().list(
            courseId=course_id, pageToken=page_token
        ).execute()
        students = response.get("students", [])
        all_students.extend(students)
        page_token = response.get("nextPageToken")
        if not page_token:
            break
    student_map = {s["userId"]: s["profile"]["name"]["fullName"] for s in all_students}
    print(f"✅ Found {len(student_map)} students in this course.")
    return student_map

def download_submissions(course_id, assignment_id,assignment_name, classroom_service, drive_service, drive_creds):
    try:
        course = classroom_service.courses().get(id=course_id).execute()
        course_name = sanitize_name(course["name"])

        submissions = classroom_service.courses().courseWork().studentSubmissions().list(
            courseId=course_id, courseWorkId=assignment_id
        ).execute().get("studentSubmissions", [])

        student_map = get_all_students(classroom_service, course_id)

        base_dir = f"downloads/{course_name}_{assignment_id}_{assignment_name}"
        os.makedirs(base_dir, exist_ok=True)

        print(f"\n📥 Downloading submissions to: {os.path.abspath(base_dir)}")

        for sub in submissions:
            if sub.get("state") != "TURNED_IN":
                print(sub.get("state"),"skipping downloding submissions --------------------------")
                continue

            user_id = sub.get("userId")
            student_name = sanitize_name(student_map.get(user_id, "Unknown_Student"))
            student_dir = os.path.join(base_dir, student_name)
            os.makedirs(student_dir, exist_ok=True)

            attachments = sub.get("assignmentSubmission", {}).get("attachments", [])
            for att in attachments:
                if "driveFile" in att:
                    drive_file = att["driveFile"].get("driveFile", att["driveFile"])
                    file_id = drive_file.get("id")
                    file_title = drive_file.get("title", "untitled")
                    if not file_id:
                        print(f"⚠️ Skipping: no file ID for {file_title}")
                        continue
                    save_path = os.path.join(student_dir, sanitize_name(file_title))
                    print(f"⬇️  {student_name} → {file_title}")
                    download_file(drive_service, drive_creds, file_id, save_path)

        print(f"\n✅ All submissions downloaded successfully to: {os.path.abspath(base_dir)}")

    except HttpError as error:
        print(f"An error occurred: {error}")


def main():
    classroom_service, classroom_creds = get_service("classroom", "v1", SCOPES)
    drive_service, drive_creds = get_service("drive", "v3", SCOPES)

    courses = list_courses(classroom_service)
    course_id = input("\nEnter course ID: ").strip()

    assignments = list_assignments(classroom_service, course_id)
    assignment_id = input("\nEnter assignment ID: ").strip()
    assignment_name = assignments[assignment_id]
    download_submissions(course_id, assignment_id,assignment_name, classroom_service, drive_service, drive_creds)


if __name__ == "__main__":
    main()

