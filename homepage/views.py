from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account import url
from .form import add_scholarship_form
from django.contrib import messages
from .models import application_table
from account.models import staff
from django.contrib.auth.models import User, auth

# Create your views here.

from .models import scholarship
def home(request):
    scholarships=scholarship.objects.all()
    if request.user.is_authenticated:
        return render(request,'homepage/index.html',{'all_scholar':scholarships})
    else:
        return render(request,'homepage/welcome_page.html',{'all_scholar':scholarships})


def add_scholarship_function(request):
    if request.method == 'POST':
        p_form = add_scholarship_form(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'scholarship added succesfully')
            return render(request, 'homepage/index.html')


    else:
        p_form = add_scholarship_form(instance=request.user)
    return render(request,'homepage/add_scholarship.html',{'p_form':p_form})

def basic(request):
    return render(request,'homepage/basic.html')


@login_required(login_url="user_login")
def show_application_form(request,x):
    if request.user.is_authenticated:
        current_scholarship = scholarship.objects.get(pk=x)
        return render(request,'homepage/application_form.html',{'current_scholarship':current_scholarship})
    else:
        return render(request,'login/login.html')



def show_scholarship_template(request,x):
    # print(type(x))
    current_scholarship=scholarship.objects.get(pk=x)
    if not request.user.is_staff or request.user.is_superuser:
        return render(request, 'homepage/scholoarship_template.html',{'current_scholarship':current_scholarship})
    else:
        applications=application_table.objects.all()
        admin=staff.objects.get(emp_no=request.user.username)
        var=admin.branch
        students=[]


        for app in applications:
            student=User.objects.get(id=app.user_id)
            if student.profile.branch==var and app.scholarship_id==int(x):
                students.append(student)

        return render(request,'homepage/admin_panel.html',{'admin':admin,'students':students,'current_scholarship':current_scholarship})



def pdf_view(request,x):
    s = scholarship.objects.get(pk=x)
    pdf_name=s.document
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')

def submit_application(request,x,y):
    if request.method=='POST':
        all_aps=application_table.objects.all()
        for app in all_aps:
            if app.scholarship_id==int(x) and app.user_id==int(y):
                messages.error(request, 'scholarship already applied')
                # return render(request,'homepage/index.html')
                return HttpResponse('scholarship already applied')

        application=application_table.objects.create(scholarship_id=x,user_id=y)
        application.save()
        messages.success(request, 'scholarship applied succesfully')
        # return render(request,'homepage/index.html')
        return HttpResponse('scholarship applied succesfully')


