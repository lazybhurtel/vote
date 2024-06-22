from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import Http404
from django.utils import timezone
from .models import Question, Choice


# Get questions and display those questions
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date',)[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


# Show question and choices
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404('Question does not exist')
    return render(request, 'polls/details.html',
                  {'question': question})


# Get question and display results
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html',
                  {'question': question})


# Vote for a question choice
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/details.html',
                      {'question': question,
                       'error_message': 'You did not select a choice.'})
    else:
        # not letting voting twice
        if request.session.get('has_voted_%s' % question_id, False):
            return render(request, 'polls/details.html',
                          {'question': question, 'error_message': 'You have already voted for this question.'})
        selected_choice.votes += 1  # vote increase
        selected_choice.save()

        request.session['has_voted_%s' % question_id] = True

        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
