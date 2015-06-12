__author__ = 'Derek'

def init():
    global cl
    global user
    global client
    global scanList
    global qrList
    global confList
    global qr_task
    global scan_task
    global tasker
    global conf_task
    global changed
    changed = dict(sc=0, qr=0)
    cl = None
    client = None
    user = None
    qr_task = None
    scan_task = None
    conf_task = None
    confList = None
    qrList = list()
    scanList = list()
    tasker = None


