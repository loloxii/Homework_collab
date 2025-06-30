<template>
    <div class="homework-panel">
      <!-- 顶部表单 -->
      <div class="form-section">
        <el-form :model="newHomework" label-width="100px">
          <el-form-item label="科目">
            <el-input v-model="newHomework.subject" placeholder="如：语文、数学" />
          </el-form-item>
  
          <el-form-item label="任务内容">
            <el-input
              v-model="newHomework.content"
              type="textarea"
              placeholder="请输入作业内容"
              :rows="2"
            />
          </el-form-item>
  
          <el-form-item label="预计时间">
            <el-input v-model="newHomework.expectedTime" placeholder="如：30分钟" />
          </el-form-item>
  
          <el-form-item>
            <el-button type="primary" @click="saveHomework">保存作业</el-button>
          </el-form-item>
        </el-form>
      </div>
  
      <!-- 底部展示区 -->
      <div class="list-section">
        <!-- 左侧科目导航 -->
        <div class="subject-list">
          <h4>科目列表</h4>
          <el-menu
            :default-active="activeSubject"
            @select="selectSubject"
            class="subject-menu"
          >
            <el-menu-item
              v-for="(items, subject) in homeworkList"
              :key="subject"
              :index="subject"
            >
              {{ subject }}
            </el-menu-item>
          </el-menu>
        </div>
  
        <!-- 右侧作业展示 -->
        <div class="subject-tasks" v-if="activeSubject && homeworkList[activeSubject]">
          <h4>{{ activeSubject }} 作业列表</h4>
          <el-card
            v-for="(item, index) in homeworkList[activeSubject]"
            :key="index"
            style="margin-bottom: 10px"
          >
            <p><strong>任务：</strong>{{ item.content }}</p>
            <p><strong>预计时间：</strong>{{ item.expectedTime }}</p>
            <el-button
              type="danger"
              size="small"
              @click="deleteHomework(activeSubject, index)"
            >
              删除
            </el-button>
          </el-card>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { reactive, ref, computed } from 'vue'
  import { ElMessage } from 'element-plus'

  const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue'])
  
  const newHomework = reactive({
    subject: '',
    content: '',
    expectedTime: ''
  })
  
  const homeworkList = computed({
  get: () => props.modelValue,
  set: (val) => emit('update:modelValue', val)
})

  const activeSubject = ref('')
  
  function saveHomework() {
  if (!newHomework.subject || !newHomework.content) {
    ElMessage.error('请填写科目和任务内容')
    return
  }

  const subject = newHomework.subject
  const updated = { ...homeworkList.value }

  if (!updated[subject]) {
    updated[subject] = []
  }

  updated[subject].push({ ...newHomework })
  homeworkList.value = updated

  ElMessage.success('作业已保存！')
  activeSubject.value = subject

  Object.assign(newHomework, {
    subject: '',
    content: '',
    expectedTime: ''
  })
}

  
  function selectSubject(subject) {
    activeSubject.value = subject
  }
  


  function deleteHomework(subject, index) {
  const updated = { ...homeworkList.value }
  if (!updated[subject]) return

  updated[subject].splice(index, 1)

  if (updated[subject].length === 0) {
    delete updated[subject]
    activeSubject.value = ''
  }

  homeworkList.value = updated
  ElMessage.success('已删除该作业项')
}
  </script>
  
  <style scoped>
  .homework-panel {
    display: flex;
    flex-direction: column;
    gap: 30px;
  }
  
  /* 顶部表单 */
  .form-section {
    background: #fefefe;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.05);
  }
  
  /* 底部展示区域 */
  .list-section {
    display: flex;
    gap: 20px;
  }
  
  /* 科目菜单 */
  .subject-list {
    width: 150px;
    border-right: 1px solid #eee;
  }
  
  .subject-menu {
    border-right: none;
    background: #f9f9f9;
  }
  
  /* 作业内容展示 */
  .subject-tasks {
    flex: 1;
  }
  </style>