<template>
  <div class="my-task-wrapper">
    <h2>任务清单</h2>

    <p v-if="filteredTasks.length === 0">⚠️ 当前没有任务显示</p>
    <p v-else>当前任务数：{{ filteredTasks.length }}，当前第 {{ currentIndex + 1 }} 个任务</p>

    <!-- 控制按钮：上一个/下一个 -->
    <div class="task-controls">
      <el-button
        type="default"
        @click="prevTask"
        :disabled="currentIndex <= 0"
      >
        上一个任务
      </el-button>

      <el-button
        type="primary"
        @click="nextTask"
        :disabled="currentIndex >= filteredTasks.length - 1"
      >
        下一个任务
      </el-button>
    </div>

    <!-- 当前任务卡片 -->
    <el-scrollbar class="task-list">
      <el-card
        v-if="currentTask"
        class="task-card"
      >
        <div class="task-title"><strong>{{ currentTask.name }}</strong></div>
        <div class="task-detail"><b>说明：</b>{{ currentTask.description }}</div>
        <div class="task-detail"><b>辅导方式：</b>{{ currentTask.tutoringMethod }}</div>
        <div class="task-detail"><b>时间安排：</b>{{ currentTask.day }} {{ currentTask.start }} ~ {{ currentTask.end }}</div>
        <div class="task-detail"><b>完成情况：</b>
          <el-tag :type="currentTask.done ? 'success' : 'warning'">
            {{ currentTask.done ? '已完成' : '未完成' }}
          </el-tag>
        </div>

        <div class="task-detail"><b>上传作业图片：</b></div>
<el-upload
  class="upload-demo"
  :http-request="uploadHomeworkImage"
  :show-file-list="true"
  :file-list="fileLists[currentTask.id] || []"
  :on-remove="(file, fileList) => handleRemove(file, fileList, currentTask.id)"
  multiple
  :limit="5"
>
  <el-button size="small" type="primary">上传</el-button>
</el-upload>

<el-button
  type="success"
  size="small"
  style="margin-top: 10px"
  @click="saveUploadedImages(currentTask)"
>
  保存图片
</el-button>

<el-button
  type="warning"
  size="small"
  style="margin-top: 10px; margin-left: 10px"
  @click="startHomework(currentTask)"
>
  开始作业
</el-button>


      </el-card>
    </el-scrollbar>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'
import { useChatStore } from '../stores/chatStore'

import { ElMessage } from 'element-plus'

const fileLists = ref({}) // 每个任务一个上传列表

const allTasks = ref([])
const filteredTasks = ref([])
const currentIndex = ref(0)

const currentTask = computed(() => {
  return filteredTasks.value.length > 0 ? filteredTasks.value[currentIndex.value] : null
})

onMounted(async () => {
  const familyId = localStorage.getItem('family_id')
  const role = localStorage.getItem('role')

  if (!role || !familyId) {
    console.warn('⚠️ 缺少登录信息')
    return
  }

  try {
    const res = await axios.get(`http://localhost:8000/s_load_saved_tasks`, {
      params: { family_id: familyId }
    })

    allTasks.value = res.data.tasks || []
    filteredTasks.value = allTasks.value.filter(task => {
      const assignees = Array.isArray(task.assignee) ? task.assignee : [task.assignee]
      return assignees.includes(role)
    })

    currentIndex.value = 0

    // ✅ 加载每个任务的上传图片列表
    for (const task of filteredTasks.value) {
      try {
        const uploadRes = await axios.get('http://localhost:8000/get_uploaded_files', {
          params: {
            family_id: familyId,
            task_id: task.id
          }
        })

        fileLists.value[task.id] = uploadRes.data.files.map(filename => ({
          name: filename,
          url: '' // 可选：设置为图片 URL 如果你支持预览
        }))
      } catch (uploadErr) {
        console.warn(`⚠️ 无法加载任务 ${task.id} 的上传文件`, uploadErr)
        fileLists.value[task.id] = []
      }
    }

  } catch (err) {
    console.error('❌ 任务加载失败:', err)
  }
})

function nextTask() {
  if (currentIndex.value < filteredTasks.value.length - 1) {
    currentIndex.value++
  }
}
function prevTask() {
  if (currentIndex.value > 0) {
    currentIndex.value--
  }
}

async function uploadHomeworkImage({ file }) {
  const family_id = localStorage.getItem('family_id')
  const role = localStorage.getItem('role')
  const task = currentTask.value

  if (!task?.id || !family_id || !role) {
    ElMessage.error('❌ 上传失败，缺少必要信息')
    return
  }

  const formData = new FormData()
  formData.append('file', file)
  formData.append('family_id', family_id)
  formData.append('user_id', role)
  formData.append('task_id', task.id)

  try {
    const response = await axios.post('http://localhost:8000/upload/homework', formData)

    ElMessage.success(`✅ 上传成功：${response.data.filename}`)

    if (!fileLists.value[task.id]) {
      fileLists.value[task.id] = []
    }
    fileLists.value[task.id].push({
      name: response.data.filename,
      url: ''  // 可选：你可以在 response 中返回文件路径作为 url
    })
  } catch (err) {
    console.error('❌ 上传出错', err)
    ElMessage.error('❌ 上传失败')
  }
}

function handleRemove(file, fileList, taskId) {
  fileLists.value[taskId] = fileList
}

const saveUploadedImages = async (task) => {
  const family_id = localStorage.getItem('family_id')
  const task_id = `task_${task.id}`  // ✅ 修正：确保传入字符串格式的 task_id

  if (!family_id || !task_id) {
    ElMessage.warning('⚠️ 缺少 family_id 或 task_id')
    return
  }

  try {
    const res = await axios.get('http://localhost:8000/analyze_homework', {
      params: {
        family_id,
        task_id
      }
    })

    ElMessage.success('✅ 图片保存并识别成功！')
    console.log('分析结果:', res.data)
  } catch (err) {
    console.error('❌ 分析失败:', err)
    ElMessage.error('❌ 图片分析失败，请稍后再试')
  }
}

const startHomework = async (task) => {
  const task_id = `task_${task.id}`
  localStorage.setItem('current_task_id', task_id)

  const family_id = localStorage.getItem('family_id')
  if (!family_id) {
    ElMessage.warning('⚠️ 缺少 family_id')
    return
  }

  try {
    // ✅ 只在后台使用提示词，不加入 chatStore
    const res = await axios.post('http://localhost:8000/chat_putong', {
      family_id,
      task_id,
      user_message: '我现在是家长，我应该如何完成这个任务'
    })

    const chatStore = useChatStore()
    chatStore.clearMessages()

    // ✅ 仅显示 AI 的建议
    chatStore.addMessage({ role: 'assistant', content: res.data.reply })

    // ✅ 再添加一句引导提问
    chatStore.addMessage({ role: 'assistant', content: '请问还有其他需要帮忙的吗？' })

    ElMessage.success('✅ 作业助手已启动')
  } catch (err) {
    console.error('❌ 启动作业助手失败:', err)
    ElMessage.error('❌ 启动失败，请稍后重试')
  }
}



</script>

<style scoped>
.my-task-wrapper {
  padding: 20px;
}
.task-list {
  max-height: 60vh;
  overflow-y: auto;
  margin-top: 10px;
}
.task-card {
  margin: 0 auto;
  max-width: 600px;
  border: 1px solid #dcdfe6;
}
.task-title {
  font-size: 16px;
  margin-bottom: 6px;
}
.task-detail {
  font-size: 14px;
  margin: 2px 0;
}
.task-controls {
  display: flex;
  justify-content: center;
  gap: 16px;
  margin: 16px 0;
}
</style>