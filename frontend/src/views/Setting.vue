<template>
  <div class="setting-wrapper">
    <div class="layout-container">
      <!-- 左侧：任务时间表 -->
      <div class="left-panel">
        <TaskScheduleBoard />
      </div>

      <!-- 右侧：控制面板 + Chatbot -->
      <div class="right-panel">
        <!-- 顶部按钮 -->
        <div class="button-group">
          <el-button type="primary" @click="showChildDialog = true">小朋友信息</el-button>
          <el-button type="primary" @click="showFamilyDialog = true">家长信息</el-button>
          <el-button type="primary" @click="uploadHomework">上传作业</el-button>
        </div>

        <!-- Chatbot 区域 -->
        <div class="chatbot-area">
          <ChatbotPanel :familyId="family_id" />
        </div>
      </div>
    </div>

    <!-- 小朋友信息弹窗 -->
    <el-dialog v-model="showChildDialog" title="小朋友信息" width="600px">
      <ChildInfoPanel v-model:child="child" />
      <template #footer>
        <el-button @click="showChildDialog = false">取消</el-button>
        <el-button type="primary" @click="saveChildInfo">保存</el-button>
      </template>
    </el-dialog>

    <!-- 家长信息弹窗 -->
    <el-dialog v-model="showFamilyDialog" title="家长信息" width="600px">
      <FamilyMemberPanel v-model:member="familyMember" />
      <template #footer>
        <el-button @click="showFamilyDialog = false">取消</el-button>
        <el-button type="primary" @click="saveFamilyInfo">保存</el-button>
      </template>
    </el-dialog>

    <!-- 上传作业弹窗 -->
    <el-dialog v-model="showUploadDialog" title="上传作业" width="700px">
      <HomeworkUpload />
      <template #footer>
        <el-button @click="showUploadDialog = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, toRaw } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

import ChildInfoPanel from '../components/ChildInfoPanel.vue'
import FamilyMemberPanel from '../components/FamilyMemberPanel.vue'
import HomeworkUpload from '../components/HomeworkUpload.vue'
import TaskScheduleBoard from '../components/TaskScheduleBoard.vue'
import ChatbotPanel from '../components/ChatbotPanel.vue'

const showChildDialog = ref(false)
const showFamilyDialog = ref(false)
const showUploadDialog = ref(false)

const username = localStorage.getItem('username')
const family_id = localStorage.getItem('family_id')

const child = reactive({
  age: '',
  grades: [],
  hobbies: [],
  traits: []
})

const familyMember = reactive({
  role: '',
  subjectPreference: [],
  educationConcept: ''
})

onMounted(() => {
  if (family_id) {
    loadChildInfo()
    loadFamilyInfo()
  }
})

async function loadChildInfo() {
  try {
    const res = await axios.get(`http://localhost:8000/get/child?family_id=${family_id}`)
    Object.assign(child, res.data.child)
  } catch {
    console.log("暂无小朋友信息")
  }
}

async function saveChildInfo() {
  try {
    await axios.post('http://localhost:8000/save/child', {
      family_id,
      child: toRaw(child)
    })
    ElMessage.success('小朋友信息已保存')
    showChildDialog.value = false
  } catch (err) {
    ElMessage.error('保存失败：' + err.message)
  }
}

async function saveFamilyInfo() {
  try {
    await axios.post('http://localhost:8000/save/family', {
      username,
      family_id,
      members: [toRaw(familyMember)]
    })
    ElMessage.success('家长信息已保存')
    showFamilyDialog.value = false
  } catch (err) {
    ElMessage.error('保存失败：' + err.message)
  }
}

async function loadFamilyInfo() {
  if (!family_id || !username) return

  try {
    const res = await axios.get(`http://localhost:8000/get/family?family_id=${family_id}&username=${username}`)
    if (res.data.members && res.data.members.length > 0) {
      Object.assign(familyMember, res.data.members[0])
    }
  } catch (err) {
    console.log("暂无家长信息，首次填写")
  }
}

function uploadHomework() {
  showUploadDialog.value = true
}
</script>

<style scoped>
.setting-wrapper {
  padding: 30px;
  max-width: 1300px;
  margin: 0 auto;
}

.layout-container {
  flex: 1;
  display: flex;
  gap: 20px;
  align-items: stretch;
  height: 100%;        /* ✅ 非常重要，给子项空间 */
}
.left-panel {
  flex: 1;
  min-width: 0;
  height: 100%;            /* ✅ 撑满可用高度 */
  display: flex;           /* ✅ 如果内部还有子元素也想控制高度 */
  flex-direction: column;  /* ✅ 保持垂直方向布局 */
}

.right-panel {
  flex: 1;
  min-width: 0;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* 控制三个按钮的大小 */
.button-group {
  display: flex;
  gap: 6px;              /* 缩小按钮之间的间距 */
  margin-bottom: -5px;    /* 缩小下边距 */
  margin-top: -45px;      /* ✅ 向上移动整个区域 */
  flex-wrap: wrap;
  padding: 0;
  height: 32px;          /* 可选：限制高度 */
  align-items: center;   /* 垂直居中对齐按钮 */
}

.chatbot-area {
  flex: 1;
  min-height: 600px;
  border: 1px solid #ddd;
  border-radius: 10px;
  padding: 3px;
  height: 100%;
  display: flex;
  flex-direction: column;

  margin-bottom: 0;       /* ✅ 确保底部没有额外间距 */
  padding-bottom: 0;      /* ✅ 去掉内边距底部 */
}
</style>