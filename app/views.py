from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import HttpResponse
from app.models import Question, Answer

# Create your views here.


QUESTIONS = (Question.objects.all())
NEWEST_QUESTIONS = Question.objects.get_newest()
HOT_QUESTIONS = Question.objects.get_hottest()

def index(request):
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(NEWEST_QUESTIONS, 20)
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


def tag(request, tag):
    TAG_QUESTIONS = Question.objects.get_by_tag(tag)
    return render(
        request, 'tag.html',
        context={'tag_questions': TAG_QUESTIONS}
    )


def question(request, question_id):
    ANSWER = Answer.objects.get_answers(question_id)
    page_num = int(request.GET.get('page', 1))
    paginator = Paginator(ANSWER, 20)
    page = paginator.page(page_num)
    one_question = QUESTIONS[question_id - 300804]
    return render(
        request, 'question.html',
        context={'answers': page.object_list, 'page_obj': page, 'one_question': one_question}
    )


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')
