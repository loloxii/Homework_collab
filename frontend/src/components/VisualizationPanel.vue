<template>
    <div>
      <h4>完成进度统计</h4>
      <el-progress :percentage="0" text-inside :stroke-width="20"/>
    </div>
  </template>
  
  <script setup>
  import { computed } from 'vue'
  const props = defineProps(['tasks'])
  
  const completionRate = computed(() => {
    if (!props.tasks.length) return 0
    const completed = props.tasks.filter(t => t.completed).length
    return Math.round((completed / props.tasks.length) * 100)
  })
  </script>