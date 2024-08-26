from fastapi import Query


class QueryParams:
    def __init__(
        self,
        page: int = Query(1, ge=1, alias="page"),
        limit: int = Query(100, ge=1, le=1000, alias="limit")
    ):
        self.page = page
        self.limit = limit
        self.offset = (page - 1) * limit
