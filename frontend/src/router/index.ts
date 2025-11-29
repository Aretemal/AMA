import { createRouter, createWebHistory } from 'vue-router'

import Home from '@/views/HomePage.vue'
import MyArticles from '@/views/MyArticlesPage.vue'
import Settings from '@/views/SettingsPage.vue'

import { AppRoutes } from '../constants/appRoutes'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: AppRoutes.HOME,
      component: Home,
    },
    {
      path: AppRoutes.MY_ARTICLES,
      component: MyArticles,
    },
    {
      path: AppRoutes.SETTINGS,
      component: Settings,
    },
  ],
})

export default router
