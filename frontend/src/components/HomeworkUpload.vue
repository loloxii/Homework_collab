<template>
  <div class="upload-wrapper">
    <el-card class="upload-card">
      <!-- 多任务描述区域 -->
      <div class="description-section">
        <el-form label-position="top">
          <el-form-item
            v-for="(task, index) in taskList"
            :key="task.id"
            :label="`任务 ${index + 1}`"
          >
            <div class="task-row">
              <el-input
                v-model="task.description"
                placeholder="请输入任务描述"
                type="textarea"
                :rows="2"
                style="flex: 1; margin-right: 8px"
              />
              <el-button type="danger" @click="removeTask(index)" :icon="Delete">删除</el-button>
            </div>
          </el-form-item>
        </el-form>

        <el-button type="success" plain icon="Plus" @click="addTask" style="margin-bottom: 10px">
          添加任务
        </el-button>
        <el-button type="primary" @click="saveAllTasks">保存所有任务描述</el-button>
      </div>

      <!-- 图片上传区域 -->
      <div class="upload-section">
        <el-upload
          class="upload-area"
          action="http://localhost:8000/upload/homework"
          :data="{ family_id: familyId, subject: 'general', description: '' }"
          accept="image/*"
          :on-success="handleSuccess"
          :on-error="handleError"
          :on-exceed="handleExceed"
          :limit="1"
          :file-list="fileList"
          drag
        >
          <i class="el-icon-upload" style="font-size: 24px; color: #409EFF" />
          <div class="el-upload__text small-text">拖入或 <em>点击上传</em> 作业图片（最多 1 张）</div>
        </el-upload>
        <el-button type="success" style="margin-top: 10px" @click="notifyImageSaved">保存</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Plus, Delete } from '@element-plus/icons-vue'
import axios from 'axios'

const taskList = ref([])  // 每项结构为 { id, description }
const familyId = ref(localStorage.getItem('family_id'))
const fileList = ref([])

function addTask() {
  taskList.value.push({ id: Date.now() + Math.random(), description: '' })
}

function removeTask(index) {
  taskList.value.splice(index, 1)
}

async function saveAllTasks() {
  const descriptions = {}
  taskList.value.forEach((task, index) => {
    const desc = task.description.trim()
    if (desc) {
      const key = `task${index + 1}`
      descriptions[key] = desc
    }
  })

  if (Object.keys(descriptions).length === 0) {
    ElMessage.warning("请至少填写一个任务描述")
    return
  }

  try {
    await axios.post("http://localhost:8000/save_task_description", {
      family_id: familyId.value,
      descriptions
    })
    ElMessage.success("所有任务描述已保存")
  } catch (err) {
    console.error(err)
    ElMessage.error("保存失败")
  }
}

onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:8000/get_task_description", {
      params: { family_id: familyId.value }
    })
    const descriptions = res.data.descriptions || {}
    taskList.value = Object.entries(descriptions).map(([_, description]) => ({
      id: Date.now() + Math.random(),
      description
    }))
  } catch (err) {
    console.error(err)
    ElMessage.error("加载任务描述失败")
  }
})

function handleSuccess(response, file) {
  ElMessage.success(`${file.name} 上传成功`)
}
function handleError(err, file) {
  ElMessage.error(`${file.name} 上传失败`)
}
function handleExceed(files) {
  ElMessage.warning('⚠️ 只能上传 1 张图片')
}
function notifyImageSaved() {
  ElMessage.success("上传记录保存成功")
}
</script>


<style scoped>
.upload-wrapper {
  max-width: 600px;
  margin: 0 auto;
  padding: 30px 20px;
}

.upload-card {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 400px;
  padding: 20px;
}

.description-section {
  flex: 1;
  margin-bottom: 20px;
}

.upload-section {
  border-top: 1px solid #ebeef5;
  padding-top: 12px;
}

.upload-area {
  width: 100%;
}

.small-text {
  font-size: 13px;
  color: #888;
}

.task-row {
  display: flex;
  align-items: center;
  width: 100%;
}
</style>