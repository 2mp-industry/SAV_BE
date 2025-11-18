from sqlalchemy.orm import Session
import uuid
from db.database import get_db
from models import user as user_model  
from schemas import user as user_schema  
from fastapi import APIRouter, Depends, HTTPException, status, Path
from sqlalchemy.exc import IntegrityError
from core.security import get_password_hash
from core.logger import app_logger  # NEW: Import logger

router = APIRouter(prefix="/Users", tags=["Users"])
logger = app_logger

@router.get("/{user_id}", response_model=user_schema.UserResponse)
def get_user(
    user_id: str = Path(..., description="The user ID (UUID)"),
    db: Session = Depends(get_db)
):
    logger.info(f"Fetching user", extra={"user_id": user_id, "operation": "get_user"})
    
    try:
        user_uuid = uuid.UUID(user_id)
    except ValueError:
        logger.warning(f"Invalid UUID format", extra={"user_id": user_id})
        raise HTTPException(
            status_code=422,
            detail="Invalid UUID format. User ID must be a valid GUID."
        )
    
    try:
        db_user = db.query(user_model.User).filter(user_model.User.id == user_uuid).first() 
        
        if not db_user:
            logger.warning(f"User not found", extra={"user_id": user_id})
            raise HTTPException(status_code=404, detail="User not found")
        
        logger.info(f"User retrieved successfully", extra={"user_id": user_id, "user_email": db_user.email})
        return db_user
        
    except Exception as e:
        logger.error(f"Error fetching user", extra={"user_id": user_id, "error": str(e)}, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")

@router.post("/Create", response_model=user_schema.UserResponse, status_code=status.HTTP_201_CREATED)  
def create_user(user_data: user_schema.UserCreate, db: Session = Depends(get_db)):  
    logger.info(
        f"Creating new user", 
        extra={
            "operation": "create_user", 
            "user_email": user_data.email,
            "user_role": user_data.role
        }
    )
    
    try:
        # Vérifier si l'email existe déjà
        existing_user = db.query(user_model.User).filter(user_model.User.email == user_data.email).first() 
        if existing_user:
            logger.warning(
                f"Email already registered", 
                extra={"user_email": user_data.email}
            )
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hasher le mot de passe
        hashed_password = get_password_hash(user_data.password)
        
        # Créer l'utilisateur
        db_user = user_model.User( 
            email=user_data.email,
            password_hash=hashed_password,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            role=user_data.role
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        logger.info(
            f"User created successfully", 
            extra={
                "user_id": str(db_user.id),
                "user_email": db_user.email,
                "user_role": db_user.role
            }
        )
        
        return db_user
        
    except IntegrityError as e:
        db.rollback()
        logger.error(
            f"Database integrity error creating user", 
            extra={"user_email": user_data.email, "error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Error creating user - database constraint violation"
        )
        
    except Exception as e:
        db.rollback()
        logger.error(
            f"Unexpected error creating user", 
            extra={"user_email": user_data.email, "error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )