# 一、前端

#### 1.markdown-it渲染文本

+ v-model双向绑定，实时渲染
+ MarkdownIt将字符串渲染成html
+ 

---
```html
<template>
    <textarea v-model="input"/>
    <div
        v-html="result"
        class="markdown-body" />
</template>

<script setup>
...
const input = ref('')
const md = new MarkdownIt()
const result = computed(() => md.render(input.value))
</script>
```
---

# 二、后端

#### 跨域问题

不同源引起，协议、域名、端口

---
```python
# 设置允许任何源的任何请求，详细查阅flask_cors文档
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
```
---


#### 数据库

#### 链接数据库

---
```python
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
# 设置数据库链接uri，链接的数据库+链接驱动://用户名:密码:地址/要链接的数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test'
db = SQLAlchemy(app)
```
---

#### 增删改查

---
```python
# 定义表结构
class tableName(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    # 构造函数
    def __init__(self, content, id=None):
        self.content = content
        self.id = id

# 查询
@app.route('/test', methods=['GET'])
def json_get():
    data = markdown.query.filter_by(id=3).all()[0]
    res = {
        "content": data.content,
        "id": data.id,
        "message": "success"
    }
    return jsonify(res)

# 插入
@app.route('/test', methods=['POST'])
def json_post():
    # 接收post数据
    data = request.get_json()
    # 取属性
    content = data.get('content')
    # 创建表实例
    message = tableName(content)
    # 插入数据
    db.session.add(message)
    # 确认提交
    db.session.commit()
```
---
```mysql
-- 清空数据
truncate table markdown;
```
---
