from typing import Callable

from etr.events import Event, ResultOfHandleEvent
from etr.events.contest import UpdateContest
from etr.events.contest import ParseCodeforcesContest
from etr.handlers.contest import handle_contest_type
from etr.handlers.contest import handle_codeforces_type_contest


HANDLERS: dict[Event, list[Callable[[Event], ResultOfHandleEvent]]] = {
    UpdateContest: [handle_contest_type],
    ParseCodeforcesContest: [handle_codeforces_type_contest]
}


def handle(event: Event) -> list:
    results = []
    queue = [event]
    while queue:
        event = queue.pop(0)
        for handler in HANDLERS[type(event)]:
            result_of_work = handler(event)
            results.append(result_of_work.results)
            queue.extend(result_of_work.events)
    return results
