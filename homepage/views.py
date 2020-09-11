from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from account import url
from django.conf import settings
from django.core.mail import send_mail
from .form import add_scholarship_form,extra_documents_form
from django.contrib import messages
from .models import application_table,session_table,scholarship,current_session
from account.models import staff,profile
from django.contrib.auth.models import User
from datetime import date
import xlwt
import random

obj = current_session.objects.get(id=3)
nowdate = obj.session

from account.models import student
from .resources import UserResource
from tablib import Dataset

from django.core.exceptions import ValidationError


from .models import scholarship



def file_size(value): # add this to some file where you can import it from
    limit =  1024
    if value.size > limit:
        raise ValidationError('File too large. Size should not exceed 1 MB.')

# mapping of father_rank for sorting porpose
def place(x):
    if x == 'Lance Naik':
        return 0
    elif x == 'Naik':
        return 1
    elif x == 'Hawaldar':
        return 2
    elif x == 'Nb Subedar':
        return 3
    elif x == 'Subedar':
        return 4
    elif x == 'Subeder Maj':
        return 5
    elif x == 'Officer':
        return 6
    else:
        return -1

#for sorting year wise
def year_value(x):
    if x == 'FE':
        return 3
    elif x == 'SE':
        return 2
    elif x == 'TE':
        return 1
    elif x == 'BE':
        return 0

def graphs():
    # calculate the list for the graph

    appobjects = application_table.objects.all()
    branchcount = {"ENTC": 0, "COMP": 0, "IT": 0, "MECH": 0}

    for app in appobjects:
        try:
            appuser = User.objects.get(id=app.user_id)
        except:
            app.delete()
            continue
        if appuser.profile.branch == 1:
            branchcount["COMP"] = branchcount["COMP"] + 1
        elif appuser.profile.branch == 2:
            branchcount["IT"] = branchcount["IT"] + 1
        elif appuser.profile.branch == 3:
            branchcount["ENTC"] = branchcount["ENTC"] + 1
        elif appuser.profile.branch == 4:
            branchcount["MECH"] = branchcount["MECH"] + 1

    # calculate the list for graph ends
    # for left table
    all_application = application_table.objects.all()
    dict = {}
    for app in all_application:
        if app.scholarship_id in dict.keys():
            temp = dict[app.scholarship_id][1] + 1
            try:
                s = scholarship.objects.get(id=app.scholarship_id)
            except:
                app.delete()
                continue
            tup = (s, temp)
            dict[app.scholarship_id] = tup

        else:
            try:
                s = scholarship.objects.get(id=app.scholarship_id)
            except:
                app.delete()
                continue
            tup = (s, 1)
            dict[app.scholarship_id] = tup

    scholarships = scholarship.objects.all()
    for sch in scholarships:
        if not sch.id in dict.keys():
            tup = (sch, 0)
            dict[sch.id] = tup

    # for left table end

    return (branchcount,dict)


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
            admin = staff.objects.get(emp_no=request.user.username)
            var = admin.branch
            for data in imported_data:
                value = User.objects.create_user(username=data[1], first_name=data[3], email=data[2], password=data[1],is_staff=False)
                value.save()

                value1 = student(reg_no=data[1], name=data[3], email=data[2])
                value1.save()

                value = User.objects.get(username=data[1])
                user_profile_obj = profile.objects.get(user_id=value.id)
                user_profile_obj.branch=var
                user_profile_obj.save(update_fields=['branch'])

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
                    messages.error(request, '1 Error found, check if the student of any reg No. exists or not')

            messages.success(request, 'Profile data imported')
            return render(request, 'homepage/upload.html')

        else:
            messages.error(request, 'Wrong format')
            return render(request, 'homepage/upload.html')
    else:
        return render(request,'homepage/upload.html')


def simple_export(request,x):
    s = scholarship.objects.get(id=int(x))
    #print(s.title,nowdate)
    students=[]
    applications = application_table.objects.all()
    for app in applications:
        student = User.objects.get(id=app.user_id)
        if app.status == 1 and app.scholarship_id == int(x):
            students.append(student)

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="selected_students.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S no.', 'Reg no.','Student name', 'Father  name', 'branch', 'Email' ]
    ws.write(0,0,s.title+" scholarship",font_style)
    ws.write(0,1,nowdate, font_style)
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)


    #mapping branch
    br = {
        1: "COMP",
        2: "IT",
        3: "ENTC",
        4:"MECH"
    }


    # Sheet body, remaining rows
    cnt=0
    font_style = xlwt.XFStyle()
    for stu in students:
        row_num += 1
        cnt+=1

        ws.write(row_num,0,cnt,font_style)
        ws.write(row_num,1, stu.username, font_style)
        ws.write(row_num,2, stu.first_name,font_style)
        ws.write(row_num,3, stu.profile.father_name, font_style)
        ws.write(row_num,4, br[stu.profile.branch], font_style)
        ws.write(row_num,5, stu.email, font_style)



    wb.save(response)
    return response

def simple_export_admin_pannel(request,x):

    s = scholarship.objects.get(id=int(x))
    applications = application_table.objects.all()
    admin = staff.objects.get(emp_no=request.user.username)
    var = admin.branch
    students = []


    for app in applications:
        try:
            student = User.objects.get(id=app.user_id)
            if student.profile.branch == var and app.scholarship_id == int(x):
                students.append(student)
        except:
            app.delete()
            continue

    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Applications_list.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users')

    # Sheet header, first row
    row_num = 2
    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['S no.', 'Reg no.', 'Student name','Marks','Attendence', 'Father  name','Father rank', 'branch', 'Email']
    ws.write(0, 0, s.title + " scholarship", font_style)
    ws.write(0, 1, str(nowdate)+" session", font_style)
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)

    # mapping branch
    br = {
        1: "COMP",
        2: "IT",
        3: "ENTC",
        4: "MECH"
    }

    # Sheet body, remaining rows
    cnt = 0
    font_style = xlwt.XFStyle()
    for stu in students:
        row_num += 1
        cnt += 1

        ws.write(row_num, 0, cnt, font_style)
        ws.write(row_num, 1, stu.username, font_style)
        ws.write(row_num, 2, stu.first_name, font_style)
        ws.write(row_num, 3, stu.profile.marks, font_style)
        ws.write(row_num, 4, stu.profile.attendence, font_style)
        ws.write(row_num, 5, stu.profile.father_name, font_style)
        ws.write(row_num, 6, stu.profile.father_rank, font_style)
        ws.write(row_num, 7, br[stu.profile.branch], font_style)
        ws.write(row_num, 8, stu.email, font_style)

    wb.save(response)
    return response


def home(request):
    branchcount,dict=graphs()
    scholarships=scholarship.objects.all()
    today_date = date.today()
    expired = []
    not_expired = []
    for s in scholarships:
        if today_date > s.toomdate or s.active==0:
            expired.append(s)
            s.active = 0
            s.save(update_fields=['active'])
        else:
            #s.active = 1
            #s.save(update_fields=['active'])
            not_expired.append(s)
    if request.user.is_authenticated:
        return render(request,'homepage/index.html',{'expired':expired,'not_expired':not_expired,'dict':dict,'branch_count':branchcount})
    else:
        return render(request,'homepage/welcome_page.html',{'expired':expired,'not_expired':not_expired})


def add_scholarship_function(request):
    if request.method == 'POST':
        p_form = add_scholarship_form(request.POST, request.FILES)
        if p_form.is_valid():
            p_form.save()
            messages.success(request, 'scholarship added succesfully, Go to dashboard')
            #return render(request, 'homepage/index.html')
            return redirect(request.META['HTTP_REFERER'])
    else:
        p_form = add_scholarship_form(instance=request.user)
    return render(request,'homepage/add_scholarship.html',{'p_form':p_form})

def basic(request):
    return render(request,'homepage/basic.html')


@login_required(login_url="user_login")
def show_application_form(request,x):
    if request.user.is_authenticated:
        try:
            app=application_table.objects.get(user_id=request.user.id,scholarship_id=x)
            p_form = extra_documents_form(instance=app)
        except:
            p_form = extra_documents_form()


        all_aps= application_table.objects.all()
        already_applied=0
        if all_aps.filter(user_id=request.user.id , scholarship_id=x).exists():
            already_applied=1
        current_scholarship = scholarship.objects.get(pk=x)
        return render(request,'homepage/application_form.html',{'current_scholarship':current_scholarship,'already_applied':already_applied,'extra_docs_form':p_form})
    else:
        return render(request,'login/login.html')


def change_session(request):
    obj = current_session.objects.get(id=3)
    cs=obj.session
    cs1=cs+1
    return render(request,'homepage/change_session.html',{'cs':cs,'cs1':cs1})

def alter_session(request,flag):
    cs=None
    cs1=None
    if flag=='1':
        obj = current_session.objects.get(id=3)
        obj.session=obj.session+1
        obj.save(update_fields=['session'])
        cs = obj.session
        #print(cs)
        cs1 = cs + 1
        messages.success(request, 'session increased succesfully')
    elif flag=='0':
        obj = current_session.objects.get(id=3)
        obj.session = obj.session - 1
        obj.save(update_fields=['session'])
        cs = obj.session
        cs1 = cs + 1
        messages.success(request, 'session decreased succesfully')
    return redirect(request.META['HTTP_REFERER'])


def delete_previous_app(request):
    messages.success(request, 'All previous applications deleted succesfully')
    application_table.objects.all().delete()
    return redirect(request.META['HTTP_REFERER'])

def delete_all_students(request):
    User.objects.filter(is_staff=False).delete()
    messages.success(request, 'All previous session Students deleted succesfully')
    return redirect(request.META['HTTP_REFERER'])


def delete_all_scholarships(request):
    messages.success(request, 'All Scholarships deleted succesfully')
    scholarship.objects.all().delete()
    return redirect(request.META['HTTP_REFERER'])


def delete_scholarship(request,x):
    try:
        s=scholarship.objects.get(pk=x)
        s.delete()
    except:
        return HttpResponse('Error in deleting,Go Back to Dashboard')

    messages.error(request, 'scholarship deleted successfully, Go to Dashboard')
    return render(request,'homepage/error_page.html')


def change_status(request,x,y,z):
    rec = User.objects.get(id=z)
    s = application_table.objects.get(id=x)
    scholarship_applied = scholarship.objects.get(id=s.scholarship_id)

    #print("current year is",nowdate)
    if y=='1':
        sessionuser = session_table.objects.create(user_id = z,scholarship_id = s.scholarship_id,session = nowdate)
        sessionuser.save()
    else:
        all_sessions = session_table.objects.all()
        if all_sessions.filter(user_id=z,scholarship_id=s.scholarship_id).exists():
            existinguser = session_table.objects.get(user_id = z)
            existinguser.delete()
        else:
            pass

    s.status = y
    s.save(update_fields=['status'])

    if y=='1':
        subject = 'AIT scholarship portsl'
        message = 'Congrats Your Application for '+scholarship_applied.title+' has been selected';
        email_from = settings.EMAIL_HOST_USER
        email_to = [rec.email]
        send_mail(subject, message, email_from, email_to, fail_silently=False)
    else:
        subject = 'AIT scholarship portsl'
        message = 'Unfortunately Your Application for '+scholarship_applied.title +' has not been selected'
        email_from = settings.EMAIL_HOST_USER
        email_to = [rec.email]
        send_mail(subject, message, email_from, email_to, fail_silently=False)


    messages.success(request, 'application status updated successfully')
    return redirect(request.META['HTTP_REFERER'])

def confirm_selection(request,x):
    s=scholarship.objects.get(id = x)
    emaillist = []
    users_id  = []
    all_applications = application_table.objects.all()
    for apps in all_applications:
        if apps.scholarship_id == int(x) and apps.status==1:
            users_id.append(apps.user_id)

    for i in users_id:
        student = User.objects.get(id=i)
        email = student.email
        emaillist.append(email)

    #print(emaillist)

    subject = 'AIT scholarship portsl'
    message = 'Congrats Your Application for ' + s.title + ' has been selected'
    email_from = settings.EMAIL_HOST_USER
    email_to = emaillist
    send_mail(subject, message, email_from, email_to, fail_silently=False)

    return redirect(request.META['HTTP_REFERER'])


def show_scholarship_template(request,x,y='0'):
    branchcount,dict=graphs()
    # print(type(x))
    current_scholarship=scholarship.objects.get(pk=x)
    if_usergot_scholarship = 0
    all_sessions = session_table.objects.all()
    if all_sessions.filter(user_id=request.user.id).exists():
        for one in all_sessions:
            print(one.session)
            print(nowdate)
            if one.user_id == request.user.id and one.session == nowdate:
                if_usergot_scholarship = 1

    #print('user status', if_usergot_scholarship)

    if not request.user.is_staff or request.user.is_superuser:

        my_record = scholarship.objects.get(id=x)
        form = add_scholarship_form(instance=my_record)
        if request.method == "POST":
            form = add_scholarship_form(request.POST,request.FILES, instance=my_record)
            if form.is_valid():
                form.save()
            messages.success(request, 'Scholarship updated succesfully')
            scholarships = scholarship.objects.all()
            return redirect(request.META['HTTP_REFERER'])#for previous page with refresh

        return render(request, 'homepage/scholoarship_template.html',{'current_scholarship':current_scholarship,'p_form':form,'got_already':if_usergot_scholarship,'dict':dict,'branch_count':branchcount})
    else:
        applications=application_table.objects.all()
        admin=staff.objects.get(emp_no=request.user.username)
        var=admin.branch
        students=[]
        selected_students=0


        for app in applications:
            try:
                student=User.objects.get(id=app.user_id)
                if student.profile.branch==var and app.scholarship_id==int(x):
                    students.append((student,app))
                    if app.status==1:
                        selected_students+=1
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
        elif y=='5':
            Sort_Tuple_rank(students,0)
        elif y=='6':
            Sort_year(students)
        elif y=='7':
            Sort_year(students,0)

        #print(selected_students)
        total=current_scholarship.both
        remains=total-selected_students

        authority=1
        if(selected_students==total):
            authority=0
        else:
            authority=1

        return render(request,'homepage/admin_panel.html',{'admin':admin,'students':students,'current_scholarship':current_scholarship,'selected':selected_students,'total':total,'remains':remains,'authority':authority})


def show_selected_applicants(request,x):
    all_admins = staff.objects.all()
    all_admin_branches = []
    all_applications = application_table.objects.all()
    current_scholarship = scholarship.objects.get(id = int(x))
    branch_one = []
    branch_two = []
    branch_three = []
    branch_four = []

    #print("branch of this admin is",all_admins[0].branch)
    #print("current scholarship is",current_scholarship.title)
    for apps in all_applications:
        Student = User.objects.get(id=apps.user_id)
        if Student.profile.branch == all_admins[0].branch and apps.status == 1 and apps.scholarship_id == int(x):
            branch_one.append((Student,apps))

    for apps in all_applications:
        Student = User.objects.get(id=apps.user_id)
        if Student.profile.branch == all_admins[1].branch and apps.status == 1 and apps.scholarship_id == int(x):
            branch_two.append((Student,apps))

    for apps in all_applications:
        Student = User.objects.get(id=apps.user_id)
        if Student.profile.branch == all_admins[2].branch and apps.status == 1 and apps.scholarship_id == int(x):
            branch_three.append((Student,apps))

    for apps in all_applications:
        Student = User.objects.get(id=apps.user_id)
        if Student.profile.branch == all_admins[3].branch and apps.status == 1 and apps.scholarship_id == int(x):
            branch_four.append((Student,apps))


    for admin in all_admins:
        if admin.branch == 1:
            all_admin_branches.append("COMP")
        elif admin.branch == 2:
            all_admin_branches.append("IT")
        elif admin.branch == 3:
            all_admin_branches.append("ENTC")
        else:
            all_admin_branches.append("MECH")

    context = {
         'current_scholarship':current_scholarship,
         'branch_one':branch_one,
        'branch_two':branch_two,
        'branch_three':branch_three,
        'branch_four':branch_four,
        'branch0':all_admin_branches[0],
        'branch1': all_admin_branches[1],
        'branch2': all_admin_branches[2],
        'branch3': all_admin_branches[3],

    }
    return render(request,'homepage/selected_applicants.html',context)


def Sort_Tuple_marks_increasing(tup):
    # getting length of list of tuples
    lst = len(tup)
    for i in range(0, lst):

        for j in range(0, lst - i - 1):
            if (tup[j][0].profile.marks < tup[j + 1][0].profile.marks):
                temp = tup[j]
                tup[j] = tup[j + 1]
                tup[j + 1] = temp
            elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                if(tup[j][0].profile.attendence < tup[j + 1][0].profile.attendence):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif(tup[j][0].profile.attendence == tup[j + 1][0].profile.attendence):
                    if (place(tup[j][0].profile.father_rank) < place(tup[j + 1][0].profile.father_rank)):
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
            elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                if (tup[j][0].profile.attendence > tup[j + 1][0].profile.attendence):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.attendence == tup[j + 1][0].profile.attendence):
                    if (place(tup[j][0].profile.father_rank) > place(tup[j + 1][0].profile.father_rank)):
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
            elif (tup[j][0].profile.attendence == tup[j + 1][0].profile.attendence):
                if (tup[j][0].profile.marks < tup[j + 1][0].profile.marks):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                    if (place(tup[j][0].profile.father_rank) < place(tup[j + 1][0].profile.father_rank)):
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
            elif (tup[j][0].profile.attendence == tup[j + 1][0].profile.attendence):
                if (tup[j][0].profile.marks > tup[j + 1][0].profile.marks):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                    if (place(tup[j][0].profile.father_rank) > place(tup[j + 1][0].profile.father_rank)):
                        temp = tup[j]
                        tup[j] = tup[j + 1]
                        tup[j + 1] = temp
    return tup


def Sort_Tuple_rank(tup,y=1):


    lst = len(tup)
    if y==1:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (place(tup[j][0].profile.father_rank) < place(tup[j + 1][0].profile.father_rank)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.father_rank == tup[j + 1][0].profile.father_rank):
                    if (tup[j][0].profile.marks < tup[j + 1][0].profile.marks):
                        temp = tup[j]
                        tup[j] = tup[j + 1]
                        tup[j + 1] = temp
                    elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                        if (tup[j][0].profile.attendence < tup[j + 1][0].profile.attendence):
                            temp = tup[j]
                            tup[j] = tup[j + 1]
                            tup[j + 1] = temp
    else:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (place(tup[j][0].profile.father_rank) > place(tup[j + 1][0].profile.father_rank)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.father_rank == tup[j + 1][0].profile.father_rank):
                    if (tup[j][0].profile.marks > tup[j + 1][0].profile.marks):
                        temp = tup[j]
                        tup[j] = tup[j + 1]
                        tup[j + 1] = temp
                    elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                        if (tup[j][0].profile.attendence > tup[j + 1][0].profile.attendence):
                            temp = tup[j]
                            tup[j] = tup[j + 1]
                            tup[j + 1] = temp

    return tup

def Sort_year(tup,y=1):


    lst = len(tup)
    if y==1:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (year_value(tup[j][0].profile.present_year) < year_value(tup[j + 1][0].profile.present_year)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.present_year == tup[j + 1][0].profile.present_year):
                    if (tup[j][0].profile.marks < tup[j + 1][0].profile.marks):
                        temp = tup[j]
                        tup[j] = tup[j + 1]
                        tup[j + 1] = temp
                    elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                        if (tup[j][0].profile.attendence < tup[j + 1][0].profile.attendence):
                            temp = tup[j]
                            tup[j] = tup[j + 1]
                            tup[j + 1] = temp
    else:
        for i in range(0, lst):
            #print(tup[i][0].profile.id)
            for j in range(0, lst - i - 1):

                if (year_value(tup[j][0].profile.present_year) > year_value(tup[j + 1][0].profile.present_year)):
                    temp = tup[j]
                    tup[j] = tup[j + 1]
                    tup[j + 1] = temp
                elif (tup[j][0].profile.present_year == tup[j + 1][0].profile.present_year):
                    if (tup[j][0].profile.marks > tup[j + 1][0].profile.marks):
                        temp = tup[j]
                        tup[j] = tup[j + 1]
                        tup[j + 1] = temp
                    elif (tup[j][0].profile.marks == tup[j + 1][0].profile.marks):
                        if (tup[j][0].profile.attendence >tup[j + 1][0].profile.attendence):
                            temp = tup[j]
                            tup[j] = tup[j + 1]
                            tup[j + 1] = temp

    return tup



def applied_application(request,x,y,z):
    application=application_table.objects.get(id=y)
    student=User.objects.get(id=x)
    authority=int(z)

    if_usergot_scholarship = 0
    all_sessions = session_table.objects.all()
    if all_sessions.filter(user_id = x).exists():
        for one in all_sessions:
            if one.user_id==int(x) and one.session==nowdate:
                if_usergot_scholarship = 1


    #print("user status",if_usergot_scholarship)


    #print(type(authority))
    return render(request, 'homepage/applied_application_form.html',{'student':student,'application':application,'authority':authority,'got_already':if_usergot_scholarship})

def pdf_view(request,x):
    s = scholarship.objects.get(pk=x)
    pdf_name=s.document
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')

def pdf_view2(request,x):
    s = scholarship.objects.get(pk=x)
    pdf_name=s.scholarship_form
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')


def pdf_view3(request,x):
    s = application_table.objects.get(pk=x)
    pdf_name=s.applied_scholarship_form
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')

def unique_name(strr):
    s=strr.split('.')
    x=random.randint(1,10000)
    ss=str(x)+'_'+s[0]+'.'+s[1]
    return ss

from django.core.files.storage import FileSystemStorage
def submit_application(request,x,y):
    if request.method=='POST':
        all_apps=application_table.objects.all()


        if request.user.profile.document10 and request.user.profile.document12 and request.user.profile.document_last_sem and request.user.profile.student_id and request.user.profile.father_id:
            for app in all_apps:
                if app.scholarship_id==int(x) and app.user_id==int(y):
                    app.delete()

            p_form = extra_documents_form(request.POST, request.FILES)
            if p_form.is_valid():
                tup=p_form.save(commit=False)
                tup.user_id=y
                tup.scholarship_id=x
                tup.applied_document10 = request.user.profile.document10
                tup.applied_document12 = request.user.profile.document12
                tup.applied_document_last_sem = request.user.profile.document_last_sem
                tup.applied_father_id = request.user.profile.father_id
                tup.applied_student_id = request.user.profile.student_id
                tup.save()

                messages.success(request, 'scholarship applied succesfully, Check the status in profile')
            else:
                messages.error(request, 'Error.Check the file size ,it should not exceed 1 MB')

            return redirect(request.META['HTTP_REFERER'])
        else:
            messages.error(request, 'Upload all documents')
            return redirect(request.META['HTTP_REFERER'])


# for registed students
def registered_students(request):

    adm = User.objects.get(id = request.user.id)
    admstaffobj = staff.objects.get(emp_no = adm.username)
    adminbranch = admstaffobj.branch

    #print("admin branch is",adminbranch)

    branch_students = []

    Userobjects = User.objects.all()
    #print(Userobjects)

    for u in Userobjects:
        if u.profile.branch == adminbranch and u.is_staff == False:
            branch_students.append((u,u.id))


    #for x,y in branch_students:
        #print(x,end=" ")
        #print(y)

    context={
        "branch_students":branch_students,
        "emp_no":admstaffobj.emp_no
    }

    return render(request,'homepage/registered_students.html',context)

def delete_particular_student(request,x):

    stud = User.objects.get(id = x)
    applications = application_table.objects.all()
    try:
        for appli in applications:
            if appli.user_id == stud.id:
                appli.delete()
    except:
        pass

    #print("student name is",stud.username)
    #print("student id is",stud.id)
    # stud.delete()
    stud.delete()

    return redirect(request.META['HTTP_REFERER'])


def delete_all_student(request,x):

    admobject = staff.objects.get(emp_no = x)
    admbranch = admobject.branch

    branch_students = []
    student_applications = []
    Userobjects = User.objects.all()
    applicationobjects = application_table.objects.all()

    for u in Userobjects:
        if u.profile.branch == admbranch and u.is_staff == False:
            branch_students.append(u)
            # print("student is ",u.id)
            for app in applicationobjects:
                if app.user_id == u.id:
                    # print("app id is",app.user_id," ",app.scholarship_id)
                    student_applications.append(app)

    for app in student_applications:
        try:
            # print(app)
            app.delete()
        except:
            pass

    for bu in branch_students:
        bu.delete()


    return redirect(request.META['HTTP_REFERER'])


def our_team(request):
    return render(request,'homepage/our_team.html')


def how_to_apply(request):
    return render(request,'homepage/how_to_apply.html')