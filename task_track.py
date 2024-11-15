from datetime import datetime, timedelta

class TaskScheduler:
    #  Schedules tasks by keeping them in available time slots based on priority level and duration
    def __init__(self):
        self.tasks = []
        self.time_slots = []
        
    def schedule_tasks(self):
        # Organizes tasks into available time slots and prioritizes higher priority levels and earlier due dates
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