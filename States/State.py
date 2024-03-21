# parent State class that describes an acitivty that exists for a period of time. a State is associated with a specific user, and
# has a start time and end time.
from datetime import datetime, timedelta 
from pandas import DataFrame
from Events.Event import Event
from Events.PageExit import PageExit


class State:
    # this list will hold the list of Events ordered by increasing timestamp, but with 'synthetic' Page Exit events
    # added for every Page Entry to more easily create State objects
    # this is a list of dictionaries corresponding to Events
    ordered_events=[]

    def __init__(self, user_id, startTime, endTime, kind=None):
        self.kind=kind
        self.user_id = user_id
        self.startTime = startTime
        self.endTime = endTime

    @staticmethod
    # This method will populate the ordered_events static list by creating a "Page Exit" Event to match every
    # Page Entry event, adding all of these to the list along with every event in the original Events
    # list (in Events.py, created when Events are parsed in), and ordering them by timestamp.
    # So the resulting ordered_events after this function returns will hold a  list of Events,
    # ordered by increasing timestamp, with new 'synthetic' Page Exits events included to complement every Page Entry.
    # takes array of Events as input
    def populateOrderedEvents(events):
        # first order the Events DF by increasing timestamp
        sortedEvents = sorted(events, key=lambda event: event['timestamp'])
        currentPage= None
        for event in sortedEvents:
            # this case is for the first page entry event found in the list
            isPageEntry = event['kind'] == 'PageEntry'
            if isPageEntry and currentPage == None:
                currentPage= event['page']
                State.ordered_events.append(event)
                continue
            # when we find the next page entry event, this corresponds to an exit from the current page.
            # Logout also counts as a 'page entry' into the Logout screen.
            # create Page Exit event for it
            if event['kind'] == 'Logout' or isPageEntry:
                # make page exit timestamp a slight bit before current pages timestamp
                exitTimestamp = subtract_millisecond(event['timestamp'])
                State.ordered_events.append((PageExit({'user_id':event['user_id'], 'timestamp': exitTimestamp}, currentPage)).__dict__)
                currentPage=event['page'] if event['kind'] == 'PageEntry' else 'Logout Page' # update current page
            State.ordered_events.append(event)
        return State.ordered_events


# given a timestamp as a string, subtracts 1 millisecond from it and returns modified timestamp
def subtract_millisecond(timestamp_str):
    # Convert string timestamp to datetime object
    original_timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S.%f')

    # Subtract 1 millisecond
    modified_timestamp = original_timestamp -timedelta(milliseconds=1)

    # Return modified timestamp
    return modified_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
