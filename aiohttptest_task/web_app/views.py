import json
from datetime import datetime

from aiohttp import web
import copy
from pytz import timezone

DATA_PATH = 'web_app/data/'
DATA_NEWS = 'news.json'
DATA_COMMENTS = 'comments.json'


async def news_list(request):
    '''Request GET /api '''
    with open(DATA_PATH+DATA_NEWS) as news_file, \
            open(DATA_PATH+DATA_COMMENTS) as comments_file:

        # Get data about news and comments
        data_news = copy.deepcopy(json.load(news_file).get('news'))
        data_comments = copy.deepcopy(json.load(comments_file).get('comments'))

        # Sort news by requirements
        sorted_news = []
        time_now = datetime.now()
        for item in data_news:
            time_item = datetime.strptime(
                item.get('date'), '%Y-%m-%dT%H:%M:%S')

            # News was not deleted and with valid time
            if time_item < time_now and item.get('deleted') == False:
                # Add comments count for current news
                comments_count = 0
                news_id = item.get('id')
                for comment in data_comments:
                    if comment.get('news_id') == news_id:
                        comments_count += 1

                item.update({
                    'comments_count': comments_count
                })

                # Add news to list with sort order from newest to oldest
                if len(sorted_news) == 0:
                    sorted_news.append(item)
                else:
                    for i in range(len(sorted_news)):
                        time_sorts_item = datetime.strptime(
                            sorted_news[i].get('date'), '%Y-%m-%dT%H:%M:%S')

                        if time_sorts_item < time_item:
                            sorted_news.insert(i, item)
                            break

                        elif i == len(sorted_news) - 1:
                            sorted_news.append(item)

        news_count = len(sorted_news)
        response_data = {
            'news': sorted_news,
            'news_count': news_count
        }

        return web.json_response(response_data)


async def get_news_by_id(request):
    '''Request GET /api/news/{id} '''
    with open(DATA_PATH+DATA_NEWS, mode='r') as news_file:
        data_news = copy.deepcopy(json.load(news_file).get('news'))
    news_id = int(request.match_info['news_id'])

    news = None
    for item in data_news:
        if item.get('id') == news_id:
            time_item = datetime.strptime(
                item.get('date'), '%Y-%m-%dT%H:%M:%S')
            time_now = datetime.now()
            if time_item < time_now and item.get('deleted') == False:
                news = item
            break

    if news is None:
        # Error 404
        raise web.HTTPNotFound()

    else:
        # Add coments to response
        with open(DATA_PATH+DATA_COMMENTS, mode='r') as comments_file:
            data_comments = copy.deepcopy(json.load(comments_file).get('comments'))
        sorted_comments = []
        for comment in data_comments:
            if comment.get('news_id') == news_id:
                # Add comments in sort order from newest to oldest
                if len(sorted_comments) == 0:
                    sorted_comments.append(comment)
                else:
                    time_comment = datetime.strptime(
                        comment.get('date'), '%Y-%m-%dT%H:%M:%S')

                    for i in range(len(sorted_comments)):
                        time_sorts_comment = datetime.strptime(
                            sorted_comments[i].get('date'), '%Y-%m-%dT%H:%M:%S')

                        if time_sorts_comment < time_comment:
                            sorted_comments.insert(i, comment)
                            break

                        elif i == len(sorted_comments) - 1:
                            sorted_comments.append(comment)

        comments_count = len(sorted_comments)
        response_data = news

        response_data.update({
            'comments': sorted_comments,
            'comments_count': comments_count
        })

        return web.json_response(response_data)


async def add_new_news(request):
    '''Request POST /api/news '''
    data = await request.text()
    data = json.loads(data)

    new_comments = copy.deepcopy(data.pop('comments'))
    time_now_string = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    data.update({
        'deleted': False,
        'date': time_now_string
    })

    # Update news
    with open(DATA_PATH+DATA_NEWS, mode='r') as news_file:
        data = json.load(news_file)
        data_news = copy.deepcopy(data)
        list_news = data_news.get('news')
        list_news.append(data)

    news_count = data_news.pop('news_count') + 1
    result_news = {
        'news': list_news,
        'news_count': news_count
    }

    with open(DATA_PATH+DATA_NEWS, mode='w') as json_file:
        json.dump(result_news, json_file)

    # Update comments
    for comment in new_comments:
        comment.update({
            'date': time_now_string
        })
    with open(DATA_PATH+DATA_COMMENTS, mode='r') as comments_file:
        data_comments = copy.deepcopy(json.load(comments_file))

    new_comments.extend(data_comments.pop('comments'))
    data_comments.update({
        'comments': new_comments,
        'comments_count': len(new_comments)
    })

    with open(DATA_PATH+DATA_COMMENTS, mode='w') as json_file:
        json.dump(data_comments, json_file)

    return web.HTTPOk()


async def delete_news_by_id(request):
    '''Request DELETE /api/news/{id} '''
    news_id = request.match_info['news_id']

    with open(DATA_PATH+DATA_NEWS) as json_file:
        data_news = copy.deepcopy(json.load(json_file))

        for item in data_news.get('news'):
            if item.get('id') == news_id:
                item.update({
                    'deleted': True
                })
                break

    with open(DATA_PATH+DATA_NEWS, mode='w') as json_file:
        json.dump(data_news, json_file)

    return web.HTTPOk()
