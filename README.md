# allie-cse5911
Repository link: https://github.com/emilyallegretti/allie-cse5911
Note for future devs: you might want to copy this repo into your own GH account
## About 
Instruction Ally ("Allie") is a data analysis system for the OSU MBCSR ECHO 1 Platform that reads, parses, and analyzes user interactions with the website, with an ultimate goal of providing personalized feedback to instructors and students based on active participation indicators found in the log data (see "Student Task Engagement Indicators" below). Allie reads in page event logs collected in ECHO's underlying SQLite database and classifies them in an object-oriented manner for easier processing. The ultimate goal of this system is to improve the MBCSR intervention experience by tracking whether or not students are actively interacting with the mental-health/wellness activities posted to the platform and if it is helping them improve. 

### ECHO - Student Task Engagement Indicators 
ECHO records the user activity and provides the functionality to keep track of different indicators that measure different variables related to the task engagement. The following is a list of the indicators that aggregate the data of the multiple activities that are part of the intervention protocol, all of which are implemented by Allie:  


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
Allie's directory structure consists of:
- A folder containing regression tests (./Tests)
- a db folder containing a recent copy of the ECHO database
- Component directories that contain class definitions of children/subcomponents of that directory
    - Events:
        - The first "layer" of Allie. Events are objects representing the various types of page interaction logs that are collected by ECHO, all inheriting from parent abstract class Event. Events can be sorted into Pandas dataframes and further filtered based on user id, etc.
    - EventContainers:
        - DataFrame representation of a chronological sequence of Event objects filtered for a specific user and action (i.e. VideoWatchSequence encapsulates a sequence of video pause/play events for a specific   user and video).
    - Posts:
         - Posts include Announcemnets, Comments, and Microblog classes. They represent the 'noun' items on the platform and are not exactly actions/events.
    - StateContainers:
         - DataFrame representation of a chronological sequence of State objects filtered for a specific user and action (i.e. WatchingVideoStateContainer).
    - States:
        - Object representation of a duration of time in which specific Events are taking place, for example the state of watching a video, or more generally being logged into the system. All inherit from parent abstract class State. Contain a startTime and endTime as attributes.
- Misc. files
  - Main.py:
      - Initially parses ECHO database tables into the Event object model.
      - After that, it's a script of (essentially) test code that displays analytical output of each active participation indicator (see by creating instances of all data classes in each 'layer' of Allie and calling their functions.  

## Prerequisites/How to Use
See UserManual.txt
## Info For Future Developers
See InfoForFutureDevelopers.txt
