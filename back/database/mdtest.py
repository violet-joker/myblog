from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# 链接mysql数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/test'
db = SQLAlchemy(app)

# 定义数据表
class markdown(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)

    def __init__(self, content, id=None):
        self.content = content
        self.id = id

# 定义article表

# 处理get请求
@app.route('/test', methods=['GET'])
def markdown_get():
    a = markdown.query.all()[0]
    # 根据id从数据库中取文档
    content, id = a.content, a.id
    res = {
        "content": content,
        "id": id
    }
    return jsonify(res)

# 处理post请求
@app.route('/test', methods=['POST'])
def markdown_post():
    data = request.get_json()
    content = data.get('content')
    mesg = markdown(content)
    db.session.add(mesg)
    db.session.commit()
    res = {
        "message": "ok",
    }
    print('ok')
    return jsonify(res)


if __name__ == '__main__':
    app.run(debug=True)
