from datetime import datetime, timedelta
from argparse import ArgumentParser
import pandas as pd
import json
import matplotlib.pyplot as plt

class TaskScheduler:
    """
    A class to manage and schedule tasks into available time slots.
    based on priority level and due date.

    Attributes:
        tasks (list): A list of task dictionaries containing task details.
        time_slots (list of tuple): A list of tuples, each representing a 
            start and end time for an available time slot.
        schedule (list): A list of dictionaries, each containing task details
            and their assigned start and end times.
    """
    def __init__(self):
        """Initializes the TaskScheduler object.

        Attributes:
            tasks (list): Initialized as an empty list.
            time_slots (list of tuple): Initialized as an empty list.
            schedule (list): Initialized as an empty list.

        Side effects:
            Initializes the attributes "tasks", "time_slots", and "schedule".
        """
        self.tasks = []
        self.time_slots = []
        self.schedule = []
        
    def schedule_tasks(self):
        """
        Schedules tasks into available time slots. Tasks that don't fit
        entirely into one slot are passed to split_up_tasks.

        Borrowed Code URL: https://docs.python.org/3/library/datetime.html
        Description: Used "datetime.strptime" for parsing due dates and 
                     "timedelta" for handling task durations.
                     
        Side effects:
            Modifies "self.schedule" and "self.time_slots"
            
        Primary Author:
            Saisidharth Seyyadri

        Techniques Demonstrated:
            Sorting with key functions (using lambda) with list.sort()
        """
        self.tasks.sort(
            key=lambda task: (task["priority"], datetime.strptime(task["due_date"], "%Y-%m-%d")),
            reverse=True,
        )

        unscheduled_tasks = []

        for task in self.tasks:
            remaining_time = task["duration"]  
            for i in range(len(self.time_slots)):
                start_time, end_time = self.time_slots[i]
                slot_duration = (end_time - start_time).total_seconds() // 60 

                if remaining_time > 0 and slot_duration > 0:
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

            if remaining_time > 0:
                unscheduled_tasks.append({"task": task, "remaining_time": remaining_time})

        self.split_up_tasks(unscheduled_tasks)
    
    def split_up_tasks(self, unscheduled_tasks):
        """
        Splits tasks across multiple time slots if their duration exceeds
        the available time in a single slot.

        Args:
            unscheduled_tasks (list): Tasks that could not be scheduled fully.
            
        Side effects:
            Modifies `self.schedule` and `self.time_slots`.

        Primary Author:
            Ryan Frampton

        Techniques Demonstrated:
            Sequence unpacking
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
                
    def get_data(self, filepath):
        """
        Reads tasks and time slots from a JSON file and validates it.
        
        Args:
            filepath(str): Path to the JSON file. 
        
        Side effects:
            Modifies "self.tasks" and "self.time_slots"
            
        Raises:
            FileNotFoundError: If the JSON file is invalid
            
        Primary Author:
            Matthew Neufell

        Techniques Demonstrated:
            json.load(), with statement.
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
                
    def print_schedule(self):
        """
        Prints the scheduled tasks in a readable format.
        
        Side Effects:
            Outputs the formatted task schedule to the console.
        
        Primary Author:
            Ryan Frampton

        Techniques Demonstrated:
            f-strings containing expressions.
        """
        print("Scheduled Tasks:")
        for entry in self.schedule:
            task = entry["task"]
            print(f"Task: {task['name']}, Start: {entry['start_time']}, End: {entry['end_time']}")

    def visualize_schedule(self):
        """
        Visualizes the daily distribution of tasks as a stacked bar chart,
        ensuring tasks are ordered by their start time within each day.
        
        Primary Author:
            Saisidharth Seyyadri

        Techniques Demonstrated:
            DataFrame filtering and data visualization with pyplot.
            
        Side effects:
            Generates and displays a graph.
        """
        if not self.schedule:
            print("No tasks scheduled to visualize.")
            return

        data = []
        for entry in sorted(self.schedule, key=lambda x: x['start_time']): 
            task = entry["task"]
            start_date = entry["start_time"].date()
            duration = (entry["end_time"] - entry["start_time"]).total_seconds() / 60 
            data.append({"Date": start_date, "Task": task["name"], "Duration": duration})

        df = pd.DataFrame(data)


        pivot = df.pivot(index="Date", columns="Task", values="Duration")

        pivot.plot(kind="bar", stacked=True, figsize=(10, 6))
        plt.xlabel("Date")
        plt.ylabel("Duration (Minutes)")
        plt.title("Daily Task Allocation")
        plt.legend(title="Tasks", loc="upper left") 
        plt.tight_layout() 
        plt.show()                
                
        

def main():
    """
    Main function to parse command-line arguments and execute the TaskScheduler program.

    Primary Author:
        Matthew Neufell

    Techniques Demonstrated:
        ArgumentParser class.
    """
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
