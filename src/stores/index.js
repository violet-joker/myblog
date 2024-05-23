import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'

export const useTodoStore = defineStore('todoList',() => {
    const todoString = localStorage.getItem('todoList')
    const todoList = JSON.parse(todoString)
    function init() {
        localStorage.removeItem('todoList')
        const data = ['操作系统', '计算机网络', '算法与数据结构', '计算机组成原理', '数据库']
        localStorage.setItem('todoList', JSON.stringify(data))
        location.reload()
    }
    function save() {
        const todoListString = JSON.stringify(todoList)
        localStorage.setItem('todoList', todoListString)
        location.reload()
    }
    return {todoList, init, save}
})
