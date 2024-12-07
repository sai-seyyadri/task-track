from datetime import datetime, timedelta
from argparse import ArgumentParser
import pandas as pd
import json
import sys
class TaskScheduler:
    """
      A class to manage and schedule tasks into available time slots based on
      priority level, due date, and duration.
      
      Attributes:
        tasks (list): A list of task objects or dictionaries
        priority (int): priority level of the task (higher is more important).
        due_date (str): due date of the task in "YYYY-MM-DD" format.
        duration (int): duration of the task in minutes.
        time_slots (list): A list of tuples, containing the task object, 
                           assigned start time (datetime object), and 
                           assigned end time (datetime object).
    """
    def __init__(self):
        self.tasks = []
        self.time_slots = []
        
    def schedule_tasks(self):
        """Author Saisidharth Seyyadri
        
        Organizes tasks into available time slots and prioritizes higher 
        priority levels and earlier due dates. Tasks that fit into the current 
        time slot are scheduled, and once scheduled, they are removed from the 
        task list to avoid futher duplication.
        
        Returns:
            list: A list of tuples, containing 
                  the task object, assigned start time (datetime object), and 
                  assigned end time (datetime object)
                  
        Borrowed Code URL: https://docs.python.org/3/library/datetime.html
        Description: Used "datetime.strptime" for parsing due dates and 
                     "timedelta" for handling task durations.
        """
        self.tasks.sort(key= lambda task: (task.priority, datetime.strptime(task.due_date, "%Y-%m-%d")), reverse= True)
        schedule = []
        
        for start_time, end_time in self.time_slots:
            current_time = start_time
            while current_time < end_time and self.tasks:
                task = self.tasks[0]
                task_end_time = current_time + timedelta(minutes=task.duration)
                if task_end_time <= end_time:
                    schedule.append((task, current_time, task_end_time))
                    current_time = task_end_time
                    self.tasks.pop(0)
                else:
                    break
        return schedule
    
    def split_up_tasks(self):
        """Author Ryan Frampton
        Splits a task across multiple time slots if the duration for that task
           excedes the amount of time available in the time slot
        
        """
        def time_to_minutes(self, str):
            """Helper method that converts the time into minutes
            
            Returns:
                int: the total minutes 
            """
            time_parts = str.split(":")
            hours = int(time_parts[0])
            minutes = int(time_parts[1])
            
            return hours * 60 + minutes
        
        
        self.tasks.sort(key=lambda task: (task.priority, task.due_date), reverse= True)
        schedule = []
            
        available_slots = [
                           (self.time_to_minutes(slot["start"]),  \
                           self.time_to_minutes(slot["end"]))  
                           for slot in self.time_slots]
        available_slots.sort()
        
        index = 0
        for task in self.tasks:
            remaining_time = task.duration

            while remaining_time > 0 and index < len(available_slots):
                start_time, end_time = available_slots[index]
                slot_duration = end_time - start_time
                
                if slot_duration <= 0:
                    index += 1
                    continue
                
                time_to_schedule = min(remaining_time, slot_duration)
                task_start_time = start_time
                task_end_time = start_time + time_to_schedule
                schedule.append(task.name, task_start_time, task_end_time)
                
                remaining_time = remaining_time - time_to_schedule
                available_slots[index] = (task_end_time, end_time)
                
                if available_slots[index][0] >= end_time:
                    index += 1
        
        return schedule
    
    def get_data(filepath):
        """
        Author Matthew Neufell
        Reads in data from json file
        
        Returns:
            df(DataFrame): DataFrame with the keys "tasks", "time_slots"
        """
        with open(filepath, 'r', encoding = "utf-8") as f:
            data = json.load(f)
            df = pd.DataFrame(data)
            return df
 
#def main():
    #tasks = TaskScheduler()     

    




def parse_args(arglist):
    """Parse command line arguments.
    
    Expect one argument:
        - str: path to a json file containing tasks and time_slots.
    
    
    Args:
        arglist (list of dictionaries): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.

    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help="file containing tasks and time_slots")
    return parser.parse_args(arglist)



if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    #main(args.filepath)