from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.contest import ContestOrm
from etr.models.problem import ProblemOrm, TagOrm
from etr.models.submission import SubmissionOrm
from etr.models.user import UserOrm
from etr.models.team import TeamOrm


def seeding(engine: Engine):
    with Session(engine) as session:
        contests = [
            ContestOrm(
                id=1234,
                name="Test Contest #1. Codeforces Trainings Season",
                type="CF",
                phase="FINISHED",
                frozen=False,
                duration_seconds=7200,
                start_time_seconds=1614552000,
                relative_time_seconds=14400,
                prepared_by="Codeforces",
                website_url="https://codeforces.com/",
                description="Test contest #1. Codeforces Trainings Season",
                difficulty=1,
                kind="CF",
                icpc_region="World Finals",
                country="Belarus",
                city="Minsk",
                season="winter",
            ),
            ContestOrm(
                id=1265,
                name="Test Contest #2. Yandex Trainings Season",
                type="CF",
                phase="FINISHED",
                frozen=False,
                duration_seconds=7200,
                start_time_seconds=1615156800,
                relative_time_seconds=14400,
                prepared_by="Codeforces",
                website_url="https://codeforces.com/",
                description="Test contest #2. Yandex Trainings Season",
                difficulty=1,
                kind="CF",
                icpc_region="World Finals",
                country="Russia",
                city="Moscow",
                season="summer",
            ),
            ContestOrm(
                id=1311,
                name="Test Contest #3. VK Trainings Season",
                type="CF",
                phase="FINISHED",
                frozen=False,
                duration_seconds=7200,
                start_time_seconds=1615761600,
                relative_time_seconds=14400,
                prepared_by="Codeforces",
                website_url="https://codeforces.com/",
                description="Test contest #3. VK Trainings Season",
                difficulty=1,
                kind="CF",
                icpc_region="World Finals",
                country="Russia",
                city="St. Petersburg",
                season="summer",
            ),
            ContestOrm(
                id=1353,
                name="Test Contest #4. dl.gsu.by Trainings Season",
                type="CF",
                phase="FINISHED",
                frozen=False,
                duration_seconds=7200,
                start_time_seconds=1616366400,
                relative_time_seconds=14400,
                prepared_by="Codeforces",
                website_url="https://dl.gsu.by/",
                description="Test contest #4. dl.gsu.by Trainings Season",
                difficulty=1,
                kind="CF",
                icpc_region="World Finals",
                country="Belarus",
                city="Gomel",
                season="spring",
            )
        ]

        tags = [
            TagOrm(tag="dp"),
            TagOrm(tag="graphs"),
            TagOrm(tag="math"),
            TagOrm(tag="recursion"),
            TagOrm(tag="trees"),
            TagOrm(tag="dfs"),
        ]

        problems = [
            ProblemOrm(
                contest_id=1234,
                index="A",
                name="A. Test Problem #1",
                type="PROGRAMMING",
                points=1000,
                rating=1000,
                tags=[
                    tags[0],
                    tags[1],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1234,
                index="B",
                name="B. Test Problem #2",
                type="PROGRAMMING",
                points=1333,
                rating=1500,
                tags=[
                    tags[0],
                    tags[2],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1234,
                index="C",
                name="C. Test Problem #3",
                type="PROGRAMMING",
                points=1666,
                rating=2000,
                tags=[
                    tags[0],
                    tags[3],
                    tags[4],
                ]
            ),

            ProblemOrm(
                contest_id=1265,
                index="A",
                name="A. Test Problem #1",
                type="PROGRAMMING",
                points=1000,
                rating=1000,
                tags=[
                    tags[5],
                    tags[1],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1265,
                index="B",
                name="B. Test Problem #2",
                type="PROGRAMMING",
                points=1333,
                rating=1500,
                tags=[
                    tags[0],
                    tags[2],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1265,
                index="C",
                name="C. Test Problem #3",
                type="PROGRAMMING",
                points=1666,
                rating=2000,
                tags=[
                    tags[0],
                    tags[3],
                    tags[4],
                ]
            ),

            ProblemOrm(
                contest_id=1311,
                index="A",
                name="A. Test Problem #1",
                type="PROGRAMMING",
                points=1000,
                rating=1000,
                tags=[
                    tags[5],
                    tags[1],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1311,
                index="B",
                name="B. Test Problem #2",
                type="PROGRAMMING",
                points=1333,
                rating=1500,
                tags=[
                    tags[0],
                    tags[2],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1311,
                index="C",
                name="C. Test Problem #3",
                type="PROGRAMMING",
                points=1666,
                rating=2000,
                tags=[
                    tags[0],
                    tags[3],
                    tags[4],
                ]
            ),

            ProblemOrm(
                contest_id=1353,
                index="A",
                name="A. Test Problem #1",
                type="PROGRAMMING",
                points=1000,
                rating=1000,
                tags=[
                    tags[5],
                    tags[1],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1353,
                index="B",
                name="B. Test Problem #2",
                type="PROGRAMMING",
                points=1333,
                rating=1500,
                tags=[
                    tags[0],
                    tags[2],
                    tags[4],
                ]
            ),
            ProblemOrm(
                contest_id=1353,
                index="C",
                name="C. Test Problem #3",
                type="PROGRAMMING",
                points=1666,
                rating=2000,
                tags=[
                    tags[0],
                    tags[3],
                    tags[4],
                ]
            ),
        ]

        users = [
            UserOrm(
                handle="Senior",
                email="senior@mail.ru",
                vk_id="vk.com/id0",
                open_id="open_id0",
                first_name="Senior",
                last_name="Senior",
                country="Belarus",
                city="Gomel",
                organization="GSU",
                rank="master",
                max_rank="master",
                last_online_time_seconds=1614552000,
                registration_time_seconds=12312314,
                friend_of_count=1,
                avatar="https://dl.gsu.by/avatars/senior.png",
                title_photo="https://dl.gsu.by/title_photos/senior.png",
            ),
            UserOrm(
                handle="chelovek_secret"
            ),
            UserOrm(
                handle="tourist",
                vk_id="vk.com/id0",
                first_name="Gennady",
                last_name="Korotkevich",
                country="Belarus",
                city="Gomel",
                organization="ITMO",
                rank="legendary grandmaster",
                max_rank="legendary grandmaster",
            ),
            UserOrm(
                handle="Petr",
                first_name="Petr",
                last_name="Mitrichev",
                country="Russia",
                city="Moscow",
                organization="MIPT",
                rank="legendary grandmaster",
                max_rank="legendary grandmaster",
            ),
            UserOrm(
                handle="Um_nik",
                first_name="Nikita",
                last_name="Belyh",
                country="Russia",
                city="St. Petersburg",
                organization="ITMO",
                rank="legendary grandmaster",
                max_rank="legendary grandmaster",
            ),
        ]

        teams = [
            TeamOrm(
                id=1,
                team_name="Team #1",
                users=[users[0], users[1]]
            ),
            TeamOrm(
                id=2,
                team_name="Team #2",
                users=[users[3], users[4]]
            ),
        ]

        submissions = [
            SubmissionOrm(
                id=1,
                contest_id=1234,
                problem=problems[0],
                author=users[0],
                programming_language="C++",
                verdict="OK",
                passed_test_count=1,
                time_consumed_millis=1000,
                memory_consumed_bytes=100000,
                creation_time_seconds=1614552000,
                relative_time_seconds=14400,
            ),
            SubmissionOrm(
                id=2,
                contest_id=1234,
                problem=problems[0],
                author=users[1],
                programming_language="Java",
                verdict="CE",
                passed_test_count=1,
                time_consumed_millis=1000,
                memory_consumed_bytes=100000,
                creation_time_seconds=1614552000,
                relative_time_seconds=14400,
            ),
            SubmissionOrm(
                id=3,
                contest_id=1234,
                problem=problems[1],
                programming_language="python",
                verdict="RE",
                passed_test_count=1,
                time_consumed_millis=1000,
                memory_consumed_bytes=100000,
                creation_time_seconds=1614552000,
                relative_time_seconds=14400,
                team=teams[0]
            ),
            SubmissionOrm(
                id=4,
                contest_id=1234,
                problem=problems[1],
                programming_language="Rust",
                verdict="OK",
                passed_test_count=1,
                time_consumed_millis=1000,
                memory_consumed_bytes=100000,
                creation_time_seconds=1614552000,
                relative_time_seconds=14400,
                team=teams[1]
            ),
            SubmissionOrm(
                id=5,
                contest_id=1234,
                problem=problems[1],
                author=users[2],
                programming_language="C++",
                verdict="OK",
                passed_test_count=1,
                time_consumed_millis=1000,
                memory_consumed_bytes=100000,
                creation_time_seconds=1614552000,
                relative_time_seconds=14400,
            ),
        ]

        session.add_all(contests)
        session.add_all(problems)
        session.add_all(users)
        session.add_all(teams)
        session.add_all(submissions)
        session.commit()
