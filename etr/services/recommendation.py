import random

from etr import db
from etr.crud.user import get_users
from etr.crud.tag import get_tags
from etr.crud.problem import get_problems_group_by_rating
from etr.crud.submission import get_submissions
from etr.schemas.problem import ProblemSchema
from etr.models.recommendation import RecommendationOrm


def choice_task(*,
    rating: int,
    count: int,
    tags: dict[str, float],
    problem_by_rating: dict[int, list[ProblemSchema]],
    solved_problem: list[ProblemSchema]
) -> list[ProblemSchema]:
    candidates = problem_by_rating.get(rating, [])
    str_solved_tasks = [
        str(problem.contest_id) + problem.index
        for problem in solved_problem
    ]
    candidates = [
        candidate
        for candidate in candidates
        if str(candidate.contest_id) + candidate.index not in str_solved_tasks
    ]
    if candidates == []:
        return []
    candidates = random.choices(
        candidates,
        weights=[
            max([tags[tag] for tag in candidate.tags]) if candidate.tags else 0
            for candidate in candidates
        ],
        k=min(count, len(candidates))
    )
    return candidates


def create_recommendations():
    users = get_users(watch=True)
    problem_by_rating = get_problems_group_by_rating()

    session = db.SessionLocal()
    session.query(RecommendationOrm).filter().delete()

    for user in users:
        middle_rating = 0
        cnt_task_has_rating = 1  # избегаем проблему деления на 0
        submissions = get_submissions(author_id=user.id, verdict="OK")
        tags: dict[str, int] = {tag: 0 for tag in get_tags()}
        solved_problem: list[ProblemSchema] = []
        for submission in submissions:
            if submission.problem:
                solved_problem.append(submission.problem)
                if submission.problem.rating:
                    middle_rating += submission.problem.rating
                    cnt_task_has_rating += 1
                for tag in submission.problem.tags:
                    tags[tag] += 1

        middle_rating /= cnt_task_has_rating
        # округляем до кратного 100
        middle_rating = round(middle_rating) // 100 * 100
        # для новичка среднее будет близко к 0, задач с таким rating нету
        middle_rating = max(900, middle_rating)
        # TODO: будет работать для опытных приемлемо
        # для новичков на codeforces возможно будет давать большие выбросы
        middle_cnt = sum(tags.values()) / len(tags.values())
        # добавляем среднее количество решенных задач к каждому тегу
        tags = {
            key: 1 / (value + middle_cnt + 1)
            for key, value in tags.items()
        }

        recommended_tasks: list[ProblemSchema] = []
        recommended_tasks += choice_task(
            rating=middle_rating - 200, count=5, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating - 100, count=10, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating - 000, count=15, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating + 100, count=30, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating + 200, count=15, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating + 300, count=10, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating + 400, count=10, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        recommended_tasks += choice_task(
            rating=middle_rating + 400, count=5, tags=tags, problem_by_rating=problem_by_rating, solved_problem=solved_problem
        )
        for recommendation in recommended_tasks:
            session.add(
                RecommendationOrm(
                    problem_id=recommendation.id,
                    user_id=user.id
                )
            )

    session.commit()
    session.close()
