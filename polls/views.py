from http.client import HTTPResponse
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages

from .models import Choice, Question


class IndexView(generic.ListView):
    """View for index.html page."""
    
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]
    
    
class DetailView(generic.DetailView):
    """View for detail.html page."""
    
    model = Question
    template_name = 'polls/detail.html'
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())
    
    def get(self, request, pk):
        """Return the correct response depends on the conditions
        
        If the quuestion is allow to vote it will render detail.html page.
        If the question is not allowed to vote it will redirect to index.html page.
        If the question dows not exist it will redirect to index.html page.

        Args:
            request : http request
            pk (int): primiry key

        Returns:
            httpresponse: response for the request
        """
        try:
            self.question = Question.objects.get(pk=pk)
            if self.question.can_vote():
                return render(request, 'polls/detail.html', {'question': self.question})
            else:
                messages.error(request, "Voting is not allowed at this time.")
                return HttpResponseRedirect(reverse('polls:index'))
        except Question.DoesNotExist:
            messages.error(request, "Question does not exist.")
            return HttpResponseRedirect(reverse('polls:index'))
        
class ResultsView(generic.DeleteView):
    """View for results.html page."""
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    """Handle a vote request from vote button at detail page.

    Args:
        request : http request
        question_id (int): question id

    Returns:
        httpresponse: response for the request
    """
    
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
