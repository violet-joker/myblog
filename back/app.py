from flask import Flask, jsonify, request
from flask.views import MethodView
from extension import db
from models import Topic, Article
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 连接mysql数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route('/')
def hello_world():
    return 'hello world!'

class topicApi(MethodView):
    # 查询菜单选项需要的数据
    def get(self):
        data = Topic.query.all()
        topics = []
        for topic in data:
            item = {
                'topic_id': topic.topic_id,
                'title': topic.title,
                'parent_id': topic.parent_id,
            }
            topics.append(item)
        res = {'message': 'ok', 'results': topics}
        return jsonify(res)

topic_view = topicApi.as_view('topic_api')
app.add_url_rule('/topics/', view_func=topic_view, methods=['GET'])


class articleAPI(MethodView):
    # 查询文章
    def get(self, article_id=None):
        if article_id == None:
            # 查询所有文章的id以及章节id
            data = Article.query.with_entities(Article.article_id, Article.topic_id, Article.title)
            articles = []
            for article in data:
                item = {
                    'article_id': article.article_id,
                    'topic_id': article.topic_id,
                    'title': article.title
                }
                articles.append(item)
            res = {'message': 'ok', 'results': articles}
            return jsonify(res)
        else: 
            # 根据文章id查询文章内容
            article = Article.query.get(article_id)
            if (article == None):
                return jsonify({'message': 'not ok', 'content': '# 暂无文章'})
            res = {'message': 'ok', 'content': article.content}
            return jsonify(res)

    # 添加新文章
    def post(self):
        data = request.json
        article = Article()
        article.topic_id = data.get('topic_id')
        article.title = data.get('title')
        article.content = data.get('content')
        article.status = data.get('status')
        db.session.add(article)
        db.session.commit()
        return jsonify({'message': '文章已添加'})

    # 根据id删除文章
    def delete(self, article_id):
        article = Article.query.get(article_id)
        if (article == None):
            return jsonify({'message': '文章id不存在'})
        db.session.delete(article)
        db.session.commit()
        return jsonify({'message': '文章已删除'})
    

article_view = articleAPI.as_view('article_api')
app.add_url_rule('/articles/', view_func=article_view, methods=['POST', 'GET'])
app.add_url_rule('/articles/<int:article_id>', view_func=article_view, methods=['GET', 'DELETE',])


if __name__ == '__main__':
    app.run(debug=True)
