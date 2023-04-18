from django.db import models
from .UserManager import CustomUserManager

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField


# custom user.
class CustomUser (AbstractBaseUser, PermissionsMixin):
    display_picture = models.ImageField(upload_to='images/user', help_text='Display picture containing a person or a logo.', null=True, blank=True)  
    name = models.CharField(max_length=20, null=False)
    phone = PhoneNumberField(null=True, blank=True, unique=True)
    email = models.EmailField(_('email_address'), unique=True, max_length=200)
    location = models.CharField(max_length=30, null=True, blank=True)
    description =  models.CharField(max_length=900, null=True, blank=True)    
    is_verified = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=False) 
    is_staff = models.BooleanField(default=False)
    
    # user type choices
    class UserType(models.IntegerChoices):
        ADMIN = 1, _('Admin'),
        COMPANY = 2, _('Company'),        
        CANDIDATE = 3, _('Candidate')
    user_type = models.IntegerField(choices=UserType.choices, blank=True, null=True)

    #  Custom username
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'location',]

    # user manager
    objects = CustomUserManager()

    def __str__(self):
        return self.name


    # User roles
    @property
    def admin(self):
        return self.user_type == self.UserType.ADMIN

    @property
    def company(self):
        return self.user_type == self.UserType.COMPANY
        
    @property
    def candidate(self):
        return self.user_type == self.UserType.CANDIDATE

# candidate table
class Candidate(models.Model):
    # Gender Selections
    gender_selection = [('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')]

    pref_selection = [('Architechture/ Interior Designing', 'Architechture/ Interior Designing'), 
                  ('IT & Telecommunication', 'IT & Telecommunication'), 
                  ('Teaching/ Education', 'Teaching/ Education'),
                  ('NGO/ INGO', 'NGO/ INGO'), 
                  ('Graphics/ Designing', 'Graphics/ Designing'),
                  ('Hospitality', 'Hospitality'), 
                  ('Sales/ Public Relation', 'Sales/ Public Relation'), 
                  ('Legal Services', 'Legal Services'),
                  ('Other', 'Other')]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField('Gender', max_length=8, 
            choices=gender_selection, default='Male', null=False)
    preference = models.CharField('Preference', max_length=200, 
            choices=pref_selection, default='Other', null=False)

    def __str__(self):
        return self.user.name

# company table
class Company(models.Model):
    selections = [('Architechture/ Interior Designing', 'Architechture/ Interior Designing'), 
                  ('IT & Telecommunication', 'IT & Telecommunication'), 
                  ('Teaching/ Education', 'Teaching/ Education'),
                  ('NGO/ INGO', 'NGO/ INGO'), 
                  ('Graphics/ Designing', 'Graphics/ Designing'),
                  ('Hospitality', 'Hospitality'), 
                  ('Sales/ Public Relation', 'Sales/ Public Relation'), 
                  ('Legal Services', 'Legal Services'),
                  ('Other', 'Other')]
    
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    industry = models.CharField('Industry', max_length=200,     
            choices=selections, null=False, default='Other')
    website = models.CharField(max_length=20, null=True, blank=True)    
    est_year = models.PositiveSmallIntegerField(null=True, blank=True)
    banner_image = models.ImageField(upload_to='images/user/company', help_text='Job Banner', null=True, blank=True)
    
    
    
    def __str__(self):
        return self.user.name


# Education
class Education(models.Model):
    candidate = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    institute = models.CharField(max_length=25, null = False)
    address = models.CharField(max_length=25)
    start_year = models.CharField(max_length=4, null=False)
    end_year = models.CharField(max_length=4, null=True)


#Experience
class Experience(models.Model):
    candidate = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    company = models.CharField(max_length=25, null = False)
    job_title = models.CharField(max_length=25)
    address = models.CharField(max_length=25)
    start_year = models.CharField(max_length=4, null=False)
    end_year = models.CharField(max_length=4, null=True)
    description = models.CharField(max_length=200, null=True)
