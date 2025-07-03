from django.shortcuts import render
from django.http import HttpResponse
import requests

# ✅ FastAPI ka deployed URL
FASTAPI_URL = "https://privydrop.onrender.com"

def home(request):
    return render(request, 'app/home.html')

def upload(request):
    message = ""
    encrypted_id = ""
    if request.method == "POST":
        file = request.FILES.get("file")
        if file:
            headers = {
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub29yYWxhbXplZXNoYW5AZ21haWwuY29tIiwicm9sZSI6Im9wcyJ9.sunsraQMlHP-_NfocfcvVfENV9IU2eEd6Dl5cM6cCfs"
            }
            response = requests.post(
                f"{FASTAPI_URL}/files/upload",
                files={"file": file},
                headers=headers
            )
            # Yeh print karo console me taaki dekho JSON kya aaya
            print("Upload Response JSON:", response.text)

            if response.status_code == 200:
                data = response.json()
                encrypted_id = data.get("encryption_id") or data.get("encrypted_id") or ""
                if encrypted_id:
                    message = "✅ File uploaded successfully!"
                else:
                    message = "⚠️ Uploaded but encryption ID missing!"
            else:
                message = f"❌ Upload failed! ({response.status_code})"

    return render(request, 'app/upload.html', {
        "message": message,
        "encrypted_id": encrypted_id
    })

def download(request):
    download_link = ""
    if request.method == "POST":
        encrypted_id = request.POST.get("encrypted_id")
        if encrypted_id:
            download_link = f"{FASTAPI_URL}/files/download-direct/{encrypted_id}"
    return render(request, 'app/download.html', {"download_link": download_link})

def about(request):
    return render(request, 'app/about.html')

def contact(request):
    return render(request, 'app/contact.html')

def file_list(request):
    files = []

    # 🔐 CLIENT ka access token
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeWVkemVlc2hhbjgwMzEwMUBnbWFpbC5jb20iLCJyb2xlIjoiY2xpZW50In0.p-30lNJ-R322NORz-3CcvLCchzAVp3LNt7u7rFR0kNg"

    # ✅ List of all files
    list_resp = requests.get(
        f"{FASTAPI_URL}/files/list",
        headers={"token": token}
    )

    if list_resp.status_code == 200:
        file_data = list_resp.json()

        # Har file ka encrypted ID
        for file in file_data:
            encrypt_resp = requests.get(f"{FASTAPI_URL}/encrypt-id/{file['id']}")
            if encrypt_resp.status_code == 200:
                encrypted_id = encrypt_resp.json()["encrypted_id"]
                files.append({
                    "id": file["id"],
                    "filename": file["filename"],
                    "encrypted_id": encrypted_id
                })

    return render(request, "app/file_list.html", {"files": files})

def download_file(request, encrypted_id):
    api_url = f"{FASTAPI_URL}/files/download-direct/{encrypted_id}"

    headers = {
        # 🔐 CLIENT ka token
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeWVkemVlc2hhbjgwMzEwMUBnbWFpbC5jb20iLCJyb2xlIjoiY2xpZW50In0.p-30lNJ-R322NORz-3CcvLCchzAVp3LNt7u7rFR0kNg"
    }

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        response_file = HttpResponse(
            response.content,
            content_type="application/octet-stream"
        )
        response_file["Content-Disposition"] = "attachment; filename=downloaded_file"
        return response_file
    else:
        return HttpResponse(f"❌ Error downloading file: {response.status_code}")
