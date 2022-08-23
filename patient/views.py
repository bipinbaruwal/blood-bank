from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum,Q
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.auth.models import User
from blood import forms as bforms
from blood import models as bmodels


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.bloodgroup=patientForm.cleaned_data['bloodgroup']
            patient.save()
            
            subject = 'WELCOME TO BLOOD BANK'
            message = 'You have been register to blood bank successfully.\n Thank you for being a family of Blood Bank.\n This system has recieved your registration and you can use the details to log in to the website make blood request or pledge to donate it.\n For futher details you can mail at naemi.shrestha63@gmail.com \n Regards,\n Blood Bank'
            
            from_email = settings.EMAIL_HOST_USER
            to_list = userForm.cleaned_data.get('email')

            send_mail(subject, message, from_email, [to_list], fail_silently=True)

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patient/patientsignup.html',context=mydict)

def patient_dashboard_view(request):
    data = []
    patient= models.Patient.objects.get(user_id=request.user.id)
    # image = models.Blood.objects.get(image = image)
    # title = models.Blood.objects.get(title = title)
    # content = models.Blood.objects.get(content = content)
    art = bmodels.Articles.objects.all()

    for datas in art:
        data.append(datas)
    data.reverse()
    dict={
        'requestpending': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Pending').count(),
        'requestapproved': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Approved').count(),
        'requestmade': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).count(),
        'requestrejected': bmodels.BloodRequest.objects.all().filter(request_by_patient=patient).filter(status='Rejected').count(),
        'data': data,
        'art':art
    }

    return render(request,'patient/patient_dashboard.html',context=dict)

def make_request_view(request):
    request_form=bforms.RequestForm()
    if request.method=='POST':
        request_form=bforms.RequestForm(request.POST)
        if request_form.is_valid():
            blood_request=request_form.save(commit=False)
            blood_request.bloodgroup=request_form.cleaned_data['bloodgroup'] 
            patient= models.Patient.objects.get(user_id=request.user.id)
            blood_request.request_by_patient=patient
            blood_request.save()
            return HttpResponseRedirect('my-request')  
    return render(request,'patient/makerequest.html',{'request_form':request_form})

def my_request_view(request):
    patient= models.Patient.objects.get(user_id=request.user.id)
    blood_request=bmodels.BloodRequest.objects.all().filter(request_by_patient=patient)
    return render(request,'patient/my_request.html',{'blood_request':blood_request})

def patient_article(request):
    data =[]
    art = bmodels.Articles.objects.all()

    for datas in art:
        data.append(datas)
    data.reverse()

    content = {'data': data}
    return render(request, 'patient/patient_article.html', content)
