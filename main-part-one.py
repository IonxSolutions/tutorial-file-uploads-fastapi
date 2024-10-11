from fastapi import FastAPI, File, UploadFile
import uvicorn
import logging

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()

    # Print information about the file to the console
    logger.debug(f"File Name: {file.filename}")
    logger.debug(f"File Size: {len(content)}")
    logger.debug(f"File MIME Type: {file.content_type}")
    
    # Return information about the file to the caller - note that the
    # content_type can easily be spoofed
    return {"filename": file.filename, "file_size": len(content), "file_mime_type": file.content_type}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
