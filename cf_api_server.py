import aiohttp
from fastapi import FastAPI, Query
from typing import List
import uvicorn
from random import choice

desc = 'API to recommend problem from <a href="https://codeforces.com">codeforces</a>'
app = FastAPI(title="Gimme API",
              version="1.0.0",
              description=desc,
              docs_url='/')


@app.on_event("startup")
async def startup_event():
    global data
    global contests
    global contest_qry
    contest_qry = {}

    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://codeforces.com/api/problemset.problems") as respose:
            data = await respose.json()
            data = data["result"]["problems"]

    async with aiohttp.ClientSession() as session:
        async with session.get(
                "https://codeforces.com/api/contest.list?gym=false"
        ) as respose:
            contests = await respose.json()
            contests = contests["result"]

            for contest in contests:
                contest_qry[contest["id"]] = contest


@app.get("/gimme")
async def gimme(handle: str,
                tags: List[str] = Query([]),
                rating: int = -1,
                contests: List[str] = Query([]),
                problem_types: List[str] = Query([])):
    async with aiohttp.ClientSession() as session:
        if rating == -1:
            print(
                f"Rating not provided. Querying codeforces for {handle}'s rating"
            )
            async with session.get(
                    f"https://codeforces.com/api/user.info?handles={handle}"
            ) as response:
                res = await response.json()
                if (res['status'] != "OK"):
                    return res
                else:
                    try:
                        rating = round(res["result"][0]["rating"], -2)
                    except KeyError:
                        rating = 800
        if rating < 800: rating = 800
        if rating > 3500: rating = 3500
        print(f"Querying codeforces for {handle}'s submissions")
        async with session.get(
                f"https://codeforces.com/api/user.status?handle={handle}"
        ) as response:
            res = await response.json()
            if (res['status'] != "OK"):
                return res
            else:
                submissions = res['result']
                solved = {
                    sub['problem']['name']
                    for sub in submissions if sub["verdict"] == 'OK'
                }
        problems = []
        for prob in data:
            try:
                if (problem_types or prob["rating"] == int(rating)) and prob["name"] not in solved and "*special" not in \
                        prob[
                            "tags"]:
                    present = len(contests) == 0

                    for contest_type in contests:
                        if contest_type in contest_qry[
                            prob["contestId"]]["name"]:
                            present = True
                            break

                    if present:
                        problems.append(prob)

            except:
                pass
        if tags:
            problem = []
            for prob in problems:
                try:
                    if all(p in prob['tags'] for p in tags):
                        problem.append(prob)
                except:
                    pass
            problems = problem

        if problem_types:
            problem = []
            for prob in problems:
                try:
                    if prob['index'] in problem_types:
                        problem.append(prob)
                except:
                    pass
            problems = problem

        if not problems:
            return ({
                "status":
                    "FAILED",
                "comment":
                    "Problems not found within the search parameters"
            })
        select = choice(problems)
        print(select)
        return ({
            "status":
                "OK",
            "name":
                select["name"],
            "rating":
                select["rating"],
            "tags":
                select["tags"],
            "url":
                "https://codeforces.com/contest/{}/problem/{}".format(
                    select["contestId"], select["index"])
        })


if __name__ == "__main__":
    uvicorn.run("main:app", host='0.0.0.0', port=8080)
