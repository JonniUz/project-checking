from django.shortcuts import render
from django.views.generic import ListView

from quizzes.models import Category, Question, Choice, Result


class IndexView(ListView):
    model = Category
    template_name = "quizzes/index.html"

    # @method_decorator(login_required)
    # def dispatch(self, *args, **kwargs):
    #     return super(IndexView, self).dispatch(*args, **kwargs)


def question(request, slug):
    category = Category.objects.get(slug=slug)
    questions = Question.objects.filter(category=category)
    print('questions = ', len(request.GET.keys()))

    return render(request, 'quizzes/questions.html', {'questions': questions})


def check(request):
    user = request.user
    question_nums = []
    answer = []
    print('check = ', request.GET)
    for key, value in request.GET.items():
        question_nums.append(key)
        answer.append(value)

    questions_l = Question.objects.filter(id__in=question_nums)
    choices = Choice.objects.filter(id__in=answer)

    correct_answer = 0
    for choice in choices:
        if choice.correct:
            correct_answer += 1
    result = (correct_answer / len(answer) * 100)

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


