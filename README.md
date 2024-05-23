# myblog

## 前端采用vue3框架编写


### todoList 任务清单

初始化数据，添加任务，删除任务

### blog

Blog-read 文章阅读页，markdown文档渲染，支持代码高亮

Blog-edit 文章修改、添加、删除，暂未完善

### test-view 写着玩的页面，暂无内容

博客文章菜单栏手动更新按钮暂时放这里了

#### 表结构

文章表 article, 菜单栏目录下具体文章

content, article_id, topic_id, status

内容        文章编号    上级id    发布状态

专栏表 topic , 组织菜单栏列表

title，       topic_id,    parent_id

专栏(文章)名称   专栏编号      父级编号

### 任务

增删改查
    - 添加新文章，更新topic表和article表，如何自动组织id信息？(article ok)
    - 根据id删除、修改文章 (删除ok)
    - 查询信息，判空 ok

密码验证 ok

代码高亮 ok

错误校验 （放在后端校验还是前端校验？）


## 后端使用python flask框架进行基础的数据操作

测试阶段使用CORS解决跨域问题

使用flask_sqlalchemy连接mysql数据库
