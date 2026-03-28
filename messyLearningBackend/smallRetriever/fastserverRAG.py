from fastapi import FastAPI,UploadFile,Form,File
from Rag_chatbot import bro, initialise_retrievers
from fastapi.responses import FileResponse, JSONResponse,HTMLResponse
import shutil
import os,requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse  
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3100"],  # React dev server ports
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)





@app.post("/upload_pdf")
async def upload_pdf(file:UploadFile = File(...)    ):
    if file.content_type != "application/pdf":
        return JSONResponse({"error": "Only PDF files are allowed"}, status_code=400)
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    
    with open(file_path,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
        
    try:
        initialise_retrievers(file_path)
        return {"message":f"{file.filename}uploaded and embedded succesfully"}
    except Exception as e:
        return JSONResponse({"error": f"Failed to process PDF: {e}"}, status_code=500)
    
    
    # headers = {"Content-Disposition": f"inline; filename={file.filename}"}
    # return FileResponse(file_path, media_type="application/pdf", headers=headers)

@app.post("/upload_and_ask")
async def upload_and_ask(file:UploadFile=File(...),query:str=Form(...)):
    if file.content_type != "application/pdf":
        return JSONResponse({"error":"only pdf files are allowed"}, status_code=400)
    
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    try:
        with open(file_path,'wb') as buffer:
            shutil.copyfileobj(file.file,buffer)
        
        initialise_retrievers(file_path)
        answer = bro(query)
        return {"message": "PDF Uploaded successfully", "answer": answer}
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in upload_and_ask:\n{error_trace}")  # Log full traceback
        return JSONResponse(
            {"error": f"Failed to process PDF: {str(e)}"}, 
            status_code=500
        )     

@app.post("/ask")
async def ask(request:dict):
    query=request.get("query","")
    if not query :
        return JSONResponse({"error":"chale jaa"})
    try:
        answer = bro(query)
        return {"answer": answer}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Failed to get response: {str(e)}"}
        )
