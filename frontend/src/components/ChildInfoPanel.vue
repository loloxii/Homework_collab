<template>
  <div class="child-info-panel">
    <el-form :model="child" label-width="100px" class="child-form">
      <!-- 年龄 -->
      <el-form-item label="年龄">
        <el-input v-model="child.age" type="number" placeholder="如：7" />
      </el-form-item>

      <!-- 年级 -->
      <el-form-item label="年级">
        <el-select
          v-model="child.grades"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入或选择年级"
        >
          <el-option v-for="grade in gradeOptions" :key="grade" :label="grade" :value="grade" />
        </el-select>
      </el-form-item>

      <!-- 兴趣爱好（可输入 + 可选） -->
      <el-form-item label="兴趣爱好">
        <el-select
          v-model="child.hobbies"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入或选择兴趣"
        >
          <el-option v-for="item in hobbyOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>

      <!-- 性格特点 -->
      <el-form-item label="性格特点">
        <el-select
          v-model="child.traits"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入或选择性格"
        >
          <el-option v-for="item in traitOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item>


      <el-form-item label="生活地区">
        <el-input v-model="child.region" placeholder="如：北京 / 上海 / 广州" />
      </el-form-item>

      <!-- 擅长科目 -->
      <!-- <el-form-item label="擅长科目">
        <el-select
          v-model="child.strengths"
          multiple
          filterable
          allow-create
          default-first-option
          placeholder="输入或选择科目"
        >
          <el-option v-for="item in subjectOptions" :key="item" :label="item" :value="item" />
        </el-select>
      </el-form-item> -->
    </el-form>
  </div>
</template>

<script setup>
defineProps({
  child: {
    type: Object,
    required: true
  }
})

// 默认选项提示（可选，可自扩展）
const gradeOptions = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级']
const hobbyOptions = ['绘画', '写作', '阅读', '运动', '音乐']
const traitOptions = ['开朗', '细心', '有耐心', '爱表达', '逻辑强']
const subjectOptions = ['语文', '数学', '英语', '科学', '美术']

</script>

<style scoped>
.child-info-panel {
  padding: 10px;
}
.child-form {
  background: #fcfcfc;
  padding: 2px;
  border-radius: 10px;
}
.form-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 5px;
  color: #409EFF; /* Element Plus 主色调 */
}
</style>