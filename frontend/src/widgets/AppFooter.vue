<script setup lang="ts">
import { onMounted } from 'vue'
import { useArticleStore } from '@/stores/article'

const articleStore = useArticleStore()

onMounted(() => {


  articleStore.fetchArticles()
})
</script>



<template>
  <div>







    <h1>  Home

    </h1>
  </div>
</template>

<style scoped>
</style>

