<template>
  <div class="member-wrapper">
    <el-card class="member-card">
      <el-form :model="member" label-width="100px" size="small">
        <el-form-item label="角色">
          <el-input v-model="member.role" placeholder="如：爸爸、妈妈" />
        </el-form-item>

        <el-form-item label="辅导偏好">
          <el-select
            v-model="member.subjectPreference"
            multiple
            filterable
            allow-create
            placeholder="请选择或填写您平时更愿意辅导的科目，或在陪伴孩子成长过程中经常参与的活动"
            style="width: 100%"
          >
            <el-option
              v-for="subject in subjectOptions"
              :key="subject"
              :label="subject"
              :value="subject"
            />
          </el-select>
        </el-form-item>

        <el-form-item label="可辅导时段">
          <el-input
            v-model="member.educationConcept"
            type="textarea"
            :rows="2"
            placeholder="填写您能陪伴孩子的时间段，我们将为您生成个性化任务计划"
          />
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
const props = defineProps({
  member: {
    type: Object,
    required: true
  }
})

const subjectOptions = ['语文', '数学', '英语', '科学', '美术']
</script>

<style scoped>
.member-wrapper {
  padding: 10px;
}
.member-card {
  width: 100%;
}
</style>