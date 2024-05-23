<template>
  <n-list-item>
    <n-input
      size="large"
      placeholder="null"
      v-model:value="msg"
      @keyup.enter="handle()"
    />
  </n-list-item>
</template>

<script setup>
import { useTodoStore} from "../../stores/index.js";
import { NListItem, NInput } from 'naive-ui'
import { ref } from 'vue'

const todoStore = useTodoStore()
const props = defineProps(['message', 'index'])
const msg = ref(props.message)
const index = props.index


function handle() {
  if (msg.value.trim() === '') {
    todoStore.todoList.splice(index, 1)
  } else {
    todoStore.todoList[index] = msg.value
  }
  todoStore.save()
  alert('success')
}
</script>