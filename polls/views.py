from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.core.urlresolvers import reverse

from models  import Question, Choice

# Create your views here.

def index(request):
    latest_questions = Question.objects.order_by('-pub_date')[:5]
    context = { 'latest_questions_list' : latest_questions }

    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    return render(request, 'polls/detail.html', {'question':question})

def results(request, question_id):
    q = get_object_or_404(Question, pk=question_id)
    response = "You are looking at the results of the question %s."
    return render(request, 'polls/results.html', {'question' : q})

def vote(request, question_id):
    q = get_object_or_404(Question,pk=question_id)
    try:
        selected = q.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html',{'question' : q , 'error_message': "You didnt select a choice!"})
    else:
        selected.votes += 1
        selected.save()
        return HttpResponseRedirect(reverse('polls:results',args=(q.id,)))
