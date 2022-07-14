from datetime import datetime

# wish message
def wish():
    now = datetime.now()
    time_now = int(now.strftime("%H"))

    if time_now<24 and time_now>16:
        return "Evening"
    elif time_now<17 and time_now>12:
        return "Afternoon"
    else:
        return "Morning"



