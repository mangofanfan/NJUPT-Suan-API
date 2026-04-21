from pathlib import Path
from typing import Annotated

import aiofiles
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

security = HTTPBearer()


async def verify_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]) -> str:
    token = credentials.credentials

    async with aiofiles.open(file=Path.cwd() / "data" / "token.txt", mode="r") as f:
        if (await f.readline()).strip() == token:
            return token
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing token. (Suan API WebUI)",
            headers={"WWW-Authenticate": "Bearer"},
        )
