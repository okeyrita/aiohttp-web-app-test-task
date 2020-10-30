import pathlib

from .views import news_list, get_news_by_id, add_new_news, delete_news_by_id

PROJECT_ROOT = pathlib.Path(__file__).parent


def setup_routes(app):
    app.router.add_get('/api', news_list, name='news_list')
    app.router.add_get('/api/news/{news_id}',
                       get_news_by_id, name='get_news_by_id')
    app.router.add_post('/api/news', add_new_news, name='add_new_news')
    app.router.add_delete('/api/news/{news_id}',
                          delete_news_by_id, name='delete_news_by_id')
    setup_static_routes(app)


def setup_static_routes(app):
    app.router.add_static('/static/',
                          path=PROJECT_ROOT / 'static',
                          name='static')
