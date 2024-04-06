import pandas as pd
from Events.Event import Event


# this EventContainer takes a userId in its constructor and creates a
# Pandas dataframe representing the user's sequence of visits to the Announcements page.
class AnnouncementsVisitsSequence:
    def __init__(self, userId):
        # first get a list of only Page Entry events where page = Announcements
        videoEvents = AnnouncementsVisitsSequence._filterEvents()
        # create dataframe out of resulting list
        df = pd.DataFrame.from_dict(videoEvents)
        # create instance variable that filters this df based on userId
        self.annVisitsDf = df[
            (df["user_id"] == userId)
        ].sort_values("timestamp")
        print(self.annVisitsDf)

    # filters Event.events to get only Announcement visits 
    @staticmethod
    def _filterEvents():
        list = []
        for item in Event.events:
            if item["kind"] == "PageEntry" and item["page"] == "Announcements":
                list.append(item)
        return list
