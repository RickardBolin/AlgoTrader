from backend.algorithm import get_event_list



## Hmmh... Not quite sure how to structure this.
class Market:

    def __init__(self, date):
        self.date = date
        self.bots = []
        # Get price changes of all stocks sorted by time
        self.event_list = get_event_list(tickers=tickers, start=start, end=end, interval=interval)


