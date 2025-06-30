<template>
  <div class="setting-wrapper">
    <div class="layout-container">
      <!-- 左侧：任务组件 -->
      <div class="left-panel">
        <Task />
      </div>

      <!-- 右侧：Chatbot 区域 -->
      <div class="right-panel">
        <div class="chatbot-area">
          <ChatbotPanel :familyId="family_id" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import Task from '../components/Task.vue'
import ChatbotPanel from '../components/Chatbot2.vue'

const family_id = localStorage.getItem('family_id')
</script>

<style scoped>
.setting-wrapper {
  padding: 30px;
  max-width: 1300px;
  margin: 0 auto;
}

.layout-container {
  flex: 1;
  display: flex;
  gap: 20px;
  align-items: stretch;
  height: 100%;
}

.left-panel {
  flex: 1;
  min-width: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.right-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
}

.chatbot-area {
  flex: 1;
  min-height: 600px;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 3px;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-bottom: 0;
  padding-bottom: 0;
}
</style>