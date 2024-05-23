<template>
  <div name="my-article"
       v-highlight
       v-html="article"
       class="markdown-body"
       style="text-align: left;
       margin: 20px;
       background-color: transparent;"
  />
</template>

<script setup>
import { computed } from 'vue'
import { marked } from 'marked'
import 'github-markdown-css'

// 传递参数
const props = defineProps({
  content: {
    type: String,
    default: '# 无文章'
  },
})
// 文本渲染
const article = computed(() => marked(props.content))
</script>