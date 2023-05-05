import time
import os
import json


from fastapi import FastAPI, Request
from fastapi.responses import PlainTextResponse
from starlette.types import Message
import uvicorn

from app.service.log import logger
from app.router import user


app = FastAPI()
app.include_router(user.user_router, prefix='/user')


@app.get("/", name="healthcheck", tags=["healthcheck"], response_class=PlainTextResponse)
async def healthcheck():
    return 'success'


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    async def set_body(request: Request):
        receive_ = await request._receive()

        async def receive() -> Message:
            return receive_

        request._receive = receive

    await set_body(request)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time

    if response.status_code != 500 and request.url.path != '/':
        request_body = await request.body()
        log = {
            'app_name': f"{os.environ.get('APP_NAME')}-{os.environ.get('STAGE')}",
            'timestamp': start_time,
            'method': request.method,
            'path': request.url.path,
            'params': str(request.query_params),
            'headers': json.dumps(dict(request.headers.items())),
            'body': request_body.decode("utf-8"),
            'process_time': process_time,
            'status_code': response.status_code
        }

        logger.emit('info', {'log': json.dumps(log)})

    return response


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level='critical', access_log=False)
