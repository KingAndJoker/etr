from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.contest import Contest
from etr.models.problem import Problem, Tag
from etr.models.submission import Submission
from etr.models.user import User
from etr.models.team import Team


def seeding(engine: Engine):
    with Session(engine) as session:
        contests = [
            Contest(
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
            Contest(
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
            Contest(
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
            Contest(
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
            Tag(tag="dp"),
            Tag(tag="graphs"),
            Tag(tag="math"),
            Tag(tag="recursion"),
            Tag(tag="trees"),
            Tag(tag="dfs"),
        ]

        problems = [
            Problem(
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
            Problem(
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
            Problem(
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

            Problem(
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
            Problem(
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
            Problem(
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

            Problem(
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
            Problem(
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
            Problem(
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

            Problem(
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
            Problem(
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
            Problem(
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
            User(
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
            User(
                handle="chelovek_secret"
            ),
            User(
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
            User(
                handle="Petr",
                first_name="Petr",
                last_name="Mitrichev",
                country="Russia",
                city="Moscow",
                organization="MIPT",
                rank="legendary grandmaster",
                max_rank="legendary grandmaster",
            ),
            User(
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
            Team(
                id=1,
                teamName="Team #1",
                users=[users[0], users[1]]
            ),
            Team(
                id=2,
                teamName="Team #2",
                users=[users[3], users[4]]
            ),
        ]

        submissions = [
            Submission(
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
            Submission(
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
            Submission(
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
            Submission(
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
            Submission(
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
