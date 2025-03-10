import traceback
from typing import Sequence
from fastapi import Request, FastAPI, HTTPException
from fastapi.responses import ORJSONResponse
from fastapi.exceptions import RequestValidationError
from app.response import (
    bad_request, not_found, bad_jwt_token,
    forbidden
)
from jose import JWTError
from loguru import logger
from settings import Settings


def init_app(app: FastAPI, settings: Settings):

    @app.exception_handler(400)
    async def bad_request_handler(
        request: Request,
        exc: HTTPException
    ):
        return bad_request(exc.detail)

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError
    ):
        """Validation Exception Handler"""
        errors: Sequence = exc.errors()
        detail = errors[0].get('msg') if errors else None
        for error in errors:
            if error.get('ctx'):
                error['ctx'] = str(error['ctx'])
        return bad_request(detail, errors)

    @app.exception_handler(JWTError)
    async def unauthorized_handler(
        request: Request,
        exc: JWTError
    ):
        return bad_jwt_token(str(exc.args[0]))

    @app.exception_handler(403)
    async def forbidden_handler(
        request: Request,
        exc: HTTPException
    ):
        return forbidden(exc.detail)

    @app.exception_handler(404)
    async def not_found_handler(
        request: Request,
        exc: HTTPException
    ):
        return not_found(exc.detail)

    @app.exception_handler(Exception)
    async def internal_server_error_handler(
        request: Request,
        exc: HTTPException
    ):
        return ORJSONResponse(
            {'msg': 'internal_server_error'},
            status_code=500,
        )