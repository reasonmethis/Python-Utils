from datetime import datetime
from time import sleep 

def sleep_until_tmstamp(tmstamp_wait_until: float):
    dt = tmstamp_wait_until - tmstamp()
    if dt > 0:
        sleep(dt)

def tmstamp() -> float:
    return datetime.now().timestamp()

'''I used to have the func below, but it was wrong, it didn't give the correct unix timestamp
because timestamp() expects local time (I guess it uses the system's timezone setting)
def utc_tmstamp() -> float:
    return datetime.utcnow().timestamp()
'''
def int_tmstamp() -> int:
    return int(datetime.now().timestamp())

def tm_cur_to_str(format_s='%Y-%m-%d %H:%M:%S'):
    return datetime.now().strftime(format_s)

def utc_cur_to_str(format_s='%Y-%m-%d %H:%M:%S UTC'):
    return datetime.utcnow().strftime(format_s)

def tmstamp_to_local_str(tmstamp, format_s='%Y-%m-%d %H:%M:%S'):
    return datetime.fromtimestamp(tmstamp).strftime(format_s)

def tmstamp_to_utc_str(tmstamp, format_s='%Y-%m-%d %H:%M:%S UTC'):
    return datetime.utcfromtimestamp(tmstamp).strftime(format_s)

if __name__ == '__main__':
    utcnow = datetime.utcnow()
    now = datetime.now()
    print(f'{int_tmstamp()=}')
    print(f'{tm_cur_to_str()=}')
    print(f'{utc_cur_to_str()=}')
    print(f'{tmstamp_to_local_str(int_tmstamp())=}')
    print(f'{tmstamp_to_utc_str(int_tmstamp())=}')
