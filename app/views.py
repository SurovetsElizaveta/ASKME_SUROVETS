from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

QUESTIONS = []
for i in range(1, 50):
    QUESTIONS.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text for question # ' + str(i)
    })

HOT_QUESTIONS = []
for i in range(1, 50):
    HOT_QUESTIONS.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text for hot question # ' + str(i)
    })

TAG_QUESTIONS = []
for i in range(1, 30):
    TAG_QUESTIONS.append({
        'title': 'title' + str(i),
        'id': i,
        'text': 'text for hot question # ' + str(i)
    })

ANSWERS = []
for i in range(1, 30):
    ANSWERS.append({
        'id': i,
        'text': 'text for answer # ' + str(i)
    })


def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(QUESTIONS, 20)
    page = paginator.page(page_num)
    return render(
        request, 'index.html',
        context={'questions': page.object_list, 'page_obj': page}
    )


def hot_questions(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(HOT_QUESTIONS, 20)
    page = paginator.page(page_num)
    return render(
        request, 'hot_questions.html',
        context={'hot_questions': page.object_list, 'page_obj': page}
    )


def tag(request):
    return render(
        request, 'tag.html',
        context={'tag_questions': TAG_QUESTIONS}
    )


def question(request, question_id):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(ANSWERS, 20)
    page = paginator.page(page_num)
    one_question = QUESTIONS[question_id]
    return render(
        request, 'question.html',
        context={'answers': page.object_list, 'page_obj': page}
    )


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')
