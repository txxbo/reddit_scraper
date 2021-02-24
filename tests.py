from datetime import datetime, timedelta
import time


def get_time_chunks(start: datetime, end: datetime, delta: timedelta) -> list:
    current_time = start
    time_chunks = []
    while current_time < end:
        chunk_start = int(current_time.timestamp())
        chunk_end = int((current_time+delta-timedelta(seconds=1)).timestamp())
        time_chunks.append((chunk_start, chunk_end))
        current_time += delta

    return time_chunks


def build_chunks():
    # example usage:
    start_date = datetime(2020, 8, 1, 0, 0)
    end_date = datetime.now()
    delta_time = timedelta(hours=4)
    chunks = get_time_chunks(start_date, end_date, delta_time)
    # : returns list of (start, end) dates

    for chunk in chunks:
        with open('chunks.txt', 'a') as f:
            used_chunk = f"{chunk[0]},{chunk[1]}\n"
            f.write(used_chunk)


def read_chunks():
    time_chunks = []
    with open('chunks.txt', 'r') as f:
        for data in f.readlines():
            line = data.split(',')
            time_chunks.append((line[0].strip(), line[1].strip()))
    return time_chunks


def test():
    chunks = read_chunks()
    while len(chunks) > 10:
        print(chunks.pop())
    new_chunks(chunks)


def new_chunks(chunks):
    with open('chunks.txt', 'w') as f:
        for chunk in chunks:
            f.write(f"{chunk[0]},{chunk[1]}\n")


def get_date():
    with open('next_time.txt', 'r') as f:
        d = int(f.read().strip())
        if d > int(datetime.utcnow().timestamp()):
            return datetime.utcnow().timestamp()
    return datetime.fromtimestamp(d)


def write_date(d):
    result = d
    with open('next_time.txt', 'w') as f:
        f.write(str(int(result.timestamp())))


def get_dates(delta=60*24*30):
    with open('next_time.txt', 'r') as f:
        d = datetime.fromtimestamp(int(f.read().strip()))
        next_date = d+timedelta(minutes=delta)
        return d, next_date

# write_date(datetime(2020,8,1,0,0))
exit()

while True:
    current, next = get_dates()

    if next > datetime.utcnow():
        next = datetime.utcnow()

    if current >= datetime.utcnow()-timedelta(hours=1):
        break

    print(current, next)
    write_date(next)
    time.sleep(1)
