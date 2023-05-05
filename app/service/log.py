import time
import os
import json
import traceback
from typing import Callable


from fastapi import Request, Response
from fastapi.exceptions import HTTPException
from fastapi.routing import APIRoute
from fluent import sender


class ValidationErrorLoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            try:
                return await original_route_handler(request)
            except (HTTPException, Exception) as exc:
                body = await request.body()
                log = {
                    'app_name': f"{os.environ.get('APP_NAME')}-{os.environ.get('STAGE')}",
                    'timestamp': time.time(),
                    'method': request.method,
                    'path': request.url.path,
                    'params': str(request.query_params),
                    'headers': json.dumps(dict(request.headers.items())),
                    'body': body.decode("utf-8"),
                    'process_time': None,
                    'status_code': 500 if not isinstance(exc, HTTPException) else exc.status_code,
                    'error_message': traceback.format_exc()
                }
                logger.emit('error', {'log': json.dumps(log)})

                if isinstance(exc, HTTPException):
                    raise exc

                raise HTTPException(status_code=500)

        return custom_route_handler


logger = sender.FluentSender('was-firelens', host=os.environ['FLUENT_HOST'], port=int(os.environ['FLUENT_PORT']))
