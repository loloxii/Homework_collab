<template>
    <div>
      <el-table :data="tasks" style="width: 100%">
        <el-table-column prop="subject" label="科目" editable>
          <template #default="scope">
            <el-input v-model="scope.row.subject" />
          </template>
        </el-table-column>
  
        <el-table-column prop="content" label="任务内容">
          <template #default="scope">
            <el-input v-model="scope.row.content" />
          </template>
        </el-table-column>
  
        <el-table-column prop="expectedTime" label="预计时间">
          <template #default="scope">
            <el-input v-model="scope.row.expectedTime" />
          </template>
        </el-table-column>
  
        <el-table-column label="完成">
          <template #default="scope">
            <el-checkbox v-model="scope.row.completed" />
          </template>
        </el-table-column>
  
        <el-table-column label="操作">
          <template #default="scope">
            <el-button type="danger" @click="deleteTask(scope.$index)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
  
      <el-button type="primary" @click="addTask" style="margin-top: 10px">添加任务</el-button>
    </div>
  </template>
  
  <script setup>
  const props = defineProps(['tasks'])
  const emit = defineEmits(['update:tasks'])
  
  function addTask() {
    emit('update:tasks', [...props.tasks, {
      subject: '', content: '', expectedTime: '', completed: false
    }])
  }
  
  function deleteTask(index) {
    const updated = [...props.tasks]
    updated.splice(index, 1)
    emit('update:tasks', updated)
  }
  </script>