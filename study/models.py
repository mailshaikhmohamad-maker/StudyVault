from django.db import models
from django.core.exceptions import ValidationError


class Department(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Semester(models.Model):

    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"Semester {self.number} - {self.department.name}"


class Subject(models.Model):

    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Unit(models.Model):

    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    unit_number = models.IntegerField()
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Unit {self.unit_number} - {self.title}"


class Resource(models.Model):

    RESOURCE_TYPES = [
        ('Notes', 'Notes'),
        ('Syllabus', 'Syllabus'),
        ('PYQ', 'Previous Year Paper'),
        ('Important Questions', 'Important Questions'),
        ('Reference', 'Reference Material'),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    unit = models.ForeignKey(
        Unit,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    title = models.CharField(max_length=200)

    resource_type = models.CharField(
        max_length=50,
        choices=RESOURCE_TYPES
    )

    file = models.FileField(upload_to='resources/')

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def clean(self):

        if not self.subject and not self.unit:
            raise ValidationError(
                'Resource must be connected to a subject or a unit.'
            )

        if self.subject and self.unit:
            raise ValidationError(
                'Resource cannot be connected to both subject and unit.'
            )

    def __str__(self):
        return self.title


class Announcement(models.Model):

    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title