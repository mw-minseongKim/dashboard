from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from dashboard.auth import dependencies, service
from dashboard.auth.models import TokenResponse, User, UserCreate, UserLogin, UserRead
from dashboard.auth.utils import create_access_token, verify_password
from dashboard.database import get_session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user account with the provided credentials. Returns the created user profile.",
)
async def signup(user_in: UserCreate, session: AsyncSession = Depends(get_session)):
    user = await service.get_user_by_email(email=user_in.email, session=session)
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="The email already exists"
        )
    user = await service.create_user(user_in=user_in, session=session)
    return user


@router.post(
    "/signin",
    response_model=TokenResponse,
    summary="Sign in",
    description="Authenticates a user with email and password.",
)
async def signin(user_in: UserLogin, session: AsyncSession = Depends(get_session)):
    user = await service.get_user_by_email(email=user_in.email, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    if not verify_password(user_in.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password"
        )

    return TokenResponse(
        access_token=create_access_token(subject=str(user.id)),
        token_type="bearer",
    )


@router.get("/me", response_model=UserRead)
async def me(current_user: User = Depends(dependencies.get_current_user)):
    return current_user
