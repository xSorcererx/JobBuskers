from django.forms import ModelForm
from user.models import CustomUser, Candidate, Company


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['name', 'location', 'email', 'phone', 'user_type']


class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['gender']


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['industry', 'website', 'est_year']