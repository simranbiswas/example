from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db import connection
from .models import Staffs, Courses, Notes
import base64

def staff_home(request):
    current_user = request.user
    cid = current_user.staffs.course_id_id
    course = Courses.objects.get(id=cid)
    sql = 'SELECT count(course_id_id) from portal_student_courses WHERE course_id_id='+str(cid)
    cursor = connection.cursor()
    cursor.execute(sql)
    count = cursor.fetchone()
    context = {
        'user': current_user,
        'courses': course,
        'count': count
    }
    return render(request, 'admin_template/base_template.html', context)


def view_profile(request):
    current_user = request.user
    if current_user.is_authenticated:
        return render(request, 'admin_template/prof.html', {'user': current_user})


def addnotesform(request):
    return render(request, "addnotes.html")

'''
def addnotes(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed<h2>")
    else:
        lec_no = request.POST.get("lec_no")
        pdfs = request.POST.get("pdf")
        pdfs = pdfs.split("/")
        video_links = request.POST.get("link")
        video_links = video_links.split("/")
        assignment = request.POST.get("assign")
        cursor = connection.cursor()
        course_id = Courses.objects.get(user.staffs.course_id = id)
        staff_id = Staffs.objects.get(user.staffs.id = id)
        try:
            notes = Notes.object.create(course_id=course_id, lec_no=lec_no, pdfs=pdfs, video_links=video_links, assignment=assignment, staff_id=staff_id)
            notes.save()
            messages.success(request, "Successfully Added!")
            return HttpResponseRedirect(reverse("notes"))
        except:
            messages.error(request, "Try again")
            return HttpResponseRedirect(reverse("notes"))

'''
