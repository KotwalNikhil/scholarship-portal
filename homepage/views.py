from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

from .models import scholarship
def home(request):
    scholarships=scholarship.objects.all()
    if request.user.is_authenticated:
        return render(request,'homepage/index.html',{'all_scholar':scholarships})
    else:
        return render(request,'homepage/welcome_page.html',{'all_scholar':scholarships})


def user_profile(request):
    return render(request,'homepage/profile.html')

def basic(request):
    return render(request,'homepage/basic.html')

def show_application_form(request,x):
    if request.user.is_authenticated:
        current_scholarship = scholarship.objects.get(pk=x)
        return render(request,'homepage/application_form.html',{'current_scholarship':current_scholarship})
    else:
        return render(request,'login/login.html')
def show_scholarship_template(request,x):
    current_scholarship=scholarship.objects.get(pk=x)
    return render(request, 'homepage/scholoarship_template.html',{'current_scholarship':current_scholarship})


# def pdf_view(request,x):
#     s = scholarship.objects.get(pk=x)
#     with open('Receipt-nik.pdf', 'rb') as pdf:
#         response = HttpResponse(pdf.read(),content_type='application/pdf')
#         response['Content-Disposition'] = 'filename=Receipt-nik.pdf'
#         return response
#
def pdf_view(request,x):
    s = scholarship.objects.get(pk=x)
    pdf_name=s.document
    path='media/'+str(pdf_name)
    image_data = open(path, 'rb').read()
    return HttpResponse(image_data, content_type='application/pdf')