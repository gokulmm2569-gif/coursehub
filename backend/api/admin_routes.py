from fastapi import APIRouter, Depends, HTTPException, Query, status

from core.models import Category, Course, Enrollment, Instructor

from .admin_schemas import (
    CategoryAdminIn,
    CategoryAdminOut,
    CourseAdminIn,
    CourseAdminOut,
    EnrollmentAdminOut,
    InstructorAdminIn,
    InstructorAdminOut,
)
from .auth_security import require_admin

router = APIRouter(prefix='/api/v1/admin', tags=['admin'])


def category_or_404(category_id: int):
    try:
        return Category.objects.get(id=category_id)
    except Category.DoesNotExist as exc:
        raise HTTPException(status_code=404, detail='Category not found') from exc


def instructor_or_404(instructor_id: int):
    try:
        return Instructor.objects.get(id=instructor_id)
    except Instructor.DoesNotExist as exc:
        raise HTTPException(status_code=404, detail='Instructor not found') from exc


def course_or_404(course_id: int):
    try:
        return Course.objects.get(id=course_id)
    except Course.DoesNotExist as exc:
        raise HTTPException(status_code=404, detail='Course not found') from exc


@router.post('/categories', response_model=CategoryAdminOut, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryAdminIn, _admin=Depends(require_admin)):
    category, created = Category.objects.get_or_create(name=payload.name, defaults={'description': payload.description})
    if not created:
        raise HTTPException(status_code=409, detail='Category already exists')
    return category


@router.get('/categories', response_model=list[CategoryAdminOut])
def list_categories(_admin=Depends(require_admin)):
    return Category.objects.all().order_by('name')


@router.post('/instructors', response_model=InstructorAdminOut, status_code=status.HTTP_201_CREATED)
def create_instructor(payload: InstructorAdminIn, _admin=Depends(require_admin)):
    return Instructor.objects.create(name=payload.name, bio=payload.bio)


@router.get('/instructors', response_model=list[InstructorAdminOut])
def list_instructors(_admin=Depends(require_admin)):
    return Instructor.objects.all().order_by('name')


@router.post('/courses', response_model=CourseAdminOut, status_code=status.HTTP_201_CREATED)
def create_course(payload: CourseAdminIn, _admin=Depends(require_admin)):
    category = category_or_404(payload.category_id)
    instructor = instructor_or_404(payload.instructor_id)
    return Course.objects.create(
        title=payload.title,
        description=payload.description,
        category=category,
        instructor=instructor,
        price=payload.price,
        is_published=payload.is_published,
    )


@router.patch('/courses/{course_id}', response_model=CourseAdminOut)
def update_course(course_id: int, payload: CourseAdminIn, _admin=Depends(require_admin)):
    course = course_or_404(course_id)
    course.category = category_or_404(payload.category_id)
    course.instructor = instructor_or_404(payload.instructor_id)
    for field in ('title', 'description', 'price', 'is_published'):
        setattr(course, field, getattr(payload, field))
    course.save()
    return course


@router.delete('/courses/{course_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_course(course_id: int, _admin=Depends(require_admin)):
    course = course_or_404(course_id)
    course.delete()


@router.get('/enrollments', response_model=list[EnrollmentAdminOut])
def list_enrollments(
    course_id: int | None = Query(default=None, gt=0),
    _admin=Depends(require_admin),
):
    enrollments = Enrollment.objects.select_related('learner', 'course').all()
    if course_id:
        enrollments = enrollments.filter(course_id=course_id)
    return [
        EnrollmentAdminOut(
            id=enrollment.id,
            learner_id=enrollment.learner_id,
            learner_email=enrollment.learner.email,
            course_id=enrollment.course_id,
            course_title=enrollment.course.title,
            enrolled_at=enrollment.created_at,
        )
        for enrollment in enrollments
    ]
