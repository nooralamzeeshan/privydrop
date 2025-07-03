import requests

# Render deployed API URL hai
API_BASE_URL = "https://privydrop.onrender.com"

# Encrypted ID yaha daalo jo tumhe milti hai /encrypt-id se
encrypted_id = "gAAAAABoZaoYmZ_2bg_yet3fkN0ICaxssqQRi28X-vc0HU_2lF9zXqUy1GgVC-BiYx2_BWnvFpYHIIGnWMgZJveaHSUXxDZezw=="

# Access token yaha daalo jo login se milta hai
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzeWVkemVlc2hhbjgwMzEwMUBnbWFpbC5jb20iLCJyb2xlIjoiY2xpZW50In0.p-30lNJ-R322NORz-3CcvLCchzAVp3LNt7u7rFR0kNg"

# Download API endpoint
download_url = f"{API_BASE_URL}/files/download-direct/{encrypted_id}"

# Headers me token bhejna jaruri hai
headers = {"token": access_token}

# Request
response = requests.get(download_url, headers=headers)

# Check karo status
if response.status_code == 200:
    # File ko save karo
    with open("CA-MCA-UnitV.pptx", "wb") as f:
        f.write(response.content)
    print("✅ File downloaded successfully!")
else:
    print("❌ Error downloading file:", response.status_code, response.text)
