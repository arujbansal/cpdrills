import csv
# from training.models import Problem, OnlineJudge, Subcategory

# file = open('/Users/arujbansal/Desktop/CPPLAT/CP-Platform/cpdrills/utils/problems3.csv')

# csvreader = csv.reader(file)

rows = []
# for row in csvreader:
#     row = row[0].split(' - ')
#     rows.append(row)

for i in range(0, 22):
    row = input().split(' - ')
    rows.append(row)
    # print(row)

for row in rows:
    # oj = OnlineJudge.objects.get(name="Codeforces")

    contest_num = ""
    p_code = ""

    for i in range(0, len(row[0])):
        if row[0][i].isalpha(): break
        contest_num += row[0][i]

    if row[0][-1].isalpha():
        p_code = row[0][-1]
    else:
        p_code = row[0][-2] + row[0][-1]

    p_link = "https://codeforces.com/problemset/problem/" + contest_num + '/' + p_code

    print(contest_num + p_code, row[1], p_link)
    # p = Problem(code="CF" + contest_num + p_code, name=row[1], source=oj, rating=1900, link=p_link, ordering_code=3000)
    # p.save()
    #
    # cat = Subcategory.objects.get(name="Level 6")
    # cat.problems.add(p)
    # cat.save()
#
# # print(rows)
#
# file.close()
