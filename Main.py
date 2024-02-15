import pandas as pd
import matplotlib.pyplot as plt
from EventContainers.EmojiSelectSequence import EmojiSelectSequence
from Events.Event import Event
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog
from SqliteUtils import Database
from EventFactory import create_announcement, create_comment, create_event_object, create_microblog
from Events.EmojiSelect import EmojiSelect

def main():
    db = Database(
        r"db\FromEchoDev240208a_echo_main_db_current.sqlite3"
    )
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

        # create a dataframe for videoactivities
        df = pd.DataFrame.from_dict(Event.events)
        print(df)

        # Example of time sequence of a user's login events
        print("************ Examples of Login Events ************")
        user_logins = df[(df['user_id'] == 75) & (df['kind']=='Login')]
        print("Emily's Login Events:")
        print(user_logins[['user_id', 'kind', 'timestamp']])

        user_logins = df[(df['user_id'] == 76) & (df['kind'] == 'Login')].sort_values('timestamp')
        print("Crystal's Login Events:")
        print(user_logins[['user_id', 'kind', 'timestamp']])
        print("**************************************************")

        # show an example of a user's emoji select sequence by plotting score(intensity, emotion) vs time
        userId = 75
        emojiDf = EmojiSelectSequence(userId).emojiEventsDf
        # convert to datetime format
        emojiDf.loc[:, 'timestamp'] = pd.to_datetime(emojiDf['timestamp'])
        # plot score vs time
        print("\n******** Examples of Emoji Select Events *********")
        plt.figure(figsize=(8, 5))
        plt.plot(emojiDf['timestamp'], emojiDf['IntensityScore'], label='Intensity', marker='o', linestyle='solid')
        plt.plot(emojiDf['timestamp'], emojiDf['EmotionScore'], label='Emotion', marker='x', linestyle='dashed')
        plt.xlabel('Time')
        plt.ylabel('Score')
        plt.legend()
        plt.title('Emoji Changes Over Time for User ' + str(userId))
        plt.show()

    finally:
        db.close()

if __name__ == "__main__":
    main()
