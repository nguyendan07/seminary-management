from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Teacher(models.Model):
    POSITION_CHOICES = [
        ('rector', 'Rector'),
        ('vice_rector', 'Vice Rector'),
        ('spiritual_director', 'Spiritual Director'),
        ('professor', 'Professor'),
        ('lecturer', 'Lecturer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True, verbose_name='Teacher ID')
    hire_date = models.DateField(verbose_name='Hire Date')
    position = models.CharField(max_length=50, choices=POSITION_CHOICES, verbose_name='Position')

    # Educational Background and Experience
    education_background = models.TextField(blank=True, verbose_name='Educational Background')
    specialization = models.CharField(max_length=200, blank=True, verbose_name='Specialization')
    experience = models.TextField(blank=True, verbose_name='Work Experience')

    # Contact Information and Assignment
    office_room = models.CharField(max_length=50, blank=True, verbose_name='Office Room')
    consultation_hours = models.TextField(blank=True, verbose_name='Consultation Hours')

    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.get_position_display()})"
