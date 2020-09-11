from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import student,staff,profile
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required

#from .form import profile_update_form
from django.core.mail import send_mail
from django.conf import settings
from homepage.models import application_table,scholarship
from .form import Profile_Form,Profile2_form,Profile2_form_for_admin_work,Profile_Form_for_admin_work


def user_profile(request):
    if request.method == 'POST':
        pro_form = Profile_Form(request.POST,request.FILES,instance=request.user)
        pro2_form = Profile2_form(request.POST,request.FILES,instance=request.user.profile)
        #print('pro2',pro2_form.is_valid())
        #print('pro',pro_form.is_valid())
        if pro2_form.is_valid() and pro_form.is_valid():
            pro_form.save()
            pro2_form.save()
            messages.success(request, 'profile updated succesfully')
            return redirect('profile')
        else:
            messages.error(request, 'Error.Check the file size or format ,it should not exceed 1 MB')
            return redirect('profile')

    else :
        pro_form = Profile_Form(instance=request.user)
        pro2_form = Profile2_form(instance=request.user.profile)

        # scholarships that the user hava applied

        applications=application_table.objects.all()
        scholarships=[]
        for app in applications:
            #print(type(app.user_id),type(request.user.id))
            if  app.user_id==request.user.id:
                #print(type(app.status))
                # a tuple of (current scholarship and its status )
                scholarships.append((scholarship.objects.get(pk=app.scholarship_id),app.status))

        # end of scholarship that user have applied
        return render(request,'homepage/profile.html',{'pro_form':pro_form,'pro2_form':pro2_form,'scholarships':scholarships})

def edit_user_profile_form(request):
    return render(request,'homepage/edit_student_profile_form.html')

def show_user_profile_for_admin_work(request):
    if request.method == 'POST':
        regno = request.POST['regno']
        try:
            student_obj=User.objects.get(username=regno)
        except:
            messages.error(request, 'Invalid Registration Number, It may not be registered ')
            return redirect(request.META['HTTP_REFERER'])


        pro_form = Profile_Form_for_admin_work(instance=student_obj)
        pro2_form = Profile2_form_for_admin_work(instance=student_obj.profile)

        # scholarships that the user have applied

        applications = application_table.objects.all()
        scholarships = []
        for app in applications:
            if app.user_id == student_obj.id:
                scholarships.append((scholarship.objects.get(pk=app.scholarship_id), app.status))

        # end of scholarship that user have applied
        return render(request, 'homepage/profile_for_admin_work.html',
                      {'pro_form': pro_form, 'pro2_form': pro2_form,'student_obj':student_obj, 'scholarships': scholarships})

    else:
        return render(request, 'homepage/edit_student_profile_form.html')


def edit_user_profile_for_admin_work(request,x):
    if request.method == 'POST':

        x = User.objects.get(id=x)
        pro_form = Profile_Form_for_admin_work(request.POST,request.FILES,instance=x)
        pro2_form = Profile2_form_for_admin_work(request.POST,request.FILES,instance=x.profile)
        print('pro2',pro2_form.is_valid())
        print('pro',pro_form.is_valid())
        if pro2_form.is_valid() and pro_form.is_valid():
            pro_form.save()
            pro2_form.save()
            messages.success(request, 'profile updated succesfully')
            return redirect(request.META['HTTP_REFERER'])

    else :
        messages.error(request, 'Error , Go back')
        return render(request, 'homepage/edit_student_profile_form.html')


def sendemail(recipient_list,emp,name):
    subject = 'Congratulations '+ name
    message =  '  You have been registered as an admin with EMP no. as '+str(emp)+' by the superuser <br>,your default password is 12345 kindly login with http://127.0.0.1:8000/log/change_password and change your password <br>,If its not you kindly report the superuser .<br>This is auto generated mail ,dont reply.'
    email_from = settings.EMAIL_HOST_USER
    #recipient_list = ['nikhilkotwalcse@gmail.com',]
    send_mail( subject, message, email_from, recipient_list,fail_silently=False )
    #return redirect('redirect to a new page')


def user_login(request):
    if request.method=='POST':
        regno =request.POST['reg_no']
        pass2 = request.POST['pass']

        user = auth.authenticate(username=regno, password=pass2)

        if user is not None :
            if user.is_staff :
                auth.login(request,user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('/')
            else :
                auth.login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect('/')

        else:
             messages.error(request,'Invalid Credintials')
             return render(request, 'login/login.html',)


    else:
        # if 'next' in request.POST:
        messages.info(request, 'please login before applying')
        return render(request, 'login/login.html',)


def user_register(request):
    if request.method=='POST':
        regno = request.POST['reg_number']
        fname = request.POST['fname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        email = request.POST['email']
        if pass1==pass2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email taken')
                return render(request,'login/register.html')
            elif User.objects.filter(username=regno).exists():
                messages.success(request, 'username taken')
                return render(request,'login/register.html')
            else:
                user = User.objects.create_user(first_name=fname,username=regno,password=pass1,email=email,is_staff=False)
                user.save();

                admin = staff.objects.get(emp_no=request.user.username)
                var = admin.branch
                user_profile_obj = profile.objects.get(user_id=user.id)
                user_profile_obj.branch=var
                user_profile_obj.save(update_fields=['branch'])

                stu=student.objects.create(name=fname,email=email,reg_no=regno)
                stu.save()

                messages.success(request, 'registration succesfull')

                return render(request, 'login/login.html')

        else :
            messages.info(request,'password not matched')
            return render(request,'login/register.html')
    else:
        return render(request,'login/register.html')



def admin_register(request):
    all_staffs=staff.objects.all()
    if request.method=='POST':
        empno = request.POST['emp_number']
        fname = request.POST['fname']
        admin_branch = request.POST['branch']
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            messages.info(request,'email taken')
            return render(request, 'login/admin_register.html',{'all_staffs':all_staffs})
        elif User.objects.filter(username=empno).exists():
            messages.info(request, 'username taken')
            return render(request, 'login/admin_register.html',{'all_staffs':all_staffs})
        else:
            for app in all_staffs:
                if app.branch == int(admin_branch):
                    messages.error(request, 'branch already taken')
                    # return render(request,'homepage/index.html')
                    return render(request, 'login/admin_register.html', {'all_staffs': all_staffs})

            user = User.objects.create_user(first_name=fname,username=empno,password="12345",email=email,is_staff=True)
            user.save()

            staf=staff.objects.create(name=fname,email=email,emp_no=empno,branch=admin_branch)
            staf.save()

            s = profile.objects.get(user_id=user.id)
            s.branch = admin_branch
            s.save(update_fields=['branch'])

            reciptent_list=[email]
            sendemail(reciptent_list,empno,fname)

            messages.info(request,'registration successfull')
            return render(request, 'login/admin_register.html',{'all_staffs':all_staffs})

    else:
        return render(request,'login/admin_register.html',{'all_staffs':all_staffs})



def logout(request):
    auth.logout(request)
    return redirect('/')


def admin_delete(request,x):
    sta=staff.objects.get(pk=x)
    u = User.objects.get(username=sta.emp_no)
    u.delete()
    sta.delete()
    messages.info(request, 'deletion successfull')
    all_staffs=staff.objects.all()
    return render(request, 'login/admin_register.html', {'all_staffs': all_staffs})


def del_user(request):
    try:

        u = User.objects.get(username = request.user.username )

        stu=student.objects.get(reg_no= request.user.username)

        auth.logout(request)
        u.delete()
        stu.delete()
        return redirect('/')
    except:
        return HttpResponse( "The user not found")

@login_required(login_url="user_login")
def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request, 'Password changed successfully successfull')
            return redirect('/')
        else:
            messages.error(request, 'Conditions not fullfilled')
            return redirect('change_password')
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'login/changePassword.html',args)
