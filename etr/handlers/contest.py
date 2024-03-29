from etr.events import ResultOfHandleEvent
from etr.events.contest import ParseContestBeforeUpdate
from etr.events.contest import ParseCodeforces
from etr.events.contest import ParseCodeforcesContest
from etr.events.contest import ParseCodeforcesGym
from etr.events.contest import AddContest
from etr.events.contest import ParseCodeforcesContestByContestId
from etr.exceptions.events import EventValueError
from etr.crud.contest import add_contest_with_schema
from etr.crud.problem import add_problem
from etr.services.problem import add_tag_for_problem
from etr.library.codeforces.codeforces_utils import get_contest
from etr.utils.codeforces.convert import convert_codeforces_contest_schema
from etr.utils.services.contest import parse_url


def handle_contest_type(
        event: ParseContestBeforeUpdate
) -> ResultOfHandleEvent:
    if not isinstance(event, ParseContestBeforeUpdate):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()

    if event.contest_url.host == "codeforces.com":
        result_of_handle_event.events.append(
            ParseCodeforces(event.contest_url)
        )

    return result_of_handle_event


def handle_codeforces_type_contest(
    event: ParseCodeforces
):
    if not isinstance(event, ParseCodeforces):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()

    if event.contest_url.path.startswith("/contest"):
        result_of_handle_event.events.append(
            ParseCodeforcesContest(event.contest_url)
        )
    if event.contest_url.path.startswith("/gym"):
        result_of_handle_event.events.append(
            ParseCodeforcesGym(event.contest_url)
        )

    return result_of_handle_event


def handle_codeforces_contest(
    event: ParseCodeforcesContest
):
    if not isinstance(event, ParseCodeforcesContest):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()
    contest_id = int(event.contest_url.path.split("/")[2])
    codeforces_contest = get_contest(contest_id=contest_id, lang="ru")
    contest = convert_codeforces_contest_schema(codeforces_contest)
    contest.type_of_source = "codeforces_contest"

    result_of_handle_event.events.append(AddContest(contest))

    return result_of_handle_event


def handle_codeforces_gym(
    event: ParseCodeforcesGym
):
    # TODO: DRY
    if not isinstance(event, ParseCodeforcesGym):
        raise EventValueError

    # TODO: DRY with handle_codeforces_contest
    result_of_handle_event = ResultOfHandleEvent()
    contest_id = int(event.contest_url.path.split("/")[2])
    codeforces_contest = get_contest(contest_id=contest_id, lang="ru")
    contest = convert_codeforces_contest_schema(codeforces_contest)
    contest.type_of_source = "codeforces_gym"

    result_of_handle_event.events.append(AddContest(contest))

    return result_of_handle_event


def handle_add_contest(
    event: AddContest
):
    if not isinstance(event, AddContest):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()

    contest = add_contest_with_schema(event.contest)
    problems = [
        add_problem(problem)
        for problem in event.contest.problems
    ]
    for problem in problems:
        [event_problem] = [
            event_problem
            for event_problem in event.contest.problems
            if event_problem.index == problem.index
        ]
        for tag in event_problem.tags:
            add_tag_for_problem(problem_id=problem.id, tag=tag)
    result_of_handle_event.results = [contest] + problems

    return result_of_handle_event


def parse_codeforces_contest_by_id(event: ParseCodeforcesContestByContestId) -> ResultOfHandleEvent:
    if not isinstance(event, ParseCodeforcesContestByContestId):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()
    if event.contest_id is None:
        # TODO: problemsetName, contestId can be missing
        return result_of_handle_event
    if event.contest_id < 100000:
        contest_url = f"https://codeforces.com/contest/{event.contest_id}"
    else:
        contest_url = f"https://codeforces.com/gym/{event.contest_id}"
    url = parse_url(contest_url)
    result_of_handle_event.events.append(ParseContestBeforeUpdate(url))

    return result_of_handle_event
