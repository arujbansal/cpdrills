from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import UserProfile


class OnlineJudge(models.Model):
    """
    Online judge consisting of problems.
    """

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Problem(models.Model):
    """
    Actual problem itself.
    """

    code = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=256)
    source = models.ForeignKey(OnlineJudge, on_delete=models.CASCADE)
    rating = models.IntegerField()
    link = models.TextField()
    # tags = models.TextField(required=False)
    # editorial = models.TextField(blank=True)
    solvers = models.ManyToManyField(UserProfile, through='ProblemStatus')  # Users who have solved this problem
    ordering_code = models.PositiveSmallIntegerField(default=3000)

    def __str__(self):
        return self.name

    # class Meta:
    #     ordering = ['']


class ProblemStatus(models.Model):
    """
    Information about a particular problem for a particular user.
    """

    userprofile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    solve_time = models.DateTimeField(default=timezone.now)  # Time at which the problem was solved
    solve_duration = models.FloatField(default=-1)  # Time taken to solve the problem
    speed_attempt = models.BooleanField(default=False)

    class Meta:
        ordering = ['solve_time']


class ProblemTopic(models.Model):
    """
    Main category of problem.
    E.g. Dynamic Programming, Graph Theory, Sorting and Searching
    """

    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    """
    Tracks within problem categories.
    E.g. Beginner, Classical, Level 1, Level 2, Level 3
    """

    name = models.CharField(max_length=256)
    problem_topic = models.ForeignKey(ProblemTopic, on_delete=models.CASCADE, related_name="subcategoryOf")
    problems = models.ManyToManyField(Problem)

    def __str__(self):
        return self.problem_topic.name + " - " + self.name

    class Meta:
        ordering = ['name']
