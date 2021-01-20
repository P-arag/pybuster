import threading
import time

initial = time.perf_counter()


def print_name():
    SEC = 1
    print(f"Sleeping for {SEC} sec")
    time.sleep(SEC)
    print(f"Done sleeping for {SEC} sec")

threads =[]
for _ in range(10):
    myThread = threading.Thread(target=print_name)
    myThread.start()
    threads.append(myThread)

for thread in threads:
    thread.join()

final = time.perf_counter()
print("Process Done in " + str(final-initial) + "secs")
