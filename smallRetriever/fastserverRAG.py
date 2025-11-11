from fastapi import FastAPI,UploadFile,Form,File
from Rag_chatbot import bro,initialise_retirevers
from fastapi.responses import FileResponse, JSONResponse,HTMLResponse
import shutil
import os,requests
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse  

app= FastAPI()

UPLOAD_DIR = "uploads"
# os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.get("/",response_class=HTMLResponse)
async def home():
    return """
<!DOCTYPE html>
    <html>
    <head>
        <title>PDF Chatbot</title>
        <style>
            body { font-family: Arial; margin: 40px; }
            #chatbox { border: 1px solid #ccc; padding: 10px; height: 400px; overflow-y: scroll; border-radius: 8px; }
            .msg { margin: 5px 0; padding: 8px; border-radius: 6px; max-width: 80%; }
            .user { background-color: #daf0ff; align-self: flex-end; }
            .bot { background-color: #eaeaea; }
            input, button { margin-top: 10px; }
        </style>
    </head>

    <body>
        <h2>Chat with your pdf </h2>
        <form id="uploadform">
            <input type="file" name="file" accept="application/pdf" required>
            <button type="submit">Upload PDF</button>
        </form>
        
        <div id="status"></div>

        
        <div id="chatContainer">
            <div id="chatbox"></div>
            <form id="chatForm">
                <input type="text" id="query" placeholder="Ask something..." size="60" required>
                <button type="submit">Send</button>
            </form>
        </div>
        
        <script>
        
        const chatbox = document.getElementById("chatbox");
            //handle the upload file
            document.getElementById("uploadform").addEventListener("submit",async(e)=>{
                e.preventDefault();
                const formData=new FormData(e.target)
                const res = await fetch("/upload_pdf", { method: "POST", body: formData });
                const data = await res.json();
            document.getElementById("status").innerText = data.message || data.error;
                if (res.ok) {
                document.getElementById("queryForm").style.display = "block";
            }
            })

        // Send query
        document.getElementById("chatForm").addEventListener("submit", async (e) => {
            e.preventDefault();
            const query = document.getElementById("query").value.trim();
            if (!query) return;

            addMessage(query, "user");
            document.getElementById("query").value = "";

            const res = await fetch("/ask", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ query })
            });

            const data = await res.json();
            addMessage(data.answer || data.error, "bot");
        });

        function addMessage(text, sender) {
            const div = document.createElement("div");
            div.className = "msg " + sender;
            div.innerText = text;
            chatbox.appendChild(div);
            chatbox.scrollTop = chatbox.scrollHeight;
        }
            
        </script>

    </body>
</html>
"""


@app.post("/upload_pdf")
async def upload_pdf(file:UploadFile = File(...)    ):
    if file.content_type != "application/pdf":
        return JSONResponse({"error": "Only PDF files are allowed"}, status_code=400)
    file_path = os.path.join(UPLOAD_DIR,file.filename)
    
    with open(file_path,'wb') as buffer:
        shutil.copyfileobj(file.file,buffer)
        
    try:
        initialise_retirevers(file_path)
        return {"message":f"{file.filename}uploaded and embedded succesfully"}
    except Exception as e:
        return JSONResponse({"error": f"Failed to process PDF: {e}"}, status_code=500)
    
    
    # headers = {"Content-Disposition": f"inline; filename={file.filename}"}
    # return FileResponse(file_path, media_type="application/pdf", headers=headers)


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
