
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from datetime import timedelta, datetime, timezone
import secrets

class JWTBearer(HTTPBearer):
    async def __call__(self, request: Request):
        return ""
    

authenticator = JWTBearer()