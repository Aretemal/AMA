import { defineStore } from 'pinia'
import { ref } from 'vue'
import { articleService } from '@/api/services/articleService'
import type { Article, ArticleCreate } from '@/api/types/article'

export const useArticleStore = defineStore('article', () => {
  const articles = ref<Article[]>([])
  const isLoading = ref(false)
  const isCreating = ref(false)
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

  async function createArticle(article: ArticleCreate) {
    try {
      isCreating.value = true
      error.value = null
      await articleService.create(article)
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
    } finally {
      isCreating.value = false
    }
  }

  async function deleteArticle(id: string, {
    needUpdate = true
  }: {
    needUpdate?: boolean
  } = {}) {
    try {
      error.value = null
      await articleService.delete(id)
      if (needUpdate) {
        articles.value = articles.value.filter(article => article.id !== id)
      }
    } catch (err) {
      error.value = err instanceof Error ? err.message : 'An unknown error occurred'
    }
  }

  return {
    articles,
    isLoading,
    isCreating,
    error,
    deleteArticle,
    fetchArticles,
    createArticle,
  }
})
