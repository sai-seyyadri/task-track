# ** Purpose of Each File **
# task_track.py : Implements a Task Scheduler program designed to manage and allocate tasks into available time slots based on priority level, due date, and estimated duration.
# tasks.json: JSON file that serves as the input data for task_track.py, containing different tasks and available time slots.
# README.md: Documentation for understanding the project, its contents, and functionality.

# ** Running the program **
# Run this on the command line: python task_track.py --file tasks.json

# ** Using and Interpreting the program **
# Once the program completes the scheduling process, it displays a list of scheduled tasks in the terminal. For each task, the output shows the following details:
# Task Name:* *The name of the task being scheduled* * ,Start: * *The exact start date and time for the task* * ,End: * *The end date and time for the task* * 
# For example, the program may display: Task: Rake the Leaves , Start: 2024-11-11 10:00:00, End: 2024-11-11 11:00:00 
# This means the task "Rake the Leaves" is scheduled to start at 10:00 AM and end at 11:00 AM on November 11, 2024

# * *Graph Output* *
# After printing the scheduled tasks, the program generates a graph titled 'Daily Task Allocation,' which provides a visual overview of how tasks are distributed across the days. Each task is represented as a color coded segment, stacked to show how your time is divided throughout the day. The graph uses the following axes:
# X-Axis: The duration of tasks in minutes.
# Y-Axis: The dates and times for the scheduled tasks
# The legend in the top left corner maps each color to its corresponding task name, making it easy to identify which part of the bar corresponds to which task.
# The terminal output provides detailed scheduling information, while the graph offers a quick visual overview of how tasks are distributed. Together, they help users understand their schedule and ensure that no time slots are overbooked or left empty

# * *Input format requirements:* *
# The program expects an input JSON file, which is already provided, but it can be noted that it should include the following keys for each task:
# "name": The task's name (ex: "Study for INST326 Exam")
# "duration": The task's duration in minutes (ex: 120)
# "priority": The priority level of the task. (ex: 3)
# "due_date": The task's due date in the format YYYY-MM-DD.
# Time slots should include start and end times in the format: "start": "2024-11-11 09:00", "end": "2024-11-11 11:00"


# ** Annotated Bibliography **



# ** Attribution ** 
| **Method/Function**      | **Primary Author**       | **Techniques Demonstrated**               |
|---------------------------|--------------------------|-------------------------------------------|
| `schedule_tasks`          | Saisidharth Seyyadri    | Sorting with key functions (using lambda) |
| `split_up_tasks`          | Ryan Frampton           | Sequence unpacking                        |
| `get_data`                | Matthew Neufell         | json.load()                               |
| `visualize_schedule`      | Saisidharth Seyyadri    | Visualizing data with pyplot              |
| `print_schedule`          | Ryan Frampton           | f-strings containing expressions          |
| `main`                    | Matthew Neufell         | The ArgumentParser class from the argparse module|



