import numpy as np
import pandas as pd
from matplotlib.dates import DateFormatter
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import os

from SqliteUtils import Database
from EventFactory import create_announcement, create_comment, create_event_object, create_microblog
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go
import pandas as pd


from EventContainers.EmojiSelectSequence import EmojiSelectSequence
from EventContainers.VideoWatchSequence import VideoWatchSequence
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
    if not results:
        print("No event results to process")
        return
    for row in results:
        event = create_event_object(row)
        if event: 
            Event.add(event)
        else:
            print("Invalid event")

# create and add post objects (Announcements, Comments, Microblogs) from query results
def create_post_objects(results, post_type):
    if not results:
        print("No post results to process")
        return
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
    if not events:
        print("No events to process")
        return
    events_df = pd.DataFrame.from_dict(events)
    events_df.to_csv(f"{output_file_name}.csv", index=False)
    return events_df

# create a dataframe of synthetic Page Exits
def create_page_exits_dataframe(events):
    if not events:
        print("No events to process")
        return
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
    if not user_activities:
        print(f"No activities found for user {user_id}.")
        return
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

# print the total time spent per day for a given user
def print_time_spent_per_day(user_activities, user_id):
    if not user_activities:
        print(f"Because of no activities found for user {user_id}, time spent per day cannot be printed")
        return
    df_activities = pd.DataFrame([vars(a) for a in user_activities])
    df_time_spent = calculate_time_spent_per_day(df_activities, user_id)
    print(f"Total time spent per day by user {user_id}:")
    print(tabulate(df_time_spent, headers='keys', tablefmt='pretty'))

# print login count per day for a given user
def print_login_count_per_day(user_activities, user_id):
    if not user_activities:
        print(f"Because of no activities found for user {user_id}, login count per day cannot be printed")
        return
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
    comments_df = create_events_dataframe(microblog_comments, "comments_for_microblog " + str(microblog_id))

# show comments made by a given author
def show_comments_for_author(author_id):
    authors_comments = Comment.get_comments_by_author(author_id)
    authors_df = create_events_dataframe(authors_comments, "comments for author " + str(author_id))

# print comment count for a given author
def print_comment_count_for_author(author_id):
    num_comments = Comment.count_comments_by_author(author_id)
    print(f"Author {author_id} has made {num_comments} comments.")

# print average comment length for a given author
def print_avg_comment_length_for_author(author_id):
    avg_length = Comment.average_comment_length_by_author(author_id)
    print(f"Author {author_id}'s average comment length is {avg_length} characters.")

# show the frequency of visits to microblogs for all users in the given DataFrame
def show_microblog_visit_frequency(df_activities):
    unique_user_ids = df_activities['user_id'].unique()
    all_visits_data = []
    for user_id in unique_user_ids:
        microblog_visits_sequence = MicroblogVisitsSequence(user_id, df_activities)
        visit_counts_sorted = microblog_visits_sequence.count_microblog_visits()
        if not visit_counts_sorted.empty:
            for index, row in visit_counts_sorted.iterrows():
                all_visits_data.append([user_id, row['date'], row['visit_count']])
    df_all_visits = pd.DataFrame(all_visits_data, columns=['User ID', 'Date', 'Visit Count'])
    df_all_visits_sorted = df_all_visits.sort_values(by=['User ID', 'Date'])
    print("\nMicroblog Visited Frequency for All Users:")
    print(tabulate(df_all_visits_sorted, headers='keys', tablefmt='pretty'))

# initialize emoji select sequence and return a dataframe of emoji select events for a given user
def create_emoji_dataframe_for_user(userId):
    emojiDf = EmojiSelectSequence(userId).emojiEventsDf
    if emojiDf.empty:
        print(f"Because of no emoji select events found for user {userId}, no dataframe can be created")
        return pd.DataFrame()
    emojiDf.loc[:, 'timestamp'] = pd.to_datetime(emojiDf['timestamp']) # convert to datetime format
    return emojiDf

# plot emoji select sequence with score vs time for a given user
def plot_emoji_select_sequence(emojiDf, userId):
    if emojiDf.empty:
        print(f"Because of no emoji select events found for user {userId}, no plot can be shown")
        return
    plt.figure(figsize=(8, 5))
    plt.plot(emojiDf['timestamp'], emojiDf['IntensityScore'], label='Intensity', marker='o', linestyle='solid')
    plt.plot(emojiDf['timestamp'], emojiDf['EmotionScore'], label='Emotion', marker='x', linestyle='dashed')
    plt.xlabel('Time')
    plt.ylabel('Score')
    plt.legend()
    plt.title(f'Emoji Changes Over Time for User {userId}')
    plt.show()

# calculate and show emoji activity indicators for a given user
def show_emoji_activity_indicators(emojiDf, userId):
    if emojiDf.empty:
        print(f"Because of no emoji select events found for user {userId}, no indicators can be shown")
        return
    indicators = EmojiIndicators(emojiDf)
    frequency = indicators.get_frequency()
    regularity = indicators.get_regularity()
    emometer_scores = indicators.get_emometer_scores()
    mindfulness = indicators.get_mindfulness()
    results = [
        ("Frequency", frequency if not isinstance(frequency, pd.Series) else float(frequency.iloc[0])),
        ("Regularity (standard deviation)", regularity if not isinstance(regularity, pd.Series) else float(regularity.iloc[0])),
        ("Emometer Intensity Baseline", emometer_scores.get('IntensityBaseline') if not isinstance(emometer_scores.get('IntensityBaseline'), pd.Series) else float(emometer_scores.get('IntensityBaseline').iloc[0])),
        ("Emometer Intensity Average", emometer_scores.get('IntensityAverage') if not isinstance(emometer_scores.get('IntensityAverage'), pd.Series) else float(emometer_scores.get('IntensityAverage').iloc[0])),
        ("Emometer Intensity StdDev", emometer_scores.get('IntensityStdDev') if not isinstance(emometer_scores.get('IntensityStdDev'), pd.Series) else float(emometer_scores.get('IntensityStdDev').iloc[0])),
        ("Emometer Emotion Baseline", emometer_scores.get('EmotionBaseline') if not isinstance(emometer_scores.get('EmotionBaseline'), pd.Series) else float(emometer_scores.get('EmotionBaseline').iloc[0])),
        ("Emometer Emotion Average", emometer_scores.get('EmotionAverage') if not isinstance(emometer_scores.get('EmotionAverage'), pd.Series) else float(emometer_scores.get('EmotionAverage').iloc[0])),
        ("Emometer Emotion StdDev", emometer_scores.get('EmotionStdDev') if not isinstance(emometer_scores.get('EmotionStdDev'), pd.Series) else float(emometer_scores.get('EmotionStdDev').iloc[0])),
        ("Mindfulness", mindfulness if not isinstance(mindfulness, pd.Series) else float(mindfulness.iloc[0])),
    ]
    print(f"\nEmoji Activity Indicators for User {userId}:\n")
    print(tabulate(results, headers=["Indicator", "Value"], tablefmt="github"))

# initialize video watch sequence and return a dataframe of video watch events for a given user
def create_video_dataframe_for_user(userId, videoId):
    videoDf = VideoWatchSequence(userId, videoId).videoEventsDf
    if videoDf.empty:
        print(f"Because of no video watch events found for user {userId}, no dataframe can be created")
        return
    videoDf.loc[:, "timestamp"] = videoDf['timestamp'].apply(lambda x: x[11:]) # get only time out of timestamp
    videoDf["time_only"] = videoDf["timestamp"]
    return videoDf

# plot video watch sequence with action vs time for a given user
def plot_video_watch_sequence(videoDf, userId, videoId):
    if videoDf is None:
        print(f"Because of no video watch events found for user {userId}, no plot can be shown")
        return
    x = videoDf["time_only"]
    y = videoDf["kind"]
    plt.figure(figsize=(8, 5))
    plt.scatter(x,y)
    plt.xlabel('Time')
    plt.ylabel('Action')
    plt.title(f'Video Actions for User {userId} for Video {videoId}')
    plt.show()


# main function
def main():
    db_name = "FROMECHOTEST2404040907a_echo_main_db_current.sqlite3"
    db = Database(os.path.join("db", db_name))
    db.connect()
    user_id = 1

    try: 
        ### PARSING EVENT LOG DATA FROM ECHO DATABASE

        # read in event objects
        event_query = "SELECT * FROM EchoApp_videoactivity"
        results = query_database(db, event_query)
        create_event_objects(results)

        for row in results:
            event = create_event_object(row)
            if event: 
                Event.add(event)
            else:
                print("Invalid event")
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
        specific_microblog_id = 6
        show_comments_for_microblog(specific_microblog_id)
        # show all comments for a given author
        author_id = user_id
        authors_df = show_comments_for_author(author_id)
        # analyze an author's all comments
        print_comment_count_for_author(author_id)
        print_avg_comment_length_for_author(author_id)

        # show frequency of visits to microblogs for all users
        show_microblog_visit_frequency(events_df)

        # show a user's emoji select events
        emoji_df = create_emoji_dataframe_for_user(user_id)
        if emoji_df is None:
            print(f"No emoji select events for user {user_id}")
        else:
            # plot
            plot_emoji_select_sequence(emoji_df, user_id)
            # show a user's emoji activity indicators
            show_emoji_activity_indicators(emoji_df, user_id)
            print()

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
        # plt.figure(figsize=(8, 5))
        # plt.plot(emojiDf['timestamp'], emojiDf['IntensityScore'], label='Intensity', marker='o', linestyle='solid')
        # plt.plot(emojiDf['timestamp'], emojiDf['EmotionScore'], label='Emotion', marker='x', linestyle='dashed')
        # plt.xlabel('Time')
        # plt.ylabel('Score')
        # plt.legend()
        # plt.title('Emoji Changes Over Time for User ' + str(userId))
        # plt.show()

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
        # plt.xlabel('Time')
        # plt.ylabel('Action')
        # plt.title('Video Actions for User ' + str(userId) + ' For ' + str(videoId) )
        # plt.show()


        # Initialize the Dash app
        app = dash.Dash(__name__)

        # Define the layout of the Dash app
        # Define the layout of the Dash app
        app.layout = html.Div([
            dcc.Dropdown(
                id='user-dropdown',
                options=[{'label': str(user_id), 'value': user_id} for user_id in events_df['user_id'].unique()],
                value=events_df['user_id'].unique()[0],  # Default value is the first user ID
                clearable=False
            ),
            dcc.Dropdown(
                id='timeframe-dropdown',
                options=[
                    {'label': 'From Start Date', 'value': 'from_start'},
                    {'label': 'Last 7 Days', 'value': 'last_7_days'},
                    {'label': 'Last Login Session', 'value': 'last_login_session'}
                ],
                value='from_start',  # Default value is 'From Start Date'
                clearable=False
            ),
            dcc.Graph(id='combined-plot')
        ])

        # Define callback to update the plot based on selected user ID and time frame
        @app.callback(
            Output('combined-plot', 'figure'),
            [Input('user-dropdown', 'value'),
            Input('timeframe-dropdown', 'value')]
        )
        def update_combined_plot(selected_user_id, selected_timeframe):
            # Fetch data based on selected user ID and time frame

            # Fetch new data for the selected user ID
            microblog_state_seq = OnMicroblogSequence(page_exit_df, selected_user_id)
            print("states of being on microblog for user selected_user_id")
            on_mb_df = microblog_state_seq.states_df
            print(on_mb_df)

            # On video page-- state sequence
            on_video_seq = OnVideoPageSequence(page_exit_df, selected_user_id)
            print("states of being on videos page for user selected_user_id")
            video_seq_df=on_video_seq.states_df
            print(video_seq_df)

            # Watching video -- state sequence
            # TODO: each video id is currently hardcoded in to get each dataframe. This should probably be paramaterized in the future
            watching_video1_states = WatchingVideoStateSequence(selected_user_id, 'video1')
            print('states of watching video1 for user selected_user_id')
            watching1_df = watching_video1_states.states_df
            print(watching_video1_states.states_df)
            watching_video2_states = WatchingVideoStateSequence(
                selected_user_id, "video2"
            )
            print("states of watching video2 for user selected_user_id")
            # Logged In -- state sequnece
            logged_in_states = LoggedInSequence(page_exit_df, selected_user_id)
            print("states of being logged in for user selected_user_id")
            logged_in_df = logged_in_states.states_df
            print(logged_in_df)

            # convert timestamp columns to datetime format
            if not watching1_df.empty:
                watching1_df["startTime"] = pd.to_datetime(watching1_df["startTime"])
                watching1_df['endTime'] = pd.to_datetime(watching1_df['endTime'])
            if not video_seq_df.empty:
                video_seq_df["startTime"] = pd.to_datetime(video_seq_df["startTime"])
                video_seq_df["endTime"] = pd.to_datetime(
                    video_seq_df["endTime"], format="%Y-%m-%d %H:%M:%S:%f"
                )
            if not on_mb_df.empty:
                on_mb_df["startTime"] = pd.to_datetime(on_mb_df["startTime"])
                on_mb_df["endTime"] = pd.to_datetime(
                    on_mb_df["endTime"], format="%Y-%m-%d %H:%M:%S:%f"
                )
            if not logged_in_df.empty:
                logged_in_df["startTime"] = pd.to_datetime(logged_in_df["startTime"])
                logged_in_df["endTime"] = pd.to_datetime(
                    logged_in_df["endTime"], format="mixed"
                )
            authors_comments = Comment.get_comments_by_author(selected_user_id)
            # Convert the list of comments to a DataFrame for better tabular representation
            authors_df = pd.DataFrame(authors_comments)
            if not authors_df.empty:
                authors_df["createdDate"] = pd.to_datetime(authors_df["createdDate"], format="mixed")
                authors_df["updatedDate"] = pd.to_datetime(authors_df["updatedDate"], format="mixed")

            #  Now filter these dataframes based on the time frame selected. If 'from start' is selected, no need for filtering
            if selected_timeframe == "last_7_days":
                today = pd.Timestamp('today')
                last_week = today - pd.Timedelta(days=7)
                # Filter dataframes for the last 7 days (if not empty)
                if not watching1_df.empty:
                    watching_df_filtered = watching1_df[(watching1_df['startTime'] >= last_week) & (watching1_df['startTime'] <= today)]
                else:
                    watching_df_filtered = watching1_df.copy()  # Empty copy to avoid errors

                if not video_seq_df.empty:
                    video_seq_df_filtered = video_seq_df[(video_seq_df['startTime'] >= last_week) & (video_seq_df['startTime'] <= today)]
                else:
                    video_seq_df_filtered = video_seq_df.copy()

                if not on_mb_df.empty:
                    on_mb_df_filtered = on_mb_df[(on_mb_df['startTime'] >= last_week) & (on_mb_df['startTime'] <= today)]
                else:
                    on_mb_df_filtered = on_mb_df.copy()

                if not logged_in_df.empty:
                    logged_in_df_filtered = logged_in_df[(logged_in_df['startTime'] >= last_week) & (logged_in_df['startTime'] <= today)]
                else:
                    logged_in_df_filtered = logged_in_df.copy()

                if not authors_df.empty:
                    authors_df_filtered = authors_df[(authors_df['createdDate'] >= last_week) & (authors_df['createdDate'] <= today)]
                else:
                    authors_df_filtered = authors_df.copy()

                # get appropriate analytics:
                # todo: overall engagement and blogging engagement?
                video_watch_frequency = len(watching_df_filtered)
                #video_watch_time = watching_df_filtered.countTotalWatchTime()
                mb_count = len(authors_df_filtered)
                # Calculate the length of each comment
                authors_df['comment_length'] = authors_df['comment'].apply(lambda x: len(x))
                # Calculate the average comment length
                average_comment_length = authors_df['comment_length'].mean()
                login_amt = len(logged_in_df_filtered)
                total_time_login = logged_in_df_filtered.countTotalSessionTime()

            elif selected_timeframe == "last_login_session":
                # Fetch data for the last login session
                # Identify the most recent login session
                if not logged_in_df.empty:
                    most_recent_login = logged_in_df.sort_values(by='startTime', ascending=False).iloc[0]
                    recent_login_start = most_recent_login['startTime']
                    recent_login_end = most_recent_login['endTime']
                else:
                    # Handle case where logged_in_df is empty (no login sessions)
                    recent_login_start = pd.Timestamp('NaT')  # Not a Time
                    recent_login_end = pd.Timestamp('NaT')

                # Filter dataframes based on most recent login session (if not empty)
                if not watching1_df.empty:
                    watching_df_filtered = watching1_df[(watching1_df['startTime'] >= recent_login_start) & (watching1_df['startTime'] <= recent_login_end)]
                else:
                    watching_df_filtered = watching1_df.copy()

                if not video_seq_df.empty:
                    video_seq_df_filtered = video_seq_df[(video_seq_df['startTime'] >= recent_login_start) & (video_seq_df['startTime'] <= recent_login_end)]
                else:
                    video_seq_df_filtered = video_seq_df.copy()
                if not on_mb_df.empty:
                    on_mb_df_filtered = on_mb_df[(on_mb_df['startTime'] >= recent_login_start) & (on_mb_df['startTime'] <= recent_login_end)]
                else:
                    on_mb_df_filtered = on_mb_df.copy()

                if not logged_in_df.empty:
                    logged_in_df_filtered = logged_in_df[(logged_in_df['startTime'] >= recent_login_start) & (logged_in_df['startTime'] <= recent_login_end)]
                else:
                    logged_in_df_filtered = logged_in_df.copy()

                if not authors_df.empty:
                    authors_df_filtered = authors_df[(authors_df['createdDate'] >= recent_login_start) & (authors_df['createdDate'] <= recent_login_end)]
                else:
                    authors_df_filtered = authors_df.copy()
                    # get appropriate analytics:
                # todo: overall engagement and blogging engagement?
                video_watch_frequency = len(watching_df_filtered)
                #video_watch_time = watching_df_filtered.countTotalWatchTime()
                mb_count = len(authors_df_filtered)
                # Calculate the length of each comment
                authors_df["comment_length"] = authors_df["comment"].apply(
                    lambda x: len(x)
                )
                # Calculate the average comment length
                average_comment_length = authors_df["comment_length"].mean()
                login_amt = len(logged_in_df_filtered)
                total_time_login = logged_in_df_filtered.countTotalSessionTime()

            else:
                # Default to fetching all data from the start date
                # no need for filtering, just copy each df
                watching_df_filtered = watching1_df.copy()
                video_seq_df_filtered = video_seq_df.copy()
                on_mb_df_filtered = on_mb_df.copy()
                logged_in_df_filtered = logged_in_df.copy()
                authors_df_filtered = authors_df.copy()

                # get appropriate analytics:
                # TODO: overall engagement and blogging engagement?
                video_watch_frequency = len(watching_df_filtered)
                #video_watch_time = watching_df_filtered.countTotalWatchTime()
                mb_count = len(authors_df_filtered)
                # Calculate the length of each comment
                authors_df["comment_length"] = authors_df["comment"].apply(
                    lambda x: len(x)
                )
                # Calculate the average comment length
                average_comment_length = authors_df["comment_length"].mean()
                login_amt = len(logged_in_df_filtered)
                total_time_login = logged_in_df_filtered.countTotalSessionTime()

            fig = go.Figure()

            # Plot each dataset from different dataframes
            for _, row in watching_df_filtered.iterrows():
                fig.add_trace(go.Scatter(x=[row["startTime"], row["endTime"]],
                                        y=[row["kind"], row["kind"]],
                                        mode='lines+markers', line=dict(color='purple',width=2), name='Watching Video'))

            for _, row in video_seq_df_filtered.iterrows():
                fig.add_trace(go.Scatter(x=[row["startTime"], row["endTime"]],
                                        y=[row["kind"], row["kind"]],
                                        mode='lines+markers', line=dict(color='red',width=2), name='On Video Page'))

            for _, row in on_mb_df_filtered.iterrows():
                fig.add_trace(go.Scatter(x=[row["startTime"], row["endTime"]],
                                        y=[row["kind"], row["kind"]],
                                        mode='lines+markers', line=dict(color='blue'), name='On Microblog'))

            for _, row in logged_in_df_filtered.iterrows():
                fig.add_trace(go.Scatter(x=[row["startTime"], row["endTime"]],
                                        y=[row["kind"], row["kind"]],
                                        mode='lines+markers', line=dict(color='blue'), name='Logged In'))

            # microblog comment instances
            if not authors_df_filtered.empty:
                fig.add_trace(go.Scatter(x=authors_df['createdDate'], y=['PostedOnMicroblog'],
                                        mode='markers', marker=dict(color='black'), name='Posted On Microblog'))

                fig.add_trace(go.Scatter(x=authors_df["updatedDate"], y=["UpdatedMicrblogComment"],
                                        mode='markers', marker=dict(color='black'), name='Updated Microblog Comment'))

                # add annotations for analytics
                # todo: overall engagement and blogging engagement?

                # get appropriate analytics:
                # todo: overall engagement and blogging engagement?
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Video Watch Frequency: {video_watch_frequency}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Total Watching Time: {video_watch_time}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Login Frequency: {login_amt}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Microblog Post Frequency: {mb_count}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Average Discussion Post Length: {average_comment_length}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )
            fig.add_annotation(
                x=0.5,
                y=-0.15,
                xref="paper",
                yref="paper",
                text=f"Total Session Time: {total_time_login}",
                showarrow=False,
                font=dict(family="Arial", size=12, color="black"),
            )

            # Update layout
            fig.update_layout(title=f'Activity For User Id = {selected_user_id} in Timeframe {selected_timeframe}',
                            xaxis_title='Time',
                            yaxis_title='State')

            return fig

        # Run the Dash app
        if __name__ == '__main__':
            app.run_server(debug=True)



        
    finally:
        db.close()

if __name__ == "__main__":
    main()