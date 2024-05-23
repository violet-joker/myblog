import TodoList from '../views/TodoList.vue'
import {createRouter, createWebHistory} from "vue-router"
import BlogRead from "../views/BlogRead.vue"
import BlogEdit from "../views/BlogEdit.vue"
import testView from "../views/testView.vue"

const routes = [
    {
        path: '/todo',
        component: TodoList,
    },
    {
        path: '/read',
        component: BlogRead,
    },
    {
        path: '/edit',
        component: BlogEdit,
    },
    {
        path: '/testView',
        component: testView,
    },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router