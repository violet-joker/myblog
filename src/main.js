import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router/index'
import naive from "naive-ui"
import './styles/global.css'
import 'highlight.js/styles/atom-one-dark.css';
import hljs from 'highlight.js/lib/core'
import 'highlight.js/lib/common'

const app = createApp(App)
const pinia=createPinia()

app.directive('highlight', function (el) {
    let highlight = el.querySelectorAll('pre code')
    highlight.forEach((block) => {
        hljs.highlightElement(block)
    })
});

app.use(naive)
app.use(router)
app.use(pinia)
app.mount("#app")
