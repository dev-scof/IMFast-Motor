"""Response Shortcuts"""
from typing import Any, Optional, Sequence
from uuid import uuid4
from bson import ObjectId
from fastapi import Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import ORJSONResponse as orjson_res
from pydantic import BaseModel


class Response200ModelFactory:

    def __getitem__(self, result_type):
        class ResponseModel200(BaseModel):
            msg: str = 'ok'
            result: result_type
        # Class Anonymization
        class_obj = ResponseModel200
        class_obj.__name__ = (
            f"Response200_{str(uuid4().hex)}"
        )
        return class_obj

    def __call__(self, result: Any = None):
        if result is not None:
            result = jsonable_encoder(
                result,
                custom_encoder={ObjectId: str}
            )
            return orjson_res(
                {'msg': 'ok', 'result': result},
                status_code=200,
            )
        else:
            return orjson_res(
                {'msg': 'ok'},
                status_code=200,
            )


OK = Response200ModelFactory()


class Response201ModelFactory:

    def __getitem__(self, result_type):
        class ResponseModel201(BaseModel):
            msg: str = 'created'
            result: result_type
        # Class Anonymization
        class_obj = ResponseModel201
        class_obj.__name__ = (
            f"Response201_{str(uuid4().hex)}"
        )
        return class_obj

    def __call__(self, result: Any = None):
        if result is not None:
            result = jsonable_encoder(
                result,
                custom_encoder={ObjectId: str}
            )
            return orjson_res(
                {'msg': 'created', 'result': result},
                status_code=201,
            )
        else:
            return orjson_res(
                {'msg': 'created'},
                status_code=201,
            )


CREATED = Response201ModelFactory()


no_content = Response(status_code=status.HTTP_204_NO_CONTENT)


def bad_request(detail: str, errors: Optional[Sequence] = None):
    if errors:
        body = {'msg': 'bad_request', 'detail': detail, 'errors': errors}
    else:
        body = {'msg': 'bad_request', 'detail': detail}
    return orjson_res(body, status_code=400)


def bad_jwt_token(detail: str):
    return orjson_res(
        {
            'msg': 'bad_jwt_token',
            'detail': detail
        },
        status_code=401,
        headers={"WWW-Authenticate": "Bearer"},
    )


def forbidden(detail: str):
    return orjson_res(
        {
            'msg': 'forbidden',
            'detail': detail
        }, status_code=403,
    )


def not_found(detail: str = "resource_not_found"):
    return orjson_res(
        {
            'msg': 'not_found',
            'detail': detail
        },
        status_code=404,
    )


def conflict(detail: str = "resource_already_exists"):
    return orjson_res(
        {'msg': 'conflict', 'detail': detail},
        status_code=409,
    )


def unprocessable_entity(detail: str, errors: Optional[list] = None):
    if errors:
        body = {'msg': 'unprocessable_entity', 'detail': detail, 'errors': errors}
    else:
        body = {'msg': 'unprocessable_entity', 'detail': detail}
    return orjson_res(body, status_code=422)
