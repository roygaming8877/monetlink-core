from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_async_db
from app.core.security import verify_password, create_access_token
from app.crud.crud_user import user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_new_publisher(payload: UserCreate, db: AsyncSession = Depends(get_async_db)):
    """Registers a new user and automatically credits the $1.00 base sign-up bonus."""
    existing_user = await user.get_by_email(db, email=payload.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Account with this email already exists."
        )
    
    # 1.0 represents the default bonus payout configured in specs
    new_user = await user.create_with_bonus(db, obj_in=payload, bonus_amount=1.0)
    return new_user

@router.post("/login")
async def login_access_token(
    db: AsyncSession = Depends(get_async_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """OAuth2 compatible token login, getting an access token for future requests."""
    db_user = await user.get_by_email(db, email=form_data.username)
    if not db_user or not verify_password(form_data.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if db_user.is_banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Account suspended.")

    access_token = create_access_token(subject=db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}
  
