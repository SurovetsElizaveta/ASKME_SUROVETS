from django.core.management.base import BaseCommand, CommandError
from django.utils.crypto import get_random_string
from app.models import Tag, Question, Answer, Profile, QuestionLike, AnswerLike
from django.contrib.auth.models import User
import random

from app.views import question


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int)

    def handle(self, *args, **options):
        num_users = options['ratio']

        tags = [Tag(name="Tag {}".format(i)) for i in range(num_users)]
        Tag.objects.bulk_create(tags)

        users = [User(username="Username {}".format(i)) for i in range(num_users)]
        User.objects.bulk_create(users)

        profiles = [Profile(user=users[i]) for i in range(num_users)]
        Profile.objects.bulk_create(profiles)


        questions = [Question(author=profiles[random.randint(0, num_users - 1)],
                              title="Title of the question {} bla bla bla".format(i), text=("text of the question bla bla bla bla bla" * 7)) for i in
                     range(num_users * 10)]
        Question.objects.bulk_create(questions)


        answers = [Answer(author=profiles[random.randint(0, num_users - 1)], text=("text of the answer to the question bla bla bla" * 5),
                          question=questions[random.randint(0, num_users * 10 - 1)]) for i in range(num_users * 100)]

        Answer.objects.bulk_create(answers)


        quesLikes = []
        for i in range(0, num_users - 1):
            for j in range(0, int(num_users / 100)):
                quesLikes.append(QuestionLike(profile=profiles[i], question=questions[j]))
                questions[j].likes_num += 1
        QuestionLike.objects.bulk_create(quesLikes)

        ansLikes = []
        for i in range(0, num_users - 1):
            for j in range(0, int(num_users / 100)):
                ansLikes.append(AnswerLike(profile=profiles[i], answer=answers[j]))
                answers[j].likes_num += 1
        AnswerLike.objects.bulk_create(ansLikes)
