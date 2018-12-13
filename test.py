# from novel import mongo
#
#
#
# categories = mongo.db.novel.find()
# print(categories)
import time

import datetime

from bson import ObjectId
from flask import Flask
from flask_pymongo import PyMongo, DESCENDING

from config import Config

app = Flask(__name__)
app.config.from_object(Config)

mongo = PyMongo(app)
# novel = mongo.db.system.novel.find()
categories_id = mongo.db.novel.distinct('category_id')
print(categories_id)
# category_name = mongo.db.novel.find_one({'category_id': 1})['category_name']
#
# mongo.db.novel.update_one({'clicks':21},{'$set':{'category_id': 2}})
# novel = mongo.db.novel.find_one({'_id':ObjectId('5bf61c7654c9af0f10279d33')})
# mongo.db.novel.update_one({'_id':ObjectId('5bf61c7654c9af0f10279d33')}, {'$set':{'clicks': 22}})
#
# result = mongo.db.novel.find({'name': {'$regex': '^.*%s.*$' % '梳子'}})
# print(result.count() == 0)
# for ret in result:
#     if ret == None:
#         print(1)
