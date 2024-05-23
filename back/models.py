# 数据模型
from extension import db


class Topic(db.Model):
    __tablename__ = 'topic'
    topic_id = db.Column(db.Integer, primary_key=True)
    parent_id = db.Column(db.Integer)
    title = db.Column(db.String)


class Article(db.Model):
    __tablename__ = 'article'
    article_id = db.Column(db.Integer, primary_key=True) 
    topic_id = db.Column(db.Integer)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    status = db.Column(db.Integer)