from datetime import datetime,timedelta



x = datetime.now()
one_day = timedelta(days=1)
tommoworw = x + timedelta(days=1)

difference = y - x
print(difference)
print(one_day)
if difference >= one_day:
    print("już przedawnione")
else: 
    print("mniejsze bądź równe 1 dniu")
