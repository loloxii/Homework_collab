<template>
  <div class="chat-wrapper">
    <!-- 消息展示区域 -->
    <div class="chat-messages">
      <div
        v-for="(msg, index) in messages"
        :key="index"
        :class="['chat-message', msg.role]"
      >
        <div class="bubble">{{ msg.content }}</div>
      </div>
    </div>

    <!-- 输入框 -->
    <div class="chat-input">
      <input
        v-model="userInput"
        @keyup.enter="sendMessage"
        placeholder="请输入你的留言..."
      />
      <button @click="sendMessage">发送</button>
    </div>

    <!-- 每周总结按钮 -->
    <div class="summary-button">
      <button @click="loadWeeklySummary">每周总结</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

const userInput = ref('')
const messages = ref([])
const family_id = localStorage.getItem('family_id') || 'test_family'

// 滚动到底部
const scrollToBottom = () => {
  setTimeout(() => {
    const container = document.querySelector('.chat-messages')
    if (container) {
      container.scrollTop = container.scrollHeight
    }
  }, 100)
}

// 加载历史消息
const loadMessages = async () => {
  try {
    const res = await axios.get(`http://localhost:8000/load_chat_history?family_id=${family_id}`)
    messages.value = res.data.history || []
    scrollToBottom()
  } catch (err) {
    console.error('❌ 加载聊天记录失败:', err)
  }
}

// 发送消息，仅保存，无AI回复
const sendMessage = async () => {
  const content = userInput.value.trim()
  if (!content) return

  const newMsg = { role: 'user', content }
  messages.value.push(newMsg)
  userInput.value = ''

  try {
    await axios.post('http://localhost:8000/save_user_message', {
      family_id,
      message: newMsg
    })
  } catch (err) {
    console.error('❌ 消息保存失败:', err)
  }

  scrollToBottom()
}


const loadWeeklySummary = async () => {
  try {
    const res = await axios.post('http://localhost:8000/task_summary', {
      family_id
    })
    messages.value.push({
      role: 'assistant',
      content: res.data.summary
    })
    scrollToBottom()
  } catch (err) {
    console.error('❌ 获取每周总结失败:', err)
    messages.value.push({
      role: 'assistant',
      content: '❌ 获取每周总结失败，请稍后重试。'
    })
    scrollToBottom()
  }
}



onMounted(() => {
  loadMessages()
})
</script>

<style scoped>
.chat-wrapper {
  width: 100%;
  max-width: 800px;
  margin: auto;
  background: #fff;
  border: 1px solid #ccc;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  height: 70vh;
}
.chat-messages {
  flex: 1;
  padding: 16px;
  overflow-y: auto;
  background-color: #f9f9f9;
}
.chat-message.user {
  text-align: right;
}
.chat-message.assistant {
  text-align: left;
}
.bubble {
  display: inline-block;
  padding: 10px 16px;
  margin: 6px 0;
  background-color: #e0e0e0;
  border-radius: 12px;
  max-width: 70%;
  word-wrap: break-word;
}
.chat-input {
  display: flex;
  border-top: 1px solid #ddd;
  padding: 12px;
  background: #fff;
}
.chat-input input {
  flex: 1;
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
  font-size: 14px;
}
.chat-input button {
  margin-left: 10px;
  padding: 10px 16px;
  background-color: #409EFF;
  color: #fff;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}

.summary-button {
  padding: 10px;
  text-align: center;
  background: #fafafa;
  border-top: 1px solid #eee;
}

.summary-button button {
  background-color: #e4e4e4;
  color: #555;
  border: none;
  border-radius: 6px;
  padding: 8px 20px;
  font-size: 14px;
  cursor: pointer;
}
</style>