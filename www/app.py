import logging; logging.basicConfig(level=logging.INFO)
import asyncio, os, json, time
from datetime import datetime
from aiohttp import web
from jinja2 import Environment, FileSystemLoader

# config 配置代码在后面会创建添加
from config import configs

import orm
from coroweb import add_routes, add_static

# handlers 是URL处理模块，当handlers.py在api章节里完全编辑完在将下一行代码的双并号去掉
## from handlers import cookie2user， COOKIE_NAME

# 初始化jinja2的函数
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

# 以下是middleware， 可以把通用的功能从每个URL处理函数中拿出来集中放到一个地方
# URL处理日志工厂
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        return (await handler(request))
    return logger

# 认证处理工厂 把当前用户绑定到request上， 并对URL/manage/进行拦截，检查当前用户是否是管理员身份
# 需要handlers.py的支持，当handlers.py在API章节里完全编辑完把下面代码的双并号去掉
async def auth_factory(app, handler):
    async def auth(request):
        logging.info('check user: %s %s' % (request.method, request.path))
        request.__user__ = None
        cookie_str = request.cookies.get(COOKIE_NAME)
        if cookie_str:
            user = await cookie2user(cookie_str)
            if user:
                logging.info('set current user: %s' % user.email)
                request.__user__ = user
        if request.path.startswith('/manage/') and (request.__user__ is None or not request.__user__.admin):
            return web.HTTPFOUND('/signin')
        return (await handler(request))
    return auth

# 数据处理工厂
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST'
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await reqeust.post()
                logging.info('request form: %s' % str(request.__data___))
        return (await handler(request))
    return parse_data

# 响应返回处理工厂




# 定义服务器应用响应请求的返回为'Awesome Website'
async def index(request):
    return web.Response(body=b'<h1>Awesome Website</h1>', content_type='text/html')

# 建立服务器应用，持续监听本地9000端口的http请求，对首页‘/’进行响应
def init():
    app = web.Application()
    app.router.add_get('/', index)
    web.run_app(app, host='127.0.0.1', port=9000)

if __name__ == '__main__':
    init()

 