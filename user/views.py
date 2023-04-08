from django.shortcuts import render
from .models import CustomUser, Candidate, Company, Education, Experience
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout

from .serializers import LoginSerializer, UserSerializer, CompanySerializer, CandidateSerializer

# rest framework
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

# email verification.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


def tokenGenerator(user):
    return RefreshToken.for_user(user)


class Activation(APIView):
    def post(request, uidb64, token):
        User = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except:
            user = None

        refresh = tokenGenerator(user)
        if user is not None and refresh.check_token(user, token):
            user.is_verified = True
            user.save()

            return Response({
                "message": "Email Verified!",
                "user_id": uid,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Invalid Activation Link!",
            }, status=status.HTTP_400_BAD_REQUEST,)



class UserActivation(APIView):
    def post(self, request):
        user = CustomUser.objects.get(id = request.query_params.get('id'))
        to_email = user.email
        refresh = tokenGenerator(user)
        mail_subject = "Verify your email for Job Buskers."
        message = render_to_string("templates/account_activation.html", {
            'user': user.name,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': str(refresh),
            "protocal": 'https' if request.is_secure() else 'http'
        })

        email = EmailMessage(mail_subject, message, to={to_email})
        if email.send():
            return Response({
                "message": "Verification link sent to your mail!",
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                "message": "Error while sending the verification mail!",
            },
                status=status.HTTP_400_BAD_REQUEST,)       


class UserRegistration(APIView):
    def post(self, request, *args, **kwargs):
        name = request.data['name']
        phone = request.data['phone']
        email = request.data['email']
        location = request.data['location']
        user_type = request.data['user_type']
        # gender = request.data['gender']
        # industry = request.data['industry']

        try:
           if CustomUser.objects.filter(email=email).exists():
                return Response({'message': 'A user with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
           elif CustomUser.objects.filter(phone=phone).exists():
                return Response({'message': 'Phone number already taken.'}, status=status.HTTP_400_BAD_REQUEST)
           else:
                print('2')
                if user_type == '2':
                    print('cs')
                    CustomUser.objects.create_user(
                        email=email,
                        password=request.data['password'],
                        name=name,
                        phone=phone,
                        location=location,
                        user_type=user_type
                    )                    
                    id = CustomUser.objects.latest('id')
                    Company.objects.create(
                        user=id,
                        industry=request.data['industry']
                    )

                elif user_type=='3':
                    print('cs')
                    CustomUser.objects.create_user(
                        email = email,
                        password = request.data['password'],
                        name=name,
                        phone=phone,
                        location=location,
                        user_type=user_type
                    )
                    id = CustomUser.objects.latest('id')
                    Candidate.objects.create(
                        user=id,
                        gender=request.data['gender']
                    )               
                
                return Response({'message': 'User Registration successful.'}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Registration Error.'}, status=status.HTTP_200_OK)

class UserLogin(APIView):
    def get(self, request):    
        user = User.objects.all()
        serializer = UserSerializer(user, many= True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            print("working")
            email = request.data['email']
            password = request.data['password']
            
        try:
            print(email)
            print(password)
            user = authenticate(
                username=email, 
                password=password
            )
            print('  ')
            print(user)
            if user is not None:
                # refresh = RefreshToken.for_user(user)
                login(request, user)
                print("login")

                userDetail = CustomUser.objects.get(email=email)
                print('done')
                serializer = LoginSerializer(userDetail, many=False)

                # response = {   
                #     # "refresh": str(refresh),
                #     # "access": str(refresh.access_token),  
                #     "user_data": serializer.data,         
                # }
                print(serializer.data)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response({"message": "User doesnot exist", }, status=status.HTTP_400_BAD_REQUEST)
            
            # return Response({"message": "Login Successful", }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({"message": "Email or password doesn't match!", }, status=status.HTTP_400_BAD_REQUEST)
        
# change password.
class ChangePw(APIView):
    def put(self, request, *args, **kwargs):
        try:
            newPw = request.data['password']
            rePw = request.data['repassword']

            if newPw == rePw:
                user = CustomUser.objects.get(email=request.user)
                user.set_password(newPw)
                user.save()
                return Response({"message":"The password has been reset."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Password does not match."}, status=status.HTTP_409_CONFLICT)
        except Exception as e:
            print(e)
            return Response({"message": "Error!", }, status=status.HTTP_400_BAD_REQUEST, )

# update user
class UpdateDetails(APIView):

    def put(self, request):
        try:        
            user_detail = CustomUser.objects.get(id = request.query_params.get('user'))
            # print(user_detail)
            # if request.data['display_picture'] is not None and request.data['display_picture'] != '':
            #     user_detail.display_picture = request.data['display_picture']
            
            print('name')
            if request.data['name'] is not None and request.data['name'] != '':
                user_detail.name = request.data['name']

            # if request.data['email'] is not None and request.data['email'] != '':
            #     user_detail.email = request.data['email']

            if request.data['phone'] is not None and request.data['phone'] != '':
                user_detail.phone = request.data['phone']

            if request.data['address'] is not None and request.data['address'] != '':
                user_detail.location = request.data['address']

            if request.data['description'] is not None and request.data['description'] != '':
                user_detail.description = request.data['description']
            
            if user_detail.user_type == '2':
                company = Company.objects.get(user=user_detail.id)
                if request.data['website'] is not None and request.data['website'] != '':
                    user_detail.website = request.data['website']

                if request.data['est_year'] is not None and request.data['est_year'] != '':
                    user_detail.est_year = request.data['est_year']

            
            user_detail.save()
            return Response({"message": "User detail(s) updated!", }, status=status.HTTP_200_OK, )
        except:
            return Response({
                "message": "Error!",
            },
                status=status.HTTP_400_BAD_REQUEST, )

    # def get(self, request, *args, **kwargs):
    #     userData = CustomUser.objects.get(email=request.user)
    #     serializer = UserSerializer(userData, many=False)
    #     return Response(serializer.data, status=status.HTTP_200_OK)


class GetCompany (APIView):
    def get(self,request):
        try:
            company = Company.objects.get(user = request.query_params.get('user'))
            print(company)
            serializer = CompanySerializer(company, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)


class GetCandidate (APIView):
    def get(self,request):
        try:
            candidate = Candidate.objects.get(user = request.query_params.get('user'))
            print(candidate)
            serializer = CandidateSerializer(candidate, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Company not found'}, status=status.HTTP_404_NOT_FOUND)
        

class Education (APIView):
    def get(self, request):
        try:
            education = Education.objects.filter(candidate= request.query_params.get('user'))
            serializer = CandidateSerializer(education, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)            
        except Exception as e:
            print(e)
            return Response({'message': 'Education not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def post(self, request, *args, **kwargs):    
        try:
            candidate = CustomUser.objects.get(id = request.query_params.get('user'))
            # testing correct object
            print(candidate)
            Education.objects.create(
                institute = request.data['institute'],
                address = request.data['address'],
                start_year = request.data['start_year'],
                end_year = request.data['end_year'],
                candidate_id = candidate.id
            )
            education =  Education.objects.latest('id')
            serializer = CandidateSerializer(education, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Education could not be created'}, status=status.HTTP_404_NOT_FOUND)


class SubEducation (APIView):
    def put(self, request, *args, **kwargs):
        try:
            education = Education.objects.get(id = request.query_params.get('id'))

            if request.data['institute'] is not None and request.data['institute'] != '':
                education.institute = request.data['institute']

            if request.data['address'] is not None and request.data['address'] != '':
                education.address = request.data['address']
            
            if request.data['start_year'] is not None and request.data['start_year'] != '':
                education.start_year = request.data['start_year']
            
            if request.data['end_year'] is not None and request.data['end_year'] != '':
                education.end_year = request.data['end_year']
            
            education.save()
            return Response({"message": "Education updated!", }, status=status.HTTP_200_OK, )
        except:
            return Response({"message": "Error!",}, status=status.HTTP_400_BAD_REQUEST, )
        
    # def delete(self, request):
    #     try:
    #         education = Education.objects.get(id = request.query_params.get('id'))
            
        


        

class Experience (APIView):
    def get(self, request):
        try:
            exp = Experience.objects.filter(candidate= request.query_params.get('user'))
            serializer = CandidateSerializer(exp, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)            
        except Exception as e:
            print(e)
            return Response({'message': 'Experience not found'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):    
        try:
            candidate = CustomUser.objects.get(id = request.query_params.get('user'))
            # testing correct object
            print(candidate)
            Experience.objects.create(
                company = request.data['company'],
                job_title = request.data['job_title'],
                address = request.data['address'],
                start_year = request.data['start_year'],
                end_year = request.data['end_year'],
                description = request.data['description'],
                candidate_id = candidate.id
            )
            exp =  Education.objects.latest('id')
            serializer = CandidateSerializer(exp, many=False)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Experience could not be created'}, status=status.HTTP_404_NOT_FOUND)

class SubExperience(APIView):
    def put(self, request, *args, **kwargs):
        try:
            experience = Experience.objects.get(id = request.query_params.get('id'))

            if request.data['company'] is not None and request.data['company'] != '':
                experience.company = request.data['company']

            if request.data['job_title'] is not None and request.data['job_title'] != '':
                experience.job_title = request.data['job_title']

            if request.data['address'] is not None and request.data['address'] != '':
                experience.address = request.data['address']
            
            if request.data['start_year'] is not None and request.data['start_year'] != '':
                experience.start_year = request.data['start_year']
            
            if request.data['end_year'] is not None and request.data['end_year'] != '':
                experience.end_year = request.data['end_year']
            
            if request.data['description'] is not None and request.data['description'] != '':
                experience.description = request.data['description']
            
            experience.save()
            return Response({"message": "experience updated!", }, status=status.HTTP_200_OK, )
        except:
            return Response({"message": "Error!",}, status=status.HTTP_400_BAD_REQUEST, )