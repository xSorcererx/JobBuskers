from django.contrib import admin
from .models import CustomUser, Company, Candidate, Education, Experience, NotificationToken


# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Candidate)
admin.site.register(Company)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(NotificationToken)