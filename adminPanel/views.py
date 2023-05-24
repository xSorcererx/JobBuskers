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
                    users = auth.authenticate(username=username, password=password)

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
    form = CustomUserForm
    cand_form = CandidateForm

    if request.method == 'POST':
        pw = request.POST['password']
        confirm_pw = request.POST['confirm_password']
        if pw == confirm_pw:
            form = CustomUserForm(request.POST)
            cand_form = CandidateForm(request.POST)

            if form.is_valid():
                user_instance=form.save(commit=False)
                user_instance.user_type = '3'
                user_instance.password = pw
                user_instance.is_active=True
                user_instance.save()
                new_sp = Candidate.objects.latest('id')

                if cand_form.is_valid():
                    instance = cand_form.save(commit=False)
                    instance.user = new_sp.id
                    instance.save()
                return redirect('../candidate')
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
        if pw == confirm_pw:
            form = CustomUserForm(request.POST)
            comp_form = CompanyForm(request.POST)

            if form.is_valid():
                user_instance=form.save(commit=False)
                user_instance.user_type = '2'
                user_instance.password = pw
                user_instance.is_active=True
                user_instance.save()
                new_sp = Company.objects.latest('id')

                if comp_form.is_valid():
                    instance = comp_form.save(commit=False)
                    instance.user = new_sp.id
                    instance.save()
                return redirect('../company')
        else:
            messages.info(request, 'Your password does not match.')

    userData = CustomUser.objects.filter(user_type='2')
    compData = Company.objects.all()
   
    context = {
               'form': form,
               'comp_form': comp_form,
               'userData': userData,
               'compData': compData,
               'title': 'Company'
               }
    return render(request, 'company.html', context)



@login_required(login_url='/')
def deleteUser(request, pk):
    uid = CustomUser.objects.get(id=pk)
    uid.delete()
    return redirect('user/')    


@login_required(login_url='/')
def getJobs(request):
    job_detail=Jobs.objects.all()
    print(job_detail)
    context = {
        'job_detail': job_detail,

        'title': 'Job Details'
    }
    return render(request, 'job.html', context)

