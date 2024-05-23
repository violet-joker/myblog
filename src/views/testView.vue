<template>
  <side-menu></side-menu>
  <button @click="getData">更新菜单栏</button>
  <hr><br><br>
  <calc/>
</template>
<script setup>
import SideMenu from "../components/blog/side-menu.vue";
import { useBlogMenuStore } from '../stores/blog/articleStores.js'
import axios from 'axios'
import { ref } from 'vue'
import Calc from "../components/calc.vue";
const Menu = useBlogMenuStore()
const data = ref(null)
async function getData() {
  const url = 'http://127.0.0.1:5000'
  // 获取菜单栏信息
  const topic_res = await axios.get(url + '/topics/')
  const article_res = await axios.get(url + '/articles/')
  data.value = topic_res.data
  // 将得到的数据映射成对象，再传参处理
  const topicList = topic_res.data.results.map(function (item) {
    return {
      topic_id: item.topic_id,
      parent_id: item.parent_id,
      title: item.title
    }
  });
  const articleList = article_res.data.results.map(function (item) {
    return {
      article_id: item.article_id,
      // 与上面的topic_id区别开
      a_topic_id: item.topic_id,
      title: item.title
    }
  });
  // 更新目录
  Menu.updateMenu(topicList, articleList);
}
</script>