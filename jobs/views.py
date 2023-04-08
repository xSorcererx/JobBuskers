from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from user.models import Company, CustomUser

from .models import Bookmarks, Jobs, JobRoles, JobRequirements

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator

from .serializers import BookmarkSerializer, CompanyJobSerializer, JobPageSerializer, JobsSerializer, RequirementSerializer, RoleSerializer

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


class Booking(APIView):
    def get(self, request):
        try:
            bookmark_user = Bookmarks.objects.filter(user=request.query_params.get('user'))
            serializer = BookmarkSerializer(bookmark_user, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Bookmarks not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request):
        try:
            user = CustomUser.objects.get(id = request.query_params.get('user'))
            job = Jobs.objects.get(job = request.query_params.get('job'))
            # testing correct object
            print(user)
            print(job)
            Bookmarks.objects.create(
                user_id = user.id,
                job_id = job.id
            )
        except Exception as e:
            print(e)
            return Response({'message': 'Bookmark could not be created'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request):
        try:
            bookmark = Bookmarks.objects.get(id=request.query_params.get('id'))
            bookmark.delete()
            return Response({'message': 'Bookmark deleted'}, status=status.HTTP_200_OK)
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
