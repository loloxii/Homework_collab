<template>
  <el-container class="task-layout">
    <!-- 左侧 Chatbot 区域 -->
    <el-aside width="600px" class="chatbot-area">
      <ChatbotPanel />
    </el-aside>

    <!-- 中间占位区域 -->
    <el-main class="placeholder-area">
  <Task />
</el-main>
  </el-container>
</template>

<script setup>
import Task from '../components/Task.vue'
import ChatbotPanel from '../components/ChatbotPanel.vue'
</script>

<style scoped>
.task-layout {
  height: 100%;
  overflow: hidden;
}

.chatbot-area {
  background: #f5f7fa;
  padding: 12px;
  overflow: hidden;
}

.placeholder-area {
  background-color: #fafafa;
  display: flex;
  justify-content: center;
  align-items: center;
  overflow: hidden;
}

.placeholder-text {
  color: #999;
  font-size: 14px;
}
</style>

<!-- 可选：禁用滚动条 -->
<style scoped>
:deep(.main-content) {
  overflow: hidden !important;
}
</style>