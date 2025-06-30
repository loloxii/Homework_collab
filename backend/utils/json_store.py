# utils/json_store.py
import json
import os

STORE_PATH = "stored_result.json"

#更新存储结果（任务分配表）到 JSON 文件
def save_result_to_file(result):
    with open(STORE_PATH, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

def load_result_from_file():
    if not os.path.exists(STORE_PATH):
        return {"suggestion": "暂无设置数据", "assignment_table": []}
    with open(STORE_PATH, "r", encoding="utf-8") as f:
        return json.load(f)



#存储聊天历史的 JSON 文件路径
HISTORY_PATH = "chat_history.json"

def load_chat_history():
    if not os.path.exists(HISTORY_PATH):
        return []
    
    with open(HISTORY_PATH, "r", encoding="utf-8") as f:
        content = f.read().strip()
        if not content:
            return []  # ✅ 文件为空，返回空历史
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            print("❌ chat_history.json 格式错误，已忽略内容")
            return []

def save_chat_history(history):
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)



#用户数据存储路径和操作函数
DATA_ROOT = "data"  # 基础目录

def get_user_json_path(family_id: str, username: str):
    folder = os.path.join(DATA_ROOT, family_id)
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, f"{username}.json")

def read_user_data(family_id: str, username: str):
    path = get_user_json_path(family_id, username)
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_user_data(family_id: str, username: str, data: dict):
    path = get_user_json_path(family_id, username)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)