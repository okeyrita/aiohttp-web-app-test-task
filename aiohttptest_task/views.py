import json
from datetime import datetime

from aiohttp import web

import aiofiles
from pytz import timezone

DATA_PATH = '/data/'
DATA_NEWS = 'news.json'
DATA_COMMENTS = 'comments.json'

TIMEZONE = 'Europe/Moscow'


async def news_list(request):
    '''Request GET /api '''
    async with aiofiles.open(DATA_PATH+DATA_NEWS, mode='r') as news_file, \
            aiofiles.open(DATA_PATH+DATA_COMMENTS, mode='r') as comments_file:

        # Get data abou news and comments
        data_comments = json.load(comments_file).get('comments')
        data_news = json.load(news_file).get('news')

        # Sort news by requirements
        sorted_news = []
        time_now = datetime.now(tz=timezone(TIMEZONE))
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
    async with aiofiles.open(DATA_PATH+DATA_NEWS, mode='r') as news_file:
        data_news = json.load(news_file).get('news')
        news_id = request.match_info['news_id']

        news = None
        for item in data_news:
            if item.get('id') == news_id:
                time_item = datetime.strptime(
                    item.get('date'), '%Y-%m-%dT%H:%M:%S')
                time_now = datetime.now(tz=timezone(TIMEZONE))
                if time_item < time_now and item.get('deleted') == False:
                    news = item
                break

        if news is None:
            # Error 404
            raise web.HTTPNotFound()

        else:
            # Add coments to response
            async with aiofiles.open(DATA_PATH+DATA_COMMENTS, mode='r') as comments_file:
                data_comments = json.load(comments_file).get('comments')
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
    data = await request.post()
    new_comments = data.pop('comments')
    time_now_string = datetime.now(tz=timezone(
        TIMEZONE)).strftime("%Y-%m-%dT%H:%M:%S")
    data.update({
        'deleted': False,
        'date': time_now_string
    })

    # Update news
    with open(DATA_PATH+DATA_NEWS, mode='r') as news_file:
        data_news = json.load(news_file)

    list_news = data_news.get('news').append(data)
    news_count = data_news.get('news_count') + 1
    data_news.update({
        'news': list_news,
        'news_count': news_count
    })
    async with aiofiles.open(DATA_PATH+DATA_NEWS, mode='w') as json_file:
        json.dump(data_news, json_file)

    # Update comments
    for comment in new_comments:
        comment.update({
            'date': time_now_string
        })
    with open(DATA_PATH+DATA_COMMENTS, mode='r') as comments_file:
        data_comments = json.load(comments_file)

    new_comments.extend(data_comments.get('comments'))
    data_comments.update({
        'comments': new_comments,
        'comments_count': len(new_comments)
    })

    async with aiofiles.open(DATA_PATH+DATA_COMMENTS, mode='w') as json_file:
        json.dump(data_comments, json_file)

    return web.HTTPOk()


async def delete_news_by_id(request):
    news_id = request.match_info['news_id']

    with open(DATA_PATH+DATA_NEWS, mode='r') as json_file:
        data_news = json.load(json_file)

    for item in data_news.get('news'):
        if item.get('id') == news_id:
            item.update({
                'deleted': True
            })
            break

    async with aiofiles.open(DATA_PATH+DATA_NEWS, mode='w') as json_file:
        json.dump(data_news, json_file)

    return web.HTTPOk()
