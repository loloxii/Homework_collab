<template>
  <div class="chatbot-wrapper">
    <div class="chatbot-header">作业助手</div>

      <div class="chat-history">
        <div v-for="(msg, index) in chatStore.chatMessages" :key="index" :class="['chat-msg', msg.role === 'user' ? 'user' : 'bot']">
          <div class="bubble">{{ msg.content }}</div>
        </div>
      </div>

    <!-- 保留任务计划按钮 -->
    <!-- ✅ 替换任务计划按钮区域为多个功能按钮 -->
    <div class="task-button-area multi-buttons">
      <button class="mini-button" @click="loadAnalysisAnswer">检查答案</button>
      <button class="mini-button" @click="loadAnalogyAnswer" >举一反三</button>
      <button class="mini-button" @click="loadGuidance">解题指导</button>
      <!-- <button class="mini-button" @click="loadGuidance" :disabled="loading">解题指导</button> -->
      <button class="mini-button">小朋友使用</button>
    </div>

    <!-- 输入区域保留但禁用 -->
    <div class="input-area">
      <input
        v-model="userInput"
        class="text-input"
        placeholder="请输入你的问题..."
        @keyup.enter="sendMessage"
      />
      <button class="mini-button" @click="sendMessage">发送</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { useChatStore } from '../stores/chatStore'

const chatStore = useChatStore()
const userInput = ref('')

const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content) return

  // 1. 显示用户消息
  chatStore.addMessage({ role: 'user', content })
  userInput.value = ''

  try {
    const family_id = localStorage.getItem('family_id')
    const task_id = localStorage.getItem('task_id') // 从 localStorage 获取任务ID

    const res = await axios.post('http://localhost:8000/chat_putong', {
      family_id,
      task_id,
      user_message: content
    })
    console.log("family_id:", family_id, "task_id:", task_id)

    // 2. 显示 AI 回复
    chatStore.addMessage({ role: 'assistant', content: res.data.reply })
  } catch (err) {
    console.error('❌ 对话失败:', err)
    chatStore.addMessage({ role: 'assistant', content: '❌ 对话失败，请稍后重试。' })
  }
}

const loading = ref(false)

const loadAnalysisAnswer = async () => {
  const family_id = localStorage.getItem('family_id')
  const task_id = localStorage.getItem('task_id')  // 直接获取完整的 task_2

  if (!family_id || !task_id) {
    chatStore.addMessage({ role: 'assistant', content: '未找到任务信息，请重新进入页面。' })
    return
  }

  loading.value = true
  try {
    const res = await axios.post('http://localhost:8000/chat_check', {
      family_id,
      task_id,
      user_message: '请帮我检查这份作业的正确性'
    })

    if (res.data && res.data.reply) {
      chatStore.addMessage({ role: 'assistant', content: res.data.reply })
    } else {
      chatStore.addMessage({ role: 'assistant', content: '未找到解析内容。' })
    }
  } catch (err) {
    console.error('❌ 加载解析失败:', err)
    chatStore.addMessage({ role: 'assistant', content: '❌ 加载作业解析失败，请稍后重试。' })
  } finally {
    loading.value = false
  }
}



const loadAnalogyAnswer = async () => {
  const family_id = localStorage.getItem('family_id')
  const task_id = localStorage.getItem('task_id')

  if (!family_id || !task_id) {
    chatStore.addMessage({ role: 'assistant', content: '未找到任务信息，请重新进入页面。' })
    return
  }

  loading.value = true
  try {
    const res = await axios.post('http://localhost:8000/chat_analogy', {
      family_id,
      task_id,
      user_message: '请根据这些题目举一反三，生成类似的新题目。'
    })

    if (res.data && res.data.reply) {
      chatStore.addMessage({ role: 'assistant', content: res.data.reply })
    } else {
      chatStore.addMessage({ role: 'assistant', content: '未生成类似题。' })
    }
  } catch (err) {
    console.error('❌ 举一反三失败:', err)
    chatStore.addMessage({ role: 'assistant', content: '❌ 举一反三生成失败，请稍后重试。' })
  } finally {
    loading.value = false
  }
}






const loadGuidance = async () => {
  const family_id = localStorage.getItem('family_id')
  const task_id = localStorage.getItem('task_id')

  if (!family_id || !task_id) {
    chatStore.addMessage({ role: 'assistant', content: '未找到任务信息，请重新进入页面。' })
    return
  }

  loading.value = true
  try {
    const res = await axios.post('http://localhost:8000/chat_guidance', {
      family_id,
      task_id,
      user_message: '请告诉我如何用孩子能理解的方式解释这些题目'
    })

    chatStore.addMessage({ role: 'assistant', content: res.data.reply })
  } catch (err) {
    console.error('❌ 解题指导失败:', err)
    chatStore.addMessage({ role: 'assistant', content: '❌ 解题指导生成失败，请稍后重试。' })
  } finally {
    loading.value = false
  }
}
</script>


<style scoped>
.chatbot-wrapper {
  display: flex;
  flex-direction: column;
  height: 70vh;
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
  background-color: #eeeeee;
  color: #333;
  border-radius: 18px;
  line-height: 1.5;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.05);
  word-break: break-word;
  white-space: pre-wrap;
  border-bottom-left-radius: 6px;
}

.chat-msg.user .bubble {
  background-color: #cce5ff; /* 用户消息颜色 */
  border-bottom-left-radius: 18px;
  border-bottom-right-radius: 6px;
}

.chat-msg.bot .bubble {
  background-color: #eeeeee; /* AI 回复颜色 */
  border-bottom-right-radius: 18px;
  border-bottom-left-radius: 6px;
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
  cursor: pointer; /* ✅ 修复：允许点击 */
}
.multi-buttons {
  display: flex;
  gap: 26px;
  justify-content: flex-end;
  flex-wrap: wrap;
}
</style>