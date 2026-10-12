from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        '',
        views.home,
        name='home'
    ),

    # Subjects
    path(
        'subjects/',
        views.subjects,
        name='subjects'
    ),

    path(
        'subjects/<int:subject_id>/',
        views.subject_detail,
        name='subject_detail'
    ),

    path(
        'subjects/<int:subject_id>/units/<int:unit_id>/',
        views.unit_detail,
        name='unit_detail'
    ),

    # Announcements
    path(
        'announcements/',
        views.announcements,
        name='announcements'
    ),

    # Syllabus
    path(
        'syllabus/',
        views.syllabus,
        name='syllabus'
    ),

    # Previous Year Questions
    path(
        'pyqs/',
        views.pyqs,
        name='pyqs'
    ),

    # Notes
    path(
        'notes/',
        views.notes,
        name='notes'
    ),

    # Important Questions
    path(
        'important-questions/',
        views.important_questions,
        name='important_questions'
    ),

    # Search
    path(
        'search/',
        views.search,
        name='search'
    ),

    # About
    path(
        'about/',
        views.about,
        name='about'
    ),
]