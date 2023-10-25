from sqlalchemy import Engine
from sqlalchemy.orm import Session

from etr.models.problem import Problem, Tag


def test_problem_create(in_memory_db_empty: Engine):
    """Test creating a problem."""

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="A",
            name="Two Sum"
        )
        session.add(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        assert problem.contest_id == 1, "contest_id is not equal to 1."
        assert problem.index == "A", "index is not equal to 'A'."
        assert problem.name == "Two Sum", "name is not equal to 'Two Sum'."
        assert problem.tags == [], "tags is not empty."
        assert problem.submissions == [], "submissions is not empty."


def test_problem_create_all_fields(in_memory_db_empty: Engine):
    """Test creating a problem with all fields."""

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=7,
            index="B",
            name="Ghoul",
            problemset_name="leetcode",
            type="PROGRAMMING",
            points=1000,
            rating=993,
            tags=[
                Tag(tag="graph"),
                Tag(tag="bfs"),
                Tag(tag="dfs")
            ]
        )
        session.add(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).filter_by(
            contest_id=7,
            index="B"
        ).one_or_none()

        assert problem.contest_id == 7, "contest_id is not equal to 7."
        assert problem.index == "B", "index is not equal to 'B'."
        assert problem.name == "Ghoul", "name is not equal to 'Ghoul'."
        assert problem.problemset_name == "leetcode", "problemset_name is not equal to 'leetcode'."
        assert problem.type == "PROGRAMMING", "type is not equal to 'PROGRAMMING'."
        assert problem.points == 1000, "points is not equal to 1000."
        assert problem.rating == 993, "rating is not equal to 993."
        assert problem.tags[0].tag == "graph", "tags[0].tag is not equal to 'graph'."
        assert problem.tags[1].tag == "bfs", "tags[1].tag is not equal to 'bfs'."
        assert problem.tags[2].tag == "dfs", "tags[2].tag is not equal to 'dfs'."
        assert problem.submissions == [], "submissions is not empty."


def test_problem_update(in_memory_db_empty: Engine):
    """Test updating a problem."""

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="С",
            name="Two Sum II - Input array is sorted"
        )
        session.add(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).filter(
            Problem.contest_id == 1,
            Problem.index == "С"
        ).one_or_none()
        problem.name = "Car Parking System"
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one()
        assert problem.name == "Car Parking System", "name is not equal to 'Car Parking System'."


def test_problem_delete(in_memory_db_empty: Engine):
    """Test deleting a problem."""

    with Session(in_memory_db_empty) as session:
        problem = Problem(
            contest_id=1,
            index="D",
            name="Design Circular Queue"
        )
        session.add(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one_or_none()
        session.delete(problem)
        session.commit()
    
    with Session(in_memory_db_empty) as session:
        problem = session.query(Problem).one_or_none()
        assert problem is None, "problem is not None."
