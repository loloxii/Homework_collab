import { defineStore } from 'pinia'

export const useTaskStore = defineStore('taskStore', {
  state: () => ({
    llmGeneratedTasks: []
  }),
  actions: {
    setLLMTasks(tasks) {
      this.llmGeneratedTasks = tasks
    }
  }
})