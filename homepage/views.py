from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account import url
from .form import add_scholarship_form
from django.contrib import messages
from .models import application_table,scholarship
from account.models import staff
from django.contrib.auth.models import User, auth
from datetime import date
# Create your views here.

from .models import scholarship
def home(request):
    scholarships=scholarship.objects.all()
    today_date = date.today()
    expired = []
    not_expired = []
    for s in scholarships:
        if today_date > s.toomdate:
            expired.append(s)
        else:
            not_expired.append(s)
    if request.user.is_authenticated:
        return render(request,'homepage/index.html',{'expired':expired,'not_expired':not_expired})
    else:
        return render(request,'homepage/welcome_page.html',{'expired':expired,'not_expired':not_expired})


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






def delete_scholarship(request,x):
    try:
        s=scholarship.objects.get(pk=x)
        s.delete()
    except:
        return HttpResponse('ERROR in deleting')

    messages.error(request, 'scholarship deleted successfully')

    scholarships=scholarship.objects.all()
    return render(request, 'homepage/index.html', {'all_scholar': scholarships})


def show_scholarship_template(request,x):
    # print(type(x))
    current_scholarship=scholarship.objects.get(pk=x)
    if not request.user.is_staff or request.user.is_superuser:

        my_record = scholarship.objects.get(id=x)
        form = add_scholarship_form(instance=my_record)
        if request.method == "POST":
            form = add_scholarship_form(request.POST, instance=my_record)
            if form.is_valid():
                form.save()
            messages.success(request, 'Scholarship updated succesfully')
            scholarships = scholarship.objects.all()
            return redirect(request.META['HTTP_REFERER'])#for previous page with refresh

        return render(request, 'homepage/scholoarship_template.html',{'current_scholarship':current_scholarship,'p_form':form})
    else:
        applications=application_table.objects.all()
        admin=staff.objects.get(emp_no=request.user.username)
        var=admin.branch
        students=[]


        for app in applications:
            try:
                student=User.objects.get(id=app.user_id)
                if student.profile.branch==var and app.scholarship_id==int(x):
                    students.append((student,app))
            except:
                app.delete()
                continue

        return render(request,'homepage/admin_panel.html',{'admin':admin,'students':students,'current_scholarship':current_scholarship})

def applied_application(request,x,y):
    application=application_table.objects.get(id=y)
    student=User.objects.get(id=x)
    return render(request, 'homepage/applied_application_form.html',{'student':student,'application':application})

def pdf_view(request,x):
    s = scholarship.objects.get(pk=x)
    pdf_name=s.document
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')

def submit_application(request,x,y):
    if request.method=='POST':
        all_aps=application_table.objects.all()
        EXTRA1 = request.POST['extra1']
        EXTRA2 = request.POST['extra2']
        for app in all_aps:
            if app.scholarship_id==int(x) and app.user_id==int(y):
                messages.error(request, 'scholarship already applied')
                # return render(request,'homepage/index.html')
                #return HttpResponse('scholarship already applied')
                return redirect(request.META['HTTP_REFERER'])

        if request.user.profile.document10 and request.user.profile.document12 and request.user.profile.document_last_sem and request.user.profile.student_id and request.user.profile.father_id:

            application=application_table.objects.create(scholarship_id=x,user_id=y,applied_document10=request.user.profile.document10,applied_document12=request.user.profile.document12,applied_document_last_sem=request.user.profile.document_last_sem,applied_father_id=request.user.profile.father_id,applied_student_id=request.user.profile.student_id,applied_extra1=EXTRA1,applied_extra2=EXTRA2)
            application.save()
            messages.success(request, 'scholarship applied succesfully')
            # return render(request,'homepage/index.html')
            #return HttpResponse('scholarship applied succesfully')
            return redirect(request.META['HTTP_REFERER'])

        else:
            messages.error(request, 'Upload all documents')
            return redirect(request.META['HTTP_REFERER'])


