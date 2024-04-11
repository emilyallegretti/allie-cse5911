# allie-cse5911
Repository link: https://github.com/emilyallegretti/allie-cse5911  
Note for future devs: you might want to copy this repo into your own GH account
## About 
Instruction Ally ("Allie") is a data analysis system for the OSU MBCSR ECHO 1 Platform that reads, parses, and analyzes user interactions with the website, with an ultimate goal of providing personalized feedback to instructors and students based on active participation indicators found in the log data (see "Student Task Engagement Indicators" below). Allie reads in page event logs collected in ECHO's underlying SQLite database and classifies them in an object-oriented manner for easier processing. The ultimate goal of this system is to improve the MBCSR intervention experience by tracking whether or not students are actively interacting with the mental-health/wellness activities posted to the platform and if it is helping them improve. 

### ECHO - Student Task Engagement Indicators 
ECHO records users' activity and provides the functionality for Allie to keep track of different indicators that measure different variables related to task engagement. The following is a list of the active participation indicators and representative variables for each activity in the MBCSR intervention protocol for which Allie measures and outputs analytics. (Table by Leon Madrid)

| Activity | Indicator | Variable |
|----------|-----------|----------|
| Discussion | Frequency |  Visits, number of postings, views |
|            | Regularity | Visits, Participation |
|            | Time       | Participation range, viewing time |
|            | Posting    | Posting length, Relational keywords |
| Video      | Frequency  | Play, Stop|  
|            | Activity   | Completed videos, completion rate 
|            | Time       |  Watching time| 
|Readings |   Frequency   |Visits |
|         |   Time        | Reading time |
|Announcements |Frequency |Visits |
|Emoji|Frequency | Visits, number of reports |
|      | Regularity | Tracking compliance participation |
|      | Emometer | Baseline, Average, Mean, Std deviation |
|      |Mindfulness | Baseline, Average, Mean, Std deviation |
|      | CSR | Baseline, Average, Mean, Std deviation |
|Login/Logout | Frequency |Visits |
|             |Time |  Session time |
|            | Autologout | Inactivity time (not yet implemented)|



## File/Object Structure
Allie's different layers of object-model hierarchies provide object-oriented tools for conducting the analyses of the participation indicators described above. The object models essentially encapsulate the raw event data taken from ECHO (`Events` below) and create more complex data structures (`States, EventContainers, StateContainers` below) that form connections and sequences between these events based on each indicator above. At Allie's current state, these objects are being used to display basic analyses of user participation with the ECHO platform based on specific users or durations of time. The goal of producing this simplistic object structure is that so when a future decision tree or machine-learning model is created, these objects can be used as input for simpler data processing. 

Allie's directory structure consists of:
- A folder containing regression tests (./Tests)
- a db folder containing a recent copy of the ECHO database. A fallback of the current system is that an updated database needs to be manually uploaded to this folder to replace the older db version. In the future, possibly Allie could connect to the ECHO database directly to collect log data in real time so that training data is always up-to-date.
- Component directories that contain class definitions of children/subcomponents of that directory
    - Events:
        - The first "layer" of Allie. Events are objects representing the various types of page interaction logs that are collected by ECHO's database--entering pages, playing a video, clicking on slides, etc.--, all inheriting from parent abstract class Event. Each Event subclass contains attributes from the database that characterize it--timestamp, necessary video or slide IDs when applicable, associated user id, etc. Events can be sorted into Pandas dataframes and further filtered based on user id, etc.
    - EventContainers:
        - DataFrame representation of a chronological sequence of Event objects filtered for a specific user and action/indicator (i.e. an instance of VideoWatchSequence encapsulates a sequence of video pause/play events for a specific user and video. An instance of MicroblogVisitsSequence encapsulates a sequence of visits to the Microblogs page for a specific user id).
    - Posts:
         - Posts include Announcements, Comments, and Microblog classes. They represent the 'noun' items on the platform and are not exactly actions/events. They are simply 'posts' that users/instructors make to the platform.
    - States:
        - Object representation of a duration of time in which specific Events are taking place, for example the state of watching a video, or more generally being logged into the system. All inherit from parent abstract class State. Contain a startTime and endTime as attributes.
    - StateContainers:
         - DataFrame representation of a chronological sequence of State objects filtered for a specific user and action/indicator (i.e. an instance of WatchingVideoStateContainer contains all the States in which a specific user is watching a specific video).
- Misc. files
  - Main.py:
      - Initially parses ECHO database tables into the Event object model.
      - After that, it's a script of (essentially) test code that uses the Events parsed in to create EventContainers, States, and StateContainers, to display analytical output of each active participation indicator by creating instances of all data classes in each 'layer' of Allie and calling their functions.
  - EventFactory.py:
  - SqliteUtils.py:

## Prerequisites/How to Use
See UserManual.txt
## Info For Future Developers
Allie is still a work in progress. There are more objectives for the system implementation to be implemented by future developer groups (See our Project Abstract and Release Plan for more details). The following objectives from our Project Abstract have been successfully implemented and tested by the current dev team:   
- (Objective 2) *Real-Time Logging*: The system will query the app’s database tables to collect a real-time event stream of users’ interactions with the platform, such as amount of time spent watching videos, page clicks, microblog comments, emoji board participation, and compliance with assignments.  
- (Objective 3) *Data Analysis*: Process the data and extract high-level patterns and trends in student activity and behavior. (Meaning, the entire indicator table provided above has been implemented into Allie's analytics). 
  
The following objectives have yet to be implemented:
- (Objective 1)
  *Pattern Learning Model*: Using the foundational object model, the system detects patterns in user page interactions and forms decisions or suggestions based on the pattern extracted from the input data.
- (Objective 4)
*Personalized Reporting*: Use patterns detected in an individual student’s platform interaction data to send personalized reports/messages to them based on their activity/behaviors. Send these same reports to the student's instructor to keep the instructor updated on students’ progress, and determine possible suggested actions for Echo to take.

Other points of improvement:  
- All of the indicators in the above graph are analyzed in the code but not all of them are shown in the output. The next goal of this project would be to have a more comprehensive output of all the active participation indicators. For example. emoji scores, time spent on announcement page, time spent reading slides, etc
- There are several TODOs throughout the codebase that point out improvement suggestions for various components.

See InfoForFutureDevelopers.txt for more details.
