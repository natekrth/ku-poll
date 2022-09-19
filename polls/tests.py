import datetime
from urllib import response

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote


class QuestionModelTests(TestCase):
    
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)
    
    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_published_date_is_in_future(self):
        """can_vote() return False for question whose pub_date is in the future."""
        time = timezone.localtime() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), False)
    
    def test_voting_allow_at_pub_date(self):
        """can_vote() return True for voting that vote at exact same time when question is published."""
        time = timezone.localtime()
        question = Question(pub_date=time)
        self.assertIs(question.can_vote(), True)
    
    def test_voting_on_time(self):
        """can_vote() return True for voting after pub_date and before end_date."""
        time = timezone.localtime() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        time_end = timezone.localtime() + datetime.timedelta(hours=23, minutes=59, seconds=59)
        question = Question(pub_date=time, end_date=time_end)
        self.assertIs(question.can_vote(), True) 
        
    def test_voting_after_end_date(self):
        """can_vote() return False for voting after question end_date."""
        time = timezone.localtime() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        # time_more = timezone.localtime().now() - datetime.timedelta(hours=20, minutes=59, seconds=59)
        question = Question(pub_date=timezone.localtime(), end_date=time)
        self.assertIs(question.can_vote(), False)
        
    def test_poll_with_no_end_date(self):
        """can_vote() return True for question that does not have end_date"""
        time = timezone.localtime()
        question = Question(pub_date=time)
        self.assertIsNone(question.end_date)
        self.assertIs(question.can_vote(), True)

def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )
        
        
class QuestionDetailViewTests(TestCase):
    
    def setUp(self):
        self.username = "test"
        self.password = "1234"
        self.voter = User.objects.create_user(username=self.username, password=self.password)
        self.voter.first_name = "Test"
        self.voter.save()
        
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 302 (Redirect).
        """
        self.client.login(username=self.username, password=self.password)
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        self.client.login(username=self.username, password=self.password)
        past_question = create_question(question_text='Past Question.', days=-5)
        self.question = Question.objects.get(pk=past_question.pk)
        vote = Vote.objects.get(user=self.voter, choice__question=self.question)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, {past_question.question_text, vote.choice.choice_text})


class QuestionVoteTest(TestCase):
    
    def setUp(self):
        self.username = "test"
        self.password = "1234"
        self.voter = User.objects.create_user(username=self.username, password=self.password)
        self.voter.first_name = "Test"
        self.voter.save()
        self.question = Question.objects.create(question_text="Test Question?", pub_date=timezone.now())
        
    def test_user_login_required_to_vote(self):
        self.client.login(username=self.username, password=self.password)
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_user_not_login_vote(self):
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

