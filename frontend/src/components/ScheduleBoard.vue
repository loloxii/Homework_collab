<template>
  <div class="schedule-board">
    <h2>作业时间安排</h2>

    <div class="calendar-grid">
      <!-- 表头 -->
      <div class="calendar-header">
        <div class="time-cell-header"></div>
        <div v-for="day in days" :key="day" class="day-header">{{ day }}</div>
      </div>

      <!-- 时间行 -->
      <div class="calendar-body">
        <div v-for="time in times" :key="time" class="time-row">
          <div class="time-cell">{{ time }}</div>
          <div
            v-for="day in days"
            :key="`${day}-${time}`"
            class="task-slot"
            @click="openTaskMenu(day, time)"
          >
            <draggable
              :list="schedule[day][time]"
              group="tasks"
              item-key="小任务"
              class="task-cell"
              :sort="true"
            >
              <template #item="{ element }">
                <div class="task-chip">
                  <div class="task-title">{{ element.小任务 }}</div>
                  <el-progress
                    :percentage="element.完成进度 || 0"
                    :stroke-width="6"
                    color="#67c23a"
                    class="progress-bar"
                    :show-text="false"
                  />
                  <div class="task-controls">
                    <el-button @click.stop="adjustProgress(element, -10)" size="small" circle>-</el-button>
                    <el-button @click.stop="adjustProgress(element, 10)" size="small" circle>+</el-button>
                    <el-button type="success" @click.stop="saveProgress(element)" size="small">✅</el-button>
                  </div>
                </div>
              </template>
            </draggable>
          </div>
        </div>
      </div>
    </div>

    <!-- 弹窗选择任务 -->
    <el-dialog v-model="taskDialogVisible" title="选择要添加的任务" width="380px">
      <el-select v-model="selectedTask" placeholder="请选择任务" style="width: 100%">
        <el-option
          v-for="task in unassignedTasks"
          :key="task.小任务"
          :label="`${task.小任务}（${task.预计用时}）`"
          :value="task"
        />
      </el-select>
      <template #footer>
        <el-button @click="taskDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmTaskSelection">添加</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import draggable from 'vuedraggable'
import { ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import axios from 'axios'


const props = defineProps(['assignmentTable'])

const days = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
const times = Array.from({ length: 13 }, (_, i) => `${9 + i}:00`)

const unassignedTasks = ref([])
const schedule = ref({})
days.forEach(day => {
  schedule.value[day] = {}
  times.forEach(time => {
    schedule.value[day][time] = []
  })
})

const taskDialogVisible = ref(false)
const selectedTask = ref(null)
const currentSlot = ref({ day: '', time: '' })

watch(
  () => props.assignmentTable,
  (newTasks) => {
    if (newTasks && newTasks.length) {
      unassignedTasks.value = [...newTasks]
    }
  },
  { immediate: true }
)

function openTaskMenu(day, time) {
  currentSlot.value = { day, time }
  selectedTask.value = null
  taskDialogVisible.value = true
}

function confirmTaskSelection() {
  const task = { ...selectedTask.value, 完成进度: 0 }
  const { day, time } = currentSlot.value
  if (!task) {
    ElMessage.warning('请先选择任务')
    return
  }
  schedule.value[day][time].push(task)
  unassignedTasks.value = unassignedTasks.value.filter(t => t.小任务 !== task.小任务)
  taskDialogVisible.value = false
}

const emit = defineEmits(['update:assignmentTable'])

function adjustProgress(task, amount) {
  task.完成进度 = Math.max(0, Math.min(100, (task.完成进度 || 0) + amount))

  // 可选：提前触发更新（不等待保存）
  const updated = props.assignmentTable.map(t =>
    t.小任务 === task.小任务 ? { ...t, 完成进度: task.完成进度 } : t
  )
  emit('update:assignmentTable', updated)
}

async function saveProgress(task) {
  try {
    await axios.post('http://localhost:8000/update_task_progress', {
      小任务: task.小任务,
      完成进度: task.完成进度
    })
    ElMessage.success(`✅ ${task.小任务} 的进度已保存`)

    // ✅ 同步更新父组件中的 assignmentTable
    const updated = props.assignmentTable.map(t =>
      t.小任务 === task.小任务 ? { ...t, 完成进度: task.完成进度 } : t
    )
    emit('update:assignmentTable', updated)

  } catch (e) {
    console.error('❌ 保存失败:', e)
    ElMessage.error('保存失败，请检查后端服务')
  }
}
</script>

<style scoped>
.schedule-board {
  padding: 16px;
  font-family: 'Segoe UI', sans-serif;
}

.calendar-grid {
  border: 1px solid #ddd;
  font-size: 12px;
  border-radius: 6px;
  overflow-x: auto;
}

.calendar-header {
  display: grid;
  grid-template-columns: 60px repeat(7, 1fr);
  background-color: #f4f6fa;
}

.time-cell-header {
  background: #f4f6fa;
}

.day-header {
  text-align: center;
  padding: 6px 0;
  font-weight: 500;
  border-left: 1px solid #ddd;
}

.calendar-body {
  display: grid;
  grid-template-rows: repeat(13, auto);
}

.time-row {
  display: grid;
  grid-template-columns: 60px repeat(7, 1fr);
  min-height: 36px;
}

.time-cell {
  text-align: center;
  background-color: #fafafa;
  border-right: 1px solid #ddd;
  padding-top: 6px;
  font-size: 11px;
}

.task-slot {
  border-left: 1px solid #eee;
  padding: 3px;
  background-color: #fff;
  min-height: 36px;
  cursor: pointer;
}

.task-cell {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.task-chip {
  background-color: #e3f2fd;
  border-radius: 4px;
  padding: 3px 5px;
  font-size: 11px;
  color: #333;
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.task-title {
  font-weight: 500;
  line-height: 1.2;
}

.task-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 4px;
}

.progress-bar {
  margin: 0;
}
</style>