import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate  # New import
from Events.Event import Event
from Events.UserActivity import create_user_activity
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog
from SqliteUtils import Database
from EventFactory import create_announcement, create_comment, create_event_object, create_microblog

def main():
    db = Database(
        r"FromEchoDev240208a_echo_main_db_current.sqlite3"    )
    
    db.connect()

    try:        
        # read in event objects
        videoactivity_query = "SELECT * FROM EchoApp_videoactivity"
        results = db.run_query(videoactivity_query)

        for row in results:
            event = create_event_object(row)
            if event: 
                Event.add(event)
            else:
                print("Invalid event")
        print(Event.events)
        # read in announcements, comments, microblog objects
        ann_query="SELECT * from EchoApp_announcement"
        results=db.run_query(ann_query)
        for row in results:
            print(row['ann_body'])
            ann = create_announcement(row)
            if ann:
                Announcement.add(ann)
        print(Announcement.announcements)

        comm_query="SELECT * from EchoApp_comment"
        results = db.run_query(comm_query)
        for row in results:
            comm = create_comment(row)
            if comm:
                Comment.add(comm)

        microblog_query="SELECT * from EchoApp_microblog"
        results = db.run_query(microblog_query)
        for row in results:
            microblog = create_microblog(row)
            if microblog:
                Microblog.add(microblog)
        print(Microblog.microblogs)

        user_activity_query = "SELECT * FROM EchoApp_videoactivity"
        results = db.run_query(user_activity_query)
        user_activities = []
        for row in results:
            activity = create_user_activity(row)
            user_activities.append(activity)


        # Create a dataframe
        df = pd.DataFrame.from_dict(Event.events)
        print(df)

        # Example of time sequence of a user's login events
        print((df['user_id']==75)[75])
        user_logins = df[(df['user_id'] == 75) & (df['kind']=='Login')]
        print("Emily's Login Events:")
        print(user_logins[['user_id', 'kind', 'timestamp']])

        user_logins = df[(df['user_id'] == 76) & (df['kind'] == 'Login')].sort_values('timestamp')
        print("Crystal's Login Events:")
        print(user_logins[['user_id', 'kind', 'timestamp']])


        df_activities = pd.DataFrame([vars(a) for a in user_activities])

        df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
        df_activities['date'] = df_activities['timestamp'].dt.date
        df_activities['time'] = df_activities['timestamp'].dt.timet

        user_id = 62  
        user_activities_df = df_activities[df_activities['user_id'] == user_id]


        grouped_activities = user_activities_df.groupby('date')

        print("Abdi's Login Events:")

        # representation for each day
        for date, group in grouped_activities:
            print(f"Activities for {date}:")
            print(tabulate(group[['user_id', 'time', 'activityType' ]], headers='keys', tablefmt='pretty'))
            print("\n")  
        
        user_activities_df = user_activities_df.sort_values('timestamp')

        

       
    finally:
        db.close()

if __name__ == "__main__":
    main()
