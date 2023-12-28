import math

from django import template
from training.models import Problem, ProblemStatus
from datetime import datetime
import time

register = template.Library()


@register.filter
def check_solve(prob_code, cur_username):
    """
    Returns the solved status of a problem for a user
    """

    user_problem_status = ProblemStatus.objects.filter(problem_id=prob_code).filter(
        userprofile__user__username=cur_username).first()

    if user_problem_status is None:
        return "False", ""
    else:
        time = user_problem_status.solve_duration

        hours = str(math.floor(time / 60))
        minutes = str(math.floor(time % 60))
        seconds = str(round((time - math.floor(time)) * 60))

        if len(hours) == 1: hours = "0" + hours
        if len(minutes) == 1: minutes = "0" + minutes
        if len(seconds) == 1: seconds = "0" + seconds;

        res = hours + ":" + minutes + ":" + seconds

        if time == -1: res = "Unknown"
        return "True", res


@register.filter
def get_js_timestamp(py_time):
    return datetime.timestamp(py_time) * 1000
