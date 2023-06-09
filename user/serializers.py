from rest_framework import serializers
from .models import CustomUser, Candidate, Company, Education, Experience, NotificationToken, Recommendation

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['user_type', 'id']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['name', 'display_picture', 'email', 'location', 'description', 'phone']

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only = True)
    class Meta:
        model = Company
        fields = '__all__'

class CandidateSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only = True)
    class Meta:
        model = Candidate
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationToken
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = '__all__'