import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    A model for polls Question.
    
    Question Model should have question_text and pub_date.
    end_date is is optional. If end_date is None, then the voting is allow anytime after pub_date.
    """
    
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', default=None, null=True)
    
    def was_published_recently(self):
        """Questoin was published less than or equal to 1 day."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    def is_published(self):
        """Check that Question is published at this time."""
        now = timezone.localtime()
        return now >= self.pub_date
    
    def can_vote(self):
        """Check that Question can be vote."""
        now = timezone.localtime()
        if self.end_date is None and self.pub_date <= now:
            return True
        return self.pub_date <= now <= self.end_date
        
    def __str__(self):
        """Representative of Question object."""
        return self.question_text


class Choice(models.Model):
    """A model for polls choice.
    
    Choice Model needs question identifier and choice_text.
    votes is optional default value is 0.
    """
    
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        """Representative of Choice object."""
        return self.choice_text
