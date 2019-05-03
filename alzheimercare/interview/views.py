from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Interview
from .forms import InterviewForm, AdultForm, ContextForm, TutorForm, CaregiverForm, ProcessForm
from alzheimercare.decorators import restricted_for_caregivers

@login_required
@restricted_for_caregivers
def index(request):
    context = {}
    interviews = Interview.objects.all()
    context['interviews_list'] = interviews
    return render(request,'interview/index.html', context)

@login_required
@restricted_for_caregivers
def add_interview(request):
    context = {}
    if request.method == 'POST':
        interviewForm = InterviewForm(request.POST)
        if interviewForm.is_valid():
            interviewForm.save()
        return HttpResponseRedirect('/entrevistas/')
    else:
        form = InterviewForm()
        context['form'] = form
    return render(request,'interview/add_interview.html', context)

@login_required
@restricted_for_caregivers
def answer_interview(request, interview_id):
    context = {}
    interview = get_object_or_404(Interview, pk = interview_id)
    context['interview'] = interview
    return render(request, 'interview/answer_interview.html', context)

@login_required
@restricted_for_caregivers
def add_adult(request, interview_id):
    context = {}
    if request.method == 'POST':
        adultForm = AdultForm(request.POST)
        if adultForm.is_valid():
            adultForm.save()
        return HttpResponseRedirect('/entrevistas/')
    else:
        interview = Interview.objects.get(pk = interview_id)
        form = AdultForm(initial = {'interview':interview_id})
        context['interview'] = interview
        context['form'] = form
    return render(request,'interview/add_adult.html', context)

@login_required
@restricted_for_caregivers
def add_context(request, interview_id):
    context = {}
    if request.method == 'POST':
        contextForm = ContextForm(request.POST)
        if contextForm.is_valid():
            contextForm.save()
        return HttpResponseRedirect('/entrevistas/llenar/'+str(interview_id))
    else:
        interview = Interview.objects.get(pk = interview_id)
        form = ContextForm(initial = {'interview':interview_id})
        context['interview'] = interview
        context['form'] = form
    return render(request,'interview/add_context.html', context)

@login_required
@restricted_for_caregivers
def add_tutor(request, interview_id):
    context = {}
    if request.method == 'POST':
        tutorForm = TutorForm(request.POST)
        if tutorForm.is_valid():
            tutorForm.save()
        return HttpResponseRedirect('/entrevistas/llenar/'+str(interview_id))
    else:
        interview = Interview.objects.get(pk = interview_id)
        form = TutorForm(initial = {'adult':interview.adult})
        context['interview'] = interview
        context['form'] = form
    return render(request,'interview/add_tutor.html', context)

@login_required
@restricted_for_caregivers
def add_caregiver(request, interview_id):
    context = {}
    if request.method == 'POST':
        caregiverForm = CaregiverForm(request.POST)
        if caregiverForm.is_valid():
            caregiverForm.save()
        return HttpResponseRedirect('/entrevistas/llenar/'+str(interview_id))
    else:
        interview = Interview.objects.get(pk = interview_id)
        form = CaregiverForm(initial = {'adult':interview.adult.pk})
        context['interview'] = interview
        context['form'] = form
    return render(request,'interview/add_caregiver.html', context)

@login_required
@restricted_for_caregivers
def add_process(request, interview_id):
    context = {}
    if request.method == 'POST':
        processForm = ProcessForm(request.POST)
        if processForm.is_valid():
            processForm.save()
        return HttpResponseRedirect('/entrevistas/llenar/'+str(interview_id))
    else:
        interview = Interview.objects.get(pk = interview_id)
        form = ProcessForm(initial = {'interview':interview_id})
        context['interview'] = interview
        context['form'] = form
    return render(request,'interview/add_process.html', context)