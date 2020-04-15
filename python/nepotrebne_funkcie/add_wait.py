import time

i = 0
while True:
    print(i)
    i += 1
    time.sleep(0.1)
    if i >= 1000:
        break