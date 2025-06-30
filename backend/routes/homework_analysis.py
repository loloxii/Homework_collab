from fastapi import APIRouter, Query, HTTPException
import os, json
from services.image_analyzer import extract_question_and_answer, chat_with_check_context, chat_with_combined_context,chat_with_analogy_context, chat_with_guidance_context
from pydantic import BaseModel
from collections import defaultdict
router = APIRouter()


@router.get("/analyze_homework")
async def analyze_homework(family_id: str = Query(...), task_id: str = Query(...)):
    """
    读取图片并提取题目答案，保存为 JSON 文件
    """
    base_dir = "/Users/liyao/Desktop/project/pvi/New_HW/backend"
    image_dir = os.path.join(base_dir, f"data/{family_id}/share/homework/{task_id}/image")
    task_json_path = os.path.join(base_dir, f"data/{family_id}/share/homework/{task_id}/task.json")


    if not os.path.exists(image_dir):
        raise HTTPException(status_code=404, detail=f"路径不存在: {image_dir}")
    if not os.path.exists(task_json_path):
        raise HTTPException(status_code=404, detail=f"未找到任务文件: {task_json_path}")

    results = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(image_dir, filename)
            try:
                content = extract_question_and_answer(image_path)
                results.append({
                    "filename": filename,
                    "answer": content
                })
            except Exception as e:
                results.append({
                    "filename": filename,
                    "error": str(e)
                })

    # 保存为 JSON 文件
    output_path = os.path.join(image_dir, "analysis_results.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)


      # === 3. 读取原 task.json 并写入 homeworkImage 字段 ===
    with open(task_json_path, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    if isinstance(task_data, dict):
        task_data = [task_data]  # 转为列表统一处理

    for task in task_data:
        if "homeworkImage" not in task:
            task["homeworkImage"] = []
        for r in results:
            if "error" not in r:
                task["homeworkImage"].append({
                    "filename": r["filename"],
                    "question": r.get("question", ""),
                    "answer": r.get("answer", "")
                })

    # === 4. 写回 task.json（可保持原格式） ===
    with open(task_json_path, "w", encoding="utf-8") as f:
        if len(task_data) == 1:
            json.dump(task_data[0], f, ensure_ascii=False, indent=2)
        else:
            json.dump(task_data, f, ensure_ascii=False, indent=2)

    return {
        "status": "success",
        "task_id": task_id,
        "num_processed": len(results),
        "results": results
    }



class ChatRequest(BaseModel):
    family_id: str
    task_id: str
    user_message: str


@router.post("/chat_putong")
def chat_putong(req: ChatRequest):
    try:
        reply, recent = chat_with_combined_context(
            family_id=req.family_id,
            task_id=req.task_id,
            user_message=req.user_message
        )
        return {"reply": reply, "history": recent}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"服务器内部错误: {e}")

#核对作业

# @router.post("/check_chat")
# async def parent_chat(req: ChatRequest):
#     reply, history = chat_with_homework_context(
#         family_id=req.family_id,
#         task_id=req.task_id,
#         user_message=req.user_message
#     )
#     return {
#         "reply": reply,
#         "history": history
#     }




#核对作业
class ChatCheckRequest(BaseModel):
    family_id: str
    task_id: str
    user_message: str

@router.post("/chat_check")
async def chat_check_handler(request: ChatCheckRequest):
    try:
        reply, recent_history = chat_with_check_context(
            family_id=request.family_id,
            task_id=request.task_id,
            user_message=request.user_message
        )
        return {"reply": reply, "history": recent_history}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检查对话出错：{str(e)}")
    


@router.post("/chat_analogy")
async def chat_analogy_handler(request: ChatCheckRequest):
    try:
        reply, recent_history = chat_with_analogy_context(
            family_id=request.family_id,
            task_id=request.task_id,
            user_message=request.user_message
        )
        return {"reply": reply, "history": recent_history}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"举一反三对话出错：{str(e)}")
    


@router.post("/chat_guidance")
def chat_guidance(req: ChatRequest):
    reply = chat_with_guidance_context(req.family_id, req.task_id, req.user_message)
    return {"reply": reply}

