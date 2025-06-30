<template>
  <div class="chatbot-wrapper">
    <div class="chatbot-header">作业助手</div>

    <div ref="chatContainer" class="chat-history">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['chat-msg', msg.sender]"
      >
        <div class="bubble">{{ msg.text }}</div>
      </div>
      <div v-if="isLoading" class="chat-msg bot">
        <div class="bubble typing">正在加载...</div>
      </div>
    </div>

    <div class="task-button-area">
      <button class="mini-button" @click="generateTasks">任务计划</button>
    </div>

    <div class="input-area">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        class="text-input"
        placeholder="请输入你的问题..."
      />
      <button class="mini-button" @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted } from 'vue'
import axios from 'axios'
import { useTaskStore } from '../stores/taskStore'
const taskStore = useTaskStore()

const props = defineProps({
  familyId: {
    type: String,
    required: true
  }
})

const messages = ref([
  { sender: 'bot', text: '你好，我是你的作业助手' }
])
const isLoading = ref(false)
const userInput = ref('')
const chatContainer = ref(null)
const hasShownGeneralSuggestion = ref(false)

function scrollToBottom() {
  nextTick(() => {
    const el = chatContainer.value
    if (el) el.scrollTop = el.scrollHeight
  })
}

async function sendMessage() {
  const content = userInput.value.trim()
  if (!content) return

  messages.value.push({ sender: 'user', text: content })
  userInput.value = ''
  isLoading.value = true
  scrollToBottom()

  try {
    // 调用任务调整接口 /adjust_plan
    const res = await axios.post('http://localhost:8000/adjust_plan', {
      family_id: props.familyId,
      user_feedback: content
    })

    const reply = res.data.reply || '暂无回应'
    messages.value.push({ sender: 'bot', text: reply })
  } catch (err) {
    messages.value.push({
      sender: 'bot',
      text: '回应失败，可能还未生成初始任务，请先点击“任务计划”按钮'
    })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

async function generateTasks() {
  if (!props.familyId) {
    messages.value.push({ sender: 'bot', text: '未找到家庭 ID，无法生成任务' })
    return
  }

  isLoading.value = true
  messages.value.push({ sender: 'bot', text: '正在生成任务，请稍候...' })

  try {
    const res = await axios.post('http://localhost:8000/generate_task_plan', {
      family_id: props.familyId
    })

    const data = res.data
    const summary = data["本周任务表总结"] || ""
    const division = data["家庭成员合作建议"] || ""
    const warmTips = data["温馨建议"] || ""
    const taskTable = data["任务分工表"] || []

    // ✅ 新增这一行：将任务同步给任务表组件
    taskStore.setLLMTasks(taskTable)

    // ✅ 保持原有聊天逻辑
    messages.value.push({ sender: 'bot', text: `本周任务表总结：\n${summary}` })
    if (division) messages.value.push({ sender: 'bot', text: `家庭成员分工建议：\n${division}` })
    if (warmTips) messages.value.push({ sender: 'bot', text: `温馨建议：\n${warmTips}` })

  } catch (err) {
    messages.value.push({ sender: 'bot', text: '❌ 生成失败，请稍后再试。' })
  } finally {
    isLoading.value = false
    scrollToBottom()
  }
}

onMounted(async () => {
  if (!props.familyId) {
    console.warn('⚠️ familyId 未传入，跳过加载 general_suggestion')
    return
  }

  if (hasShownGeneralSuggestion.value) return

  try {
    const res = await axios.get('http://localhost:8000/load_general_suggestion', {
      params: { family_id: props.familyId }  // ✅ key 为后端要求的格式
    })

    const summary = res.data.summary || ''
    const division = res.data.division || ''
    const tips = res.data.tips || ''

    if (summary) messages.value.push({ sender: 'bot', text: `本周任务表总结：\n${summary}` })
    if (division) messages.value.push({ sender: 'bot', text: `家庭成员分工建议：\n${division}` })
    if (tips) messages.value.push({ sender: 'bot', text: `温馨建议：\n${tips}` })

    hasShownGeneralSuggestion.value = true
    scrollToBottom()
  } catch (err) {
    console.error('无法加载 general_suggestion:', err)
    messages.value.push({ sender: 'bot', text: '无法加载上次建议内容，请稍后再试。' })
  }
})

</script>

<style scoped>
.chatbot-wrapper {
  display: flex;
  flex-direction: column;
  height: 70vh; /* ✅ 固定高度，撑满整个视口 */
  width: 100%;
  border-radius: 16px;
  background-color: #fff;
  overflow: hidden;
}

.chatbot-header {
  background-color: #409EFF;
  color: white;
  text-align: center;
  font-size: 18px;
  font-weight: bold;
  padding: 16px;
  flex-shrink: 0;
}

.chat-history {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: #f9f9f9;
  min-height: 0;
}

.chat-history::-webkit-scrollbar {
  width: 6px;
}
.chat-history::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 3px;
}

.chat-msg {
  display: flex;
  margin-bottom: 12px;
}

.chat-msg.user {
  justify-content: flex-end;
}

.chat-msg.bot {
  justify-content: flex-start;
}

.bubble {
  max-width: 75%;
  padding: 12px 16px;
  font-size: 15px;
  background-color: #e8f4fe;
  color: #333;
  border-radius: 18px;
  line-height: 1.5;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  word-break: break-word;
  white-space: pre-wrap;
}

.chat-msg.bot .bubble {
  background-color: #eeeeee;
  border-bottom-left-radius: 6px;
}

.typing {
  font-style: italic;
  color: #888;
  font-size: 14px;
}

.task-button-area {
  padding: 8px 16px 0;
  text-align: right;
  background: #f0f0f0;
  flex-shrink: 0;
}

.input-area {
  display: flex;
  gap: 8px;
  padding: 10px 16px;
  border-top: 1px solid #ddd;
  background-color: #f0f0f0;
  flex-shrink: 0;
}

.text-input {
  flex: 1;
  padding: 8px 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
  font-size: 14px;
}

.mini-button {
  background-color: #409EFF;
  color: white;
  border: none;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 13px;
  cursor: pointer;
}

.mini-button:hover {
  background-color: #66b1ff;
}
</style>