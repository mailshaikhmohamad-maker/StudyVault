from django.shortcuts import render, get_object_or_404
from django.db.models import Q

from .models import Subject, Unit, Announcement, Resource


# ================= HOME =================

def home(request):

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    return render(request, 'study/home.html', {
        'announcements': announcements
    })


# ================= SUBJECTS =================

def subjects(request):

    selected_semester = request.GET.get('semester')

    all_subjects = Subject.objects.select_related(
        'semester',
        'semester__department'
    ).all()

    selected_semester_number = None

    if selected_semester:

        try:
            selected_semester_number = int(selected_semester)

            all_subjects = all_subjects.filter(
                semester__number=selected_semester_number
            )

        except ValueError:

            selected_semester_number = None

    return render(request, 'study/subjects.html', {
        'subjects': all_subjects,
        'selected_semester': selected_semester_number
    })


# ================= SUBJECT DETAIL =================

def subject_detail(request, subject_id):

    subject = get_object_or_404(
        Subject.objects.select_related(
            'semester',
            'semester__department'
        ),
        id=subject_id
    )

    units = subject.unit_set.all().order_by(
        'unit_number'
    )

    subject_resources = Resource.objects.filter(
        subject=subject
    ).order_by(
        'resource_type',
        'title'
    )

    return render(request, 'study/subject_detail.html', {
        'subject': subject,
        'units': units,
        'subject_resources': subject_resources
    })


# ================= UNIT DETAIL =================

def unit_detail(request, subject_id, unit_id):

    unit = get_object_or_404(
        Unit.objects.select_related(
            'subject',
            'subject__semester',
            'subject__semester__department'
        ),
        id=unit_id,
        subject_id=subject_id
    )

    resources = unit.resource_set.all().order_by(
        'resource_type',
        'title'
    )

    return render(request, 'study/unit_detail.html', {
        'unit': unit,
        'resources': resources
    })


# ================= ANNOUNCEMENTS =================

def announcements(request):

    all_announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    return render(request, 'study/announcements.html', {
        'announcements': all_announcements
    })


# ================= SYLLABUS =================

def syllabus(request):

    selected_semester = request.GET.get('semester')

    syllabus_resources = Resource.objects.filter(
        resource_type='Syllabus'
    ).select_related(
        'subject',
        'subject__semester',
        'subject__semester__department'
    ).order_by(
        'subject__semester__number',
        'subject__name'
    )

    selected_semester_number = None

    if selected_semester:

        try:

            selected_semester_number = int(selected_semester)

            syllabus_resources = syllabus_resources.filter(
                subject__semester__number=selected_semester_number
            )

        except ValueError:

            selected_semester_number = None

    return render(request, 'study/syllabus.html', {
        'syllabus_resources': syllabus_resources,
        'selected_semester': selected_semester_number
    })


# ================= PYQS =================

def pyqs(request):

    selected_semester = request.GET.get('semester')

    pyq_resources = Resource.objects.filter(
        resource_type='PYQ'
    ).select_related(
        'subject',
        'subject__semester',
        'subject__semester__department'
    ).order_by(
        'subject__semester__number',
        'subject__name',
        'title'
    )

    selected_semester_number = None

    if selected_semester:

        try:

            selected_semester_number = int(selected_semester)

            pyq_resources = pyq_resources.filter(
                subject__semester__number=selected_semester_number
            )

        except ValueError:

            selected_semester_number = None

    return render(request, 'study/pyqs.html', {
        'pyq_resources': pyq_resources,
        'selected_semester': selected_semester_number
    })


# ================= NOTES =================

def notes(request):

    selected_semester = request.GET.get('semester')

    note_resources = Resource.objects.filter(
        resource_type='Notes'
    ).select_related(
        'subject',
        'subject__semester',
        'subject__semester__department'
    ).order_by(
        'subject__semester__number',
        'subject__name',
        'title'
    )

    selected_semester_number = None

    if selected_semester:

        try:

            selected_semester_number = int(selected_semester)

            note_resources = note_resources.filter(
                subject__semester__number=selected_semester_number
            )

        except ValueError:

            selected_semester_number = None

    return render(request, 'study/notes.html', {
        'note_resources': note_resources,
        'selected_semester': selected_semester_number
    })


# ================= IMPORTANT QUESTIONS =================

def important_questions(request):

    important_question_resources = Resource.objects.filter(
        resource_type='Important Questions'
    ).select_related(
        'subject',
        'unit',
        'subject__semester',
        'subject__semester__department',
        'unit__subject'
    ).order_by(
        'subject__semester__number',
        'subject__name',
        'title'
    )

    return render(request, 'study/important_questions.html', {
        'resources': important_question_resources
    })


# ================= SEARCH =================

def search(request):

    query = request.GET.get('q', '').strip()

    subjects_results = Subject.objects.none()
    resource_results = Resource.objects.none()

    if query:

        search_text = query.lower()

        # ================= SUBJECT SEARCH =================

        subjects_results = Subject.objects.filter(

            Q(name__icontains=query) |
            Q(code__icontains=query)

        ).select_related(
            'semester',
            'semester__department'
        ).order_by(
            'semester__number',
            'name'
        )


        # ================= RESOURCE SEARCH =================

        resource_query = (

            Q(title__icontains=query) |

            Q(resource_type__icontains=query) |

            Q(subject__name__icontains=query) |

            Q(subject__code__icontains=query) |

            Q(unit__title__icontains=query)

        )


        # ================= RESOURCE TYPE ALIASES =================

        if search_text in [
            'pyq',
            'pyqs',
            'previous year question',
            'previous year questions',
            'previous year question paper',
            'previous year question papers'
        ]:

            resource_query |= Q(
                resource_type='PYQ'
            )


        if search_text in [
            'note',
            'notes'
        ]:

            resource_query |= Q(
                resource_type='Notes'
            )


        if search_text in [
            'syllabus'
        ]:

            resource_query |= Q(
                resource_type='Syllabus'
            )


        if search_text in [
            'important question',
            'important questions',
            'important question paper',
            'important question papers'
        ]:

            resource_query |= Q(
                resource_type='Important Questions'
            )


        resource_results = Resource.objects.filter(
            resource_query
        ).select_related(
            'subject',
            'unit',
            'subject__semester',
            'subject__semester__department',
            'unit__subject'
        ).order_by(
            'resource_type',
            'title'
        )


    return render(request, 'study/search.html', {
        'query': query,
        'subjects_results': subjects_results,
        'resource_results': resource_results
    })


# ================= ABOUT =================

def about(request):

    return render(request, 'study/about.html')