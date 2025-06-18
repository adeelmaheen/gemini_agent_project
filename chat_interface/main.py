from fastapi import FastAPI
from chainlit.utils import mount_chainlit
import os
from dotenv import load_dotenv

# Load your variables
load_dotenv()
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")

app = FastAPI()

# Keep your FastAPI endpoints
@app.get("/hello")
def hello():
    return {"message": "Hello from FastAPI!"}

# Mount Chainlit chat as sub-app under /chat
mount_chainlit(app=app, target="app.py", path="/chat")
