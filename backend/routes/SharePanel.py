from fastapi import APIRouter, Request, HTTPException
from pydantic import BaseModel
import json
import os
from collections import defaultdict

router = APIRouter()

DATA_DIR = "data"

# POST 请求的格式
class UserMessage(BaseModel):
    family_id: str
    message: dict  # 形如 {"role": "user", "content": "你好"}

@router.get("/load_chat_history")
def load_chat_history(family_id: str):
    filepath = os.path.join(DATA_DIR, family_id, "share", "share_history.json")
    if not os.path.exists(filepath):
        return {"history": []}
    with open(filepath, "r", encoding="utf-8") as f:
        history = json.load(f)
    return {"history": history}

@router.post("/save_user_message")
def save_user_message(msg: UserMessage):
    family_dir = os.path.join(DATA_DIR, msg.family_id, "share")
    os.makedirs(family_dir, exist_ok=True)
    filepath = os.path.join(family_dir, "share_history.json")

    history = []
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            history = json.load(f)

    history.append(msg.message)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

    return {"status": "ok"}



class TaskSummaryRequest(BaseModel):
    family_id: str

@router.post("/task_summary")
async def summarize_tasks(request: TaskSummaryRequest):
    family_id = request.family_id
    try:
        task_path = f"/Users/liyao/Desktop/project/pvi/New_HW/backend/data/{family_id}/share/saved_tasks.json"
        if not os.path.exists(task_path):
            raise FileNotFoundError(f"任务文件不存在：{task_path}")

        with open(task_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)

        member_stats = defaultdict(lambda: {"done": 0, "total": 0})

        for task in tasks:
            for member in task["assignee"]:
                member_stats[member]["total"] += 1
                if task["done"]:
                    member_stats[member]["done"] += 1

        summary_sentences = []
        for member, stats in member_stats.items():
            done = stats["done"]
            total = stats["total"]
            rate = done / total if total else 0
            percent = f"{rate * 100:.0f}%"

            # 参与度评价和建议
            if rate >= 0.75:
                sentence = f"{member}本周共参与 {total} 项任务，已完成 {done} 项（完成率 {percent}），参与度很高，建议继续保持。"
            elif rate >= 0.4:
                sentence = f"{member}本周共协助完成 {total} 项任务，其中 {done} 项已完成（完成率 {percent}），建议适当提高参与频率。"
            else:
                sentence = f"{member}仅完成了 {done}/{total} 项任务（完成率 {percent}），参与度偏低，建议增加参与任务的数量。"
            summary_sentences.append(sentence)

        overall_summary = "以下是本周家庭成员的作业辅导参与情况总结：\n\n" + "\n".join(summary_sentences)
        return {"summary": overall_summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务总结失败：{str(e)}")