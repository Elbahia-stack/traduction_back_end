from database import Base, engine,get_db
import model  # ton fichier models.py
from fastapi import FastAPI, HTTPException, Depends,Header
from sqlalchemy.orm import Session
from schemas import UserRegistre,TranslateRequest,TranslateResponse
from security import hash_password, verify_password 
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from dotenv import load_dotenv
from auth import create_access_token, verify_token,fake_users
from fastapi.middleware.cors import CORSMiddleware
import os
import requests

Base.metadata.create_all(bind=engine)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

load_dotenv()

API_URL = os.getenv("API_URL")
HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN is missing in .env")

headers = {"Authorization": f"Bearer {HF_TOKEN}"}

def query(payload,model_name):
    url = f"{API_URL}/{model_name}" 
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    return response.json()


app=FastAPI()

origins = [
     "http://localhost:3000",
    "http://172.26.112.1:3000",
    "https://traduction-front-end.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/register")
def regester(user:UserRegistre,db: Session = Depends(get_db)):
    db_user = db.query(model.User).filter(model.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    hashed = hash_password(user.password)

    new_user = model.User(username=user.username, password=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"id": new_user.id, "username": new_user.username}


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
   
    user = db.query(model.User).filter(model.User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Username ou password incorrect")

    token = create_access_token(user.username,user.password)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/traduire", response_model=TranslateResponse)
def translate_text(data: TranslateRequest, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    if data.sens == "en-fr":
        model_name = "Helsinki-NLP/opus-mt-en-fr"
    elif data.sens == "fr-en":
        model_name = "Helsinki-NLP/opus-mt-fr-en"
    else:
        raise HTTPException(status_code=400, detail="Sens de traduction invalide, utilisez 'en-fr' ou 'fr-en'")

    result = query({"inputs": data.text}, model_name=model_name)
    traduction = result[0]['translation_text'] if result else ""

    return TranslateResponse(
        
        original=data.text,
        translated=traduction
    )












