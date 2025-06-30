from fastapi import APIRouter, Body, Query, HTTPException
from pydantic import BaseModel
from typing import List
import os, json
from pathlib import Path

router = APIRouter()

class Task(BaseModel):
    id: str
    name: str
    description: str
    assignee: List[str]
    tutoringMethod: str
    day: str
    start: str
    end: str
    done: bool
    homeworkImage: list = []  # ✅ 保证 homeworkImage 字段保存

class TaskSaveRequest(BaseModel):
    family_id: str
    tasks: List[Task]

@router.post("/save_tasks")
async def save_tasks(payload: TaskSaveRequest = Body(...)):
    print("✅ 正在保存任务（assignee 是 role）:", payload.family_id)
    BASE_DIR = Path(__file__).resolve().parent.parent
    save_path = BASE_DIR / "data" / payload.family_id / "share" / "saved_tasks.json"
    os.makedirs(save_path.parent, exist_ok=True)

    try:
        # 直接保存 role 而非 member_id
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump([task.dict() for task in payload.tasks], f, ensure_ascii=False, indent=2)

        print(f"✅ 写入成功: {save_path}")
        return {"message": f"✅ Tasks saved for family '{payload.family_id}'"}
    except Exception as e:
        print("❌ 写入失败:", e)
        raise HTTPException(status_code=500, detail=f"写入任务文件失败：{e}")


@router.get("/load_tasks")
def load_tasks(family_id: str = Query(..., description="家庭 ID")):
    from pathlib import Path
    BASE_DIR = Path(__file__).resolve().parent.parent  # 即 backend/
    load_path = BASE_DIR / "data" / family_id / "share" / "saved_tasks.json"
    
    print(f"🪵 正在尝试读取任务文件: {load_path}")  # ✅ 添加调试信息

    if not load_path.exists():
        return {"tasks": []}

    try:
        with open(load_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
        return {"tasks": tasks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"加载任务失败：{str(e)}")
    

