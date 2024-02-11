from SqliteUtils import Database
from EventFactory import create_event_object

def main():
    db = Database(
        r"FromEchoDev240208a_echo_main_db_current.sqlite3"
    )
    db.connect()

    try:        
        query_string = "SELECT * FROM EchoApp_videoactivity"
        results = db.run_query(query_string)

        events = []
        for row in results:
            event = create_event_object(row)
            if event: 
                events.append(event.__init__)
                print(event.__dict__)
            else:
                print("Invalid event")
    
        # Create a dataframe
        df = db.create_dataframe(query_string)
        print(df.head())

        # Example of time sequence of a user's login events
        user_logins = df[(df['user_id'] == 75) & (df['kind'] == 'Login')].sort_values('timestamp')
        print("Emily's Login Events:")
        print(user_logins[['user_id', 'action', 'timestamp']])

        user_logins = df[(df['user_id'] == 76) & (df['kind'] == 'Login')].sort_values('timestamp')
        print("Crystal's Login Events:")
        print(user_logins[['user_id', 'action', 'timestamp']])
    finally:
        db.close()

if __name__ == "__main__":
    main()
