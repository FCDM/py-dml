class TimelineError(Exception):
    """
    An error thrown when an attempt is made to alter a Timeline
    after it has already begun running.
    """
    pass


class Timeline(object):
    """
    A scheduling system that stores a list of time-based events
    (Timestamp objects).
    """

    def __init__(self):
        self._timestamps = []
        self._next = None
        self._running = False

    def addTimestamp(self, timestamp):
        """Add a timestamp to the timeline."""
        if self._running:
            raise TimelineError(
                "Cannot add timestamp while timeline is active.")
        self._timestamps.append(timestamp)

    def begin(self):
        """Begin running the timeline."""
        self._timestamps.sort(key=lambda x: x.time)
        if self._timestamps:
            self._next = self._timestamps.pop()

    def doNext(self, time, *args, **kwargs):
        """Perform the next action in the timeline."""
        while self._next and self._next.time > time:
            self._next.performAction(*args, **kwargs)
            self._next = self._timestamps.pop() if self._timestamps else None


class Timestamp(object):
    """
    A single action to perform, stored by the timeline.
    """

    def __init__(self, time, action):
        self.time = time
        self.performAction = action
