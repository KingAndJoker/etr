from etr.events import ResultOfHandleEvent
from etr.events.contest import ParseContestBeforeUpdate
from etr.events.contest import ParseCodeforces
from etr.events.contest import ParseCodeforcesContest
from etr.events.contest import ParseCodeforcesGym
from etr.exceptions.events import EventValueError


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
