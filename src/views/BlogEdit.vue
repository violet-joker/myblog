<template>
  <div>
    topic_id:
    <input type="number" @keyup.enter="fetchData" v-model="article_id"/><br><br>
    title:
    <input type="text" v-model="title"/><br><br>
    <button @click="fetchData">get</button>
    <button @click="submitData">post</button>
    <button @click="deleteData">delete</button>
  </div>
  <div style="display: flex; height: auto;">
    <n-input id="editor" type="textarea" v-model:value="input"/>
    <my-article id="article-edit" :content="input"/>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import axios from 'axios';
import MyArticle from "../components/blog/my-article.vue";

const input = ref('')
const article_id = ref(10001)
const title = ref('')
const url = 'http://localhost:5000/articles/'

function checkPassword() {
  let password = prompt('输入密码进行验证：')
  if (password === '0') {
    alert('ok')
    return true
  } else {
    alert('密码错误')
    return false
  }
}
function fetchData() {
// 发送get请求申请数据，根据id获取文章
  axios.get(url+article_id.value)
    .then(function (response) {
      console.log(response)
      input.value = response.data.content
    })
}

function submitData() {
  if (!checkPassword()) return
// 发送post请求提交数据，提交文章
  const content = input.value
  axios.post(url, {
    topic_id: article_id.value,
    title: title.value,
    content: content,
    status: 1
  })
    .then(function (response) {
      console.log(response)
    })
}

function deleteData() {
  if (!checkPassword()) return
  axios.delete(url+article_id.value)
    .then(function (response) {
      console.log(response)
      input.value = '# 文章已删除'
    })
}
</script>

<style>
#editor {
  margin: 10px;
  width: 50%;
  text-align: left;
}
#article-edit {
  text-align: left;
  margin: 10px;
  width: 50%;
}
</style>