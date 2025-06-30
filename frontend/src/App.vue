<template>
  <div class="app-background">
    <div class="app-container">
      <!-- 顶部导航栏 -->
      <div class="topbar">
        <Sidebar />
      </div>

      <!-- 主内容区域 -->
      <div class="main-content">
        <router-view />
      </div>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue'
</script>

<style scoped>
.app-background {
  position: fixed;               /* 🔒 固定整个背景，防止滑动 */
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: #e0f0ff;
  display: flex;
  justify-content: center;
  align-items: flex-start;
  padding: 40px 0;
  overflow: hidden;              /* 禁止外部滚动 */
  z-index: 0;
}

.app-container {
  background-color: #ffffff;
  width: 90%;
  height: 90vh;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.topbar {
  height: 60px;
  background-color: #f5f7fa;
  border-bottom: 1px solid #dcdfe6;
  display: flex;
  align-items: center;
  padding: 0 20px;
  overflow-x: auto;
  flex-shrink: 0;
}

.main-content {
  flex: 1;
  padding: 24px;
  overflow-y: auto;            /* ✅ 内容区域可滚动 */
  background-color: #ffffff;
}
</style>