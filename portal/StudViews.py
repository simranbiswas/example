from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.db import connection
from .models import Staffs, Students, Courses, student_courses, Notes

def viewcourses(request):
    current_user = request.user
    context = {'courses_list': Courses.objects.all(), 'user': current_user}
    return render(request, "admin_template/stud_template.html", context)

def enroll(request, sid, id):
    sql = 'SELECT course_name from portal_courses where id='+str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    name = cursor.fetchone()
    current_user = request.user
    res = current_user.first_name

    student_courses.objects.get_or_create(
        course_name=name[0], course_id=Courses.objects.get(id=id), student_id=Students.objects.get(id=sid), student_name=res)
    
    sql1 = 'SELECT * from portal_student_courses where student_id_id='+str(sid)
    cursor1 = connection.cursor()
    cursor1.execute(sql1)
    result = cursor1.fetchall()
    context = {'sc_list': result, 'user': current_user}
    return render(request, 'admin_template/mycourses.html', context)
    #context = {'name': name[0],'sid': sid, 'res': res, 'cid': id }
    #return render(request, 'admin_template/sample.html', context)

def viewcourselist(request, id):
    current_user = request.user
    sql1 = 'SELECT * from portal_student_courses where student_id_id='+str(id)
    cursor1 = connection.cursor()
    cursor1.execute(sql1)
    result = cursor1.fetchall()
    context = {'sc_list': result, 'user': current_user}
    return render(request, 'admin_template/mycourses.html', context)

def unenroll(request, sid, id):
    try:
        course = student_courses.objects.get(student_id=sid, course_id=id)
        course.delete()
        current_user = request.user
        sql1 = 'SELECT * from portal_student_courses where student_id_id='+str(sid)
        cursor1 = connection.cursor()
        cursor1.execute(sql1)
        result = cursor1.fetchall()
        context = {'sc_list': result, 'user': current_user}
        return render(request, 'admin_template/mycourses.html', context)
    except:
        current_user = request.user
        context = {'courses_list': Courses.objects.all(
        ), 'user': current_user, 'alert_flag': True}
        return render(request, "admin_template/stud_template.html", context)

def viewnotes(request, id):
    sql = 'SELECT course_id_id,course_name from portal_student_courses WHERE student_id_id='+str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    res = cursor.fetchall()
    sql1 = 'SELECT course_id_id from portal_student_courses WHERE student_id_id='+str(id)
    cursor1 = connection.cursor()
    cursor1.execute(sql1)
    res1 = cursor1.fetchall()
    context = {'notes': res, 'course_ids':res1}
    return render(request, 'admin_template/viewnotes.html', context)

def accessnotes(request, id):
    note = Notes.objects.get(course_id=id)
    context = {'notes': note, 'user': request.user}
    return render(request, 'admin_template/live.html', context)

