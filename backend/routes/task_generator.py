from fastapi import APIRouter, Body, Query
from pydantic import BaseModel
from services.task_allocation import generate_task_plan, chat_with_feedback, refresh_chat_history
from typing import List, Dict
import json
from pathlib import Path

router = APIRouter()

class TaskGenRequest(BaseModel):
    family_id: str

class AdjustRequest(BaseModel):
    family_id: str
    user_feedback: str

@router.post("/generate_task_plan")
def task_with_history(request: TaskGenRequest):
    """
    接收前端传来的 family_id，调用 DeepSeek 生成家庭作业任务建议
    """
    result = generate_task_plan(request.family_id)
    return result

# @router.post("/adjust_plan")
# def adjust_plan_from_feedback(request: AdjustRequest):
#     """
#     接收用户反馈，结合 saved_tasks 和 general_suggestion，调用 DeepSeek 进行任务调整建议
#     """
#     reply = chat_with_feedback(
#         family_id=request.family_id,
#         user_feedback=request.user_feedback
#     )
#     return {"reply": reply}


@router.post("/adjust_plan")
def adjust_plan_from_feedback(request: AdjustRequest):
    """
    接收用户反馈，结合 saved_tasks 和 general_suggestion，调用 DeepSeek 进行任务调整建议
    """
    reply = chat_with_feedback(
        family_id=request.family_id,
        user_feedback=request.user_feedback,
    )
    return {"reply": reply}



class RefreshRequest(BaseModel):
    family_id: str


@router.post("/refresh_chat_history")
def refresh_history(request: RefreshRequest):
    """
    重置该家庭的对话历史，基于最新 saved_tasks 和 general_suggestion 内容
    """
    try:
        refresh_chat_history(request.family_id)
        return {"message": "Chat history refreshed successfully"}
    except Exception as e:
        return {"error": str(e)}


@router.get("/load_general_suggestion")
def load_general_suggestion(family_id: str = Query(...)):
    base = Path(__file__).resolve().parent.parent
    path = base / "data" / family_id / "share" / "general_suggestion.json"
    if not path.exists():
        return {"message": "❌ 暂无建议", "summary": "", "division": "", "tips": ""}
    
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "summary": data.get("本周任务表总结", ""),
        "division": data.get("家庭成员合作建议", ""),
        "tips": data.get("温馨建议", "")
    }