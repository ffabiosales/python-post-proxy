from aiohttp import web, ClientSession
from datetime import datetime, timedelta
import json
import jwt
# import asyncio

STARTED_AT = datetime.now()
COUNT_REQUESTS = 0
JWT_SECRET = "a9ddbcaba8c0ac1a0a812dc0c2f08514b23f2db0a68343cb8199ebb38a6d91e4ebfb378e22ad39c2d01d0b4ec9c34aa91056862ddace3fbbd6852ee60c36acbf"
POST_URL = "https://postman-echo.com/post"

routes = web.RouteTableDef()

@routes.post('/')
async def index(request):
    global COUNT_REQUESTS, POST_URL
    now = datetime.now()
    COUNT_REQUESTS += 1
    
    claims = {
        'iat': datetime.timestamp(now),
        'jti': '',
        'payload': {
            'user': "ffabiosales",
            'date': now.strftime("%Y-%m-%d %H:%M:%S")
        }
    }

    token = jwt.encode(claims, JWT_SECRET, algorithm="HS512")
    payload = await request.json()
    async with ClientSession() as session:

        async with session.post(
            POST_URL, 
            data= payload, 
            headers={"x-my-jwt": token, "content-type": request.content_type}
            ) as resp:
                response = await resp.json()
    
    return web.json_response(response)


@routes.get('/status')
async def status(request):
    current_time = datetime.now()
    time_running = current_time - STARTED_AT
    time_running_formated = str(timedelta(seconds=time_running.seconds))
    response = {'started_at': STARTED_AT.strftime("%Y-%m-%d %H:%M:%S"), 'time_running': time_running_formated, 'requests': COUNT_REQUESTS}
    return web.json_response(response)

async def app_factory():
    app = web.Application()
    app.add_routes(routes)
    return app

if __name__ == "__main__":
    web.run_app(app_factory())