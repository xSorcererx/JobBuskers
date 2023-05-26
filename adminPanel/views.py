from django.shortcuts import render, redirect
from django.http import HttpResponse

from user.models import CustomUser, Company, Candidate
from django.contrib import messages
from .forms import CustomUserForm, CandidateForm, CompanyForm
from django.contrib.auth. models import auth
from django.contrib.auth.decorators import login_required
from jobs.models import Jobs


def loginPage(request):
    try:
        if request.user.is_authenticated:
                return redirect('dashboard/')
        else:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']

                admin = CustomUser.objects.get(email=username)

                if admin.user_type == 1:
                    users = auth.authenticate(
                        username=username, password=password)

                    if users is not None:
                        auth.login(request, users)
                        return redirect('dashboard/')
                    else:
                        messages.error(request, "Invalid user or password!")
                        return redirect('/')
                else:
                    return HttpResponse("You are not authorized to this page.")
            else:
                return render(request, 'login.html')
    except:
        messages.error(request, "Invalid user or password!")
        return redirect('/')


@login_required(login_url='/')
def dashboard(request):
    company = CustomUser.objects.filter(user_type='2').count()
    candidate = CustomUser.objects.filter(user_type='3').count()
    jobs = Jobs.objects.all().count()

    flutter = Jobs.objects.filter(title='Flutter Developer').count()
    react = Jobs.objects.filter(title='React Developer').count()
    django = Jobs.objects.filter(title='Django Developer').count()
    receptionist = Jobs.objects.filter(title='Receptionist').count()

    response = {
        'compCount': company,
        'candCount': candidate,
        'title': 'Dashboard',
        'jobCount': jobs,
        'flutterCount': flutter,
        'reactCount': react,
        'djangoCount': django,
        'receptionistCount': receptionist,
    }

    return render(request, 'dashboard.html', response)


def logoutUser(request):
    auth.logout(request)
    return redirect('/')


@login_required(login_url='/')
def addCandidate(request):
    form=CustomUserForm
    cand_form=CandidateForm

    if request.method == 'POST':
        pw = request.POST['password']
        confirm_pw = request.POST['confirm_password']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        location = request.POST['location']
        gender = request.POST['gender']
        user_type = '3'

        if pw == confirm_pw:
            CustomUser.objects.create_user(
                email=email,
                password=pw,
                name=name,
                phone=phone,
                location=location,
                is_verified=True,
                user_type=user_type
            )

            id = CustomUser.objects.latest('id')
            Candidate.objects.create(
                user=id,
                gender=gender,
            )
        else:
            messages.info(request, 'Your password does not match.')

    userData = CustomUser.objects.filter(user_type='3')
    candData = Candidate.objects.all()
   
    context = {
        'form': form,
        'cand_form': cand_form,
        'userData': userData,
        'candData': candData,
        'title': 'Candidates'
    }
    return render(request, 'candidate.html', context)



@login_required(login_url='/')
def addCompany(request):
    form = CustomUserForm
    comp_form = CompanyForm
    if request.method == 'POST':
        pw = request.POST['password']
        confirm_pw = request.POST['confirm_password']
        name = request.POST['name']
        phone = request.POST['phone']
        email = request.POST['email']
        location = request.POST['location']
        user_type = '3'

        if pw == confirm_pw:
            CustomUser.objects.create_user(
                email=email,
                password=pw,
                name=name,
                phone=phone,
                location=location,
                user_type=user_type,
                is_verified=True
            )

            id = CustomUser.objects.latest('id')
            Company.objects.create(
                user=id,
                industry=request.POST['industry'],
            )
        else:
            messages.info(request, 'Your password does not match.')

    userData = CustomUser.objects.filter(user_type='2')
    compData = Company.objects.all()
   
    context = {
               'form': form,
               'comp_form': comp_form,
               'userData': userData,
               'compData': compData,
               'title': 'Companies'
               }
    return render(request, 'company.html', context)



@login_required(login_url='/')
def deleteUser(request, pk):
    uid = CustomUser.objects.get(id=pk)
    uid.delete()
    return redirect('/')


@login_required(login_url='/')
def getJobs(request):
    job_detail=Jobs.objects.all()
    print(job_detail)
    context = {
        'job_detail': job_detail,

        'title': 'Job Details'
    }
    return render(request, 'job.html', context)

