from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
import os, shutil, json
from pydantic import BaseModel
from pathlib import Path

router = APIRouter()



#在每个小任务中，上传作业图片的接口
BASE_PATH = "/Users/liyao/Desktop/project/pvi/New_HW/backend/data"

import json

@router.post("/upload/homework")
async def upload_homework(
    file: UploadFile = File(...),
    family_id: str = Form(...),
    user_id: str = Form(...),
    task_id: str = Form(...)
):
    if not (family_id and user_id and task_id):
        raise HTTPException(status_code=400, detail="❌ 缺少必要参数")

    task_folder = os.path.join(BASE_PATH, family_id, "share", "homework", f"task_{task_id}")
    if not os.path.isdir(task_folder):
        raise HTTPException(status_code=404, detail=f"❌ 未找到任务文件夹: task_{task_id}")

    image_folder = os.path.join(task_folder, "image")
    os.makedirs(image_folder, exist_ok=True)

    save_path = os.path.join(image_folder, file.filename)

    try:
        with open(save_path, "wb") as f:
            shutil.copyfileobj(file.file, f)

        # ✅ 将文件名记录到 task_uploads.json
        record_path = os.path.join(task_folder, "task_uploads.json")
        uploads = []
        if os.path.exists(record_path):
            with open(record_path, "r", encoding="utf-8") as f:
                uploads = json.load(f)

        if file.filename not in uploads:
            uploads.append(file.filename)
            with open(record_path, "w", encoding="utf-8") as f:
                json.dump(uploads, f, ensure_ascii=False, indent=2)

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

    return {
        "status": "success",
        "filename": file.filename,
        "saved_to": save_path,
        "user_id": user_id
    }


@router.get("/get_uploaded_files")
async def get_uploaded_files(family_id: str = Query(...), task_id: str = Query(...)):
    task_folder = os.path.join(BASE_PATH, family_id, "share", "homework", f"task_{task_id}")
    record_path = os.path.join(task_folder, "task_uploads.json")

    if not os.path.exists(record_path):
        return {"files": []}

    with open(record_path, "r", encoding="utf-8") as f:
        uploads = json.load(f)

    return {"files": uploads}







#文本框上传内容的接口
class DescriptionRequest(BaseModel):
    family_id: str
    description: str
   #接受从前端传来的任务描述信息，并保存到对应的家庭目录下的 task_description.json 文件中
@router.post("/save_task_description")
def save_task_description(data: DescriptionRequest):
    base_path = Path(__file__).resolve().parent.parent / "data" / data.family_id / "share"
    base_path.mkdir(parents=True, exist_ok=True)
    save_file = base_path / "task_description.json"

    with open(save_file, "w", encoding="utf-8") as f:
        json.dump({"description": data.description}, f, ensure_ascii=False, indent=2)

    return {"message": "描述信息已保存", "path": str(save_file)}
    #将task_description.json文件中的任务描述信息读取出来，并返回给前端（保证刷新和每一位家庭成员能够看到）
@router.get("/get_task_description")
def get_description(family_id: str = Query(...)):
    path = Path(__file__).resolve().parent.parent / "data" / family_id / "share" / "task_description.json"
    if not path.exists():
        return {"description": ""}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"description": data.get("description", "")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取失败：{e}")






























# from fastapi import APIRouter, UploadFile, File, Form, HTTPException, Query
# import os, shutil, json

# router = APIRouter()

# BASE_PATH = "/Users/liyao/Desktop/project/pvi/New_HW/backend/data"

# @router.post("/upload/homework")
# async def upload_homework(
#     file: UploadFile = File(...),
#     family_id: str = Form(...)
# ):
#     if not family_id:
#         raise HTTPException(status_code=400, detail="缺少 family_id")

#     # 保存路径（不分类）
#     homework_dir = os.path.join(BASE_PATH, family_id, "share", "homework")
#     os.makedirs(homework_dir, exist_ok=True)

#     save_path = os.path.join(homework_dir, file.filename)

#     try:
#         with open(save_path, "wb") as f:
#             shutil.copyfileobj(file.file, f)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"文件保存失败: {str(e)}")

#     # ✅ 写入记录文件
#     record_path = os.path.join(homework_dir, "record.json")
#     if os.path.exists(record_path):
#         with open(record_path, "r", encoding="utf-8") as f:
#             record = json.load(f)
#     else:
#         record = []

#     if file.filename not in record:
#         record.append(file.filename)

#     with open(record_path, "w", encoding="utf-8") as f:
#         json.dump(record, f, ensure_ascii=False, indent=2)

#     return {
#         "status": "success",
#         "filename": file.filename,
#         "saved_to": save_path
#     }


# @router.get("/get/homework")
# async def get_homework(family_id: str = Query(...)):
#     record_path = os.path.join(BASE_PATH, family_id, "share", "homework", "record.json")
    
#     if not os.path.exists(record_path):
#         return {"homework": []}

#     with open(record_path, "r", encoding="utf-8") as f:
#         record = json.load(f)

#     return {"homework": record}