from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas import UserCreate, User, Token, Role
from database import get_db
from auth import hash_password, create_access_token, verify_password
from models import User as UserModel, Role as RoleModel

from user_role import get_current_user, role_required

router = APIRouter()

# User registration
@router.post("/roleauth/register", response_model=User )
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    db_user = UserModel(username=user.username, hashed_password=hashed_password, role_id=user.role_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# User login
@router.post("/roleauth/login", response_model=Token)
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Get all roles
@router.get("/roleauth/roles", response_model=list[Role], dependencies=[Depends(role_required("owner"))])
def get_roles(db: Session = Depends(get_db)):
    return db.query(RoleModel).all()

# Admin-only route
@router.get("/roleauth/admin", dependencies=[Depends(role_required("admin"))])
def read_admin_data():
    return {"message": "Welcome, Admin!"}

# Owner-only route
@router.get("/roleauth/owner", dependencies=[Depends(role_required("owner"))])
def read_owner_data():
    return {"message": "Welcome, Owner!"}

# User group 1 route
@router.get("/roleauth/user-group-1", dependencies=[Depends(role_required("user group 1"))])
def read_user_group_1_data():
    return {"message": "Welcome, User Group 1!"}

# User group 2 route
@router.get("/roleauth/user-group-2", dependencies=[Depends(role_required("user group 2"))])
def read_user_group_2_data():
    return {"message": "Welcome, User Group 2!"}
