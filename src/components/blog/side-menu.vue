<template>
  <n-menu
    id="sideMenu"
    :options="Menu.topics"
    @update:value="handleUpdateValue"
  />
</template>

<script setup>
import { useBlogMenuStore, useArticleStore } from '../../stores/blog/articleStores.js'
import axios from 'axios'
import { ref } from 'vue'
const Menu = useBlogMenuStore()
const Article = useArticleStore()
const url = 'http://localhost:5000/articles/'
function handleUpdateValue(key) {
  axios.get(url+key)
    .then(function (response) {
      console.log(response)
      Article.content = response.data.content
    })
}
</script>

<style>
#sideMenu {
  position: absolute;
  top: 84px;
  right: 40px;
  width: 200px;
  background-color: rgba(58, 61, 65, 0.9);
  font-size: 18px;
  font-weight: bolder;
  text-align: left;
}
@media (max-width: 1200px) {
  #sideMenu {
    display: none;
  }
}
</style>