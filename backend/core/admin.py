from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Category, Course, Enrollment, Instructor, User

@admin.register(User)
class CourseHubUserAdmin(UserAdmin):
    ordering = ('email',)
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('role', 'is_active', 'is_staff')
    fieldsets = ((None, {'fields': ('email', 'password')}), ('Profile', {'fields': ('first_name', 'last_name', 'role')}), ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}))
    add_fieldsets = ((None, {'classes': ('wide',), 'fields': ('email', 'password1', 'password2', 'role', 'is_staff')}),)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'description')

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name', 'bio')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'instructor', 'price', 'is_published', 'created_at')
    list_filter = ('is_published', 'category', 'instructor')
    search_fields = ('title', 'description')
    autocomplete_fields = ('category', 'instructor')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('learner', 'course', 'created_at')
    search_fields = ('learner__email', 'course__title')
    list_filter = ('course',)
    readonly_fields = ('created_at',)
