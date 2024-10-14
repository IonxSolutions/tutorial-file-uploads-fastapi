from fastapi import FastAPI, File, UploadFile
import uvicorn
import requests
import logging

VERISYS_API_URL = "https://eu1.api.av.ionxsolutions.com/v1/malware/scan/file"
API_KEY = "your_api_key"

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

class ScanResult:
    def __init__(self, filename="", status="", content_type="", signals=None, metadata=None):
        self.filename = filename
        self.status = status
        self.content_type = content_type
        self.signals = signals if signals is not None else []
        self.metadata = metadata if metadata is not None else []

    def __repr__(self):
        return f"ScanResult(filename={self.filename},status={self.status}, content_type={self.content_type}, signals={self.signals}, metadata={self.metadata})"

def scan_file(file_content, filename):
    files = {'file': (filename, file_content)}
    headers = {'X-API-Key': API_KEY, 'Accept': '*/*'}
    
    response = requests.post(VERISYS_API_URL, headers=headers, files=files)

    # Was the scan successful?    
    if response.status_code == 201:
        result = response.json()

        # Print the full scan result to the console
        logger.debug(f"Scan result: {result}")

        scan_result = ScanResult(
            filename=filename,
            status=result["status"],
            content_type=result["content_type"],
            signals=result["signals"],
            metadata=result["metadata"]
        )

        return scan_result
    else:
        return ScanResult(status="error", metadata=[{"message": "Failed to scan file"}])

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    # Print information about the file to the console
    logger.debug(f"File Name: {file.filename}")
    logger.debug(f"File Size: {len(content)}")
    logger.debug(f"File MIME Type: {file.content_type}")
    
    # Scan file with Verisys API
    scan_result = scan_file(content, file.filename)

    # In real-life, you'd now use the scan result to determine what to do 
    # next - but here, we'll just return the scan results to the caller
    
    return scan_result

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
