from django.contrib import admin
from .models import Jobs, JobRequirements, JobRoles, Bookmarks

admin.site.register(Jobs)
admin.site.register(JobRoles)
admin.site.register(JobRequirements)
admin.site.register(Bookmarks)