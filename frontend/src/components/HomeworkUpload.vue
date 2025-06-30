<template>
  <div class="upload-wrapper">
    <el-card class="upload-card">
      <template #header>
      </template>

      <!-- 文本输入框 + 保存按钮 -->
      <div class="description-section">
        <el-form :model="{ description }" label-position="top">
          <el-form-item label="任务要求">
            <el-input
              type="textarea"
              v-model="description"
              placeholder="请输入题目内容、要求或备注说明..."
              :rows="5"
              resize="vertical"
              clearable
            />
          </el-form-item>
        </el-form>
        <el-button type="primary" @click="saveDescription">保存题目描述</el-button>
      </div>

      <!-- 图片上传区域 + 保存提示按钮 -->
      <div class="upload-section">
        <el-upload
          class="upload-area"
          action="http://localhost:8000/upload/homework"
          :data="{ family_id: familyId, subject: 'general', description: description }"
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
import axios from 'axios'

const familyId = ref(localStorage.getItem('family_id'))
const description = ref('')
const fileList = ref([])

// ✅ 刷新页面时拉取后端数据
onMounted(async () => {
  try {
    const res = await axios.get("http://localhost:8000/get_task_description", {
      params: { family_id: familyId.value }
    })
    description.value = res.data.description || ''
    console.log("✅ 当前描述：", description.value)
  } catch (err) {
    console.error("❌ 拉取失败:", err)
    ElMessage.error("加载描述失败")
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

async function saveDescription() {
  if (!description.value.trim()) {
    ElMessage.warning("请输入作业要求再保存")
    return
  }

  try {
    await axios.post("http://localhost:8000/save_task_description", {
      family_id: familyId.value,
      description: description.value
    })
    ElMessage.success("作业描述保存成功")
  } catch (err) {
    console.error("保存失败:", err)
    ElMessage.error("保存失败")
  }
}

function notifyImageSaved() {
  ElMessage.success("上传记录保存成功（如需后端持久化，请扩展接口）")
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

.card-header {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
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
</style>