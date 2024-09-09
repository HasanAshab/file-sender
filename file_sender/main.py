from kivy.app import App
from kivy.uix.label import Label
from jnius import autoclass, cast
from android import mActivity
from . import settings


Intent = autoclass('android.content.Intent')
PendingIntent = autoclass('android.app.PendingIntent')
AlarmManager = autoclass('android.app.AlarmManager')
SystemClock = autoclass('android.os.SystemClock')


class FileSenderApp(App):
    def build(self):
        return Label(text="Background Service Running")

    def on_start(self):
        self._schedule_service()

    def _schedule_service(self):
        interval = settings.INTERVAL
        context = mActivity.getApplicationContext()
        intent = Intent(context, autoclass('org.kivy.android.PythonService'))
        intent.setAction('com.example.documents.UPLOAD')
        pending_intent = PendingIntent.getService(context, 0, intent, PendingIntent.FLAG_IMMUTABLE)
        alarm_manager = cast(AlarmManager, context.getSystemService(context.ALARM_SERVICE))
        alarm_manager.setInexactRepeating(AlarmManager.ELAPSED_REALTIME_WAKEUP, SystemClock.elapsedRealtime() + interval, interval, pending_intent)


if __name__ == '__main__':
    FileSenderApp().run()
