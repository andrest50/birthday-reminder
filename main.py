from win10toast import ToastNotifier
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import schedule
import time
import sys
import os
import logging

"""
To do:
- Error handle the input file data
- Fix program exiting if notification time is invalid
"""

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        os.execv(sys.executable, ['python'] + sys.argv)

def notification(people):
    names = []
    today = datetime.today().strftime("%m/%d")
    if(today.startswith("0")):
        today = today[1:]
    for person in people:
        if(person[1] == today):
            names.append(person[0])
    if(len(names) > 0):
        toast = ToastNotifier()
        toast.show_toast("Birthday Reminder", "It is {}'s brithday today!".format(", ".join(names)), duration=20)

def main():
    path = os.getcwd()

    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    print("Birthday notification system is active.")
    people = []
    if(os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.txt')):
        f = open(sys.argv[1], "r")
        lines = f.readlines()
        notifyTime = lines[0].rstrip()
        lines.pop(0)
        try:
            print(datetime.strptime(notifyTime, '%H:%M'))
        except:
            print("Invalid time for notification.")
             
        for line in lines:
            person = line.rstrip().split(' ')
            people.append(person)
    else:
        print("File is not valid! Only .txt files!")
        return

    try:
        schedule.every().day.at(str(notifyTime)).do(notification, people)

        while True:
            schedule.run_pending()
            time.sleep(1)
    except:
        print("Scheduler not working.")
    finally:
        observer.stop()
        observer.join()

if __name__ == "__main__":
    main()