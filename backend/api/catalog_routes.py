from fastapi import APIRouter, Depends, HTTPException, Query, status
from django.db import IntegrityError

from .auth_security import current_user
from .catalog_schemas import (
    CourseDetail,
    CourseListItem,
    CourseListResponse,
    EnrollmentOut,
    EnrollmentRequest,
    EnrollmentResponse,
    InstructorOut,
)
from core.models import Course, Enrollment, User

router = APIRouter(prefix="/api/v1", tags=["catalog"])


def media_url(value):
    return value.url if value else None


def course_item(course, enrolled=False):
    return CourseListItem(
        id=course.id,
        title=course.title,
        description=course.description,
        price=course.price,
        image=media_url(course.image),
        category=course.category,
        instructor=InstructorOut(
            id=course.instructor.id,
            name=course.instructor.name,
            bio=course.instructor.bio,
            photo=media_url(course.instructor.photo),
        ),
        is_enrolled=enrolled,
    )


@router.get("/courses", response_model=CourseListResponse)
def list_courses(
    q: str | None = Query(default=None, max_length=120),
    category: str | None = Query(default=None, max_length=120),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=12, ge=1, le=50),
):
    courses = Course.objects.filter(is_published=True).select_related("category", "instructor")
    if q:
        from django.db.models import Q
        courses = courses.filter(Q(title__icontains=q) | Q(description__icontains=q))
    if category:
        courses = courses.filter(category__name__iexact=category)
    total = courses.count()
    start = (page - 1) * page_size
    items = [course_item(course) for course in courses[start : start + page_size]]
    return CourseListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/courses/{course_id}", response_model=CourseDetail)
def get_course(course_id: int):
    try:
        course = Course.objects.select_related("category", "instructor").get(id=course_id, is_published=True)
    except Course.DoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc
    return CourseDetail(**course_item(course).model_dump(), created_at=course.created_at)


@router.post("/enrollments", response_model=EnrollmentResponse, status_code=status.HTTP_201_CREATED)
def enroll(request: EnrollmentRequest, user: User = Depends(current_user)):
    if user.role != User.Role.LEARNER:
        raise HTTPException(status_code=403, detail="Learner role required")
    try:
        course = Course.objects.get(id=request.course_id, is_published=True)
    except Course.DoesNotExist as exc:
        raise HTTPException(status_code=404, detail="Course not found") from exc
    enrollment, created = Enrollment.objects.get_or_create(learner=user, course=course)
    result = EnrollmentOut(id=enrollment.id, course_id=course.id, course_title=course.title, enrolled_at=enrollment.created_at)
    return EnrollmentResponse(enrollment=result, already_enrolled=not created)


@router.get("/me/enrollments", response_model=list[EnrollmentOut])
def my_enrollments(user: User = Depends(current_user)):
    if user.role != User.Role.LEARNER:
        raise HTTPException(status_code=403, detail="Learner role required")
    return [EnrollmentOut(id=e.id, course_id=e.course_id, course_title=e.course.title, enrolled_at=e.created_at) for e in Enrollment.objects.filter(learner=user).select_related("course")]
