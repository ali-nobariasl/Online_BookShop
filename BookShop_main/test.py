from datetime import time


for h in range(0,24):
   for m in (0,30):
       a = (time(h,m).strftime('%I:%M %p'))
       
t = 's'
print(t)