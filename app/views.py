from audioop import reverse

from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse

from app.forms import LoginForm, UserForm, EditProfileForm, AskForm, AnswerForm
from app.models import Question, Answer, Profile
from django.urls import reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.


QUESTIONS = (Question.objects.all())
NEWEST_QUESTIONS = Question.objects.get_newest()
HOT_QUESTIONS = Question.objects.get_hottest()


def pagination(request, array):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(array, 20)
    page = paginator.page(page_num)
    return page


def index(request):
    page = pagination(request, NEWEST_QUESTIONS)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )


def hot_questions(request):
    page = pagination(request, HOT_QUESTIONS)
    return render(
        request, 'hot_questions.html',
        context={'hot_questions': page.object_list, 'page_obj': page}
    )


def tag(request, tag):
    TAG_QUESTIONS = Question.objects.get_by_tag(tag)
    return render(
        request, 'tag.html',
        context={'tag_questions': TAG_QUESTIONS}
    )


def question(request, question_id):
    ANSWER = Answer.objects.get_answers(question_id)
    page = pagination(request, ANSWER)
    one_question = QUESTIONS[question_id - 1]
    form = AnswerForm
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = request.user.profile
            answer.question = one_question
            answer.save()
            return redirect(reverse('question', args=[question_id]))
    return render(
        request, 'question.html',
        context={'answers': page.object_list, 'page_obj': page, 'one_question': one_question, 'form': form}
    )


def login(request):
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = auth.authenticate(request, **form.cleaned_data)
            if user:
                auth.login(request, user)

                return redirect(reverse('ask'))
            form.add_error('password', 'Invalid username or password.')

    return render(request, 'login.html', {'form': form})


@login_required
def logout(request):
    print('logout')
    auth.logout(request)
    return redirect(reverse('index'))


def signup(request):
    form = UserForm
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect(reverse('index'))
    return render(request, 'signup.html', {"form": form})


@login_required
def ask(request):
    if request.method == 'POST':
        form = AskForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user.profile
            question.save()
            QUESTIONS = Question.objects.all()
            return redirect(reverse('question', args=[len(QUESTIONS) - 1]))
    else:
        form = AskForm

    return render(request, 'ask.html', {'form': form})


# @login_required
# def profile_edit(request):
#     form = EditProfileForm
#     if request.method == 'POST':
#         form = EditProfileForm(request.POST)
#         if form.is_valid():
#             if request.POST.get("tags").split(' ') <= 3:
#                 form.save()
#                 return redirect(reverse('profile_edit'))
#     return render(request, 'profile/edit.html', {"form": form})

@login_required
def profile_edit(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_edit')
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'profile/edit.html', {'form': form})
