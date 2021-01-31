from win10toast import ToastNotifier
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import schedule
import time
import sys
import os
import logging

class MyHandler(FileSystemEventHandler):
    def __init__(self, observer):
        object.__init__(self)
        self.observer = observer
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        self.observer.stop()
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

def checkDate(date):
    parts = date.split('/')
    if(len(parts) != 2 or int(parts[0]) < 1 or int(parts[0]) > 12
        or int(parts[1]) < 1 or int(parts[1]) > 31):
        return 0
    return 1

def main():
    path = os.getcwd()

    print("Birthday notification system is active.")
    people = []
    if(len(sys.argv) != 2):
        print("Invalid number of arguments. Run: ./py -3 main.py [text_file]")
        sys.exit(0)
    if(os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.txt')):
        f = open(sys.argv[1], "r")
        lines = f.readlines()
        notifyTime = lines[0].rstrip()
        lines.pop(0)
        try:
            datetime.strptime(notifyTime, '%H:%M')
        except ValueError:
            print("Invalid time for notification.")
             
        for line in lines:
            person = line.rstrip().split(' ')
            if(len(person) != 2):
                print("Text file has an invalid entry.")
            elif(checkDate(person[1]) == 0):
                print("Text file has an invalid date.")
            people.append(person)
    else:
        print("File is not valid! Only .txt files!")
        return

    observer = Observer()
    event_handler = MyHandler(observer)
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    try:
        schedule.every().day.at(str(notifyTime)).do(notification, people)
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    except:
        print("Scheduler not working.")
    observer.join()

if __name__ == "__main__":
    main()