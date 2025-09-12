from django.db import models
from django.contrib.auth import get_user_model

from church_structure.models import Parish, Community

User = get_user_model()


class Student(models.Model):
    YEAR_CHOICES = [
        (1, 'Năm thứ nhất'),
        (2, 'Năm thứ hai'),
        (3, 'Năm thứ ba'),
        (4, 'Năm thứ tư'),
        (5, 'Năm thứ năm'),
        (6, 'Năm thứ sáu'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Đang học'),
        ('suspended', 'Tạm dừng'),
        ('graduated', 'Đã tốt nghiệp'),
        ('dropped', 'Đã thôi học'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    entry_year = models.IntegerField(verbose_name='Năm nhập học')
    current_year = models.IntegerField(choices=YEAR_CHOICES, verbose_name='Năm hiện tại')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name='Trạng thái')

    # Personal Information
    hometown = models.TextField(blank=True, verbose_name='Quê quán')

    # Spiritual Information
    baptism_name = models.CharField(max_length=100, blank=True, verbose_name='Tên thánh')
    baptism_date = models.DateField(null=True, blank=True, verbose_name='Ngày Rửa Tội')
    confirmation_date = models.DateField(null=True, blank=True, verbose_name='Ngày Thêm Sức')
    parish = models.ForeignKey(Parish, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Giáo xứ')
    community = models.ForeignKey(Community, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Giáo họ')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Chủng sinh'
        verbose_name_plural = 'Chủng sinh'

    def __str__(self):
        return f"{self.user.username} - {self.user.get_full_name()}"


class StudentNote(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    note_type = models.CharField(max_length=50, choices=[
        ('academic', 'Học tập'),
        ('behavior', 'Hạnh kiểm'),
        ('spiritual', 'Tâm linh'),
        ('health', 'Sức khỏe'),
        ('general', 'Chung'),
    ])
    title = models.CharField(max_length=200)
    content = models.TextField()
    is_private = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()}"
