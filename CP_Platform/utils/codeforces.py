rating_correspondence = {}


def setup_rating_dict():
    level = 1
    for rating in range(800, 3500, 100):
        rating_correspondence[rating] = level

        if rating % 2 != 0:
            level += 1


setup_rating_dict()


def code_extract_contest(problem_url):
    code = ""

    count = 0
    for i in range(len(problem_url) - 1, -1, -1):
        if problem_url[i] == '/':
            count += 1
            continue

        if count == 1:
            continue

        if count >= 3:
            break

        code += problem_url[i]

    return code[::-1]


def code_extract_problemset(problem_url):
    code = ""

    count = 0
    for i in range(len(problem_url) - 1, -1, -1):
        if problem_url[i] == '/':
            count += 1
            continue

        if count >= 2:
            break

        code += problem_url[i]

    return code[::-1]


def code_extractor(problem_url):
    if "contest" in problem_url:
        return "CF" + code_extract_contest(problem_url)
    else:
        return "CF" + code_extract_problemset(problem_url)
