class Event:
    pass


class ResultOfHandleEvent:
    events: list[Event]
    results: list

    def __init__(self, events=None, results=None) -> None:
        if events is None:
            events = []
        if results is None:
            results = []

        self.events = events
        self.results = results
