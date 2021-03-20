
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

class CustomUser(AbstractUser):
    user_type_data = ((1, "Staff"), (2, "Student"))
    user_type = models.CharField(
        default=1, choices=user_type_data, max_length=10)


class Courses(models.Model):
    id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    objects = models.Manager()


class Staffs(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    qualification = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING)
    job_title = models.CharField(max_length=255)
    photo = models.ImageField(upload_to="media")
    objects = models.Manager()


class Students(models.Model):
    id = models.AutoField(primary_key=True)
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=255)
    stream = models.CharField(max_length=255)
    university = models.CharField(max_length=255)
    objects = models.Manager()


class Notes(models.Model):
    id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    lec_no = models.CharField(max_length=4)
    pdfs = models.CharField(max_length=255)
    video_links = models.CharField(max_length=255)
    assignment = models.CharField(max_length=255)
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    objects = models.Manager()


class student_courses(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE)
    course_name = models.CharField(max_length=255)
    student_name = models.CharField(max_length=255)
    objects = models.Manager()


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 1:
            Staffs.objects.create(
                admin=instance, course_id=Courses.objects.get(id=1))
        if instance.user_type == 2:
            Students.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 1:
        instance.staffs.save()
    if instance.user_type == 2:
        instance.students.save()
