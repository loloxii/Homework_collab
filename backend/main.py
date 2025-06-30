from fastapi import FastAPI
from models.schemas import SettingsPayload,ChatInput
# from services.generator import generate_suggestion,parent_chat_with_context
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from utils.family_loader import load_family_data_with_members
from utils.json_store import save_result_to_file, load_result_from_file
from routes import auth, user_data, login_data, upload_homework,homework_analysis, task, task_generator,s_load_tasks,SharePanel


app = FastAPI()

# 添加跨域中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 允许的前端地址（开发模式用）
    allow_credentials=True,
    allow_methods=["*"],                      # 允许所有方法（GET、POST等）
    allow_headers=["*"],                      # 允许所有请求头
)

app.include_router(auth.router)
app.include_router(login_data.router)
app.include_router(user_data.router)
app.include_router(upload_homework.router)
app.include_router(homework_analysis.router)
app.include_router(task.router,prefix="/api")
app.include_router(task_generator.router)
app.include_router(s_load_tasks.router)
app.include_router(SharePanel.router)











# @app.post("/generate_suggestion")
# async def generate_suggestion_api(payload: SettingsPayload):
#     print("✅ 收到前端数据:", payload)
#     result = generate_suggestion(payload)
#     print("生成结果:", result)
#     save_result_to_file(result)
#     print("📝 已保存至 JSON 文件:", result)
#     return {
#         "message": "生成成功",
#         "suggestion": result["suggestion"],
#         "assignment_table": result["assignment_table"]
#     }


# @app.get("/load_settings")
# async def load_settings():
#     result = load_result_from_file()
#     return {
#         "suggestion": result.get("suggestion", "暂无设置数据"),
#         "assignment_table": result.get("assignment_table", [])
#     }

# @app.post("/save_assignment_table")
# async def save_assignment_table(data: dict):
#     assignment_table = data.get("assignment_table", [])
    
#     # 加载旧结果
#     old_data = load_result_from_file()

#     # 用 assignment_table 覆盖旧数据中的表，保留 suggestion
#     updated_data = {
#         "suggestion": old_data.get("suggestion", "暂无设置数据"),
#         "assignment_table": assignment_table
#     }

#     save_result_to_file(updated_data)
#     return {"message": "任务清单已保存"}


# @app.post("/parent_chat")
# async def parent_chat(input: ChatInput):
#     reply = parent_chat_with_context(input.message)
#     return {"reply": reply}

# @app.post("/update_task_progress")
# async def update_task_progress(data: dict):
#     print(f"📩 收到进度更新请求: {data}")  # 一定要加这行！
#     task_name = data.get("小任务")
#     new_progress = data.get("完成进度")

#     if not task_name or new_progress is None:
#         return {"error": "任务名或进度缺失"}

#     result = load_result_from_file()
#     updated = False
#     for task in result["assignment_table"]:
#         if task["小任务"] == task_name:
#             task["完成进度"] = new_progress
#             updated = True
#             break

#     if not updated:
#         return {"error": f"未找到小任务 {task_name}"}

#     save_result_to_file(result)
#     return {"message": f"✅ 已更新 {task_name} 的进度为 {new_progress}%"}