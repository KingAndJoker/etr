from etr.events import ResultOfHandleEvent
from etr.events.contest import ParseContestBeforeUpdate
from etr.events.contest import ParseCodeforcesContest
from etr.exceptions.events import EventValueError


def handle_contest_type(
        event: ParseContestBeforeUpdate
) -> ResultOfHandleEvent:
    if not isinstance(event, ParseContestBeforeUpdate):
        raise EventValueError

    result_of_handle_event = ResultOfHandleEvent()

    if event.contest_url.host == "codeforces.com":
        result_of_handle_event.events.append(
            ParseCodeforcesContest(event.contest_url)
        )

    return result_of_handle_event


def handle_codeforces_type_contest(
    event
):
    pass
