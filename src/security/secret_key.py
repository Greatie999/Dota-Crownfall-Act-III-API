from fastapi.security import APIKeyHeader

secret_key_scheme = APIKeyHeader(
    name="X-Secret-Key",
    auto_error=False
)
