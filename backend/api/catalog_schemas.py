from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CategoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    description: str


class InstructorOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    bio: str
    photo: str | None = None


class CourseListItem(BaseModel):
    id: int
    title: str
    description: str
    price: Decimal
    image: str | None = None
    category: CategoryOut
    instructor: InstructorOut
    is_enrolled: bool = False


class CourseDetail(CourseListItem):
    created_at: datetime


class CourseListResponse(BaseModel):
    items: list[CourseListItem]
    total: int
    page: int
    page_size: int


class EnrollmentOut(BaseModel):
    id: int
    course_id: int
    course_title: str
    enrolled_at: datetime


class EnrollmentResponse(BaseModel):
    enrollment: EnrollmentOut
    already_enrolled: bool = False


class EnrollmentRequest(BaseModel):
    course_id: int = Field(gt=0)
