from rest_framework import serializers
from .models import Jobs, JobRoles, JobRequirements, Bookmarks, JobApplication
from user.serializers   import CompanySerializer

class JobsSerializer(serializers.ModelSerializer):
    company_id = CompanySerializer(many=False, read_only=True)
    class Meta:
        model = Jobs
        fields = ['id', 'title', 'address', 'company_id', 'job_type', 'level', ]

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmarks
        fields = '__all__'

class CompanyJobSerializer(serializers.ModelSerializer):
     class Meta:
        model = Jobs
        fields = ['id', 'title', 'company_id', 'job_type', 'level', 'industry']
class RequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobRequirements
        fields = '__all__'


class JobPageSerializer(serializers.ModelSerializer):
#      job_id = RoleSerializer(many=True, read_only=True)
#      job_id = RequirementSerializer(many=True, read_only=True)
    company_id = CompanySerializer(many=False, read_only=True)

    class Meta:
        model = Jobs
        fields = '__all__'

class RoleSerializer(serializers.ModelSerializer):
#      job_id = JobPageSerializer(many=False, read_only=True)
# #      job_id = RequirementSerializer(many=False, read_only=True)
     class Meta:
        model = JobRoles
        fields = ['roles', 'id', 'job_id']

class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'