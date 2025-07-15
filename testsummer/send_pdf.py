# send_pdf.py
import httpx, json, pathlib

PDF_FILE = "4-16.pdf"
url = "http://127.0.0.1:8000/upload-pdf"

with httpx.Client(timeout=60.0) as client:
    files = {"file": (pathlib.Path(PDF_FILE).name,
                      open(PDF_FILE, "rb"),
                      "application/pdf")}
    resp = client.post(url, files=files)
    print(json.dumps(resp.json(), ensure_ascii=False, indent=2))
