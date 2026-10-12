from django.contrib import admin
from .models import (
    Department,
    Semester,
    Subject,
    Unit,
    Resource,
    Announcement
)


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ('id', 'department', 'number')
    list_filter = ('department', 'number')
    search_fields = ('department__name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'semester')
    list_filter = ('semester',)
    search_fields = ('name', 'code')


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display = ('id', 'unit_number', 'title', 'subject')
    list_filter = ('subject',)
    search_fields = ('title', 'subject__name')


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'title',
        'resource_type',
        'subject',
        'unit',
        'uploaded_at'
    )

    list_filter = (
        'resource_type',
        'subject',
        'unit__subject'
    )

    search_fields = (
        'title',
        'subject__name',
        'unit__title',
        'unit__subject__name'
    )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at')
    search_fields = ('title', 'message')
    ordering = ('-created_at',)