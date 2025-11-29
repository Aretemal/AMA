import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { articleService } from '@/api/services/articleService'
import type { Article, ArticleCreate } from '@/api/types/article'

export const useArticleStore = defineStore('article', () => {
  const articles = ref<Article[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  async function fetchArticles() {
    try {
      isLoading.value = true
         error.value = null

      const response = await articleService.getAll(  )
      articles.value = response.data
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
    } finally {
      isLoading.value = false
    }
  }

  return {
    articles,
    isLoading,
    error,
    fetchArticles,
  }
})
