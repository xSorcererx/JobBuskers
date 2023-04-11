from django.urls import path
from .views import AddJobs, JobRole, JobReqs, GetJob, CompanyJob, JobPage, GetRoles, GetRequirements, Bookmark, CandidateApplication, CompanyApplication

urlpatterns = [
    path('add_job/<int:pk>/', AddJobs.as_view(), name='add_job'),

    path('get_job/', GetJob.as_view(), name='get_job'),
    path('company_jobs/', CompanyJob.as_view(), name='company_job'),
    path('job_page/', JobPage.as_view(), name='job'),

    path('get_roles/', GetRoles.as_view(), name='get_roles'),
    path('get_requirements/', GetRequirements.as_view(), name='get_requirements'),

    path('job_roles/<int:pk>/', JobRole.as_view(), name='job_roles'),
    path('job_reqs/<int:pk>/', JobReqs.as_view(), name='job_reqs'),

    path('bookmarks/', Bookmark.as_view(), name='bookmarks'),
    
    
    path('apply/', CandidateApplication.as_view(), name='apply'),
    path('view_job_applications/', CompanyApplication.as_view(), name='company-application-history'),

]
