from fastapi import APIRouter, Depends, Body
from .auth import oauth2_scheme, SECRET_KEY, ALGORITHM
from jose import jwt
from utils.json_store import read_user_data, save_user_data
from fastapi.exceptions import HTTPException

router = APIRouter()

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return {
            "username": payload["sub"],
            "role": payload["role"],
            "family_id": payload["family_id"]
        }
    except:
        raise HTTPException(status_code=401, detail="Token 无效")

#  获取用户定制化信息（从 json 读取）
@router.get("/me_data")
async def get_my_data(user=Depends(get_current_user)):
    return read_user_data(user["family_id"], user["username"])

#  保存用户定制化信息（写入 json 文件）
@router.post("/me_data")
async def update_my_data(data: dict = Body(...), user=Depends(get_current_user)):
    save_user_data(user["family_id"], user["username"], data)
    return {"message": "个人信息保存成功"}