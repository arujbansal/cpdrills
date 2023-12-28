import plotly.graph_objs as go
from training.models import ProblemStatus
import pytz
from django.utils import timezone
import plotly.express as px

from datetime import datetime

# Generated using:
# for rating in range(800, 3600, 100):
#     print(str(rating) + ": '" + '#'+''.join(random.sample(chars,6)) + '"')

colors = {800: "#DC39A8",
           900: "#D401F5",
           1000: "#CE2958",
           1100: "#FB48C1",
           1200: "#0B5317",
           1300: "#CA0B37",
           1400: "#E689A2",
           1500: "#3C4120",
           1600: "#46B350",
           1700: "#9C0F63",
           1800: "#28D6E9",
           1900: "#320581",
           2000: "#0EF538",
           2100: "#29C60B",
           2200: "#E89132",
           2300: "#C6409A",
           2400: "#28A516",
           2500: "#678E0C",
           2600: "#92B8ED",
           2700: "#BC1357",
           2800: "#B1546D",
           2900: "#F4381C",
           3000: "#CA1324",
           3100: "#5C0E8F",
           3200: "#73DEA0",
           3300: "#28DC17",
           3400: "#DA12B7",
           3500: "#813F7C",
           "Non Codeforces": "#AF43D0"}


def convert_to_localtime(utctime):
    """
    Converts datetime object to the user's local timezone.
    """

    fmt = '%d/%m/%Y'
    utc = utctime.replace(tzinfo=pytz.UTC)
    localtz = utc.astimezone(timezone.get_current_timezone())
    return localtz.strftime(fmt)


def num_to_month(num):
    return datetime(1, num, 1).strftime("%B")


def average_speed_line_graph(user, topic, speed_attempt, show_all):
    """
    Graph: Time Taken v.s. Rating
    Line 1: Average time
    Scatter 1: Raw time
    """

    if topic == "null":
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, speed_attempt=speed_attempt).all()
    else:
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user,
                                                    problem__subcategory__problem_topic_id=1).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, problem__subcategory__problem_topic_id=1,
                                                    speed_attempt=speed_attempt).all()

    sum_dict = {}
    cnt_dict = {}
    x1 = []
    y1 = []
    x2 = []
    y2 = []

    finalise_order = []

    for prob in problems:
        rating = prob.problem.rating

        if prob.solve_duration == -1 or rating == -1:
            continue

        x2.append(rating)
        y2.append(prob.solve_duration)

        if rating in cnt_dict:
            sum_dict[rating] += prob.solve_duration
            cnt_dict[rating] += 1
        else:
            sum_dict[rating] = prob.solve_duration
            cnt_dict[rating] = 1

    for k, v in sum_dict.items():
        finalise_order.append((k, v / cnt_dict[k]))

    finalise_order.sort()

    for k, v in finalise_order:
        x1.append(k)
        y1.append(v)

    trace1 = go.Scatter(x=x1, y=y1, name='Average Time')
    trace2 = go.Scatter(x=x2, y=y2, name='Raw Time', mode='markers')

    title = "Speed (Speed Training)" if speed_attempt else "Speed"

    if topic != "null":
        title = "Speed (" + topic + ")"

    layout = go.Layout(title=title,
                       xaxis={'title': 'Codeforces Problem Rating', 'autorange': True, 'tick0': '800', 'dtick': '100'},
                       yaxis={'title': 'Time (Minutes)', 'autorange': True},
                       autosize=True)

    figure = go.Figure(data=[trace2, trace1], layout=layout)
    figure.update_layout(autosize=True)

    figure.update_layout(yaxis_range=[0, 90])
    figure.update_layout(xaxis_range=[800, 3500])

    graph = figure.to_html(include_plotlyjs=False)
    return graph


# def stacked_bar_solve_count_graph(user, topic, speed_attempt, show_all):
#     """
#     Graph: Number of problems solved v.s. Date
#     Stacked bar graph - stack of ratings
#     """
#
#     if topic == "null":
#         if show_all:
#             problems = ProblemStatus.objects.filter(userprofile__user=user).all()
#         else:
#             problems = ProblemStatus.objects.filter(userprofile__user=user, speed_attempt=speed_attempt).all()
#     else:
#         if show_all:
#             problems = ProblemStatus.objects.filter(userprofile__user=user, problem__subcategory__problem_topic_id=1,
#                                                     speed_attempt=speed_attempt).all()
#         else:
#             problems = ProblemStatus.objects.filter(userprofile__user=user,
#                                                     problem__subcategory__problem_topic_id=1).all()
#
#     cnt_dict = {}
#     rating_bars = {}
#     for rating in range(800, 3600, 100):
#         cnt_dict[rating] = {}
#         rating_bars[rating] = [[], []]
#
#     mx = 15
#
#     for problem in problems:
#         cur_date = str(convert_to_localtime(problem.solve_time))
#         cur_rating = problem.problem.rating
#
#         if cur_rating not in cnt_dict:
#             cnt_dict[cur_rating] = {}
#
#         if cur_date in cnt_dict[cur_rating]:
#             cnt_dict[cur_rating][cur_date] += 1
#             mx = max(cnt_dict[cur_rating][cur_date], mx)
#         else:
#             cnt_dict[cur_rating][cur_date] = 1
#
#     for k, v in cnt_dict.items():
#         for k2, v2 in cnt_dict[k].items():
#             if k not in rating_bars:
#                 rating_bars[k] = [[], []]
#
#             rating_bars[k][0].append(k2)
#             rating_bars[k][1].append(v2)
#
#     title = "Solve Count (Speed Training)" if speed_attempt else "Solve Count"
#
#     if topic != "null":
#         title = "Solve Count (" + topic + ")"
#
#     layout = go.Layout(title=title, xaxis={'title': 'Date', },
#                        yaxis={'title': 'Number of Problems Solved'})
#
#     bar_traces = []
#
#     for k, v in rating_bars.items():
#         name = ""
#
#         if k == -1:
#             name = "Not Codeforces"
#         else:
#             name = str(k)
#
#         trace = go.Bar(x=v[0], y=v[1], name=name)
#         bar_traces.append(trace)
#
#     figure = go.Figure(data=bar_traces, layout=layout)
#     figure.update_layout(autosize=True)
#     figure.update_layout(barmode='stack')
#     figure.update_xaxes(automargin=True)
#     figure.update_layout(xaxis=dict(tickformat="%d-%b, %Y"))
#
#     figure.update_layout(yaxis_range=[0, mx + 5])
#
#     graph = figure.to_html(include_plotlyjs=False)
#     return graph


def average_speed_date_graph(user, topic, speed_attempt, show_all):
    """
    Graph: Average time taken v.s. Date
    Line for every rating.
    """

    if topic == "null":
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, speed_attempt=speed_attempt).all()
    else:
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user,
                                                    problem__subcategory__problem_topic_id=1).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, problem__subcategory__problem_topic_id=1,
                                                    speed_attempt=speed_attempt).all()
    cur_month = datetime.now().month

    ratings = {}
    for rating in range(800, 3600, 100):
        ratings[rating] = {}

    for prob in problems:
        if prob.problem.source.name != "Codeforces" or prob.solve_duration <= 0:
            continue

        p_rating = prob.problem.rating
        solve_month = prob.solve_time.month
        solve_duration = prob.solve_duration

        if solve_month not in ratings[p_rating]:
            ratings[p_rating][solve_month] = [solve_duration, 1]
        else:
            ratings[p_rating][solve_month][0] += solve_duration
            ratings[p_rating][solve_month][1] += 1

    # x = []
    # for month in range(1, 13, 1):
    #     x.append(datetime(1, month, 1).strftime("%B"))

    traces = []

    for rating in range(800, 3600, 100):
        total_time = 0
        total_cnt = 0

        x = []
        y = []

        for month in range(1, cur_month + 1, 1):
            if month in ratings[rating]:
                total_time += ratings[rating][month][0]
                total_cnt += ratings[rating][month][1]

            if total_cnt == 0:
                continue

            x.append(num_to_month(month))
            y.append(total_time / total_cnt)

        trace = go.Scatter(x=x, y=y, name=rating, line=dict(color=colors[rating]))
        traces.append(trace)

    title = "Speed Over Time (Speed Training)" if speed_attempt else "Speed Over Time"

    if topic != "null":
        title = "Speed Over Time (" + topic + ")"

    layout = go.Layout(title=title, xaxis={'title': 'Month', 'autorange': True},
                       yaxis={'title': 'Time (Minutes)', 'autorange': True},
                       autosize=True)

    figure = go.Figure(data=traces, layout=layout)

    figure.update_layout(autosize=True)
    figure.update_layout(yaxis_range=[0, 90])
    figure.update_layout(xaxis_range=[1, 12])

    graph = figure.to_html(include_plotlyjs=False)
    return graph


def stacked_bar_solve_count_graph(user, topic, speed_attempt, show_all):
    """
    Graph: Number of problems solved v.s. Date
    Stacked bar graph - stack of ratings
    """

    if topic == "null":
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, speed_attempt=speed_attempt).all()
    else:
        if show_all:
            problems = ProblemStatus.objects.filter(userprofile__user=user,
                                                    problem__subcategory__problem_topic_id=1).all()
        else:
            problems = ProblemStatus.objects.filter(userprofile__user=user, problem__subcategory__problem_topic_id=1,
                                                    speed_attempt=speed_attempt).all()
    problems = problems.distinct()

    cur_month = datetime.now().month
    mx = 15

    ratings = {}
    for rating in range(800, 3600, 100):
        ratings[rating] = {}

    ratings["Non Codeforces"] = {}

    to_iter = [rating for rating in range(800, 3600, 100)]
    to_iter.append("Non Codeforces")

    for prob in problems:
        p_rating = prob.problem.rating
        solve_month = prob.solve_time.month

        if prob.problem.source.name != "Codeforces":
            p_rating = "Non Codeforces"

        if solve_month not in ratings[p_rating]:
            ratings[p_rating][solve_month] = 1
        else:
            ratings[p_rating][solve_month] += 1
            mx = max(mx, ratings[p_rating][solve_month])

    traces = []

    for rating in to_iter:
        x = []
        y = []

        for month in range(1, cur_month + 1, 1):
            if month not in ratings[rating]:
                ratings[rating][month] = 0

            x.append(num_to_month(month))
            y.append(ratings[rating][month])

        trace = go.Bar(x=x, y=y, name=rating, marker=dict(color=colors[rating]))
        traces.append(trace)

    title = "Solve Count (Speed Training)" if speed_attempt else "Solve Count"

    if topic != "null":
        title = "Solve Count (" + topic + ")"

    layout = go.Layout(title=title, xaxis={'title': 'Month', },
                       yaxis={'title': 'Number of Problems Solved'})

    figure = go.Figure(data=traces, layout=layout)
    figure.update_layout(autosize=True)
    figure.update_layout(barmode='stack')
    figure.update_xaxes(automargin=True)
    figure.update_layout(yaxis_range=[0, mx + 5])

    graph = figure.to_html(include_plotlyjs=False)
    return graph
