from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user.models import Company, CustomUser

from .models import Bookmarks, Jobs, JobRoles, JobRequirements, JobApplication

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import ApplicationSerializer, BookmarkSerializer, CompanyJobSerializer, JobPageSerializer, JobsSerializer, RequirementSerializer, RoleSerializer

from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
# @login_required
class AddJobs(APIView):
    # permission_classes=[IsAuthenticated]
    def post(self, request, pk, *args, **kwargs):
        try:
            print(pk)
            company = Company.objects.get(id = pk)
            print(company.user)
            Jobs.objects.create(
                title = request.data['title'],
                address = request.data['address'],
                industry = request.data['industry'],
                job_type = request.data['job_type'],
                status = request.data['status'],
                salary = request.data['salary'],
                level = request.data['level'],
                company_id_id = company.id
            )
            job = Jobs.objects.latest('id')
            serializer = JobsSerializer(job, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'message': 'Vacancy could not be posted'}, status=status.HTTP_400_BAD_REQUEST)

class JobRole(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            print(pk)
            job = Jobs.objects.latest('id')
            print(job)
            JobRoles.objects.create(
                job_id_id = job.id,
                roles = request.data['roles'],
            )
            print('after')
            return Response({'message': 'Roles updated successfully.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'message': 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)
        
class JobReqs(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            print(pk)
            job = Jobs.objects.latest('id')
            print(job)
            JobRequirements.objects.create(
                job_id_id = job.id,
                requirements = request.data['requirements'],
            )
            print('after')
            return Response({'message': 'Requirements updated successfully.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({'message': 'Invalid'}, status=status.HTTP_400_BAD_REQUEST)

class GetJob(APIView):
    def get(self, request):
        try:
            jobs = Jobs.objects.all()
            serializer = JobsSerializer(jobs, many=True)
            
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Jobs not found'}, status=status.HTTP_404_NOT_FOUND)


class Bookmark(APIView):
    def get(self, request):
        try:
            bookmark_user = Bookmarks.objects.filter(user=request.query_params.get('user'))
            serializer = BookmarkSerializer(bookmark_user, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Bookmarks not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(id = request.query_params.get('user'))
            job = Jobs.objects.get(id = request.data['job_id'])
            print(user)
            print(job)
            Bookmarks.objects.create(
                user_id = user.id,
                job_id = job.id
            )
            bookmark = Bookmarks.objects.latest('id')
            serializer = BookmarkSerializer(bookmark, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)            
        except Exception as e:
            print(e)
            return Response({'message': 'Bookmark could not be created'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try:
            bookmark = Bookmarks.objects.get(id=request.query_params.get('id'))
            bookmark.delete()

            new_bookmark = Bookmarks.objects.all()
            serializer = BookmarkSerializer(new_bookmark, many = True)

            return Response(serializer.data, status=status.HTTP_200_OK)
            # return Response({'message': 'Bookmark deleted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Bookmarks not found'}, status=status.HTTP_404_NOT_FOUND)
        


class CompanyJob(APIView):
    def get(self, request):
        try:
            jobs = Jobs.objects.filter(company_id=request.query_params.get('company'))
            serializer = CompanyJobSerializer(jobs, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Jobs not found'}, status=status.HTTP_404_NOT_FOUND)
        
# class JobPage(APIView):
#     def get(self, request):
#         try:
#             jobs = Jobs.objects.get(id=request.query_params.get('job'))
            
#             serializer = JobPageSerializer(jobs, many=False)

#             return Response(serializer.data, status=status.HTTP_200_OK)
#         except Exception as e:
#             print(e)
#             return Response({'message': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)
        

class JobPage(APIView):
    def get(self, request):
        try:
            jobs = Jobs.objects.get(id=request.query_params.get('job'))
            job_serializer = JobPageSerializer(jobs, many=False)

            requirements = JobRequirements.objects.filter(job_id = request.query_params.get('job'))
            reqs_serializer = RequirementSerializer(requirements, many=True)

            roles = JobRoles.objects.filter(job_id = request.query_params.get('job'))
            roles_serializer = RoleSerializer(roles, many=True)

            context = {
                'job':job_serializer.data,
                'reqs':reqs_serializer.data,
                'roles':roles_serializer.data,
            }

            return Response(context, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)


class GetRequirements(APIView):
    def get(self, request):
        try:
            reqs = JobRequirements.objects.get(job_id = request.query_params.get('job'))
            serializer = RequirementSerializer(reqs, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Requirement not found'}, status=status.HTTP_404_NOT_FOUND)
        

class GetRoles(APIView):
    def get(self, request):
        try:
            roles = JobRoles.objects.filter(job_id = request.query_params.get('job'))
            serializer = RoleSerializer(roles, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Role not found'}, status=status.HTTP_404_NOT_FOUND)
        

class CandidateApplication(APIView):
    def get(self, request):
        try:
            apply = JobApplication.objects.filter(candidate = request.query_params.get('user'))
            serializer = ApplicationSerializer(apply, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)  
        except Exception as e:
            print(e)
            return Response({'message': 'No Applications'}, status=status.HTTP_404_NOT_FOUND)
    

class ApplyJob(APIView):
    def post(self, request, *args, **kwargs):    
        try:
            candidate = CustomUser.objects.get(id = request.query_params.get('user'))
            job = Jobs.objects.get(id = request.data['job'])
            # testing correct object
            print(job)
            print(candidate)
            JobApplication.objects.create(
                applicant_name = request.data['applicant_name'],
                email = request.data['email'],
                cv = request.data['cv'],
                cover_letter = request.data['cover_letter'],
                job_id = job.id,
                candidate_id = candidate.id
            )
            # application =  JobApplication.objects.latest('id')
            # serializer = ApplicationSerializer(application, many=False)
            # return Response(serializer.data, status=status.HTTP_200_OK) 

            return Response({'message': 'Application posted'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Application could not be posted'}, status=status.HTTP_404_NOT_FOUND)
        
class CompanyApplication(APIView):
    def get(self, request):
        try:
            job = Jobs.objects.get(id = request.query_params.get('job'))
            apply = JobApplication.objects.filter(job = job.id)
            serializer = ApplicationSerializer(apply, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)        
        except Exception as e:
            print(e)
            return Response({'message': 'Applicaion(s) not found.'}, status=status.HTTP_404_NOT_FOUND)
        

class SearchJobs(ListAPIView):
    queryset = Jobs.objects.all()
    serializer_class = CompanyJobSerializer
    # pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'industry',]

