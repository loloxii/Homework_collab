<template>
  <div class="schedule-wrapper">
    <div class="header">
      <h3>任务时间安排</h3>
      <el-button type="primary" size="small" @click="openAddDialog">新建任务</el-button>
    </div>

    <div class="calendar">
      <div class="calendar-header">
        <div class="time-col-header"></div>
        <div v-for="day in days" :key="day" class="day-header">{{ day }}</div>
      </div>

      <div class="calendar-body">
        <div v-for="hour in hours" :key="hour" class="hour-row">
          <div class="time-label">{{ hour }}</div>
          <div v-for="day in days" :key="`${day}-${hour}`" class="calendar-cell"></div>
        </div>

        <div
          v-for="task in tasks"
          :key="task.id"
          class="task-block"
          :style="getTaskStyle(task)"
          @click="openEditDialog(task)"
        >
          {{ task.name }} ({{ getAssigneeName(task.assignee) }})
        </div>
      </div>
    </div>

    <el-dialog v-model="dialogVisible" title="任务详情" width="400px">
      <el-form :model="form">
        <el-form-item label="任务 ID">
          <el-input v-model="form.id" type="number" />
        </el-form-item>
        <el-form-item label="任务名称">
          <el-input v-model="form.name" />
        </el-form-item>

        <el-form-item label="任务描述">
        <el-input v-model="form.description" placeholder="填写任务目标与内容" />
      </el-form-item>

            <el-form-item label="负责人">
              <el-select
                v-model="form.assignee"
                multiple            
                collapse-tags
                placeholder="选择家庭成员"
              >
                <el-option
                  v-for="m in members"
                  :key="m.member_id"
                  :label="m.role"
                  :value="m.role"
                />
              </el-select>
            </el-form-item>

            <el-form-item label="辅导方式说明">
              <el-input
                v-model="form.tutoringMethod"
                type="textarea"
                :rows="2"
                placeholder="填写如何协助与辅导"
              />
            </el-form-item>

        <el-form-item label="日期">
          <el-select v-model="form.day" placeholder="选择日期">
            <el-option v-for="day in days" :key="day" :label="day" :value="day" />
          </el-select>
        </el-form-item>
        <!-- <el-form-item label="开始时间">
          <el-time-picker v-model="form.start" format="HH:mm" value-format="HH:mm" />
        </el-form-item>
        <el-form-item label="结束时间">
          <el-time-picker v-model="form.end" format="HH:mm" value-format="HH:mm" />
        </el-form-item> -->
        <el-form-item label="开始时间">
            <el-time-picker
              v-model="form.start"
              format="HH:mm"
              value-format="HH:mm"
              :disabled-hours="disabledStartHours"
            />
          </el-form-item>

          <el-form-item label="结束时间">
            <el-time-picker
              v-model="form.end"
              format="HH:mm"
              value-format="HH:mm"
              :disabled-hours="disabledEndHours"
            />
          </el-form-item>

        <el-form-item label="是否完成">
          <el-switch v-model="form.done" />
        </el-form-item>

        <el-form-item label="上传作业图片">
        <el-upload
            class="upload-demo"
            action=""
            :http-request="uploadHomework"
            :file-list="uploadFileList"
            :show-file-list="true"
            :limit="5"
            :on-remove="handleRemove"
            multiple
        >
            <el-button size="small" type="primary">选择图片</el-button>
        </el-upload>
        </el-form-item>

        <el-form-item v-if="form.homeworkImage.length" label="图片处理">
        <el-button type="success" size="small" @click="submitAllHomeworkImages">
            提交
        </el-button>
        </el-form-item>
        </el-form> 

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="danger" v-if="form.id" @click="deleteTask">删除</el-button>
        <el-button type="primary" @click="saveTask">保存</el-button>
      </template>
    </el-dialog>

    <el-button type="success" class="save-button" @click="submitAllTasksToBackend">保存所有任务</el-button>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'
import { useTaskStore } from '../stores/taskStore'

const days = ['Day 1', 'Day 2', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
const hours = Array.from({ length: 17 }, (_, i) => `${i + 8}:00`)
// const tasks = ref([])
const members = ref([])
const dialogVisible = ref(false)
const uploadFileList = ref([])


const form = reactive({
  id: '',
  name: '',
  description: '',
  assignee: [],
  tutoringMethod: '',
  day: '',
  start: '',
  end: '',
  done: false,
  homeworkImage: []
})

const taskStore = useTaskStore()
const tasks = ref([])
const hasLoadedFromBackend = ref(false)  // ✅ 控制只加载一次

onMounted(async () => {
  const family_id = localStorage.getItem('family_id')
  if (!family_id) return

  try {
    const res = await axios.get(`http://localhost:8000/get_members?family_id=${family_id}`)
    members.value = res.data.members || []
    console.log("👨‍👩‍👧 家庭成员加载完成：", members.value)

    const taskRes = await axios.get(`http://localhost:8000/api/load_tasks?family_id=${family_id}`)
    tasks.value = taskRes.data.tasks || []
    console.log('✅ 初始任务来自后端:', tasks.value)

  } catch (err) {
    console.error("❌ 获取家庭成员或任务失败：", err)
  }
})

// ✅ 一旦 Chatbot 生成了新任务，就立即覆盖
watch(
  () => taskStore.llmGeneratedTasks,
  (newTasks) => {
    if (newTasks && newTasks.length) {
        tasks.value = newTasks.map((task, idx) => ({
          id: task.id || `${Date.now()}-${idx}`,
          name: task.name,
          description: task.description || '', // ✅ 补上
          
          tutoringMethod: task.tutoringMethod || '', // ✅ 补上
          day: task.day || 'Day 1',
          start: task.start || '08:00',
          end: task.end || '09:00',
          done: task.done || false,
          homeworkImage: task.homeworkImage || []
        }))
      console.log('✅ 已更新任务时间表:', tasks.value)
    }
  },
  { immediate: true }
)

function getAssigneeName(assignee) {
  if (Array.isArray(assignee)) {
    return assignee
      .map(role => {
        const member = members.value.find(m => m.role === role)
        return member ? member.role : role
      })
      .join(', ')
  } else {
    const member = members.value.find(m => m.role === assignee)
    return member ? member.role : assignee
  }
}
function openAddDialog() {
  Object.assign(form, {
    id: '',
    name: '',
    assignee: '',
    day: '',
    start: '',
    end: '',
    done: false,
    homeworkImage: []  // ✅ 修正这里
  })
  dialogVisible.value = true
}

function openEditDialog(task) {
  Object.assign(form, {
    ...task,
    assignee: Array.isArray(task.assignee) ? task.assignee : [task.assignee]
  })
  dialogVisible.value = true
}

function saveTask() {
  if (!form.day || !form.start || !form.end || !form.id || !form.assignee) {
    ElMessage.warning('请填写完整任务信息')
    return
  }

  // 通过角色查找对应的 member_id
  // const member = members.value.find(m => m.role === form.assignee)
  const selectedRoles = Array.isArray(form.assignee) ? form.assignee : [form.assignee]

  const memberIds = selectedRoles.map(role => {
    const member = members.value.find(m => m.role === role)
    return member ? member.member_id : role  // fallback
  })

  // if (!member) {
  //   ElMessage.error('无法找到对应成员，请重新选择')
  //   return
  // }

  const finalTask = {
    ...form,
    assignee: memberIds,
    description: form.description,
    tutoringMethod: form.tutoringMethod
  }

  const idx = tasks.value.findIndex(t => t.id === form.id)
  if (idx !== -1) {
    tasks.value[idx] = finalTask
  } else {
    tasks.value.push(finalTask)
  }

  ElMessage.success('任务已保存')
  dialogVisible.value = false
}

function deleteTask() {
  const idx = tasks.value.findIndex(t => t.id === form.id)
  if (idx !== -1) tasks.value.splice(idx, 1)
  ElMessage.success('任务已删除')
  dialogVisible.value = false
}

async function uploadHomework({ file }) {
  try {
    const formData = new FormData()
    const family_id = localStorage.getItem('family_id') || 'default'
    const user_id = form.assignee || 'unknown'
    const task_id = form.id || 'no_id'

    formData.append('file', file)
    formData.append('family_id', family_id)
    formData.append('user_id', user_id)
    formData.append('task_id', task_id)

    const response = await axios.post('http://localhost:8000/upload/homework', formData)

    ElMessage.success(`上传成功：${response.data.filename}`)

    if (!Array.isArray(form.homeworkImage)) {
      form.homeworkImage = []
    }
    form.homeworkImage.push(response.data.filename)
  } catch (error) {
    console.error('上传失败', error.response?.data || error.message)
    ElMessage.error('上传失败')
  }
}

function handleRemove(file, fileList) {
  uploadFileList.value = fileList
  const name = file.name
  form.homeworkImage = form.homeworkImage.filter(f => f !== name)
}

async function submitAllHomeworkImages() {
  const family_id = localStorage.getItem('family_id') || 'default'
  const folderName = form.id || '1'

  if (!form.homeworkImage.length) {
    ElMessage.warning('没有可处理的图片')
    return
  }

  try {
    await axios.post(
      'http://localhost:8000/extract_homework_text',
      {
        family_id,
        filename: folderName
      },
      {
        headers: { 'Content-Type': 'application/json' }
      }
    )

    // ✅ 只提示“后台处理成功”
    ElMessage.success(`✅ 图片已提交处理，结果请在后台查看`)
  } catch (err) {
    console.error('❌ 作业图片识别失败', err)
    ElMessage.error('❌ 提交失败，请稍后重试')
  }
}

function getTaskStyle(task) {
  const totalMinutes = 16 * 60; // 从 08:00 到 24:00，共 960 分钟
  const totalPixelHeight = 22 * 26; // 22 行，每行 22px，总 484px

  const pixelsPerMinute = totalPixelHeight / totalMinutes; // ≈ 0.504 px/min

  const [startH, startM] = task.start.split(':').map(Number);
  const [endH, endM] = task.end.split(':').map(Number);

  const startMin = startH * 60 + startM;
  const endMin = endH * 60 + endM;

  const calendarStartMin = 8 * 60; // 起始是08:00
  const startOffsetPx = (startMin - calendarStartMin) * pixelsPerMinute -3;
  const taskHeightPx = Math.max((endMin - startMin) * pixelsPerMinute, 1);

  const dayIndex = days.indexOf(task.day);
  const columnWidth = `(100% - 80px) / 7`;

  return {
    position: 'absolute',
    top: `${startOffsetPx}px`,
    height: `${taskHeightPx}px`,
    left: `calc(${columnWidth} * ${dayIndex} + 80px)`,
    width: `calc(100% / 7 - 10px)`,
    backgroundColor: '#c6ecff',
    border: '1px solid #91d5ff',
    borderRadius: '6px',
    padding: '2px',
    fontSize: '12px',
    zIndex: 5,
    overflow: 'hidden'
  };
}

async function submitAllTasksToBackend() {
  console.log("🔥 saveToBackend 被调用了")
  try {
    const family_id = localStorage.getItem('family_id')
    if (!family_id) {
      ElMessage.error('未找到家庭 ID，无法保存')
      return
    }

    // 构建 role → member_id 映射
    const roleToIdMap = {}
    for (const m of members.value) {
      roleToIdMap[m.role] = m.member_id
    }


const cleanTasks = tasks.value.map(task => {
  const assignees = Array.isArray(task.assignee) ? task.assignee : [task.assignee]
  const roleNames = assignees.map(id => {
    const member = members.value.find(m => m.member_id === id)
    return member ? member.role : id
  })

  return {
    id: String(task.id ?? ''),
    name: String(task.name ?? ''),
    description: String(task.description ?? ''),  // 🆕 任务描述
    assignee: roleNames,
    tutoringMethod: String(task.tutoringMethod ?? ''),  // 🆕 辅导方式说明
    day: String(task.day ?? ''),
    start: String(task.start ?? ''),
    end: String(task.end ?? ''),
    done: !!task.done,
    homeworkImage: Array.isArray(task.homeworkImage) ? task.homeworkImage : []
  }
})

    const payload = { family_id, tasks: cleanTasks }

const res = await axios.post('http://localhost:8000/api/save_tasks', payload)

if (res.data?.message?.includes('Tasks saved')) {
  ElMessage.success('✅ 所有任务已成功保存')

  // ✅ 刷新聊天上下文
  await axios.post('http://localhost:8000/refresh_chat_history', { family_id })
  console.log("📘 对话历史已重置")

  // ✅ 【新增】调用 update_saved_tasks 创建文件夹
try {
  await axios.post('http://localhost:8000/saved_tasks_folds',
    {
      family_id: family_id,
      tasks: cleanTasks
    },
    {
      headers: {
        'Content-Type': 'application/json'
      }
    }
  )
  console.log("📁 文件夹检查更新完成")
} catch (updateErr) {
  console.error('❌ 文件夹更新失败', updateErr.response?.data || updateErr.message)
  ElMessage.warning('⚠️ 部分任务资料目录未能成功创建')
}

} else {
  ElMessage.warning('⚠️ 后端未返回成功提示')
}
    // } else {
    //   ElMessage.warning('⚠️ 后端未返回成功提示')
    // }
  } catch (error) {
    console.error('保存失败:', error?.response?.data || error.message)
    ElMessage.error('❌ 保存失败，请稍后重试')
  }
}


function disabledStartHours() {
  // 禁用 0~7 点
  return Array.from({ length: 8 }, (_, i) => i) // [0, 1, ..., 7]
}

function disabledEndHours() {
  // 禁用 0~7 点
  return Array.from({ length: 8 }, (_, i) => i)
}

</script>

<style scoped>
.schedule-wrapper {
  margin-top: 10px;
}
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: -70px; /* ✅ 向上移动10px */
  margin-bottom: 0px;
}
.calendar {
  position: relative;
  border: 1px solid #ccc;
  overflow: hidden;
}
.calendar-header {
  display: grid;
  grid-template-columns: 80px repeat(7, 1fr);
  background-color: #f6f6f6;
  font-weight: bold;
  border-bottom: 1px solid #ddd;
}
.time-col-header {
  text-align: center;
  line-height: 30px;
}
.day-header {
  text-align: center;
  padding: 4px;
  border-left: 1px solid #eee;
}
.calendar-body {
  display: grid;
  grid-template-columns: 80px repeat(7, 1fr);
  position: relative;
  height: calc(22px * 27); /* ✅ 原来是 17，现在加高为 22 行 */
  flex-shrink: 0;
}
.hour-row {
  display: contents;
  height: 22px;
  border-top: 1px dashed #eee;
}
.time-label {
  text-align: center;
  font-size: 12px;
  background-color: #f8f8f8;
  border-right: 1px solid #eee;
  line-height: 22px;
}
.calendar-cell {
  border-left: 1px solid #f3f3f3;
  border-bottom: 1px dashed #eee;
}

:deep(.task-block) {
  font-size: 10px !important;
  padding: 1px !important;
  line-height: 1.2 !important;
}

.save-button {
  margin-top: 16px;
  display: block;
  margin-left: auto;
  margin-right: auto;
}
</style>