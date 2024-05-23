import { defineStore } from 'pinia'
import { ref } from 'vue'
import { menuCalc } from '../../scripts/sideMenuCalc.js'

// 菜单栏相关数据管理
export const useBlogMenuStore = defineStore('blogMenu', () => {
    const topics = ref([])
    function initMenu() {
        let data
        if (localStorage.getItem('blogMenu') === null) {
            data = [{label: '暂无数据', key: 1}]
            localStorage.setItem('blogMenu', JSON.stringify(data))
        } else
            data = JSON.parse(localStorage.getItem('blogMenu'))
        topics.value = data
    }
    initMenu()
    function updateMenu(topicList, articleList) {
        const data = menuCalc(topicList, articleList)
        localStorage.setItem('blogMenu', JSON.stringify(data))
        topics.value = data
        console.log('菜单已更新')
    }
    return { topics, updateMenu }
})

// 博客文章数据管理
export const useArticleStore = defineStore('blogArticle', () => {
    const content = ref('# hello world')
    return  { content }
})