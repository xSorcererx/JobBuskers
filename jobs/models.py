from django.db import models
from user.models import CustomUser, Company, Candidate

class Jobs(models.Model):
    industry_selections = [('Architechture/ Interior Designing', 'Architechture/ Interior Designing'), 
                  ('IT & Telecommunication', 'IT & Telecommunication'), 
                  ('Teaching/ Education', 'Teaching/ Education'),
                  ('NGO/ INGO', 'NGO/ INGO'), 
                  ('Graphics/ Designing', 'Graphics/ Designing'),
                  ('Hospitality', 'Hospitality'), 
                  ('Sales/ Public Relation', 'Sales/ Public Relation'), 
                  ('Legal Services', 'Legal Services'),
                  ('Other', 'Other')]
    
    status_selections = [('On-Site', 'On-Site'),
                    ('Remote', 'On-Site'),
                    ('Hybrid', 'Hybrid')]
    
    level_selections = [('Senior', 'Senior'),
                    ('Mid-level', 'Mid-level'),
                    ('Junior', 'Junior'),]

    title = models.CharField(max_length=250, null=False, blank=False)
    address = models.CharField(max_length=50, null=False,blank=False)
    industry = models.CharField('Industry', max_length=200,    
            choices=industry_selections, null=False, default='Other')
    job_type = models.CharField('Status', max_length=200,   
            choices=status_selections, default='On-Site', null=False)
    salary = models.CharField(max_length=20, default='Negotiable', null=False)
    level = models.CharField('Level', max_length=200,   
            choices=level_selections, default='Junior', null=False)
    status = models.BooleanField(default=True)
    company_id = models.ForeignKey(to=Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    


class JobRoles(models.Model):
    job_id = models.ForeignKey(to=Jobs, on_delete=models.CASCADE)
    roles = models.CharField(max_length=1500, null=False, blank=False)


class JobRequirements(models.Model):
   job_id = models.ForeignKey(to=Jobs, on_delete=models.CASCADE)
   requirements = models.CharField(max_length=1500, null=False, blank=False)

class Bookmarks(models.Model):
    user = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(to=Jobs, on_delete=models.CASCADE)

class JobApplication(models.Model):
    candidate = models.ForeignKey(to=CustomUser, on_delete=models.CASCADE)
    job = models.ForeignKey(to=Jobs, on_delete=models.CASCADE)
    cover_letter = models.CharField(max_length=200, blank=True, null=True)
    applicant_name = models.CharField(max_length=20, blank=False, null=False)
    email = models.EmailField(null=False, blank=False)
    cv = models.FileField(upload_to='files', null=True, blank=True)

