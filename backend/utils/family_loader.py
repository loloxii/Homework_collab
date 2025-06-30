import json
import os

def load_family_data_with_members(family_id: str):
    """
    加载指定家庭的 child_info, 所有成员信息，以及作业描述。

    Args:
        family_id (str): 家庭编号，例如 "fam001"

    Returns:
        tuple: (child_info: dict, members: list, homework_descriptions: str)
    """
    base_path = f"/Users/liyao/Desktop/project/pvi/New_HW/backend/data/{family_id}"
    share_path = os.path.join(base_path, "share")

    # 加载 child.json
    with open(os.path.join(share_path, "child.json"), "r", encoding="utf-8") as f:
        raw_child = json.load(f)
        child_info = {
            "grade": raw_child.get("grades", []),
            "traits": raw_child.get("traits", []),
            "hobbies": raw_child.get("hobbies", [])
        }

    # 加载 task_description.json
    with open(os.path.join(share_path, "task_description.json"), "r", encoding="utf-8") as f:
        task = json.load(f)
        homework_descriptions = task.get("description", "无作业内容")

    # 遍历所有成员目录，读取 family.json
    members = []
    for member_id in os.listdir(base_path):
        member_dir = os.path.join(base_path, member_id)
        if not os.path.isdir(member_dir):
            continue
        member_file = os.path.join(member_dir, "family.json")
        if os.path.exists(member_file):
            with open(member_file, "r", encoding="utf-8") as f:
                member_data = json.load(f)
                if isinstance(member_data, list):
                    members.extend(member_data)
                # 如果是单个 dict，兼容性处理（不推荐的旧格式）
                elif isinstance(member_data, dict):
                    members.append(member_data)

    return child_info, members, homework_descriptions