from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from quizzes.models import Category, Question, Choice, Result


class IndexView(ListView):
    model = Category
    template_name = "quizzes/index.html"

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)


class ResultListView(ListView):
    template_name = 'quizzes/user_account.html'

    def get_queryset(self):
        return Result.objects.filter(users=self.request.user)

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(ResultListView, self).dispatch(request, *args, **kwargs)

@login_required
def question(request, slug):
    category = Category.objects.get(slug=slug)
    questions = Question.objects.filter(category=category)
    print('questions = ', len(request.GET.keys()))

    return render(request, 'quizzes/questions.html', {'questions': questions})

@login_required
def check(request):
    user = request.user
    answer = []
    questions_numb = []
    for key, value in request.GET.items():
        questions_numb.append(key)
        answer.append(int(value))

    questions_l = Question.objects.filter(id__in=questions_numb)
    choices = Choice.objects.filter(id__in=answer)

    correct_answers = 0
    for ch in choices:
        if ch.correct:
            correct_answers += 1
    result = (correct_answers / len(answer) * 100)

    Result.objects.update_or_create(
        users=user, subject=questions_l[0].category,
        defaults={
            'users': user,
            'subject': questions_l[0].category,
            'result': result
        },
    )

    return render(request, 'quizzes/questions.html',
                  {'questions_l': questions_l,
                   'answer': answer,
                   'result': result
                   })
