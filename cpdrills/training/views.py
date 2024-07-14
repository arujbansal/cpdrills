import os

from django.shortcuts import render, redirect
from .forms import SpeedTrainProblemForm
from django.contrib import messages
from .models import ProblemTopic, Subcategory, ProblemStatus, Problem, OnlineJudge
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import JsonResponse
import requests
from utils import codeforces, graph_plots
from dotenv import load_dotenv
load_dotenv('../../.env')

API_URL = os.getenv('API_URL') + '/gimme'  # Problem finder API


@login_required
def train(request):
    """
    Renders the training page
    """

    topics = ProblemTopic.objects.all()
    problems = ProblemStatus.objects.filter(userprofile__user=request.user).order_by('-solve_time')

    cnt = ProblemStatus.objects.filter(userprofile__user=request.user,
                                       problem__subcategory__problem_topic_id=1).count()

    total_cnt = problems.count()

    graph_solved_bar = graph_plots.stacked_bar_solve_count_graph(request.user, "null", False, True)
    graph_speed = graph_plots.average_speed_line_graph(request.user, "null", False, True)
    graph_time_date = graph_plots.average_speed_date_graph(request.user, "null", False, True)

    paginator = Paginator(problems, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'training/main_pages/train.html',
                  {"topics": [topic.name for topic in topics], "dp_cnt": cnt,
                   "graph_solved_bar": graph_solved_bar,
                   "graph_speed": graph_speed,
                   "graph_time_date": graph_time_date,
                   'page_obj': page_obj,
                   "total_cnt": total_cnt})


@login_required
def practice(request, topic, subcategory):
    """
    Problem list page.
    """

    topic_object = ProblemTopic.objects.get(name=topic)
    subcategory_object = Subcategory.objects.get(name=subcategory)

    subcategories = topic_object.subcategoryOf.all()

    problems_list = subcategory_object.problems.all().order_by('ordering_code')
    paginator = Paginator(problems_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    graph1 = graph_plots.average_speed_line_graph(request.user, "Dynamic Programming", False, False)
    graph_bar_count = graph_plots.stacked_bar_solve_count_graph(request.user, "Dynamic Programming", False, False)
    graph_time_date = graph_plots.average_speed_date_graph(request.user, "Dynamic Programming", False, False)

    context = {"topic": topic,
               "subcategories": [subcategory.name for subcategory in subcategories],
               "cur_sub": subcategory,
               "page_obj": page_obj,
               "graph1": graph1,
               "graph_bar_count": graph_bar_count,
               "graph_time_date": graph_time_date}

    return render(request, 'training/main_pages/practice.html', context)


@login_required
def speed_train(request):
    """
    Speed Training module. Using API for finding unsolved problems.
    """

    graph1 = graph_plots.average_speed_line_graph(request.user, "null", True, False)
    graph_bar_count = graph_plots.stacked_bar_solve_count_graph(request.user, "null", True, False)
    graph_time_date = graph_plots.average_speed_date_graph(request.user, "null", True, False)

    context = {'form': SpeedTrainProblemForm(), "graph1": graph1, "graph_bar_count": graph_bar_count,
               "graph_time_date": graph_time_date}

    if 'problem' in request.session:
        try:
            context['problem'] = Problem.objects.get(code=request.session['problem'])
        except:
            del request.session['problem']

    if request.method == "POST":
        form = SpeedTrainProblemForm(request.POST)

        if form.is_valid():
            cur_handle = request.user.userprofile.codeforces_handle
            if not cur_handle:
                cur_handle = "DrowsyPanda"

            api_payload = {'handle': cur_handle,
                           'rating': form.cleaned_data['rating'],
                           'tags': form.cleaned_data['topics'],
                           'contests': form.cleaned_data['contest_type'],
                           'problem_types': form.cleaned_data['problem_type']}

            api_response = requests.get(API_URL, params=api_payload)

            if api_response.status_code != 200:
                messages.error(request, 'Codeforces might be unavailable at this moment. Please try again later.')
                return render(request, 'training/main_pages/speedtrain_form.html', context)

            api_data = api_response.json()

            if api_data['status'] != 'OK':
                messages.error(request,
                               'No problem found. Please also check whether the codeforces handle under your profile '
                               'is valid. Ensure that it is a username and not a link.')
                return render(request, 'training/main_pages/speedtrain_form.html', context)

            codeforces_oj = OnlineJudge.objects.get(name="Codeforces")
            problem_code = codeforces.code_extractor(api_data['url'])
            problem = Problem.objects.get_or_create(code=problem_code, rating=api_data['rating'],
                                                    source=codeforces_oj, name=api_data['name'],
                                                    link=api_data['url'])

            # context['problem'] = problem[0]
            request.session['problem'] = problem[0].code

            return redirect('speed_train')
            # return render(request, 'training/main_pages/speedtrain_form.html', context)
        else:
            messages.error(request, 'Rating must be in the range [800, 3500].')

    return render(request, 'training/main_pages/speedtrain_form.html', context)


@login_required
def problem_status_update(request):
    """
    Receives an AJAX call to update problem statuses for the logged-in user.
    """

    if request.method == "POST" and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        problem_status_tuple = ProblemStatus.objects.get_or_create(problem_id=request.POST['problem_code'],
                                                                   userprofile=request.user.userprofile)

        if request.POST['action'] == 'save':
            time_taken = int(request.POST['hours']) * 60 + int(
                request.POST['minutes']) + round(
                int(request.POST['seconds'])) / 60

            if time_taken == 0:
                time_taken = -1

            problem_status_tuple[0].solve_duration = time_taken
            speed_attempt = True if request.POST['speed_attempt'] == 'True' else False
            problem_status_tuple[0].speed_attempt = speed_attempt

            problem_status_tuple[0].save()

            return JsonResponse({'status': 'Success',
                                 'msg': 'Successfully updated.',
                                 'solve_time': problem_status_tuple[0].solve_time})
        else:
            problem_status_tuple[0].delete()
            return JsonResponse({'status': 'Success',
                                 'msg': 'Successfully deleted.'})

    return JsonResponse({'status': 'Fail', 'msg': 'Something went wrong.'})
