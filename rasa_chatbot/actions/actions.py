# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List
#
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import Restarted
import requests

API = "http://django:8000/"
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

def findScholarship(school_id, scholarship_name):
    response = requests.get(API + "queryScholarships/" + school_id + "/" + scholarship_name + "/")
    scholarships = response.json().get('scholarships')
    if len(scholarships) > 0:
        return scholarships[0]
    else:
        return None
    
def findProcess(school_id, process_name):
    response = requests.get(API + "queryProcessGuides/" + school_id + "/" + process_name + "/")
    processes = response.json().get('processes')
    if len(processes) > 0:
        return processes[0]
    else:
        return None
    
def listCourses(school_id, college_group):
    response = requests.get(API + "queryCourses/" + school_id + "/" + college_group + "/")
    college = response.json().get('courses')
    courses_list = ""
    for courses in college:
        for course in courses['course_list']:
            courses_list += course + "\n"
    return courses_list

class ActionResetSlots(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(self, dispatcher, tracker, domain):
        return [Restarted()]

class ActionListScholarships(Action):
    def name(self) -> Text:
        return "action_list_scholarships"

    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryScholarships/" + school_id + "/")
        scholarships = response.json().get('scholarships')
        scholarships_list = ""
        for scholarship in scholarships:
            scholarships_list += scholarship['scholarship_name'] + "\n"
        dispatcher.utter_message(text=scholarships_list)
        return []

class ActionListProcesses(Action):
    def name(self) -> Text:
        return "action_list_processes"

    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryProcessGuides/" + school_id + "/")
        processes = response.json().get('processes')
        processes_list = ""
        for process in processes:
            processes_list += process['process_name'] + "\n"
        dispatcher.utter_message(text=processes_list)
        return []

class ActionListColleges(Action):
    def name(self) -> Text:
        return "action_list_colleges"

    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryCourses/" + school_id + "/")
        colleges = response.json().get('courses')
        colleges_list = ""
        for college in colleges:
            colleges_list += college['college_group'] + "\n"
        dispatcher.utter_message(text=colleges_list)
        return []

class ActionDescribeScholarship(Action):
    def name(self) -> Text:
        return "action_describe_scholarship"

    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        scholarship_name = tracker.get_slot("scholarship_name")
        scholarship = findScholarship(school_id, scholarship_name)
        if scholarship is None:
            dispatcher.utter_message(text="Sorry, I don't know that scholarship.")
        else:
            dispatcher.utter_message(text=scholarship['description'])
        return []

class ActionListCourses(Action):
    def name(self) -> Text:
        return "action_list_courses"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        college_group = tracker.get_slot("college_group")
        courses = listCourses(school_id, college_group)
        if courses == "":
            dispatcher.utter_message(text="Sorry, I don't know that college.")
        else:
            dispatcher.utter_message(text=courses)
        return []
    
class ActionDescribeProcess(Action):
    def name(self) -> Text:
        return "action_describe_process"

    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        process_name = tracker.get_slot("process_name")
        process = findProcess(school_id, process_name)
        if process is None:
            dispatcher.utter_message(text="Sorry, I don't know that process.")
        else:
            dispatcher.utter_message(text=process['description'])
        return []
    
class ActionApply(Action):
    def name(self) -> Text:
        return "action_apply"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryProcessGuides/" + school_id + "/2/")
        processes = response.json().get('processes')
        process = processes[0]
        dispatcher.utter_message(text=process['description'])
        return []
    
class ActionListPlaces(Action):
    def name(self) -> Text:
        return "action_list_places"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryPlaces/" + school_id + "/")
        places = response.json().get('places')
        places_list = ""
        for place in places:
            places_list += place['name'] + "\n"
        dispatcher.utter_message(text=places_list)
        return []
    
class ActionListPlacesByType(Action):
    def name(self) -> Text:
        return "action_list_places_by_type"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        place_type = tracker.get_slot("place_type")
        response = requests.get(API + "queryPlacesByType/" + school_id + "/" + place_type + "/")
        places = response.json().get('places')
        places_list = ""
        for place in places:
            places_list += place['name'] + "\n"
        dispatcher.utter_message(text=places_list)
        return []
    
class ActionDescribePlace(Action):
    def name(self) -> Text:
        return "action_describe_place"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        place_name = tracker.get_slot("place_name")
        response = requests.get(API + "queryPlaces/" + school_id + "/" + place_name + "/")
        places = response.json().get('places')
        place = places[0]
        dispatcher.utter_message(text=place['description'])
        return []
    
class ActionListEvents(Action):
    def name(self) -> Text:
        return "action_list_events"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        response = requests.get(API + "queryEvents/" + school_id + "/")
        events = response.json().get('events')
        events_list = ""
        for event in events:
            events_list += event['name'] + "\n"
        dispatcher.utter_message(text=events_list)
        return []
    
class ActionDescribeEvent(Action):
    def name(self) -> Text:
        return "action_describe_event"
    
    def run(self, dispatcher, tracker, domain):
        school_id = str(int(tracker.get_slot("school_id")))
        event_name = tracker.get_slot("event_name")
        response = requests.get(API + "queryEvents/" + school_id + "/" + event_name + "/")
        events = response.json().get('events')
        event = events[0]
        dispatcher.utter_message(text=event['description'])
        return []