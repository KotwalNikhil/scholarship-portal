from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import student,staff
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

def user_login(request,register):
    if request.method=='POST':
        regno =request.POST['reg_no']
        pass2 = request.POST['pass']


        if register==True:

            user = auth.authenticate(username=regno, password=pass2)

            if user is not None and user.is_staff :
                auth.login(request,user)
                return redirect('/')

            else:
                return HttpResponse('invalid credintials')

        else :
            user = auth.authenticate(username=regno, password=pass2)


            if user is not None and user.is_staff is False :
                auth.login(request,user)
                return redirect('/')
            else:
                return HttpResponse('invalid credintials')


    else:
        return render(request, 'login/login.html', {'register':register})



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
                return render(request,'login/login.html')
            elif User.objects.filter(username=regno).exists():
                messages.info(request, 'username taken')
                return render(request,'login/login.html')
            else:
                user = User.objects.create_user(first_name=fname,username=regno,password=pass1,email=email,is_staff=False)
                user.save();

                stu=student.objects.create(name=fname,email=email,reg_no=regno)
                stu.save()


                return render(request, 'login/login.html')

        else :
            messages.info(request,'password not matched')
            return render(request,'login/login.html')
    else:
        return render(request,'login/register.html')



def admin_register(request):
    if request.method=='POST':
        empno = request.POST['emp_number']
        fname = request.POST['fname']
        admin_branch = request.POST['branch']
        # pass2 = request.POST['pass2']
        email = request.POST['email']
        # if pass1==pass2:
        if User.objects.filter(email=email).exists():
            messages.info(request,'email taken')
            return HttpResponse("<h2>email taken</h2>")
        elif User.objects.filter(username=empno).exists():
            messages.info(request, 'username taken')
            return HttpResponse("<h2>username taken</h2>")
        else:
            user = User.objects.create_user(first_name=fname,username=empno,password="12345",email=email,is_staff=True)
            user.save();

            staf=staff.objects.create(name=fname,email=email,emp_no=empno,branch=admin_branch)
            staf.save()


            return HttpResponse("<h2>registration successfull</h2>")

        # else :
        #     messages.info(request,'password not matched')
        #     return render(request,'login/login.html')
    else:
        return render(request,'login/admin_register.html')



def logout(request):
    auth.logout(request)
    return redirect('/')


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


def change_password(request):
    if request.method=='POST':
        form=PasswordChangeForm(data=request.POST,user=request.user)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            return redirect('/')
        else:
            return redirect('change_password')
    else:
        form=PasswordChangeForm(user=request.user)
        args={'form':form}
        return render(request,'login/changePassword.html',args)
