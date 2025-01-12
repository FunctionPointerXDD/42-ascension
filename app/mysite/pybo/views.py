from django.shortcuts import render # html convert method
from .models import Question

# Create your views here.

def index(request):
    print("index")
    question_list = Question.objects.order_by('-create_date') #reverse order '-'
    context = {'question_list': question_list}
    return render(request, 'pybo/question_list.html', context)

def detail(request, question_id):
    print("detail")
    question = Question.objects.get(id=question_id)
    context = {'question': question}
    return render(request, 'pybo/question_detail.html', context)
