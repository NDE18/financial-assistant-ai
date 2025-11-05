from pydantic import BaseModel
from typing import Optional

class CategoryBase(BaseModel):
    name: str
    type: str
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryCreate(CategoryBase):
    monthly_budget: Optional[float] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    monthly_budget: Optional[float] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryResponse(CategoryBase):
    id: int
    monthly_budget: Optional[float]

    class Config:
        from_attributes = True
