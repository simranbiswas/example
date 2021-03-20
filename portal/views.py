from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from portal.EmailBackend import EmailBackEnd
from django.contrib import messages
from portal.models import CustomUser
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from .forms import adminInputForm
from django.db import connection
from django.views import View
from django.core.mail import EmailMessage, send_mail
from django.conf import settings

# Create your views here.


def showDemoPage(request):
    return render(request, "demo.html")


def ShowLoginPage(request):
    return render(request, "opt.html")

def redirstaff(request):
    return render(request, "login.html")

def redirstud(request):
    return render(request, "log.html")

def resignup(request):
    return render(request, "signup.html")

def doLogin(request):

    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed<h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            return HttpResponseRedirect("/staff_home")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")

def stuLogin(request):
    
    if request.method != "POST":
        return HttpResponse("<h2>Method not Allowed<h2>")
    else:
        user = EmailBackEnd.authenticate(request, username=request.POST.get(
            "email"), password=request.POST.get("password"))
        if user != None:
            login(request, user)
            return HttpResponseRedirect("/student_home")
        else:
            messages.error(request, "Invalid Login Details")
            return HttpResponseRedirect("/")

def GetUserDetails(request):
    if request.user != None:
        return HttpResponse("User : "+request.user.email+" usertype : "+str(request.user.user_type))
    else:
        return HttpResponse("Please Login First")


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup(request):
    if request.method != "POST":
        return HttpResponse("Method Not Allowed")
    else:
        first_name = request.POST.get("fname")
        last_name = request.POST.get("lname")
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        gender = request.POST.get("gender")
        stream = request.POST.get("stream")
        university = request.POST.get("university")
        try:
            user = CustomUser.objects.create_user(
                username=username, password=password, email=email, last_name=last_name, first_name=first_name, user_type=2)
            user.students.gender = gender
            user.students.stream = stream
            user.students.university = university
            user.save()
            login(request, user)
            subject = 'Welcome to E-Learning Portal'
            message = f'Hi {user.first_name}, thank you for registering in e-learning portal.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [user.email, ]
            send_mail(subject, message, email_from, recipient_list)
            messages.success(request, "Successfully Registered! Mail Sent")
            return HttpResponseRedirect(reverse("resignup"))
        except:
            messages.error(request, "Try again")
            return HttpResponseRedirect(reverse("resignup"))


def admin(request):
    # if this is a POST request we need to process the form data
    context = {}
    current_user = request.user
    id = current_user.staffs.course_id_id
    sql = 'SELECT email from portal_customuser pcu INNER JOIN portal_students ps ON pcu.id=ps.admin_id INNER JOIN portal_student_courses psc on psc.student_id_id=ps.id WHERE psc.course_id_id=' + \
        str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    recipient = []
    for re in result:
        for email in re:
            recipient.append(email)

    if request.method == 'POST':
        try:
            if request.method == 'POST' and request.FILES["file"]:
                uploaded_file = request.FILES['file']
                fs = FileSystemStorage()
                name = fs.save(uploaded_file.name, uploaded_file)
                context['url'] = fs.url(name)
        except:
            pass
        # create a form instance and populate it with data from the request:
        form = adminInputForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            number1 = form.cleaned_data['lectureno']
            number2 = form.cleaned_data['videolink']
            number3 = form.cleaned_data['Assignment']

            import smtplib
            from email.mime.text import MIMEText
            from email.mime.image import MIMEImage

            from email.mime.multipart import MIMEMultipart
            from email.mime.application import MIMEApplication

            smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
            smtp_ssl_port = 465
            username = 'hackteammercury@gmail.com'
            password = '#mercury0'
            sender = 'hackteammercury@gmail.com'

            msg = MIMEMultipart()

            body = MIMEText("Lecture no is :"+number1+"\n" +
                            "Video link is :"+number2+"\n"+"Assignment is :"+number3)
            msg.attach(body)
            msg['Subject'] = "New Material From Instructor"
            msg['From'] = sender
            msg['To'] = ", ".join(recipient)
            try:
                filepath = 'C:/Users/Simran/Desktop/hackathon/learn/media/'+str(name)
                import os
                img = MIMEApplication(open(filepath, "rb").read())

                img.add_header('Content-Disposition',
                               'attachment',
                               filename=os.path.basename(filepath))
                msg.attach(img)
            except:
                pass

            server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
            server.login(username, password)
            server.sendmail(sender, recipient, msg.as_string())
            server.quit()
            return render(request, 'message.html')
    return render(request, 'message.html', context)

def sample(request):
    current_user = request.user
    id = current_user.staffs.course_id_id
    sql = 'SELECT email from portal_customuser pcu INNER JOIN portal_students ps ON pcu.id=ps.admin_id INNER JOIN portal_student_courses psc on psc.student_id_id=ps.id WHERE psc.course_id_id='+str(id)
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    recipient = []
    for re in result:
        for email in re:
            recipient.append(email)
    context = {'sc_list': recipient, 'user': current_user}
    return render(request, 'admin_template/sample.html', context)
