from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account import url
from .form import add_scholarship_form
from django.contrib import messages
from .models import application_table,scholarship
from account.models import staff,profile
from django.contrib.auth.models import User, auth
from datetime import date

from account.models import student
from .resources import UserResource
from tablib import Dataset
from .models import scholarship
from account.resources import profileResource
# Create your views here.

from .models import scholarship



def simple_upload(request):
    if request.method=='POST':
        dataset = Dataset()
        try:
            new_user = request.FILES['myfile']
        except:
            new_user=None
        try:
            new_profile = request.FILES['myfile2']
        except:
            new_profile=None

        if  not new_user==None and new_user.name.endswith('xlsx'):
            imported_data = dataset.load(new_user.read(), format='xlsx')
            for data in imported_data:
                value = User.objects.create_user(username=data[1], first_name=data[3], email=data[2], password=data[1],is_staff=False)
                value.save()

                value1 = student(reg_no=data[1], name=data[3], email=data[2])
                value1.save()
            messages.success(request, 'user data imported')
            return render(request, 'homepage/upload.html')

        if  not new_profile==None and new_profile.name.endswith('xlsx'):
            imp_profile_data = dataset.load(new_profile.read(), format='xlsx')
            for data in imp_profile_data:
                try:
                    value=User.objects.get(username=data[1])
                    user_profile_obj=profile.objects.get(user_id=value.id)
                except:
                    value=None

                if value is not None:
                    user_profile_obj.marks=data[2]
                    user_profile_obj.save(update_fields=['marks'])
                    user_profile_obj.attendence=data[3]
                    user_profile_obj.save(update_fields=['attendence'])
                else:
                    messages.error(request, '1 error found')

            messages.success(request, 'profile data imported')
            return render(request, 'homepage/upload.html')

        else:
            messages.error(request, 'wrong format')
            return render(request, 'homepage/upload.html')
    else:
        return render(request,'homepage/upload.html')








def home(request):
    scholarships=scholarship.objects.all()
    today_date = date.today()
    expired = []
    not_expired = []
    for s in scholarships:
        if today_date > s.toomdate:
            expired.append(s)
            s.active = 0
            s.save(update_fields=['active'])
        else:
            s.active = 1
            s.save(update_fields=['active'])
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

def change_status(request,x,y):
    s = application_table.objects.get(pk=x)
    s.status = y
    s.save(update_fields=['status'])
    messages.success(request, 'application status updated successfully')
    return redirect(request.META['HTTP_REFERER'])

def show_scholarship_template(request,x,y='0'):
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

        #print(type(y))
        if y=='0':
            Sort_Tuple_marks_increasing(students)
        elif y=='1':
            Sort_Tuple_marks_decreasing(students)
        elif y=='2':
            Sort_Tuple_attendence_increasing(students)
        elif y=='3':
            Sort_Tuple_attendence_decreasing(students)
        elif y=='4':
            Sort_Tuple_rank(students)
        else :
            Sort_Tuple_rank(students,0)


        return render(request,'homepage/admin_panel.html',{'admin':admin,'students':students,'current_scholarship':current_scholarship})


def Sort_Tuple_marks_increasing(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0].profile.marks < tup[j + 1][0].profile.marks):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

def Sort_Tuple_marks_decreasing(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0].profile.marks > tup[j + 1][0].profile.marks):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

def Sort_Tuple_attendence_increasing(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0].profile.attendence < tup[j + 1][0].profile.attendence):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup

def Sort_Tuple_attendence_decreasing(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0].profile.attendence > tup[j + 1][0].profile.attendence):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
    return tup


def Sort_Tuple_rank(tup,y=1):

    def place(x):
        if x == 'Lance Naik':
            return 0
        elif x=='Naik':
            return 1
        elif x=='Hawaldar':
            return 2
        elif x=='Nb Subedar':
            return 3
        elif x=='Subedar':
            return 4
        elif x=='Subeder Maj':
            return 5
        elif x=='Officer':
            return 6
        else:
            return -1


    lst = len(tup)
    if y==1:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (place(tup[j][0].profile.father_rank) > place(tup[j + 1][0].profile.attendence)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
    else:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (place(tup[j][0].profile.father_rank) < place(tup[j + 1][0].profile.attendence)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp

    return tup



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


