import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import os

from SqliteUtils import Database
from EventFactory import create_announcement, create_comment, create_event_object, create_microblog
from Events.Event import Event
from Posts.Announcement import Announcement
from Posts.Comment import Comment
from Posts.Microblog import Microblog
from EventContainers.EmojiSelectSequence import EmojiSelectSequence
from EventContainers.VideoWatchSequence import VideoWatchSequence
from EventContainers.UserActivity import UserActivity, calculate_time_spent_per_day, count_login_page_activities_per_day
from States.State import State
from StateContainers.LoggedInStateSequence import LoggedInSequence
from StateContainers.OnMicroblogStateSequence import OnMicroblogSequence
from StateContainers.OnVideoPageStateSequence import OnVideoPageSequence
from StateContainers.WatchingVideoStateSequence import WatchingVideoStateSequence
from EventContainers.MicroblogVisitsSequence import MicroblogVisitsSequence
from EmojiIndicators import EmojiIndicators

# execute a given query and return the results
def query_database(db, query):
    return db.run_query(query)

# create and add event objects from query results
def create_event_objects(results):
    for row in results:
        event = create_event_object(row)
        if event: 
            Event.add(event)
        else:
            print("Invalid event")

# create and add post objects (Announcements, Comments, Microblogs) from query results
def create_post_objects(results, post_type):
    for row in results:
        if post_type == 'announcement':
            post = create_announcement(row)
            if post:
                Announcement.add(post)
        elif post_type == 'comment':
            post = create_comment(row)
            if post:
                Comment.add(post)
        elif post_type == 'microblog':
            post = create_microblog(row)
            if post:
                Microblog.add(post)

# create a dataframe from query results from database
def create_events_dataframe(events, output_file_name):
    events_df = pd.DataFrame.from_dict(events)
    events_df.to_csv(f"{output_file_name}.csv", index=False)
    return events_df

# create a dataframe of synthetic Page Exits
def create_page_exits_dataframe(events):
    page_exit_list = State.populateOrderedEvents(events)
    page_exit_df = pd.DataFrame.from_dict(page_exit_list)
    page_exit_df.to_csv("page_exit_df.csv", index=False)
    return page_exit_df

# filter activities by user_id from a given events dataframe
def filter_activities_by_user(events_df, user_id):
    return events_df[events_df['user_id'] == user_id]

# filter login events for a given user from a given events dataframe
def filter_login_events(events_df, user_id):
    return events_df[(events_df['user_id'] == user_id) & (events_df['kind'] == 'Login')].sort_values('timestamp')

# show all activities for a given user
def show_user_activities(user_activities, user_id):
    df_activities = pd.DataFrame([vars(a) for a in user_activities])
    df_activities['timestamp'] = pd.to_datetime(df_activities['timestamp'])
    df_activities['date'] = df_activities['timestamp'].dt.date
    df_activities['time'] = df_activities['timestamp'].dt.time
    user_activities_df = filter_activities_by_user(df_activities, user_id)
    grouped_activities = user_activities_df.groupby('date')
    # representation for each day
    print(f"Activities for user {user_id}:")
    for date, group in grouped_activities:
        print(f"Date: {date}")
        print(tabulate(group[['user_id', 'time', 'activityType', 'page' ]], headers='keys', tablefmt='pretty'))
        print("\n")  
    user_activities_df = user_activities_df.sort_values('timestamp')

# print the total time spent per day by a given user
def print_time_spent_per_day(user_activities, user_id):
    df_activities = pd.DataFrame([vars(a) for a in user_activities])
    df_time_spent = calculate_time_spent_per_day(df_activities, user_id)
    print(f"Total time spent per day by user {user_id}:")
    print(tabulate(df_time_spent, headers='keys', tablefmt='pretty'))

# print login count per day for a given user
def print_login_count_per_day(user_activities, user_id):
    df_activities = pd.DataFrame([vars(a) for a in user_activities])
    login_count_per_user_day = count_login_page_activities_per_day(df_activities, user_id)
    if not login_count_per_user_day.empty:
        print(f"Number of 'Login Page' activities per day for user {user_id}:")
        print(tabulate(login_count_per_user_day, headers='keys', tablefmt='pretty'))
    else:
        print(f"No 'Login Page' activities found for user {user_id}.")

# show all comments for a given microblog
def show_comments_for_microblog(microblog_id):
    # create a dataframe for all comments of a given microblog
    microblog_comments = Comment.get_comments_for_microblog(microblog_id)
    comments_for_microblog_df = create_events_dataframe(microblog_comments, "comments_for_microblog" + str(microblog_id))

# show all comments made by a given author
def show_comments_for_author(author_id):
    author_comments = Comment.get_comments_by_author(author_id)
    comments_for_author_df = create_events_dataframe(author_comments, "comments for author" + str(author_id))


# main function
def main():
    db = Database(os.path.join("db", "FromEchoDev240208a_echo_main_db_current.sqlite3"))
    db.connect()
    try:
        # read in event objects
        event_query = "SELECT * FROM EchoApp_videoactivity"
        results = query_database(db, event_query)
        create_event_objects(results)

        # read in announcements, comments, microblog objects
        ann_query = "SELECT * from EchoApp_announcement"
        results = query_database(db, ann_query)
        create_post_objects(results, 'announcement')
        comm_query="SELECT * from EchoApp_comment"
        results = query_database(db, comm_query)
        create_post_objects(results, 'comment')
        microblog_query="SELECT * from EchoApp_microblog"
        results = query_database(db, microblog_query)
        create_post_objects(results, 'microblog')

        # read in user activity objects
        activity_results = query_database(db, event_query)
        user_activities = []
        for row in activity_results:
            activity = UserActivity.create_user_activity(row)
            user_activities.append(activity)
        
        # create a df for all users' activities based on videoactivities
        events_df = create_events_dataframe(Event.events, "events_df")

        # create updated df of events with synthetic Page Exits
        page_exit_df = create_page_exits_dataframe(Event.events)

        # =====examples for a user=====
        user_id = 75

        # show a user's login events
        user_logins_df = filter_login_events(events_df, user_id)
        print(f"Login events for user {user_id}:")
        print(user_logins_df[['user_id', 'kind', 'timestamp']])

        # show a user's all activities
        show_user_activities(user_activities, user_id)
        # analyze a user's all activities by day
        print_time_spent_per_day(user_activities, user_id)
        print_login_count_per_day(user_activities, user_id)

        # show all comments for a given microblog
        microblog_id = 6
        show_comments_for_microblog(microblog_id)
        # show all comments for a given author
        author_id = 30
        show_comments_for_author(author_id)





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
        # plt.show()

        tracker = EmojiIndicators(emojiDf)
        # Calculate the indicators
        frequency = tracker.get_frequency()
        regularity = tracker.get_regularity()
        emometer_scores = tracker.get_emometer_scores()
        mindfulness = tracker.get_mindfulness()

        # Display the results
        results = [
            ("Frequency", frequency),
            ("Regularity (standard deviation)", regularity),
            ("Emometer Intensity Baseline", emometer_scores.get('IntensityBaseline')),
            ("Emometer Intensity Average", emometer_scores.get('IntensityAverage')),
            ("Emometer Intensity StdDev", emometer_scores.get('IntensityStdDev')),
            ("Emometer Emotion Baseline", emometer_scores.get('EmotionBaseline')),
            ("Emometer Emotion Average", emometer_scores.get('EmotionAverage')),
            ("Emometer Emotion StdDev", emometer_scores.get('EmotionStdDev')),
            ("Mindfulness", mindfulness),
        ]
    
        print(f"\nEmoji Activity Indicators for User {userId}:\n")
        print(tabulate(results, headers=["Indicator", "Value"], tablefmt="github"))


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
        # plt.scatter(x,y)
        plt.xlabel('Time')
        plt.ylabel('Action')
        plt.title('Video Actions for User ' + str(userId) + ' For ' + str(videoId) )
        # plt.show()

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

        # Show State objects

        # On Microblog state-- create sequence
        microblog_state_seq = OnMicroblogSequence(page_exit_df, 76)
        print("states of being on microblog for user 76")
        on_mb_df = microblog_state_seq.states_df
        print(on_mb_df)

        # On video page-- state sequence
        on_video_seq = OnVideoPageSequence(page_exit_df, 76)
        print("states of being on videos page for user 76")
        video_seq_df=on_video_seq.states_df
        print(video_seq_df)

        # Watching video -- state sequence
        watching_video_states = WatchingVideoStateSequence(76, 'video1')
        print('states of watching video1 for user 76')
        watching_df = watching_video_states.states_df
        print(watching_video_states.states_df)
        # Logged In -- state sequnece
        logged_in_states = LoggedInSequence(page_exit_df, 76)
        print("states of being logged in for user 76")
        logged_in_df = logged_in_states.states_df
        print(logged_in_df)

        # plot
        # video watching
        watching_df["startTime"] = pd.to_datetime(watching_df["startTime"])
        watching_df['endTime'] = pd.to_datetime(watching_df['endTime'])
        video_seq_df["startTime"] = pd.to_datetime(video_seq_df["startTime"])
        print(video_seq_df['endTime'])
        video_seq_df["endTime"] = pd.to_datetime(
            video_seq_df["endTime"], format="%Y-%m-%d %H:%M:%S.%f"
        )
        on_mb_df["startTime"] = pd.to_datetime(on_mb_df["startTime"])
        on_mb_df["endTime"] = pd.to_datetime(
            on_mb_df["endTime"], format="%Y-%m-%d %H:%M:%S.%f"
        )
        logged_in_df["startTime"] = pd.to_datetime(logged_in_df["startTime"])
        logged_in_df["endTime"] = pd.to_datetime(
            logged_in_df["endTime"], format="mixed"
        )
        print(authors_df)
        authors_comments = Comment.get_comments_by_author(76)
        # Convert the list of comments to a DataFrame for better tabular representation
        authors_df = pd.DataFrame(authors_comments)
        authors_df["createdDate"] = pd.to_datetime(authors_df["createdDate"], format="mixed")
        authors_df["updatedDate"] = pd.to_datetime(authors_df["updatedDate"], format="mixed")

        fig, ax = plt.subplots()
        # Watching Video State
        for _, row in watching_df.iterrows():
            ax.plot(
                [row["startTime"], row["endTime"]],
                [row["kind"], row["kind"]],
                marker="o", color='purple'
            )
        for _, row in video_seq_df.iterrows():
            ax.plot(
                [row["startTime"], row["endTime"]],
                [row["kind"], row["kind"]],
                marker="o", color='red'
            )
        for _, row in microblog_state_seq.states_df.iterrows():
            ax.plot(
                [row["startTime"], row["endTime"]],
                [row["kind"], row["kind"]],
                marker="o", color='blue'
            )
        for _, row in on_mb_df.iterrows():
            ax.plot(
                [row["startTime"], row["endTime"]],
                [row["kind"], row["kind"]],
                marker="o",
                color="blue",
            )
        for _, row in logged_in_df.iterrows():
            ax.plot(
                [row["startTime"], row["endTime"]],
                [row["kind"], row["kind"]],
                marker="o",
                color="blue",
            )
            # microblog comment instances
        ax.plot(authors_df['createdDate'], ['PostedOnMicroblog'],marker="o", color="black")
        ax.plot(
            authors_df["updatedDate"], ["UpdatedMicrblogComment"], marker="o", color="black"
        )

        # Set labels and title
        # Customize font for different text elements
        title_font = {'family': 'serif', 'color': 'blue', 'weight': 'bold', 'size': 16}
        axis_label_font = {'family': 'sans-serif', 'color': 'green', 'weight': 'normal', 'size': 12}
        tick_label_font = {'family': 'monospace', 'color': 'red', 'weight': 'normal', 'size': 10}   
        ax.set_xlabel('Timestamp', fontdict=axis_label_font)
        ax.set_ylabel('Kind of Interaction', fontdict=axis_label_font)
        ax.set_title('Timeline of Interactions for User 76', fontdict=title_font)
        plt.xticks(rotation=20)
        plt.xticks(fontsize=6)

        date_format = DateFormatter('%Y-%m-%d %H:%M:%S.%f')
        ax.xaxis.set_major_formatter(date_format)

        mb_count = Comment.count_comments_by_author(76)
        avg_len = Comment.average_comment_length_by_author(76)
        login_amt = count_login_page_activities_per_day(user_activities, 76)
        print(login_amt["login_count"].sum())
        print(login_amt["login_count"].count())
        avg_logins = login_amt['login_count'].sum() / login_amt['login_count'].count()
        text_content = """
            Number of Microblog posts made by this author: {}
            Average Length of Microblog Posts In Characters: {}
            Avg Amount of Logins Per Day: {}       
        """.format(mb_count, avg_len, avg_logins)
        ax.text(0.3, 0.5, text_content, transform=ax.transAxes,
        fontsize=12, ha='center', va='center')

        plt.show()

    finally:
        db.close()

if __name__ == "__main__":
    main()
