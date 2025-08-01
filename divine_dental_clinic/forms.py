from django import forms
from .models import Doctor, Admin, Patient, Queue
from django.contrib.auth.models import User


#----------ADD ADMIN FORMS-------------
class Add_Admin_UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password']
        widgets={
            'password':forms.PasswordInput(attrs={'class':'form-control mx-sm-3','placeholder':'Password'}),
            'username':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Username'})
        }

class Add_Admin_Form(forms.ModelForm):
    class Meta:
        model = Admin
        fields=['name','phone']
        widgets={
            'phone':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Phone'}),
            'name':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Name of Admin'}) 
        }

        
#----------ADD DOCTOR FORMS-------------
class Add_Doctor_UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password']
        widgets={
            'password':forms.PasswordInput(attrs={'class':'form-control mx-sm-3','placeholder':'Password'}),
            'username':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Username'})
        }

class Add_Doctor_Form(forms.ModelForm):
    class Meta:
        model = Doctor
        fields=['name','phone']
        widgets={
            'phone':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Phone'}),
            'name':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Name of Doctor'})
        }

#----------ADD PATIENT FORMS-------------
class Add_Patient_UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username','password']
        widgets={
            'password':forms.PasswordInput(attrs={'class':'form-control mx-sm-3','placeholder':'Password'}),
            'username':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Username'})
        }

class Add_Patient_Form(forms.ModelForm):
    class Meta:
        model = Patient
        fields=['first_name','last_name','phone','residence','gender','date_of_birth','email'] 
        widgets={
            'phone':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Phone'}),
            'first_name':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'First name'}),
            'last_name':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Last name'}),
            'residence':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Residence'}),
            'gender':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Male/Female'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email':forms.TextInput(attrs={'class':'form-control mx-sm-3','placeholder':'Email'}),
        }

class Queue_Patient_Form(forms.ModelForm):
    class Meta:
        model = Queue
        fields = ['number', 'id_number', 'date']
        widgets = {
            'number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Patient number'}),
            'id_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'I.D. No.'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }