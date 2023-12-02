from typing import Callable

from etr.events import Event, ResultOfHandleEvent
from etr.events.contest import ParseContestBeforeUpdate
from etr.events.contest import ParseCodeforces
from etr.events.contest import ParseCodeforcesContest
from etr.events.contest import ParseCodeforcesGym
from etr.events.contest import AddContest
from etr.handlers.contest import handle_contest_type
from etr.handlers.contest import handle_codeforces_type_contest
from etr.handlers.contest import handle_codeforces_contest
from etr.handlers.contest import handle_codeforces_gym
from etr.handlers.contest import handle_add_contest


HANDLERS: dict[Event, list[Callable[[Event], ResultOfHandleEvent]]] = {
    ParseContestBeforeUpdate: [handle_contest_type],
    ParseCodeforces: [handle_codeforces_type_contest],
    ParseCodeforcesContest: [handle_codeforces_contest],
    ParseCodeforcesGym: [handle_codeforces_gym],
    AddContest: [handle_add_contest],
}


def handle(event: Event) -> list:
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            result_of_work = handler(event)
            results.extend(result_of_work.results)
            queue.extend(result_of_work.events)
    return results
