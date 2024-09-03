from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, cast
from android import mActivity
import os
import requests
from time import sleep


Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
AlarmManager = autoclass('android.app.AlarmManager')
SystemClock = autoclass('android.os.SystemClock')

class FileSenderApp(App):
    def build(self):
        return Label(text="Background Service Running")

    def on_start(self):
        self.schedule_service()

    def schedule_service(self):
        context = mActivity.getApplicationContext()

        intent = Intent(context, autoclass('org.kivy.android.PythonService'))
        intent.setAction('com.example.documents.UPLOAD')

        pending_intent = PendingIntent.getService(context, 0, intent, PendingIntent.FLAG_IMMUTABLE)
        
        alarm_manager = cast(AlarmManager, context.getSystemService(context.ALARM_SERVICE))

        interval = 6 * 60 * 60 * 1000  # 6 hours in milliseconds
        alarm_manager.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, SystemClock.elapsedRealtime() + interval, interval, pending_intent)
        print("Service scheduled to run every 6 hours.")

if __name__ == '__main__':
    BackgroundApp().run()
