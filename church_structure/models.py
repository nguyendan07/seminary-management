from django.db import models
from django.urls import reverse

class Diocese(models.Model):
    """Giáo phận"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Tên giáo phận')
    code = models.CharField(max_length=10, unique=True, verbose_name='Mã giáo phận')
    bishop = models.CharField(max_length=100, blank=True, verbose_name='Giám mục')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Điện thoại')
    email = models.EmailField(blank=True, verbose_name='Email')
    website = models.URLField(blank=True, verbose_name='Website')
    
    patron_saint = models.CharField(max_length=100, blank=True, verbose_name='Thánh bảo trợ')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Giáo phận'
        verbose_name_plural = 'Giáo phận'
        ordering = ['name']
        
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('church_structure:diocese_detail', kwargs={'pk': self.pk})
    
    @property
    def parish_count(self):
        return self.parishes.count()
    
    @property 
    def student_count(self):
        """Tính số chủng sinh từ giáo phận này"""
        return sum(parish.student_count for parish in self.parishes.all())

class Parish(models.Model):
    """Giáo xứ"""
    name = models.CharField(max_length=100, verbose_name='Tên giáo xứ')
    code = models.CharField(max_length=20, verbose_name='Mã giáo xứ')
    diocese = models.ForeignKey(Diocese, on_delete=models.CASCADE, 
                               related_name='parishes', verbose_name='Giáo phận')
    pastor = models.CharField(max_length=100, blank=True, verbose_name='Linh mục quản xứ')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Điện thoại')
    email = models.EmailField(blank=True, verbose_name='Email')
    
    patron_saint = models.CharField(max_length=100, blank=True, verbose_name='Thánh bảo trợ')
    established_date = models.DateField(null=True, blank=True, verbose_name='Ngày thành lập')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Giáo xứ'
        verbose_name_plural = 'Giáo xứ'
        unique_together = ['name', 'diocese']
        ordering = ['diocese', 'name']
        
    def __str__(self):
        return f"{self.name} ({self.diocese.name})"
    
    def get_absolute_url(self):
        return reverse('church_structure:parish_detail', kwargs={'pk': self.pk})
    
    @property
    def community_count(self):
        return self.communities.count()
    
    @property
    def student_count(self):
        """Tính số chủng sinh từ giáo xứ này"""
        return self.students.count()

class Community(models.Model):
    """Giáo họ"""
    name = models.CharField(max_length=100, verbose_name='Tên giáo họ')
    parish = models.ForeignKey(Parish, on_delete=models.CASCADE, 
                              related_name='communities', verbose_name='Giáo xứ')
    leader = models.CharField(max_length=100, blank=True, verbose_name='Trưởng giáo họ')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Điện thoại')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Giáo họ'
        verbose_name_plural = 'Giáo họ'
        unique_together = ['name', 'parish']
        ordering = ['parish', 'name']
        
    def __str__(self):
        return f"{self.name} - {self.parish.name}"
    
    def get_absolute_url(self):
        return reverse('church_structure:community_detail', kwargs={'pk': self.pk})
    
    @property
    def student_count(self):
        """Tính số chủng sinh từ giáo họ này"""
        return self.students.count()
