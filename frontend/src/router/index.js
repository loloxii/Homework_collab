import { createRouter, createWebHistory} from 'vue-router'
import Setting from '../views/Setting.vue'
import TaskList from '../views/TaskList.vue'
import AIGenerator from '../views/AIGenerator.vue'
import LoginPage from '../views/LoginPage.vue'

const routes = [
  { path: '/', redirect: '/login' },
  { path: '/login', component: LoginPage },
  { path: '/setting', component: Setting, meta: { requiresAuth: true } },
  { path: '/tasks', component: TaskList, meta: { requiresAuth: true } },
  { path: '/ai', component: AIGenerator, meta: { requiresAuth: true } },
]


const router = createRouter({
    history: createWebHistory(),
    routes
})

// 🔒 导航守卫
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')
  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else {
    next()
  }
})

export default router