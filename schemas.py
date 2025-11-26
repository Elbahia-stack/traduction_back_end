from pydantic import BaseModel



class UserRegistre(BaseModel):
    username: str
    password: str




class TranslateRequest(BaseModel):
    text: str
    sens: str
class TranslateResponse(BaseModel):
       
    original: str   
    translated: str     