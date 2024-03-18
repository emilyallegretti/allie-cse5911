import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import os

from EventContainers.EmojiSelectSequence import EmojiSelectSequence
from EventContainers.VideoWatchSequence import VideoWatchSequence
from Events.Event import Event
from Events.UserActivity import create_user_activity
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog
from SqliteUtils import Database
from EventFactory import create_announcement, create_comment, create_event_object, create_microblog

from EventContainers.MicroblogVisitsSequence import MicroblogVisitsSequence


def main():
    db = Database(os.path.join("db", "FromEchoDev240208a_echo_main_db_current.sqlite3"))
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
        #print(Event.events)
        # read in announcements, comments, microblog objects
        ann_query="SELECT * from EchoApp_announcement"
        results=db.run_query(ann_query)
        for row in results:
            print(row['ann_body'])
            ann = create_announcement(row)
            if ann:
                Announcement.add(ann)
        #print(Announcement.announcements)

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
        #print(Microblog.microblogs)

        user_activity_query = "SELECT * FROM EchoApp_videoactivity"
        results = db.run_query(user_activity_query)
        user_activities = []
        for row in results:
            activity = create_user_activity(row)
            user_activities.append(activity)

        
        # create a dataframe for videoactivities
        df = pd.DataFrame.from_dict(Event.events)
        df.to_csv("output.csv")
        # pretty print
        print(df)
        
        
        # Example of time sequence of a user's login events
        print("************ Examples of Login Events ************")
        user_logins = df[(df['user_id'] == 75) & (df['kind']=='Login')]
        print("Emily's Login Events:")
        print(user_logins[["user_id", "kind", "timestamp"]])

        user_logins = df[(df['user_id'] == 76) & (df['kind'] == 'Login')].sort_values('timestamp')
        print("Crystal's Login Events:")
        print(user_logins[['user_id', 'kind', 'timestamp']])
        print("**************************************************")

        
        df_activities = pd.DataFrame([vars(a) for a in user_activities])

        df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
        df_activities['date'] = df_activities['timestamp'].dt.date
        df_activities['time'] = df_activities['timestamp'].dt.time

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

        
        # Get all comments for a specific microblog
        specific_microblog_id = 6  # replace with the actual microblog_id you want to query
        comments = Comment.get_comments_for_microblog(specific_microblog_id)

        comments_df = pd.DataFrame(comments)

        print(comments_df)
        print("-" * 144)

        # Get all comments for a specific author
        author_id = 30
        authors_comments = Comment.get_comments_by_author(author_id)

        # Convert the list of comments to a DataFrame for better tabular representation
        authors_df = pd.DataFrame(authors_comments)

        # Display the DataFrame
        print(authors_df)
        
        
        
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

        # show an example of a user's video watching sequence by plotting pauses/plays vs time
        userId = 74
        videoId = 'video2'
        videoDf = VideoWatchSequence(userId, videoId).videoEventsDf
        # get only time out of timestamp
        videoDf.loc[:, "timestamp"] = videoDf['timestamp'].apply(lambda x: x[11:])
        # plot action vs time
        videoDf["time_only"] = videoDf["timestamp"]
        x = videoDf["time_only"]
        y = videoDf["kind"]
        plt.scatter(x,y)
        plt.xlabel('Time')
        plt.ylabel('Action')
        plt.title('Video Actions for User ' + str(userId) + ' For ' + str(videoId) )
        plt.show()


        # Microblog Visited Frequency
        # get all users' id
        unique_user_ids = df_activities['user_id'].unique()
        print("\nMicroblog Visited Frequency for All Users:")
        # initialize a list for all visits data
        all_visits_data = []  
        # iterate each user to create an instance, and get their visit counts
        for user_id in unique_user_ids:
            microblog_visits_sequence = MicroblogVisitsSequence(user_id, df_activities)
            visit_counts_sorted = microblog_visits_sequence.count_microblog_visits()
            if not visit_counts_sorted.empty:
                for index, row in visit_counts_sorted.iterrows():
                    all_visits_data.append([user_id, row['date'], row['visit_count']])
        # convert all visits data to a DataFrame for easily showing the result
        df_all_visits = pd.DataFrame(all_visits_data, columns=['User ID', 'Date', 'Visit Count'])
        # sort the DataFrame by user_id and date
        df_all_visits_sorted = df_all_visits.sort_values(by=['User ID', 'Date'])
        # show the table
        print(tabulate(df_all_visits_sorted, headers='keys', tablefmt='pretty'))

        print("**************************************************")

        author_id = 1

        # Get the number of comments by the author
        num_comments = Comment.count_comments_by_author(author_id)
        print(f"Author {author_id} has made {num_comments} comments.")

        # Get the average comment length by the author
        avg_length = Comment.average_comment_length_by_author(author_id)
        print(f"Author {author_id}'s average comment length is {avg_length} characters.")


    finally:
        db.close()

if __name__ == "__main__":
    main()
