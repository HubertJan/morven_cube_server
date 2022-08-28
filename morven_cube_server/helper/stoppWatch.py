import time


class StoppWatch:
    def __init__(self, runningTimeInMS=0):
        self._latestRunningTime = runningTimeInMS
        self._lastFetchTime = self._getCurrentMillisTime()
        self._isStopped = False

    @property
    def runningTime(self):
        if(self._isStopped == True):
            return self._latestRunningTime
        return self._getCurrentMillisTime() - self._lastFetchTime + self._latestRunningTime

    def setRunningTimeInMS(self, runningTime, stopTimer=False):
        self._latestRunningTime = runningTime
        if(stopTimer == True or self._isStopped == True):
            self._lastFetchTime = time.time()

    def stop(self):
        self._isStopped = True
        self._latestRunningTime = self._getCurrentMillisTime() - self._lastFetchTime + self._latestRunningTime
        self._lastFetchTime = None

    def start(self):
        self._isStopped = False
        self._lastFetchTime = self._getCurrentMillisTime()

    def _getCurrentMillisTime(self):
        return int(round(time.time() * 1000))