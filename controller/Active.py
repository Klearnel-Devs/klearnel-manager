## @package controller
#   Handles communication between Klearnel & Klearnel Manager
#
# @author Antoine Ceyssens <a.ceyssens@nukama.be> & Derek Van Hove <d.vanhove@nukama.be>



## Function to initialize variables required throughout the manager
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
    changed = dict(sc=0, qr=0, cl=0)
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


