from fastapi import APIRouter, Query, HTTPException
import os
import json
from pathlib import Path
from pydantic import BaseModel
from typing import List,Any

router = APIRouter()

@router.get("/s_load_saved_tasks")
def load_saved_tasks(family_id: str = Query(...)):
    file_path = f"data/{family_id}/share/saved_tasks.json"

    if not os.path.exists(file_path):
        return {"tasks": []}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"tasks": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取任务失败: {str(e)}")
    


#能够在后端生成对应的文件夹


class TaskModel(BaseModel):
    id: int
    name: str
    description: str
    assignee: List[str]
    tutoringMethod: str
    day: str
    start: str
    end: str
    done: bool
    homeworkImage: List[Any]

class SaveTasksRequest(BaseModel):
    family_id: str
    tasks: List[TaskModel]


BASE_PATH = Path("/Users/liyao/Desktop/project/pvi/New_HW/backend/data")



def task_changed(old_task, new_task):
    for key in new_task:
        if key != "homeworkImage" and old_task.get(key) != new_task.get(key):
            return True
    return False

@router.post("/saved_tasks_folds")
async def update_saved_tasks(request: SaveTasksRequest):
    family_id = request.family_id
    new_tasks = [task.dict() for task in request.tasks]

    family_dir = BASE_PATH / family_id
    saved_path = family_dir / "share" / "saved_tasks.json"
    homework_base = family_dir / "share" / "homework"
    homework_base.mkdir(parents=True, exist_ok=True)

    is_first_time = not saved_path.exists()

    if not is_first_time:
        with open(saved_path, 'r') as f:
            old_tasks = {int(t["id"]): t for t in json.load(f)}
    else:
        old_tasks = {}

    updated_tasks = []
    new_task_ids = set()

    for task in new_tasks:
        tid = int(task["id"])
        new_task_ids.add(tid)
        task_folder = homework_base / f"task_{tid}"
        task_json_path = task_folder / "task.json"

        # 新建/更新任务目录
        if is_first_time or (tid not in old_tasks) or task_changed(old_tasks[tid], task):
            task_folder.mkdir(parents=True, exist_ok=True)
            print(f"📁 新建或更新任务文件夹: {task_folder}")

            # ✅ 写入 task.json
            with open(task_json_path, "w", encoding="utf-8") as tf:
                json.dump(task, tf, ensure_ascii=False, indent=2)
            print(f"📄 写入任务详情到: {task_json_path}")
        else:
            print(f"✅ 跳过未变动任务: task_{tid}")

        updated_tasks.append(task)

    # ✅ 删除多余目录
    existing_folders = [p for p in homework_base.iterdir() if p.is_dir() and p.name.startswith("task_")]
    deleted_folders = []

    for folder in existing_folders:
        try:
            folder_id = int(folder.name.replace("task_", ""))
            if folder_id not in new_task_ids:
                for f in folder.iterdir():
                    f.unlink()
                folder.rmdir()
                deleted_folders.append(folder.name)
                print(f"🗑️ 删除多余任务目录: {folder}")
        except Exception as e:
            print(f"⚠️ 无法删除 {folder}: {e}")

    # ✅ 保存 saved_tasks.json
    with open(saved_path, 'w') as f:
        json.dump(updated_tasks, f, ensure_ascii=False, indent=2)

    return {
        "status": "ok",
        "first_time": is_first_time,
        "updated_count": len(updated_tasks),
        "deleted_folders": deleted_folders
    }