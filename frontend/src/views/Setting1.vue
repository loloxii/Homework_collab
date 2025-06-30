<template>
  <div class="setting-wrapper">
    <h1 class="setting-title">个性化设置面板</h1>

    <!-- ✅ 小朋友信息 -->
    <el-card class="panel-card">
      <h3 class="panel-title">小朋友信息</h3>
      <ChildInfoPanel v-model:child="child" />
    </el-card>

    <!-- ✅ 家庭作业信息 -->
    <el-card class="panel-card">
      <h3 class="panel-title">家庭作业</h3>
      <HomeworkPanel v-model="homeworkList" />
    </el-card>

    <!-- ✅ 家庭成员信息 -->
    <el-card class="panel-card">
      <FamilyMembersPanel v-model:members="familyMembers" />
    </el-card>

    <!-- ✅ 保存按钮 -->
    <div style="text-align: center; margin-top: 20px">
      <el-button type="primary" @click="saveAll">保存设置</el-button>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { toRaw } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

import ChildInfoPanel from '../components/ChildInfoPanel.vue'
import FamilyMembersPanel from '../components/FamilyMembersPanel.vue'
import HomeworkPanel from '../components/HomeworkPanel.vue'

// 小朋友信息
const child = reactive({
  age: '',
  grades: [],
  hobbies: [],
  traits: [],
  strengths: []
})

// 家庭成员信息
const familyMembers = ref([
  {
    role: '',
    subjectPreference: [],
    educationConcept: ''
  }
])

// 作业列表（按科目分类）
const homeworkList = ref({})

// 保存设置，提交到后端
async function saveAll() {
  try {
    const payload = {
      child: JSON.parse(JSON.stringify(toRaw(child))),
      members: JSON.parse(JSON.stringify(toRaw(familyMembers.value))),
      homework: JSON.parse(JSON.stringify(toRaw(homeworkList.value)))
    }

    await axios.post('http://localhost:8000/generate_suggestion', payload)
    ElMessage.success('设置已成功提交！')
    console.log('协作建议：', res.data.suggestion)
    console.log('任务分工表：', res.data.assignment_table)
  } catch (err) {
    console.error('提交失败', err)
    ElMessage.error('提交失败：' + err.message)
  }
}
</script>

<style scoped>
.setting-wrapper {
  max-width: 900px;
  margin: 0 auto;
  padding: 30px;
}
.setting-title {
  text-align: center;
  font-size: 24px;
  margin-top: -40px;
  margin-bottom: 10px;
}
.panel-card {
  margin-bottom: 20px;
  padding: 20px;
}
.panel-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
  color: #409EFF;
}
.panel-row {
  margin-bottom: 20px;
}
</style>