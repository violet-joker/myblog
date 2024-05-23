<template>
  <nav class="main-nav">
    <router-link to="/todo">TodoList</router-link> |
    <router-link to="/read">Blog-read</router-link> |
    <router-link to="/edit">Blog-edit</router-link> |
    <router-link to="/testView">test-view</router-link>
  </nav>
  <div class="main-body"><router-view></router-view></div>
</template>

<script setup>
</script>

<style>
.main-nav {
  left: 0;
  right: 0;
  position: sticky;
  top: 0;
  background-color: rgba(12, 12, 12, 0.8);
  font-size: 15px;
  padding: 20px 0 20px 0;
  margin-bottom: 20px;
}

.main-body {
  background-color: rgba(89, 111, 120, 0.8);
  opacity: 1;
  max-width: 1170px;
  margin-left: auto;
  margin-right: auto;
  padding-top: 50px;
  padding-bottom: 50px;
  height: auto;
  min-height: 800px;
  overflow: auto;
}
</style>