from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status, Depends, Cookie
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pydantic import BaseModel
import pytesseract
from PIL import Image
from auth.access import get_user
import templates
from fastapi import Request
from fastapi.security import OAuth2PasswordBearer
import tempfile
import os
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
from auth.pwdencryp import hash_pass, verify_pass
from auth.JWT import create_token, verify_token

# FastAPI instance
app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

temp_db = {} #for storing user creds temporarily

class User(BaseModel):
    username: str
    password: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") #related to auth0


#-----------USER REGISTER---------
#register html
@app.get("/register", response_class=HTMLResponse)
async def show_register_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

#register endpoint
@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    if username in temp_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already registered user")
    
    hashed_pass = hash_pass(password)
    temp_db[username] = hashed_pass
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND) 
    #JSONResponse(content={"message": "Registration successful! Please log in."}, status_code=status.HTTP_201_CREATED))
    #return {"message": "User registration complete"}


#-------LOGIN after REGISTER-------
#login html
@app.get("/login", response_class=HTMLResponse)
async def show_login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#login endpoint
@app.post("/login")
async def login(username: str=Form(...), password: str= Form()):
    hashed = temp_db.get(username)
    if hashed is None or not verify_pass(password, hashed):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect credentials")
    
    token = create_token(user_id=username)
    response = RedirectResponse(url="/upload", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=token, httponly=True)  # Set httponly for security
    return response



#--------UPLOAD FILE and perform OCR--------
#file upload html
@app.get("/upload", response_class=HTMLResponse)
async def show_upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

#file content extraction 
ocr_extracted_storage={}

#Token-based access and file upload
@app.post("/upload")
async def upload_file(file: UploadFile = File(...) ,User: dict = Depends(get_user)):
    if not file.filename.endswith(".png"):
        raise HTTPException(status_code=400, detail="Only PNG files are allowed.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        temp_file.write(await file.read())
        temp_file_path = temp_file.name

    try:
        image = Image.open(temp_file_path)
        ocr_extracted = pytesseract.image_to_string(image)
        # Store OCR result for later (you can enhance this part)
        ocr_extracted_storage[file.filename] = ocr_extracted
        return {"filename": file.filename, "text": ocr_extracted.strip()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during OCR processing: {str(e)}")
    



#--------------QA model distibert------------------
#from models.longformer import process
from models.AutoQA import generate_answers

#ask html
@app.get("/ask", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("ask.html", {"request": request})

def clean_text(text):
    # Add any preprocessing steps here (e.g., removing unwanted characters, correcting spacing)
    return text.strip()

#ask endpoiny
@app.post("/ask")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    ocr_texts = ocr_extracted_storage.get(filename)
    if not ocr_texts:
        raise HTTPException(status_code=400, detail="No OCR extracted text found as input")
    context = clean_text(ocr_texts)
    answer = generate_answers(question, context)
    print("Reached main ask_question")
    return {"answer": answer}



#---------------Authorize user----------------
def get_user(request: Request)-> User:
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token missing")
    
    try:
        payload = verify_token(token)
        username = payload["sub"]  # Extract the username from the token payload
        user = temp_db.get(username)  # Retrieve user data from your temporary DB
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return {"username": username, "password": user}  # Return a dictionary-like user object
        #return payload["sub"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


"""def get_user(token: str = Dependsoauth2_scheme)():
    try:
        payload = verify_token(token)
        return payload["sub"]
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")"""
