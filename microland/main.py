from fastapi import FastAPI,UploadFile, File, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from pdf2image import convert_from_path
import pytesseract
from pytesseract import image_to_string
from PIL import Image
import tempfile
import templates
import os

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    return {"message": f"User {username} registered successfully!"}

ocr_extracted_storage={}

@app.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload_files(file: UploadFile=File(...)):
    if not file.filename.endswith(".png"):
        raise HTTPException(status_code=400, detail="Only JPG and JPEG files are allowed.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png" )as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        image = Image.open(temp_file_path)
        ocr_extracted = pytesseract.image_to_string(image)

        ocr_extracted_storage[file.filename]=ocr_extracted
        return {"filename": file.filename, "text": ocr_extracted.strip()}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during OCR processing: {str(e)}")
    

from models.longformer import process
from models.AutoQA import generate_answers

@app.get("/ask", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("ask.html", {"request": request})

def clean_text(text):
    # Add any preprocessing steps here (e.g., removing unwanted characters, correcting spacing)
    return text.strip()


@app.post("/ask")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    ocr_texts = ocr_extracted_storage.get(filename)
    
    if not ocr_texts:
        raise HTTPException(status_code=400, detail="No OCR extracted text found as input")

    # Process the OCR text using the Longformer model
    context = clean_text(ocr_texts)
    
    # Generate answers using the QA model based on the processed context
    answer = generate_answers(question, context)
    
    print("Reached main ask_question")
    
    return {"answer": answer}

