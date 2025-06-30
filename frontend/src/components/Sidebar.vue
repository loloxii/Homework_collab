<template>
  <el-menu
    mode="horizontal"
    :default-active="$route.path"
    router
    class="el-menu-horizontal"
  >
    <el-menu-item index="/setting">
      <i class="el-icon-house"></i>
      <span>任务分配</span>
    </el-menu-item>
    <el-menu-item index="/tasks">
      <i class="el-icon-document"></i>
      <span>任务辅导</span>
    </el-menu-item>
    <el-menu-item index="/ai">
      <i class="el-icon-brush"></i>
      <span>总结与反馈</span>
    </el-menu-item>
  </el-menu>
</template>

<script setup>
import { useRoute } from 'vue-router'
</script>

<style scoped>
.el-menu-horizontal {
  flex: 1;
  border-bottom: none;
  background-color: transparent;
}

.el-menu-item {
  min-width: 120px;
  justify-content: center;
}

.el-menu-item span {
  white-space: nowrap;
  overflow: visible;
  text-overflow: unset;
}
</style>