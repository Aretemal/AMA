import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import Home from '@/views/HomePage.vue'
import MyArticles from '@/views/MyArticlesPage.vue'
import Settings from '@/views/SettingsPage.vue'
import Login from '@/views/LoginPage.vue'
import Register from '@/views/RegisterPage.vue'

import { AppRoutes } from '../constants/appRoutes'
import CreateArticleForm from '@/views/CreateArticleForm.vue'
import EditArticleForm from '../views/EditArticleForm.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: AppRoutes.LOGIN,
      name: 'login',
      component: Login,
      meta: { requiresGuest: true },
    },
    {
      path: AppRoutes.REGISTER,
      component: Register,
      meta: { requiresGuest: true },
    },
    {
      path: AppRoutes.HOME,
      component: Home,
      meta: { requiresAuth: true },
    },
    {
      path: AppRoutes.MY_ARTICLES,
      component: MyArticles,
      meta: { requiresAuth: true },
    },
    {
      path: AppRoutes.SETTINGS,
      component: Settings,
      meta: { requiresAuth: true },
    },
    {
      path: AppRoutes.CREATE_ARTICLE,
      component: CreateArticleForm,
      meta: { requiresAuth: true },
    },
    {
      path: AppRoutes.ARTICLE_DETAILS,
      component: EditArticleForm,
      meta: { requiresAuth: true },
    },
  ],
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiredAuth) {
    const isAuthenticated = await authStore.checkAuth()
    if (!isAuthenticated) {
      next({ name: 'login', query: { redirect: to.path } })
      return
    }
  }

  next()
})

export default router
