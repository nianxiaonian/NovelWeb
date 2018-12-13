from bson import ObjectId
from flask import current_app, jsonify
from flask import render_template
from flask import request


from novel import mongo
from . import index_blu


@index_blu.route('/index')
def index():
    '''首页小说列表展示'''
    # 分类展示
    try:
        categories_id = mongo.db.book136.distinct('category_id')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=500, errmsg='查询分类数据失败')
    if not categories_id:
        return jsonify(errno=400, errmsg='无分类数据')
    category_list = []
    for category_id in categories_id:
        try:
            category_name = mongo.db.book136.find_one({'category_id': category_id})['category_name']
        except Exception as e:
            current_app.logger.error(e)
            return jsonify(errno=500, errmsg='查询数据失败')
        if not category_name:
            return jsonify(errno=400, errmsg='当前分类id未查询到分类name')

        category_list.append({'category_name': category_name, 'category_id': category_id})

    # 排行榜展示
    try:
        novels = mongo.db.book136.find().sort('clicks', -1).limit(10)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=401, errmsg='查询小说排行榜失败')

    novel_list = []
    for novel in novels:
        novel['_id'] = str(novel['_id'])
        novel_list.append(novel)

    data = {
        'category_list': category_list,
        'novel_list': novel_list,
    }

    return render_template('index.html', data=data)


@index_blu.route('/novel_list')
def novel_list():
    cid = request.args.get('cid', 1)
    page = request.args.get('page', 1)
    # per_page = request.args.get('per_page', 1)
    try:
        cid, page= int(cid), int(page)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=401, errmsg="参数错误")

    try:
        novels = mongo.db.book136.find({'category_id': cid})
        total_count = novels.count()
        novels = novels.limit(10).skip(10*(page-1))
        total_page = total_count//10 + 1

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=401, errmsg='查询小说列表失败')

    novel_list = []
    for novel in novels:
        novel['_id'] = str(novel['_id'])
        novel_list.append(novel)

    data = {
        'novel_list': novel_list,
        'total_page': total_page,
        'current_page': page

    }

    return jsonify(errno=0, errmsg='OK', data=data)


@index_blu.route('/<novel_id>')
def get_novel_detail(novel_id):
    # 排行榜展示
    try:
        novels = mongo.db.book136.find().sort('clicks', -1).limit(10)

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=401, errmsg='查询小说排行榜失败')

    novel_list = []
    for novel in novels:
        novel['_id'] = str(novel['_id'])
        novel_list.append(novel)

    # 小说详情页展示
    try:
        novel = mongo.db.book136.find_one({'_id':ObjectId(novel_id)})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=500, errmsg='查询小说详情失败')
    if not novel:
        return jsonify(errno=500, errmsg='无小说详情数据')
    # 修改小说点击量
    try:
        clicks = novel['clicks'] + 1
        mongo.db.book136.update_one({'_id':ObjectId(novel_id)}, {'$set':{'clicks': clicks}})
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=500, errmsg='修改点击量失败')

    data = {
        'novel_list': novel_list,
        'novel_detail': novel,
    }

    return render_template('detail.html', data=data)


@index_blu.route('/search', methods=['GET','POST'])
def search_novel():
    keyword = request.args.get('q')
    print(keyword)
    try:
        novels = mongo.db.book136.find({'name':{'$regex':'^.*%s.*$' % keyword}})
        print(novels)
        if novels.count() == 0:
            novels = mongo.db.book136.find({'author': {'$regex': '^.*%s.*$' % keyword, '$options':'s'}})
        if novels.count() == 0:
            novels = mongo.db.book136.find({'content': {'$regex': '^.*%s.*$' % keyword, '$options':'s'}})
        if novels.count() == 0:
            return jsonify(errno=500, errmsg='找不到资源')

    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=500, errmsg='搜索失败')

    novel_list = []
    for novel in novels:
        novel['_id'] = str(novel['_id'])
        novel_list.append(novel)

    data = {
        'novel_list': novel_list,
    }

    # return render_template('search.html', data=data)
    return jsonify(errno=0, data=data)






@index_blu.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')


