from django.contrib import admin
from .models import Jobs, JobRequirements, JobRoles, Bookmarks, JobApplication

admin.site.register(Jobs)
admin.site.register(JobRoles)
admin.site.register(JobRequirements)
admin.site.register(Bookmarks)
admin.site.register(JobApplication)