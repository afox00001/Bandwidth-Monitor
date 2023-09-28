# Bandwidth-Monitor
I made this Python project because (probably like most people) my ISP was severely shorting me on my bandwidth... So I made a Python script so I could show the technician what i was talking about.

Just run the script, and open: http://127.0.0.1:8050/

By deafult, it will take 4 band width sample's, each 10 minutes appart from each other before it plots the average of all of them. So it will take about 40 minutes before you see the first plot on the graph. This can be adjusted in the script using the "intervalTimeDelay" and "smaWindow" varibles in the script.
