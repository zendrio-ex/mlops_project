import uuid
import traceback
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from src.application.routers import router
from src.application.utils import request_id
from loguru import logger


async def request_middleware(request: Request, call_next):
    request_id.set(str(uuid.uuid4()))
    try:
        response = await call_next(request)
    except Exception as e:
        logger.exception("internal server error")
        response = JSONResponse(
            {"request_id": request_id.get(),
             "error": e.__class__.__name__ + ': ' + str(e),
             "traceback": traceback.format_exc()
             },
            status_code=500)
    finally:
        logger.info(f"[{request.url.path}] request end")
        return response


def create_app():
    app = FastAPI(title='pet-service')

    app.middleware('http')(request_middleware)

    app.include_router(router)

    logger.info("service was run")
    return app
