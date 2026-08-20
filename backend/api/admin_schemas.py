from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryAdminIn(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    description: str = Field(default='', max_length=2000)


class CategoryAdminOut(CategoryAdminIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime


class InstructorAdminIn(BaseModel):
    name: str = Field(min_length=2, max_length=160)
    bio: str = Field(default='', max_length=5000)


class InstructorAdminOut(InstructorAdminIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    photo: str | None = None
    created_at: datetime


class CourseAdminIn(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=10)
    category_id: int = Field(gt=0)
    instructor_id: int = Field(gt=0)
    price: Decimal = Field(ge=0, max_digits=10, decimal_places=2)
    image: str | None = None
    is_published: bool = True


class CourseAdminOut(CourseAdminIn):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
    updated_at: datetime


class EnrollmentAdminOut(BaseModel):
    id: int
    learner_id: int
    learner_email: str
    course_id: int
    course_title: str
    enrolled_at: datetime

    model_config = ConfigDict(from_attributes=True)
