# backend/auth.py
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import datetime, timedelta

router = APIRouter()

# 硬编码的用户数据
fake_users_db = {
    "p11": {"password": "111111", "role": "爸爸", "family_id": "fam001"},
    "p12": {"password": "111111", "role": "妈妈", "family_id": "fam001"},
    "p13": {"password": "111111", "role": "奶奶", "family_id": "fam001"},
    "p14": {"password": "111111", "role": "小朋友自己", "family_id": "fam001"},

    "p21": {"password": "444444", "role": "father", "family_id": "fam002"},
    "p22": {"password": "555555", "role": "mother", "family_id": "fam002"},
    "p23":  {"password": "666666", "role": "child",  "family_id": "fam002"},

    "father3": {"password": "777777", "role": "father", "family_id": "fam003"},
    "mother3": {"password": "888888", "role": "mother", "family_id": "fam003"},
    "child3":  {"password": "999999", "role": "child",  "family_id": "fam003"},
}
SECRET_KEY = "your-secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

# create JWT token
def create_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

#判断当前用户是否存在
@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user = fake_users_db.get(form.username)
    if not user or user["password"] != form.password:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token_data = {
        "sub": form.username,
        "role": user["role"],
        "family_id": user["family_id"]
    }
    token = create_token(token_data)
    return {
        "access_token": token,
        "token_type": "bearer",
        "username": form.username,
        "role": user["role"],
        "family_id": user["family_id"]  # 前端可直接使用
    }

# 获取当前用户的所有信息
@router.get("/me")
async def get_user_info(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload["sub"],
            "role": payload["role"],
            "family_id": payload["family_id"]
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="无效 Token")
    

@router.get("/get_members")
async def get_family_members(family_id: str = Query(...)):
    members = []
    for username, info in fake_users_db.items():
        if info["family_id"] == family_id:
            members.append({
                "member_id": username,
                "role": info["role"]
            })
    return {"members": members}