# backend\core\security.py
from jose import jwt, ExpiredSignatureError, JWTError
from datetime import datetime, timedelta
from typing import Any, Union, Optional

from passlib.context import CryptContext

from core.config import settings

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")



ALGORITHM = settings.ALGORITHM



def create_access_token(

    subject: Union[str, Any], expires_delta: timedelta = None

) -> str:

    if expires_delta:

        expire = datetime.utcnow() + expires_delta

    else:

        expire = datetime.utcnow() + timedelta(

            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES

        )

    to_encode = {"exp": expire, "sub": str(subject)}

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=ALGORITHM)

    return encoded_jwt



def verify_password(plain_password: str, hashed_password: str) -> bool:

    return pwd_context.verify(plain_password, hashed_password)



def get_password_hash(password: str) -> str:

    return pwd_context.hash(password)



def decode_token(token: str) -> Optional[str]:

    """

    Decodes the access token.



    :param token: The encoded access token.

    :return: The user ID (subject) from the token payload if valid, otherwise None.

    """

    try:

        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[ALGORITHM])

        user_id = payload.get("sub")

        if user_id is None:

            return None

        return user_id

    except ExpiredSignatureError:

        # Token has expired

        return None

    except JWTError:

        # Any other JWT error

        return None