from django.shortcuts import render, redirect
from django.http import HttpResponse
import requests

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
                # OPS token
                "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJub29yYWxhbXplZXNoYW5AZ21haWwuY29tIiwicm9sZSI6Im9wcyJ9.sunsraQMlHP-_NfocfcvVfENV9IU2eEd6Dl5cM6cCfs"
            }
            response = requests.post(
                f"{FASTAPI_URL}/files/upload",
                files={"file": file},
                headers=headers
            )
            print("Upload Response JSON:", response.text)
            if response.status_code == 200:
                data = response.json()
                # Multiple key fallback
                encrypted_id = data.get("encryption_id") or data.get("encrypted_id") or data.get("encryptedId") or ""
                if encrypted_id:
                    message = f"✅ File uploaded successfully! Encryption ID: {encrypted_id}"
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
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeWVkemVlc2hhbjgwMzEwMUBnbWFpbC5jb20iLCJyb2xlIjoiY2xpZW50In0.p-30lNJ-R322NORz-3CcvLCchzAVp3LNt7u7rFR0kNg"

    list_resp = requests.get(
        f"{FASTAPI_URL}/files/list",
        headers={"token": token}
    )

    if list_resp.status_code == 200:
        file_data = list_resp.json()
        for file in file_data:
            encrypt_resp = requests.get(f"{FASTAPI_URL}/encrypt-id/{file['id']}")
            if encrypt_resp.status_code == 200:
                encrypted_id = encrypt_resp.json().get("encrypted_id", "")
                files.append({
                    "id": file["id"],
                    "filename": file["filename"],
                    "encrypted_id": encrypted_id
                })

    return render(request, "app/file_list.html", {"files": files})


def download_file(request, encrypted_id):
    api_url = f"{FASTAPI_URL}/files/download-direct/{encrypted_id}"
    headers = {
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


# Optional signup/login views (if you want to integrate)
def signup(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            response = requests.post(
                f"{FASTAPI_URL}/users/signup",
                json={"email": email, "password": password}
            )
            if response.status_code == 200:
                message = "✅ Signup successful! Please login."
            else:
                message = f"❌ Signup failed! ({response.status_code})"
    return render(request, "app/signup.html", {"message": message})


def login(request):
    message = ""
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if email and password:
            response = requests.post(
                f"{FASTAPI_URL}/users/login",
                data={"username": email, "password": password}
            )
            if response.status_code == 200:
                token = response.json().get("access_token")
                request.session["user_token"] = token
                return redirect("home")
            else:
                message = "❌ Login failed!"
    return render(request, "app/login.html", {"message": message})


def logout(request):
    request.session.pop("user_token", None)
    return redirect("home")
