import { createRouter, createWebHashHistory } from 'vue-router'
import LoginView from '../views/LoginView.vue'
import HomeView from '../views/HomeView.vue'
import RegisterView from '../views/RegisterView.vue'
import AudienceView from '../views/AudienceView.vue'
import TeacherView from '../views/TeacherView.vue'
const routes = [
  {
    path: '/',
    name: 'Home',
    component: HomeView // 确保组件存在且路径正确
  },
  {
    path: '/login',
    name: 'login',
    component: LoginView
  },
  {
    path: '/register',
    name: 'register',
    component: RegisterView 
  },
  {
    path: '/audience',
    name: 'audience',
    component: AudienceView
  },
  {
    path: '/teacher',
    name: 'teacher',
    component: TeacherView
  },
]

const router = createRouter({
  history: createWebHashHistory(process.env.BASE_URL),
  routes
})

export default router
