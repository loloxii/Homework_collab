# backend/routes/user_data.py

from fastapi import APIRouter, HTTPException
import os, json
from pydantic import BaseModel
from fastapi import Query

router = APIRouter()

class ChildPayload(BaseModel):
    family_id: str
    child: dict

BASE_PATH = "/Users/liyao/Desktop/project/pvi/New_HW_v2/backend/data"

# ✅ 保存共享：小朋友信息 → 存到 share 文件夹中
@router.post("/save/child")
async def save_child_info(payload: ChildPayload):
    family_id = payload.family_id
    child_info = payload.child

    if not family_id or not child_info:
        raise HTTPException(status_code=400, detail="缺少 family_id 或 child")

    save_path = os.path.join(BASE_PATH, family_id, "share", "child.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(child_info, f, ensure_ascii=False, indent=2)

    return {"status": "success", "path": save_path}


# ✅ 获取共享：小朋友信息 → 从share文件夹中读取
@router.get("/get/child")
async def get_child_info(family_id: str = Query(...)):
    load_path = os.path.join(BASE_PATH, family_id, "share", "child.json")
    if not os.path.exists(load_path):
        raise HTTPException(status_code=404, detail="未找到小朋友信息")

    with open(load_path, "r", encoding="utf-8") as f:
        child_info = json.load(f)

    return {"child": child_info}



# ✅ 保存个人：家庭成员信息 → 存到个人文件夹中
@router.post("/save/family")
async def save_family_info(data: dict):
    family_id = data.get("family_id")
    username = data.get("username")
    members_info = data.get("members")

    if not family_id or not username or not members_info:
        raise HTTPException(status_code=400, detail="缺少 family_id、username 或 members")

    save_path = os.path.join(BASE_PATH, family_id, username, "family.json")
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "w", encoding="utf-8") as f:
        json.dump(members_info, f, ensure_ascii=False, indent=2)

    return {"status": "success", "path": save_path}

# ✅ 获取个人：家庭成员信息
@router.get("/get/family")
async def get_family_info(family_id: str = Query(...), username: str = Query(...)):
    file_path = os.path.join(BASE_PATH, family_id, username, "family.json")
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="未找到家长信息")

    with open(file_path, "r", encoding="utf-8") as f:
        members_info = json.load(f)

    return {"members": members_info}