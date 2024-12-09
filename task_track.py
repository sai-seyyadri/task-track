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
        self.schedule = []
        
    def schedule_tasks(self):
        """Organizes tasks into available time slots and prioritizes higher 
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
        self.tasks.sort(key= lambda task: (task['priority'], 
                        datetime.strptime(task['due_date'], "%Y-%m-%d")), 
                        reverse= True)
        
        for start_time, end_time in self.time_slots:
            current_time = start_time
            while current_time < end_time and self.tasks:
                task = self.tasks[0]
                task_end_time = current_time + timedelta(minutes=task.duration)
                if task_end_time <= end_time:
                    self.schedule.append((task, current_time, task_end_time))
                    current_time = task_end_time
                    self.tasks.pop(0)
                else:
                    break
        return self.schedule
    
    def split_up_tasks(self, unscheduled_tasks):
        """
        Splits tasks across multiple time slots if their duration exceeds
        the available time in a single slot.

        Args:
            unscheduled_tasks (list): Tasks that could not be scheduled fully.

        Returns:
            None
        """
        for entry in unscheduled_tasks:
            task = entry["task"]
            remaining_time = entry["remaining_time"]

            for i in range(len(self.time_slots)):
                start_time, end_time = self.time_slots[i]
                slot_duration = (end_time - start_time).total_seconds() // 60

                if slot_duration > 0 and remaining_time > 0:
                    time_to_schedule = min(remaining_time, slot_duration)
                    task_start_time = start_time
                    task_end_time = start_time + timedelta(minutes=time_to_schedule)

                    self.schedule.append({
                        "task": task,
                        "start_time": task_start_time,
                        "end_time": task_end_time,
                    })

                    self.time_slots[i] = (task_end_time, end_time)

                    remaining_time -= time_to_schedule

                    if self.time_slots[i][0] >= end_time:
                        self.time_slots.pop(i)
                        break

                if remaining_time <= 0:
                    break
    def reschedule_missed_tasks(self, tasks):
        pass
    
    def get_data(self, filepath):
        """
        Reads tasks and time slots from a JSON file and validates the structure.
        
        Args:
            filepath(str): Path to the JSON file. 
            
        Raises:
            Exception: If the JSON file is invalid
        """
        try:
            with open(filepath, 'r', encoding = "utf-8") as f:
                data = json.load(f)
                self.tasks = data.get("tasks", [])
                self.time_slots = [
                    (
                       datetime.strptime(slot["start"], "%Y-%m-%d %H:%M"),
                       datetime.strptime(slot["end"], "%Y-%m-%d %H:%M"),  
                        
                    )
                    for slot in data.get("time_slots", [])
                    
                ]
                
        except FileNotFoundError as e:
            print(f"Error: The file '{filepath}' was not found.")
            return None
                
                
                
        

def main():
    parser = ArgumentParser(description="Task Scheduler Program")
    parser.add_argument("--file", required=True, help="Path to the tasks JSON file")
    args = parser.parse_args()
    
    scheduler = TaskScheduler()
    scheduler.get_data(args.file)
    scheduler.schedule_tasks()
    scheduler.print_schedule()
    scheduler.visualize_schedule()
    
    
if __name__== "__main__":
    main()
