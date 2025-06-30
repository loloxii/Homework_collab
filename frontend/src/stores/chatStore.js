// stores/chatStore.js
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useChatStore = defineStore('chatStore', () => {
  const chatMessages = ref([])

  const addMessage = (msg) => {
    chatMessages.value.push(msg)
  }

  const clearMessages = () => {
    chatMessages.value = []  // ✅ 这行是关键！
  }

  return {
    chatMessages,
    addMessage,
    clearMessages,  // ✅ 确保这个方法被暴露
  }
})