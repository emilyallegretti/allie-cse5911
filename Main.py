from SqliteUtils import Database
from EventFactory import create_event_object

def main():
    db = Database(r'echo_main_db_current.sqlite3')
    db.connect()
    
    try:        
        query_string = "SELECT * FROM EchoApp_videoactivity"
        results = db.run_query(query_string)
        
        events = []
        for row in results:
            event = create_event_object(row)
            events.append(event)
        
    finally:
        db.close()

if __name__ == "__main__":
    main()
