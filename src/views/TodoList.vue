<template>
  <input-bar />
  <n-list
    :bordered=true
    :clickable=true
    style="max-height: 400px; width: 600px; margin: auto; text-align: left; overflow-y: scroll;"
  >
    <list-item
      v-for="(item, index) in todoList"
      :key= "item"
      :message = item
      :index = "index"
    />
  </n-list>
</template>

<script setup>
import { NList } from 'naive-ui'
import ListItem from "../components/todolist/list-item.vue";
import InputBar from "../components/todolist/input-bar.vue";
import { computed } from "vue";
import { useTodoStore} from "../stores/index.js";
const todoStore = useTodoStore()
const todoList = computed(() => todoStore.todoList)
</script>
