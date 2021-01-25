from win10toast import ToastNotifier
from datetime import datetime
from watchdog.observers import Observer
import schedule
import time
import sys
import os
import logging

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f'event type: {event.event_type}  path : {event.src_path}')
        os.execv(sys.executable, ['python'] + sys.argv)

def notification(people):
    names = []
    today = datetime.today().strftime("%m/%d")
    if(str.startswith(today, "0")):
        today = today[1:]
    print(today)
    for person in people:
        if(person[1] == today):
            names.append(person[0])
    print(names)
    if(len(names) != 0):
        toast = ToastNotifier()
        toast.show_toast("Birthday Reminder", "It is {}'s brithday today!".format(", ".join(names)), duration=20)

def main():
    people = []

    if(os.path.isfile(sys.argv[1]) and sys.argv[1].endswith('.txt')):
        f = open(sys.argv[1], "r")
        lines = f.readlines()
        for line in lines:
            person = line.rstrip().split(' ')
            people.append(person)
        print(people)
    else:
        print("File is not valid! Only .txt files!")
        return

    schedule.every().day.at("09:00").do(notification, people)

    path = os.getcwd()

    observer = Observer()
    event_handler = MyHandler()
    observer.schedule(event_handler, path, recursive=False)
    observer.start()

    while True:
        schedule.run_pending()
        time.sleep(1)

    observer.stop()
    observer.join()

if __name__ == "__main__":
    main()