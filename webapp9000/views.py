import time
import threading
import os
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db import connection


def log_db_conn_info():
    with connection.cursor() as cur:
        print(f"database connection {cur.connection.thread_id()}, PID {os.getpid()}, Thread {threading.get_ident()}")


def sleep(request: HttpRequest):
    log_db_conn_info()

    log_db_conn_info()

    futs = []

    with ThreadPoolExecutor(2) as executor:
        futs.append(executor.submit(log_db_conn_info))
        futs.append(executor.submit(log_db_conn_info))

        for f in as_completed(futs):
            f.result()

    time.sleep(float(request.GET.get("secs", 0)))
    return HttpResponse(b"OK")


def set_thing(var):
    time.sleep(0.3)
    var.x = random.randint(1,10)


def do_thing(var):
    time.sleep(0.3)
    print(f"{var.x} Thread {threading.get_ident()}")


def run():
    fut1 = []
    fut2 = []
    mydata = threading.local()
    with ThreadPoolExecutor(2) as exec:
        fut1.append(exec.submit(set_thing, mydata))
        fut1.append(exec.submit(set_thing, mydata))
        for f in as_completed(fut1):
            f.result()
        fut2.append(exec.submit(do_thing, mydata))
        fut2.append(exec.submit(do_thing, mydata))
        fut2.append(exec.submit(do_thing, mydata))
        fut2.append(exec.submit(do_thing, mydata))
        for f in as_completed(fut2):
            f.result()

