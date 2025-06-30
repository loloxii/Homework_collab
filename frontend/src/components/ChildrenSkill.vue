<template>
  <div class="chart-wrapper">
    <h3>技能进度雷达图</h3>
    <v-chart :option="radarOption" autoresize style="height: 400px;" />
  </div>
</template>

<script setup>
import { computed, watch, ref } from 'vue'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import {
  CanvasRenderer
} from 'echarts/renderers'
import {
  RadarChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent
} from 'echarts/components'

use([
  CanvasRenderer,
  RadarChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent
])

const props = defineProps({
  assignmentTable: {
    type: Array,
    default: () => []
  }
})

const radarOption = ref({
  title: {
    text: '技能维度雷达图',
    left: 'center',
    textStyle: { fontSize: 16 }
  },
  tooltip: {},
  radar: {
    indicator: [], // 会在下方 computed 中动态生成
    radius: '65%',
    splitNumber: 5,
    shape: 'polygon'
  },
  series: [
    {
      name: '技能完成进度',
      type: 'radar',
      data: []
    }
  ]
})

// 动态更新雷达图数据
const updateRadarData = () => {
  const skillMap = {} // { "语言智能": [80, 10, 70, 50], ... }

  props.assignmentTable.forEach(task => {
    const skills = (task.培养技能 || '').split(/，|,/)
    skills.forEach(skill => {
      skill = skill.trim()
      if (!skill) return
      const progress = task.完成进度 ?? 0
      if (!skillMap[skill]) skillMap[skill] = []
      skillMap[skill].push(progress)
    })
  })

  const indicators = Object.keys(skillMap).map(skill => ({
    name: skill,
    max: 100
  }))

  const averagedData = Object.values(skillMap).map(progressList => {
    const total = progressList.reduce((a, b) => a + b, 0)
    return Math.round(total / progressList.length)
  })

  radarOption.value.radar.indicator = indicators
  radarOption.value.series[0].data = [
    {
      value: averagedData,
      name: '平均进度'
    }
  ]
}

watch(() => props.assignmentTable, updateRadarData, { immediate: true })
</script>

<style scoped>
.chart-wrapper {
  margin-top: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
}
</style>