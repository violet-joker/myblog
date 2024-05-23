<template>
  <my-article :content="ArticleStore.content"/>
  <side-menu/>
</template>

<script setup>
import { useArticleStore } from "../stores/blog/articleStores.js";
import SideMenu from "../components/blog/side-menu.vue"
import MyArticle from "../components/blog/my-article.vue";
const ArticleStore = useArticleStore()
</script>