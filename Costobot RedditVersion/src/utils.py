from datetime import datetime

def get_timespamp():
    now = datetime.now()
    msg = ""
    msg = "( "+str(now.hour)+"H - "+str(now.minute)+ "M - " + str(now.second)+ "S )"
    return msg
