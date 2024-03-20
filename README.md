# allie-cse5911
## About 
Instruction Ally ("Allie") is a data analysis system for the OSU MBCSR ECHO 1 Platform that reads, parses, and analyzes user interactions with the website, with an ultimate goal of providing personalized feedback to instructors and students based on active participation indicators found in the log data. Allie reads in page event logs collected in ECHO's underlying SQLite database and classifies them in an object-oriented manner for easier processing. The ultimate goal of this system is to improve the MBCSR intervention experience by tracking whether or not students are actively interacting with the mental-health/wellness activities posted to the platform and if it is helping them improve. 
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

## Prerequisites/How to Use
See UserManual.txt
## Info For Future Developers
See InfoForFutureDevelopers.txt
