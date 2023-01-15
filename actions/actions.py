# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
 
from typing import Any, Text, Dict, List
import random
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
 
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from sqlalchemy.orm import Session

#from rasa.core.actions.action import Action
#from rasa.core.actions import SlotSet
#from rasa.core.actions import Action
#from rasa_sdk.events import SlotSet

import sqlalchemy
from sqlalchemy import create_engine
#from rasa.core.actions import Action
#from rasa.core.events import SlotSet
 
# computer_choice & determine_winner functions refactored from
# https://github.com/thedanelias/rock-paper-scissors-python/blob/master/rockpaperscissors.py, MIT liscence



engine = create_engine('sqlite:///RPS2.db')
session = Session(bind=engine)
Base = declarative_base()


# class Event(Base):
#     __tablename__ = 'wins'
#     id = Column(Integer, primary_key=True)
#     win = Column(String)

# Base.metadata.create_all(engine)
 
class ActionPlayRPS(Action):
    #event = Event()
    def name(self) -> Text:
        return "action_play_rps"
 
    def computer_choice(self):
        generatednum = random.randint(1,3)
        if generatednum == 1:
            computerchoice = "rock"
        elif generatednum == 2:
            computerchoice = "paper"
        elif generatednum == 3:
            computerchoice = "scissors"
       
        return(computerchoice)
 
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
 
        # play rock paper scissors
        user_choice = tracker.get_slot("choice")
        dispatcher.utter_message(text=f"You chose {user_choice}")
        comp_choice = self.computer_choice()
        dispatcher.utter_message(text=f"The computer chose {comp_choice}")

        
        if user_choice == "rock" and comp_choice == "scissors":
            dispatcher.utter_message(text="Congrats, you won!")
            tracker.slots["win"] = True
            #tracker.slots.set("win", True)
            #event.win = True
            #a = SlotSet("win", True)
            #return [SlotSet("win", True)]
        elif user_choice == "rock" and comp_choice == "paper":
            dispatcher.utter_message(text="The computer won this round.")
            tracker.slots["win"] = False
            #tracker.slots.set("win", False)
            #event.win = False
            #a = SlotSet("win", False)
            #return [SlotSet("win", False)]
        elif user_choice == "paper" and comp_choice == "rock":
            dispatcher.utter_message(text="Congrats, you won!")
            tracker.slots["win"] = True
            #tracker.slots.set("win", True)
            #event.win = True
            #a = SlotSet("win", True)
            #return [SlotSet("win", True)]
        elif user_choice == "paper" and comp_choice == "scissors":
            dispatcher.utter_message(text="The computer won this round.")
            tracker.slots.set("win", False)
            tracker.slots["win"] = False
            #event.win = False
            #a = SlotSet("win", False)
            #return [SlotSet("win", False)]
        elif user_choice == "scissors" and comp_choice == "paper":
            dispatcher.utter_message(text="Congrats, you won!")
            tracker.slots["win"] = True
            #tracker.slots.set("win", True)
            #event.win = True
            #a = SlotSet("win", True)
            #return [SlotSet("win", True)]
        elif user_choice == "scissors" and comp_choice == "rock":
            dispatcher.utter_message(text="The computer won this round.")
            tracker.slots["win"] = False
            #tracker.slots.set("win", False)
            #event.win = False
            #a = SlotSet("win", False)
            #return [SlotSet("win", False)]
        else:
            dispatcher.utter_message(text="It was a tie!")

        slot_value = tracker.get_slot("win")

        event = Event()
        event.win = slot_value
        conn.execute(Event.__table__.insert(), event.__dict__)

        #dispatcher.utter_message(text="{}".format(slot_value))
        #dispatcher.utter_message(text="The computer won this round.")
        #print(slot_value)
        #engine = create_engine('sqlite:///RPS2.db')
        #conn = engine.connect()
        #conn.execute(wins.__table__.insert(), event.__dict__)
        
        session.add("INSERT INTO wins VALUES ('{}')".format(slot_value))
        session.commit()
        session.close()
        return []