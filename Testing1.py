import time

myTime = int(input("How long would you like your timer to be?: "))

for x in range(myTime,0,-1):
    print(x)
    time.sleep(1)

print("Happy New Year!")