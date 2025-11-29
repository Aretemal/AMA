export type Article = {
  id: string
  title: string
  content: string
  author: string
  createdAt: string
  updatedAt: string
}

export type ArticleUpdate = Partial<Article>

export type ArticleCreate = Omit<Article, 'id' | 'createdAt' | 'updatedAt' | 'author'>
