import apiClient from '../client'
import type { Article, ArticleUpdate, ArticleCreate } from '../types/article'

export const articleService = {
  getAll: () => apiClient.get<Article[]>('/articles'),
  getById: (id: string) => apiClient.get<Article>(`/articles/${id}`),
  create: (article: ArticleCreate) => apiClient.post<Article>('/articles', article),
  update: (id: string, article: ArticleUpdate) => apiClient.put<Article>(`/articles/${id}`, article),
  delete: (id: string) => apiClient.delete<void>(`/articles/${id}`),
}
