from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request

app = FastAPI()

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

# Serve static files (if needed)
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    return templates.TemplateResponse("create_user.html", {"request": request})

@app.post("/register")
async def register(username: str = Form(...), password: str = Form(...)):
    # Here you would typically save the user information to a database
    return {"message": f"User {username} registered successfully!"}
