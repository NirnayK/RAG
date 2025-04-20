import os
from typing import Any, Optional, Type, TypeVar

from fastapi import HTTPException, status
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)


class BaseResponse:
    def __init__(
        self,
        message: Optional[str] = None,
        data: Any = None,
        errors: Any = None,
        model: Type[ModelType] | None = None,
    ):
        self.message = message
        self.errors = errors
        if not self.model:
            self.model = model
        # if a Pydantic model is provided, serialize ORM objects/lists automatically
        if self.model and data is not None:
            self.data = self._serialize(data, model)
        else:
            self.data = data

    def _serialize(self, data: Any, model: Type[ModelType]) -> Any:
        # Pydantic v2
        if isinstance(data, list):
            return [model.model_validate(obj).model_dump() for obj in data]
        return model.model_validate(data).model_dump()

    def dict(self) -> dict:
        payload: dict = {"message": self.message}
        if self.data is not None:
            payload["data"] = self.data
        if self.errors is not None:
            payload["errors"] = self.errors
        return payload

    @classmethod
    def ok(
        cls,
        data: Any = None,
        message: str = "Success",
        model: Type[ModelType] | None = None,
    ) -> JSONResponse:
        inst = cls(message, data, None, model)
        return JSONResponse(status_code=status.HTTP_200_OK, content=inst.dict())

    @classmethod
    def created(
        cls,
        data: Any = None,
        message: str = "Created",
        model: Type[ModelType] | None = None,
    ) -> JSONResponse:
        inst = cls(message, data, None, model)
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=inst.dict())

    @classmethod
    def bad_request(
        cls,
        errors: Any = None,
        message: str = "Bad Request",
    ) -> JSONResponse:
        inst = cls(message, None, errors)
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=inst.dict())

    @classmethod
    def unauthorized(cls, message: str = "Unauthorized") -> None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=message)

    @classmethod
    def forbidden(cls, message: str = "Forbidden") -> None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=message)

    @classmethod
    def not_found(cls, message: str = "Not Found") -> None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    @classmethod
    def internal_error(
        cls,
        message: str = "Internal Server Error",
        errors: Any = None,
    ) -> JSONResponse:
        inst = cls(message, None, errors)
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=inst.dict())

    @classmethod
    def file(
        cls,
        path: str,
        filename: str | None = None,
        media_type: str | None = None,
    ) -> FileResponse:
        """
        Returns a FileResponse for downloads.
        """
        return FileResponse(
            path=path,
            filename=filename or os.path.basename(path),
            media_type=media_type,
        )
        )
