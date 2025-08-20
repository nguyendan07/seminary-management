from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator

from students.models import Student
from teachers.models import Teacher

User = get_user_model()


class AcademicYear(models.Model):
    """Năm học"""

    name = models.CharField(
        max_length=20, unique=True, verbose_name="Năm học"
    )  # VD: "2024-2025"
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    is_current = models.BooleanField(default=False, verbose_name="Năm học hiện tại")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Năm học"
        verbose_name_plural = "Năm học"
        ordering = ["-name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            # Chỉ có một năm học hiện tại
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
        super().save(*args, **kwargs)


class Subject(models.Model):
    CATEGORY_CHOICES = [
        ("theology", "Thần học"),
        ("philosophy", "Triết học"),
        ("scripture", "Kinh thánh"),
        ("liturgy", "Phụng vụ"),
        ("canon_law", "Luật tắc"),
        ("pastoral", "Mục vụ"),
        ("church_history", "Lịch sử Giáo hội"),
        ("moral_theology", "Luân lý thần học"),
        ("spirituality", "Tâm linh học"),
        ("catechetics", "Giáo lý học"),
        ("languages", "Ngoại ngữ"),
        ("general", "Giáo dục chung"),
    ]

    LEVEL_CHOICES = [
        ("basic", "Cơ bản"),
        ("intermediate", "Trung cấp"),
        ("advanced", "Nâng cao"),
        ("specialized", "Chuyên sâu"),
    ]

    code = models.CharField(max_length=20, unique=True, verbose_name="Mã môn học")
    name = models.CharField(max_length=200, verbose_name="Tên môn học")
    english_name = models.CharField(
        max_length=200, blank=True, verbose_name="Tên tiếng Anh"
    )
    category = models.CharField(
        max_length=50, choices=CATEGORY_CHOICES, verbose_name="Loại môn học"
    )
    level = models.CharField(
        max_length=20, choices=LEVEL_CHOICES, default="basic", verbose_name="Trình độ"
    )

    credits = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Số tín chỉ",
    )
    theory_hours = models.IntegerField(default=0, verbose_name="Giờ lý thuyết")
    practice_hours = models.IntegerField(default=0, verbose_name="Giờ thực hành")

    description = models.TextField(blank=True, verbose_name="Mô tả")
    learning_objectives = models.TextField(blank=True, verbose_name="Mục tiêu học tập")
    prerequisites = models.ManyToManyField(
        "self", blank=True, symmetrical=False, verbose_name="Môn tiên quyết"
    )

    # Thông tin bổ sung
    is_required = models.BooleanField(default=True, verbose_name="Môn bắt buộc")
    year_taught = models.IntegerField(
        choices=Student.YEAR_CHOICES, null=True, blank=True, verbose_name="Năm học dạy"
    )

    is_active = models.BooleanField(default=True, verbose_name="Còn giảng dạy")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Môn học"
        verbose_name_plural = "Môn học"
        ordering = ["category", "year_taught", "name"]

    def __str__(self):
        return f"{self.code} - {self.name}"

    def get_absolute_url(self):
        return reverse("courses:subject_detail", kwargs={"pk": self.pk})

    @property
    def total_hours(self):
        return self.theory_hours + self.practice_hours

    @property
    def current_courses_count(self):
        """Số lớp học hiện tại của môn này"""
        return self.courses.filter(is_active=True).count()


class Course(models.Model):
    SEMESTER_CHOICES = [
        ("fall", "Học kỳ I"),
        ("spring", "Học kỳ II"),
        ("summer", "Học kỳ hè"),
    ]

    STATUS_CHOICES = [
        ("planning", "Đang lập kế hoạch"),
        ("open_registration", "Mở đăng ký"),
        ("in_progress", "Đang diễn ra"),
        ("completed", "Đã hoàn thành"),
        ("cancelled", "Đã hủy"),
    ]

    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name="courses",
        verbose_name="Môn học",
    )
    instructor = models.ForeignKey(
        Teacher,
        on_delete=models.CASCADE,
        related_name="taught_courses",
        verbose_name="Giảng viên",
    )
    academic_year = models.ForeignKey(
        AcademicYear, on_delete=models.CASCADE, verbose_name="Năm học"
    )
    semester = models.CharField(
        max_length=20, choices=SEMESTER_CHOICES, verbose_name="Học kỳ"
    )

    # Thông tin lớp học
    class_code = models.CharField(
        max_length=20, verbose_name="Mã lớp"
    )  # VD: "TH101-01"
    max_students = models.IntegerField(
        default=30,
        validators=[MinValueValidator(1)],
        verbose_name="Số sinh viên tối đa",
    )

    # Lịch học
    schedule = models.JSONField(
        default=list, blank=True, verbose_name="Lịch học"
    )  # [{"day": "monday", "start": "08:00", "end": "09:30", "room": "A101"}]
    classroom = models.CharField(
        max_length=50, blank=True, verbose_name="Phòng học chính"
    )

    # Thời gian
    start_date = models.DateField(verbose_name="Ngày bắt đầu")
    end_date = models.DateField(verbose_name="Ngày kết thúc")
    registration_start = models.DateTimeField(
        null=True, blank=True, verbose_name="Bắt đầu đăng ký"
    )
    registration_end = models.DateTimeField(
        null=True, blank=True, verbose_name="Hết hạn đăng ký"
    )

    # Trạng thái và ghi chú
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="planning",
        verbose_name="Trạng thái",
    )
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    # Yêu cầu và đánh giá
    attendance_required = models.BooleanField(
        default=True, verbose_name="Bắt buộc điểm danh"
    )
    midterm_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=30.00,
        verbose_name="Trọng số giữa kỳ (%)",
    )
    final_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=50.00,
        verbose_name="Trọng số cuối kỳ (%)",
    )
    assignment_weight = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=20.00,
        verbose_name="Trọng số bài tập (%)",
    )

    is_active = models.BooleanField(default=True, verbose_name="Đang mở")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
        unique_together = ["subject", "academic_year", "semester", "class_code"]
        ordering = ["-academic_year", "semester", "subject__name"]

    def __str__(self):
        return f"{self.subject.name} - {self.class_code} ({self.academic_year.name})"

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"pk": self.pk})

    @property
    def enrolled_count(self):
        """Số sinh viên đã đăng ký"""
        return self.enrollments.filter(status="enrolled").count()

    @property
    def available_slots(self):
        """Số chỗ còn lại"""
        return self.max_students - self.enrolled_count

    @property
    def is_full(self):
        """Kiểm tra lớp đã đầy chưa"""
        return self.enrolled_count >= self.max_students

    @property
    def completion_rate(self):
        """Tỷ lệ hoàn thành"""
        total = self.enrollments.count()
        if total == 0:
            return 0
        completed = self.enrollments.filter(status="completed").count()
        return (completed / total) * 100


class Enrollment(models.Model):
    STATUS_CHOICES = [
        ("enrolled", "Đang học"),
        ("completed", "Hoàn thành"),
        ("failed", "Không đạt"),
        ("withdrawn", "Rút môn"),
        ("suspended", "Tạm dừng"),
    ]

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Chủng sinh",
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="enrollments",
        verbose_name="Lớp học",
    )
    enrollment_date = models.DateTimeField(
        auto_now_add=True, verbose_name="Ngày đăng ký"
    )

    # Điểm số chi tiết
    assignment_scores = models.JSONField(
        default=list, blank=True, verbose_name="Điểm bài tập"
    )  # [{"name": "BT1", "score": 8.5, "max": 10}]
    midterm_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Điểm giữa kỳ",
    )
    final_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Điểm cuối kỳ",
    )
    overall_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Điểm tổng kết",
    )
    letter_grade = models.CharField(
        max_length=5, blank=True, verbose_name="Điểm chữ"
    )  # A, B+, B, C+, C, D, F

    # Đánh giá thêm
    attendance_count = models.IntegerField(default=0, verbose_name="Số buổi có mặt")
    total_sessions = models.IntegerField(default=0, verbose_name="Tổng số buổi học")
    participation_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Điểm tham gia",
    )

    # Trạng thái và ghi chú
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="enrolled",
        verbose_name="Trạng thái",
    )
    withdrawal_reason = models.TextField(blank=True, verbose_name="Lý do rút môn")
    instructor_notes = models.TextField(
        blank=True, verbose_name="Ghi chú của giảng viên"
    )

    # Thời gian
    completion_date = models.DateField(
        null=True, blank=True, verbose_name="Ngày hoàn thành"
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ["student", "course"]
        verbose_name = "Đăng ký học"
        verbose_name_plural = "Đăng ký học"
        ordering = ["-enrollment_date"]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.subject.name}"

    def save(self, *args, **kwargs):
        # Tự động tính điểm tổng kết
        if self.midterm_score is not None and self.final_score is not None:
            course = self.course
            assignment_avg = self.get_assignment_average()

            self.overall_score = (
                (self.midterm_score * course.midterm_weight / 100)
                + (self.final_score * course.final_weight / 100)
                + (assignment_avg * course.assignment_weight / 100)
            )

            # Tính điểm chữ
            self.letter_grade = self.calculate_letter_grade()

        super().save(*args, **kwargs)

    def get_assignment_average(self):
        """Tính điểm trung bình bài tập"""
        if not self.assignment_scores:
            return 0

        total_score = sum(
            score["score"] for score in self.assignment_scores if "score" in score
        )
        total_max = sum(
            score["max"] for score in self.assignment_scores if "max" in score
        )

        if total_max == 0:
            return 0

        return (total_score / total_max) * 10  # Chuẩn hóa về thang điểm 10

    def calculate_letter_grade(self):
        """Tính điểm chữ dựa trên điểm tổng kết"""
        if self.overall_score is None:
            return ""

        score = float(self.overall_score)
        if score >= 9.0:
            return "A"
        elif score >= 8.5:
            return "B+"
        elif score >= 8.0:
            return "B"
        elif score >= 7.0:
            return "C+"
        elif score >= 6.0:
            return "C"
        elif score >= 5.0:
            return "D"
        else:
            return "F"

    @property
    def attendance_rate(self):
        """Tỷ lệ chuyên cần"""
        if self.total_sessions == 0:
            return 0
        return (self.attendance_count / self.total_sessions) * 100

    @property
    def is_passing(self):
        """Kiểm tra có đạt môn không"""
        return self.overall_score is not None and self.overall_score >= 5.0


class Assignment(models.Model):
    """Bài tập/Đề tài cho từng lớp học"""

    TYPE_CHOICES = [
        ("homework", "Bài tập về nhà"),
        ("essay", "Tiểu luận"),
        ("presentation", "Thuyết trình"),
        ("project", "Đồ án"),
        ("quiz", "Kiểm tra nhỏ"),
        ("research", "Nghiên cứu"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="Lớp học",
    )
    title = models.CharField(max_length=200, verbose_name="Tiêu đề")
    type = models.CharField(
        max_length=20, choices=TYPE_CHOICES, verbose_name="Loại bài tập"
    )
    description = models.TextField(verbose_name="Mô tả")

    # Thời gian
    assigned_date = models.DateTimeField(auto_now_add=True, verbose_name="Ngày giao")
    due_date = models.DateTimeField(verbose_name="Hạn nộp")

    # Điểm số
    max_score = models.DecimalField(
        max_digits=4, decimal_places=2, default=10.00, verbose_name="Điểm tối đa"
    )
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, default=10.00, verbose_name="Trọng số (%)"
    )

    # Tài liệu
    instruction_file = models.FileField(
        upload_to="assignments/instructions/", blank=True, verbose_name="File hướng dẫn"
    )

    is_active = models.BooleanField(default=True, verbose_name="Đang hoạt động")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Bài tập"
        verbose_name_plural = "Bài tập"
        ordering = ["-due_date"]

    def __str__(self):
        return f"{self.title} - {self.course.subject.name}"


class Attendance(models.Model):
    """Điểm danh từng buổi học"""

    STATUS_CHOICES = [
        ("present", "Có mặt"),
        ("absent", "Vắng mặt"),
        ("late", "Đi trễ"),
        ("excused", "Vắng có phép"),
    ]

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="attendances",
        verbose_name="Lớp học",
    )
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, verbose_name="Chủng sinh"
    )
    date = models.DateField(verbose_name="Ngày học")
    session_number = models.IntegerField(verbose_name="Buổi học số")

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, verbose_name="Trạng thái"
    )
    notes = models.TextField(blank=True, verbose_name="Ghi chú")

    recorded_by = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Người điểm danh"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["course", "student", "date", "session_number"]
        verbose_name = "Điểm danh"
        verbose_name_plural = "Điểm danh"
        ordering = ["-date", "session_number"]

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.course.subject.name} - {self.date}"
