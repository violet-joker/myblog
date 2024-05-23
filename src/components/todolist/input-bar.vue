<template>
  <NInput
    type="text"
    size="large"
    round
    placeholder="add something to do..."
    style="width: 400px; margin: 10px;"
    v-model:value="todoName"
    @keyup.enter="add"
  />
  <n-button @click="todoStore.init()">初始化</n-button>
</template>

<script setup>
import { NInput, NButton } from 'naive-ui'
import { ref, computed } from 'vue'
import { useTodoStore} from "../../stores/index.js";

const todoStore = useTodoStore()
const todoName = ref('')
const todoList = computed(() => todoStore.todoList)
function add() {
  if (todoName.value.trim() === '') return
  todoList.value.push(todoName.value)
  todoName.value = ''
  todoStore.save()
}
</script>