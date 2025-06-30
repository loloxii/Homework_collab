# import json
# #任务分工的prompt
# def build_homework_allocation_prompt(child_info: dict, members: list, homework_descriptions: str) -> str:
#     # strategies = open("/Users/liyao/Desktop/project/pvi/New_HW/backend/prompts/family_strategies.txt", encoding="utf-8").read()
#     return f"""
# 你是一位擅长任务协作设计的儿童家庭教育专家。现在你需要协助一个家庭**高效地协作完成孩子的假期作业**，并促进小朋友综合能力的成长；
# 在设计任务时，请充分考虑家庭成员的特长，个人优势，以及小朋友的年龄，认知水平，兴趣爱好，性格特点，擅长科目；
# 你的目标是通过合理的任务分工和协作，帮助小朋友在家庭作业中全面提升能力，同时促进家庭成员之间的合作与沟通；
# 将每个家庭作业内容拆解为多个小任务，并合理分配给家庭成员，尽量让每个家庭成员都要参与。每个小任务都要明确目标、负责人、辅导方式以及培养的小朋友能力。

# ---
# 请基于以下信息，为他们设计一份**详细的家庭辅导计划**，包括合理的任务拆解和具体的分工安排。

# 小朋友信息：
# {child_info}

# 家庭成员信息：
# {format_family_members(members)}

# 假期作业内容：
# {homework_descriptions}
# ---

# 必须生成以下内容：
# 1. 本周任务总结：对本周需要完成的假期作业，对每个假期作业中所有子任务进行总结；
# 2. 家庭成员合作建议:对每一个家庭作业，分别说明家庭成员如何配合完整每一个子任务；
# 3. 任务分工表：请将每个“家庭作业”细化为小任务，包含每天的作业安排和每个家庭成员的具体任务，并为每个任务明确指定负责的家庭成员；
#     3.1 每个子任务需要指定：
#         - 任务名称
#         - 辅导人（家庭成员姓名）
#         - 辅导方式说明 （如何协助与辅导）
#         - 第几天（Day 1 到 Day 7）
#         - 开始作业时间（时间返回格式比如:09:00）
#         - 预计结束时间（时间返回格式比如:15:00）
#     3.2 每个任务需具有唯一 ID，从 1 开始编号；
#     3.3 辅导人中只能出现家庭成员的角色，辅导人不能是小朋友，不能够出现“合作”，每个小任务都需要一位有具体的辅导人者；
#     3.4 所有任务需以 JSON 数组返回，字段包括：
#         - id, name, assignee, day, start, end, done（初始为 false）, homeworkImage（为空数组）；
#     3.5 开始时间和结束时间不能全部集中在同一时间段，应该分散在每天的不同时间段，若在家庭成员不可以辅导的时间，可以安排一些小朋友能够独立在家完成的任务。
#     3.6 早上，下午，晚上，各个时间段至少要有1个小任务
# 4. 生成家长辅导小朋友作业过程中的温馨建议；

# ---


# 请以 JSON 数组格式输出，结构如下：
# {{
#   "本周任务表总结":“简洁总结每项假期任务和其子任务目标。”,
#   “家庭成员合作建议”: “为每项作业提供具体的家庭成员配合方式。”,
#   "任务分工表": [
#     {{
#       "id": 1,
#       "name": "任务名称",
#       “description”: "任务目标与内容"
#       "assignee": "参与者姓名",
#       “tutoringMethod”: "具体的协助或辅导方式",
#       "day": "",
#       "start": "HH:MM",
#       "end": "HH:MM",
#       "done": false,
#       "homeworkImage": []
#     }},
#   "温馨建议": "针对家长辅导过程中给出的亲切建议和注意事项。",
#     ...
#   ]
# }}

# """.strip()








# # 在任务分配时引导用户进行继续对话的prompt
# def build_chat_intro_prompt(child_info: dict, members: list, saved_tasks: dict, general_suggestion: dict) -> str:
#     return f"""
# 你现在是一名了解家庭背景的作业协作助手。
# 以下是该家庭的孩子信息、家庭成员信息、任务分工表和协作建议。请你在与家长的对话中，根据其反馈生成**简洁明了、清晰易懂、个性化**的修改建议。

# 请注意：
# 1. 不得使用 JSON 格式返回任务数据；
# 2. 生成的建议必须符合{', '.join(child_info.get('grade', []))}小朋友的学习能力和知识储备；
# 3. 需要考虑家庭成员的辅导时间和擅长科目，建议内容应与家庭成员的偏好和能力相匹配；
# 4. 建议内容应结合小朋友的年级、作业类型、学习习惯，以及家长的辅导时间与擅长科目；
# 3. 建议应在已有安排基础上进行微调，而非完全重写；
# 4. 请用鼓励、亲切的语气引导家长提出反馈，共同优化任务分工。


# 【家庭成员信息】
# {format_family_members(members)}

# 【任务分工表】
# {json.dumps(saved_tasks, ensure_ascii=False, indent=2)}

# 【协作建议】
# {json.dumps(general_suggestion, ensure_ascii=False, indent=2)}
# """.strip()



# def format_family_members(members: list) -> str:
#     return "\n".join([f"- {m['role']}，比较擅长{m['subjectPreference']}, 可以进行辅导的时间段：{m['educationConcept']}" for m in members])



# #deepseek的prompt
# import json
# #任务分工的prompt
# def build_homework_allocation_prompt(child_info: dict, members: list, homework_descriptions: str) -> str:
#     return f"""
# 你现在是{', '.join(child_info.get("grade"))}小学生家长。
# 暑假第一周目前计划完成以下假期作业内容{homework_descriptions}，将假期作业内容拆解为多个小任务，并合理分配给家庭成员。

# 你的任务是：
# 1. 根据每位家庭成员的信息充分考虑每一位家庭成员辅导偏好，优势和可以进行辅导的时间，将每个作业合理分配给家庭成员；{format_family_members(members)}；
# 2. 在作业分工过程中需要尽量让每一位家庭成员都参与到小任务中，帮助小朋友在假期作业中全面提升能力，同时促进家庭成员之间的合作与沟通；
# 3. 生成本周任务表总结
# 4. 生成家庭成员合作建议:每一个假期作业，不同家庭成员之间如何协助与辅导
# 5. 生成一周作业计划表，包含每天的作业安排和每个家庭成员的具体任务，尽量让每个家庭成员的参与度相等，白天家庭成员没空时，可以安排一些小朋友能够独立完成的任务；
#     5.1 小作业个任务需要指定：
#         - 任务名称（如“阅读理解”）
#         - 负责人（家庭成员角色，可以是多位比如[爸爸，妈妈]）
#         - 第几天（Day 1 到 Day 7）
#         - 开始时间（如 09:00）
#         - 结束时间（如 10:00）
#     5.2 每个任务需具有唯一 ID，从 1 开始编号；
#     5.3 所有任务需以 JSON 数组返回，字段包括：
#         - id, name, assignee, day, start, end, done（初始为 false）, homeworkImage（为空数组）；
# 6. 生成家长辅导小朋友作业过程中的温馨建议；


# 请以 JSON 数组格式输出，结构如下：
# {{
#   "本周任务表总结": "",
#   “家庭成员合作建议”: "",
#   "任务分工表": [
#     {{
#       "id": 1,
#       "name": "任务名称",
#       "assignee": "负责人姓名",
#       "day": "Day 1",
#       "start": "09:00",
#       "end": "10:00",
#       "done": false,
#       "homeworkImage": []
#     }},
#   "温馨建议": "",
#     ...
#   ]
# }}

# """.strip()




















import json
#任务分工的prompt
def build_homework_allocation_prompt(child_info: dict, members: list, homework_descriptions: str) -> str:
    
    return f"""
你是一位在家庭合作策略与任务规划领域拥有丰富经验的儿童家庭教育专家。现在你需要协助一个家庭**高效地协作完成孩子的假期作业**，并促进小朋友综合能力的成长；
在设计任务时，请充分考虑家庭成员的特长，个人优势，以及小朋友的年龄，认知水平，兴趣爱好，性格特点，擅长科目；
你的目标是通过合理的任务分工和协作，帮助小朋友在家庭作业中全面提升能力，同时促进家庭成员之间的合作与沟通；
将每个家庭作业内容拆解为多个小任务，并合理分配给家庭成员，尽量让每个家庭成员都要参与。每个小任务都要明确目标、负责人、辅导方式以及培养的小朋友能力;
每个家庭作业都要有多位家庭成员的参与。

注意：
1. 该小朋友是{', '.join(child_info.get("grade"))}小学生，生成的内容要符合该年级的小朋友学习；



请基于以下信息，为他们设计一份**详细的家庭辅导计划**，包括合理的任务拆解和具体的分工安排。
---
小朋友信息：
{child_info}

家庭成员信息：
{format_family_members(members)}

多个家庭作业内容：
{homework_descriptions}

---

必须生成以下内容：
1. 本周任务总结：对本周需要完成的假期作业，对每个假期作业中所有子任务进行总结；
2. 家庭成员合作建议:对每一个家庭作业，分别说明家庭成员如何配合完整每一个子任务，输出需要是字符串；
3. 任务分工表：请将每个“家庭作业”细化为小任务，包含每天的作业安排和每个家庭成员的具体任务，并为每个任务明确指定负责的家庭成员；
    3.1 每个子任务需要指定：
        - 任务名称
        - 辅导人（家庭成员姓名）
        - 辅导方式说明 （如何协助与辅导）
        - 第几天（Day 1 到 Day 7）
        - 开始作业时间（时间返回格式比如:09:00）
        - 预计结束时间（时间返回格式比如:15:00）
    3.2 每个任务需具有唯一 ID，从 1 开始编号；
    3.3 辅导人中只能出现家庭成员的角色，辅导人不能是小朋友，不能够出现“合作”，每个小任务都需要一位有具体的辅导人者；
    3.4 所有任务需以 JSON 数组返回，字段包括：
        - id, name, assignee, day, start, end, done（初始为 false）, homeworkImage（为空数组）；
    3.5 开始时间和结束时间不能全部集中在同一时间段，应该分散在每天的不同时间段，若在家庭成员不可以辅导的时间，可以安排一些小朋友能够独立在家完成的任务。
    3.6 早上，下午，晚上，各个时间段至少要有1个小任务
    3.7 分配给每位家庭成员的任务数量要尽可能相等
4. 生成家长辅导小朋友作业过程中的温馨建议；


请以 JSON 数组格式输出，结构如下：
{{
  "本周任务表总结":“”,
  “家庭成员合作建议”: “”,
  "任务分工表": [
    {{
      "id": 1,
      "name": "任务名称",
      “description”: "任务目标与内容"
      "assignee": "辅导人姓名",
      “tutoringMethod”: "如何协助与辅导",
      "day": "",
      "start": "",
      "end": "",
      "done": false,
      "homeworkImage": []
    }},
  "温馨建议": "",
    ...
  ]
}}

""".strip()



# 在任务分配时引导用户进行继续对话的prompt
def build_chat_intro_prompt(child_info: dict, members: list, saved_tasks: dict, general_suggestion: dict) -> str:
    return f"""
你现在是一名了解家庭背景的作业协作助手。
以下是该家庭的孩子信息、家庭成员信息、任务分工表和协作建议。请你在与家长的对话中，根据其反馈生成**简洁明了、清晰易懂、个性化**的修改建议。

请注意：
1. 不得使用 JSON 格式返回任务数据；
2. 生成的建议必须符合{', '.join(child_info.get('grade', []))}小朋友的学习能力和知识储备；
3. 需要考虑家庭成员的辅导时间和擅长科目，建议内容应与家庭成员的偏好和能力相匹配；
4. 建议内容应结合小朋友的年级、作业类型、学习习惯，以及家长的辅导时间与擅长科目；
3. 建议应在已有安排基础上进行微调，而非完全重写；
4. 请用鼓励、亲切的语气引导家长提出反馈，共同优化任务分工。


【家庭成员信息】
{format_family_members(members)}

【任务分工表】
{json.dumps(saved_tasks, ensure_ascii=False, indent=2)}

【协作建议】
{json.dumps(general_suggestion, ensure_ascii=False, indent=2)}
""".strip()



def format_family_members(members: list) -> str:
    return "\n".join([f"- {m['role']}，比较擅长{m['subjectPreference']}, 可以进行辅导的时间段：{m['educationConcept']}" for m in members])
