from dataclasses import asdict

from sanic.request import Request
from sanic.response import json
from sanic_jwt import protected
from sanic_restful import Resource

from src.db import data_db
from src.definitions import BadRequestError, ApiError, Data, KeyVal


class DataResource(Resource):
    decorators = [protected()]

    async def get(self, request: Request, object_id: int):
        result = data_db.get(doc_id=object_id)

        if not result:
            raise ApiError(
                status_code=404,
                error_code="Not Found",
                message=f"Resource with id {object_id} was not found",
            )

        return json(asdict(Data(object_id=result.doc_id, data=result["data"])))

    async def delete(self, request: Request, object_id: int):
        try:
            _ = data_db.remove(doc_ids=[object_id])
        except KeyError:
            pass
        return "", 204


class DataResourceList(Resource):
    async def get(self, request: Request):
        results = data_db.all()
        return json(
            [
                asdict(Data(object_id=result.doc_id, data=result["data"]))
                for result in results
            ]
        )

    async def post(self, request: Request):
        try:
            body = request.json
            values = [asdict(KeyVal(**value)) for value in body.get("data")]
            object_id = data_db.insert({"data": values})
            return json({"object_id": object_id, "data": values})
        except Exception as e:
            raise BadRequestError(message=str(e))
