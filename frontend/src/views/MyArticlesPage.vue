<script setup lang="ts">
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()

const articles = articleStore.articles;

onMounted(() => {
  articleStore.fetchArticles()
})
</script>

<template>
  <div class="w-full flex flex-col gap-1">
    <h1 class="text-2xl font-bold">My Articles</h1>
    <div v-if="!articles.length" class="p-4 flex flex-col justify-center items-center gap-4 bg-gray-100 rounded-xl">
      <p>No articles found. Create your first article to get started.</p>
      <el-button type="primary" class="w-fit">Create Article</el-button>
    </div>
  </div>
</template>

<style scoped>
</style>

