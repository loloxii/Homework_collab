import base64
import os
import io
from PIL import Image
import requests
import json
from dotenv import load_dotenv

API_KEY = os.getenv("DOUBAO_API_KEY"),
API_URL = "https://ark.cn-beijing.volces.com/api/v1/chat/completions"
MODEL_NAME = "doubao-1.5-vision-lite-250315"

def extract_question_and_answer(image_path: str) -> str:
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图像不存在: {image_path}")

    try:
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            buf = io.BytesIO()
            img.save(buf, format="PNG")
            b64_img = base64.b64encode(buf.getvalue()).decode()
    except Exception as e:
        raise Exception(f"图片处理失败：{e}")

    prompt = "请阅读这张图中的题目内容，提取题目内容, 并写出清晰的解答步骤和最终答案。"

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64_img}"}},
                    {"type": "text", "text": prompt}
                ]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API 请求失败：{response.status_code} - {response.text}")
    




#普通模式
import os
import json
import requests

API_KEY = "b8f775f7-98ff-405d-a522-0abff5a558cb"
API_URL = "https://ark.cn-beijing.volces.com/api/v1/chat/completions"
MODEL_NAME = "doubao-1.5-vision-lite-250315"

def chat_with_combined_context(family_id: str, task_id: str, user_message: str):
    """
    基于 task.json 与用户对话，记录历史为 putong/chat_history.json 和 putong/check.json
    """
    import os, json, requests

    BASE_DIR = "/Users/liyao/Desktop/project/pvi/New_HW/backend"
    task_dir = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}")
    image_dir = os.path.join(task_dir, "image")
    putong_dir = os.path.join(image_dir, "putong")

    os.makedirs(putong_dir, exist_ok=True)

    # === 1. 读取 task.json ===
    task_path = os.path.join(task_dir, "task.json")
    if not os.path.exists(task_path):
        raise FileNotFoundError(f"❌ 未找到任务文件：{task_path}")

    with open(task_path, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    if isinstance(task_data, dict):
        task_data = [task_data]
    elif not isinstance(task_data, list):
        raise ValueError("task.json 格式错误，必须是字典或列表")

    # === 2. 构造 Prompt（只基于 task.json） ===
    prompt = "以下是孩子需要完成的作业任务以及识别出的内容，请帮助家长辅导孩子完成，回答的内容要简洁明了，清晰易懂，最多不能超过100字：\n\n"

    for task in task_data:
        prompt += f"【任务名称】{task.get('name', '无名称')}\n"
        prompt += f"【说明】{task.get('description', '无说明')}\n"
        prompt += f"【辅导方式】{task.get('tutoringMethod', '无辅导方式')}\n"

        hw_imgs = task.get("homeworkImage", [])
        for idx, img in enumerate(hw_imgs):
            prompt += f"\n📎 图片 {idx+1}: {img.get('filename', '')}\n"
            question = img.get("question", "").strip()
            answer = img.get("answer", "").strip()
            if question:
                prompt += f"【题目】{question}\n"
            if answer:
                prompt += f"【解答】{answer}\n"

        prompt += "\n"

    # === 3. 加载历史对话 ===
    chat_path = os.path.join(putong_dir, "chat_history.json")
    check_path = os.path.join(putong_dir, "check.json")
    history_messages = []

    if os.path.exists(chat_path):
        with open(chat_path, "r", encoding="utf-8") as f:
            history_messages = json.load(f)

    # === 4. 构造消息并调用豆包 API ===
    messages = [{"role": "system", "content": prompt}] + history_messages + [
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    try:
        data = response.json()
    except Exception:
        raise Exception(f"⚠️ 无法解析 JSON 响应: {response.text}")

    if "choices" not in data or not data["choices"]:
        raise Exception(f"⚠️ API 响应异常: {data}")

    reply = data["choices"][0]["message"]["content"]

    # === 5. 保存对话历史 ===
    history_messages.append({"role": "user", "content": user_message})
    history_messages.append({"role": "assistant", "content": reply})

    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(history_messages, f, ensure_ascii=False, indent=2)

    with open(check_path, "w", encoding="utf-8") as f:
        json.dump(history_messages, f, ensure_ascii=False, indent=2)

    return reply, history_messages[-6:]




#检查模式
def chat_with_check_context(family_id: str, task_id: str, user_message: str):
    """
    基于 analysis_results.json 内容初始化对话，并将历史记录保存在 image/check 文件夹中。
    """
    BASE_DIR = "/Users/liyao/Desktop/project/pvi/New_HW/backend"
    image_dir = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}/image")
    check_dir = os.path.join(image_dir, "check_mode")

    # 1. 创建 check 文件夹（如果不存在）
    os.makedirs(check_dir, exist_ok=True)

    # 2. 加载 analysis_results.json
    analysis_path = os.path.join(image_dir, "analysis_results.json")
    if not os.path.exists(analysis_path):
        raise FileNotFoundError(f"未找到分析文件: {analysis_path}")

    with open(analysis_path, "r", encoding="utf-8") as f:
        analysis_data = json.load(f)

    # 3. 构造系统提示：展示所有答案（而不是题目）
    system_prompt = "以下是孩子的作业答案内容，请根据这些内容与家长进行互动：\n\n"
    for i, item in enumerate(analysis_data):
        answer = item.get("answer", "")
        system_prompt += f"【内容{i+1}】\n{answer}\n\n"

    # 4. 历史记录路径（check 文件夹内）
    chat_path = os.path.join(check_dir, "chat_history.json")
    check_path = os.path.join(check_dir, "check.json")

    history_messages = []
    if os.path.exists(chat_path):
        with open(chat_path, "r", encoding="utf-8") as f:
            history_messages = json.load(f)

    # 5. 构造对话消息体
    messages = [{"role": "system", "content": system_prompt}] + history_messages + [
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"豆包 API 失败: {response.status_code} - {response.text}")

    reply = response.json()["choices"][0]["message"]["content"]

    # 6. 保存历史记录
    history_messages.append({"role": "user", "content": user_message})
    history_messages.append({"role": "assistant", "content": reply})

    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(history_messages, f, ensure_ascii=False, indent=2)
    with open(check_path, "w", encoding="utf-8") as f:
        json.dump(history_messages, f, ensure_ascii=False, indent=2)

    return reply, history_messages[-6:]




#举一反三
def chat_with_analogy_context(family_id: str, task_id: str, user_message: str):
    """
    基于 task.json 中的作业答案内容生成类似题目，实现“举一反三”模式。
    保存历史记录在 image/analogy_mode 文件夹。
    """
    import os, json, requests

    BASE_DIR = "/Users/liyao/Desktop/project/pvi/New_HW/backend"
    task_path = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}/task.json")
    analogy_dir = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}/image/analogy_mode")
    os.makedirs(analogy_dir, exist_ok=True)

    if not os.path.exists(task_path):
        raise FileNotFoundError(f"❌ 未找到任务文件: {task_path}")

    with open(task_path, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    if isinstance(task_data, dict):
        task_data = [task_data]
    elif not isinstance(task_data, list):
        raise ValueError("task.json 格式错误，必须是 dict 或 list")

    # 构造系统提示
    system_prompt = "以下是孩子的作业题目及答案，请基于这些题目生成3~5个举一反三的类似题，题型、知识点应保持一致，适合小学阶段：\n\n"

    for task in task_data:
        name = task.get("name", "")
        system_prompt += f"【任务】{name}\n"
        images = task.get("homeworkImage", [])
        for img in images:
            answer = img.get("answer", "").strip()
            if answer:
                system_prompt += f"【内容】\n{answer}\n\n"

    # 加载历史对话
    chat_path = os.path.join(analogy_dir, "chat_history.json")
    history_messages = []
    if os.path.exists(chat_path):
        with open(chat_path, "r", encoding="utf-8") as f:
            history_messages = json.load(f)

    # 构造完整消息体
    messages = [{"role": "system", "content": system_prompt}] + history_messages + [
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"豆包 API 调用失败: {response.status_code} - {response.text}")

    data = response.json()
    reply = data["choices"][0]["message"]["content"]

    # 保存历史记录
    history_messages.append({"role": "user", "content": user_message})
    history_messages.append({"role": "assistant", "content": reply})

    with open(chat_path, "w", encoding="utf-8") as f:
        json.dump(history_messages, f, ensure_ascii=False, indent=2)

    return reply, history_messages[-6:]



def chat_with_guidance_context(family_id: str, task_id: str, user_message: str):
    """
    为家长生成适合小学生理解的解题指导。
    读取 task.json 文件，输出面向儿童的解释建议。
    """
    import os, json, requests

    BASE_DIR = "/Users/liyao/Desktop/project/pvi/New_HW/backend"
    task_path = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}/task.json")
    guidance_dir = os.path.join(BASE_DIR, f"data/{family_id}/share/homework/{task_id}/image/guidance")

    os.makedirs(guidance_dir, exist_ok=True)

    if not os.path.exists(task_path):
        raise FileNotFoundError(f"未找到任务文件：{task_path}")

    with open(task_path, "r", encoding="utf-8") as f:
        task_data = json.load(f)

    if isinstance(task_data, dict):
        task_data = [task_data]

    # 构建 prompt：为家长生成适合儿童理解的讲解方式
    prompt = "请根据以下任务，为家长提供如何向小学生解释这些题目的方法。语言要通俗易懂、贴近孩子的认知水平。\n\n"

    for task in task_data:
        prompt += f"【任务名称】{task.get('name', '')}\n"
        prompt += f"【说明】{task.get('description', '')}\n"
        prompt += f"【辅导方式】{task.get('tutoringMethod', '')}\n"

        for idx, img in enumerate(task.get("homeworkImage", [])):
            prompt += f"\n📎 图片 {idx+1}: {img.get('filename', '')}\n"
            answer = img.get("answer", "").strip()
            if answer:
                prompt += f"【解答】{answer}\n"

        prompt += "\n"

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": user_message}
    ]

    payload = {
        "model": MODEL_NAME,
        "messages": messages
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        raise Exception(f"豆包 API 请求失败: {response.status_code} - {response.text}")

    reply = response.json()["choices"][0]["message"]["content"]

    # 保存记录
    history_path = os.path.join(guidance_dir, "guidance.json")
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump(messages + [{"role": "assistant", "content": reply}], f, ensure_ascii=False, indent=2)

    return reply




