from langchain_community.chat_models import ChatOpenAI
from langchain.chat_models import ChatOpenAI 
from langchain.schema import SystemMessage, AIMessage, BaseMessage, HumanMessage
from utils.family_loader import load_family_data_with_members
from prompts.task_allocation_prompt import build_chat_intro_prompt, build_homework_allocation_prompt
import json
import os
import re
from dotenv import load_dotenv

load_dotenv() 
# 初始化 DeepSeek Chat 模型
llm = ChatOpenAI(
    model="deepseek-chat",    #"deepseek-chat"
    temperature=0.5,
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),

    openai_api_base="https://api.deepseek.com"
)

def clean_and_parse_output(raw_output: str) -> dict:
    """
    清理 LLM 的 Markdown JSON 格式输出并解析
    """
    cleaned = re.sub(r"^```json\s*|\s*```$", "", raw_output.strip())
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return {"error": "模型输出无法解析为 JSON", "raw_output": raw_output}


def generate_task_plan(family_id: str) -> dict:
    """
    使用 DeepSeek LLM 根据家庭数据生成作业任务分工 JSON，并保存到本地文件

    Args:
        family_id: 家庭编号

    Returns:
        dict: 包含 “整体协作建议” 和 “任务分工表” 的 JSON
    """
    # 加载数据
    child_info, members, homework_desc = load_family_data_with_members(family_id)

    # 构造 Prompt
    prompt = build_homework_allocation_prompt(child_info, members, homework_desc)

    # 保存路径
    save_dir = f"/Users/liyao/Desktop/project/pvi/New_HW/backend/data/{family_id}/share"
    os.makedirs(save_dir, exist_ok=True)

    intro_path = os.path.join(save_dir, "debug_intro_prompt1.txt")
    with open(intro_path, "w", encoding="utf-8") as txt_file:
        txt_file.write(prompt)

    # 调用 LLM
    response = llm([HumanMessage(content=prompt)])
    result = clean_and_parse_output(response.content)

    # 如果解析失败，返回错误
    if "error" in result:
        print("⚠️ 模型输出解析失败:\n", result["raw_output"])
        return result


    # 保存“整体协作建议”为 JSON 格式
    general_path = os.path.join(save_dir, "general_suggestion.json")
    with open(general_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "本周任务表总结": result.get("本周任务表总结", "无"),
                "家庭成员合作建议": result.get("家庭成员合作建议", "无"),
                "温馨建议": result.get("温馨建议", "无")
            },
            f,
            ensure_ascii=False,
            indent=2
        )

    # 保存“任务分工表”
    task_path = os.path.join(save_dir, "saved_tasks.json")
    with open(task_path, "w", encoding="utf-8") as f:
        json.dump(result.get("任务分工表", []), f, ensure_ascii=False, indent=2)

    return result





# def chat_with_feedback(family_id: str, user_feedback: str) -> str:
#     base_dir = f"/Users/liyao/Desktop/project/pvi/New_HW/backend/data/{family_id}/share"
#     task_path = os.path.join(base_dir, "saved_tasks.json")
#     suggestion_path = os.path.join(base_dir, "general_suggestion.json")
#     history_path = os.path.join(base_dir, "task_allocation_chat_history.json")

#     # ✅ 自动加载家庭结构数据
#     child_info, members, homework_descriptions = load_family_data_with_members(family_id)

#     messages: list[BaseMessage] = []

#     # 若存在历史则加载
#     if os.path.exists(history_path):
#         with open(history_path, "r", encoding="utf-8") as f:
#             raw = json.load(f)
#             for msg in raw:
#                 if msg["type"] == "human":
#                     messages.append(HumanMessage(content=msg["content"]))
#                 elif msg["type"] == "ai":
#                     messages.append(AIMessage(content=msg["content"]))
#     else:
#         # 首次构造上下文
#         with open(task_path, "r", encoding="utf-8") as f:
#             saved_tasks = json.load(f)
#         with open(suggestion_path, "r", encoding="utf-8") as f:
#             general_suggestion = json.load(f)

#         # ✅ prompt 构建时也可以加入 homework_descriptions
#         intro = build_chat_intro_prompt(child_info, members, saved_tasks, general_suggestion)

#         intro_path = os.path.join(base_dir, "debug_intro_prompt2.txt")
#         with open(intro_path, "w", encoding="utf-8") as txt_file:
#             txt_file.write(intro)

#         messages.append(HumanMessage(content=intro))
#         messages.append(AIMessage(content="✅ 我已了解当前情况，请问您希望我如何调整？"))

#     messages.append(HumanMessage(content=user_feedback))

#     response = llm(messages)
#     messages.append(AIMessage(content=response.content))

#     with open(history_path, "w", encoding="utf-8") as f:
#         json.dump(
#             [{"type": "human" if isinstance(m, HumanMessage) else "ai", "content": m.content} for m in messages],
#             f,
#             ensure_ascii=False,
#             indent=2
#         )

#     return response.content




# def refresh_chat_history(family_id: str):
#     """
#     刷新并重置对话历史为当前 saved_tasks + general_suggestion 内容
#     """
#     base_dir = f"/Users/liyao/Desktop/project/pvi/New_HW/backend/data/{family_id}/share"
#     history_path = os.path.join(base_dir, "task_allocation_chat_history.json")
#     task_path = os.path.join(base_dir, "saved_tasks.json")
#     suggestion_path = os.path.join(base_dir, "general_suggestion.json")

#     with open(task_path, "r", encoding="utf-8") as f:
#         saved_tasks = json.load(f)
#     with open(suggestion_path, "r", encoding="utf-8") as f:
#         general_suggestion = json.load(f)

#     child_info, members, homework_descriptions = load_family_data_with_members(family_id)
#     intro = build_chat_intro_prompt(child_info, members, saved_tasks, general_suggestion)

#     intro_path = os.path.join(base_dir, "debug_intro_prompt3.txt")
#     with open(intro_path, "w", encoding="utf-8") as txt_file:
#         txt_file.write(intro)

#     # intro = (
#     #     "以下是该家庭目前的任务分工表和协作建议，请根据用户后续反馈给出合理的修改建议。"
#     #     "建议需要简洁明了，用户能够清晰易懂，不能使用JSON格式返回任务数据到前端。\n\n"
#     #     f"【任务分工表】\n{json.dumps(saved_tasks, ensure_ascii=False, indent=2)}\n\n"
#     #     f"【协作建议】\n{json.dumps(general_suggestion, ensure_ascii=False, indent=2)}"
#     # )

#     history = [
#         {"type": "human", "content": intro},
#         {"type": "ai", "content": "✅ 好的，我已了解当前任务安排，请问您有什么建议或反馈？"}
#     ]

#     with open(history_path, "w", encoding="utf-8") as f:
#         json.dump(history, f, ensure_ascii=False, indent=2)


