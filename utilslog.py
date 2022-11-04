import logging as lg

longformat_s = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
shortformat_s = '%(asctime)s - %(message)s'
#the following will affect not just my files but imported modules
#lg.basicConfig(level=lg.ERROR)#, filemode='w')
_cur_logger = None

def get_cur_logger() -> lg.Logger:
    return _cur_logger or makelogger(set_as_current=True)

def makelogger(filename='defaultlog.txt', name='log', fmt=longformat_s, level=lg.DEBUG, set_as_current=False):
    global _cur_logger
    handler = lg.FileHandler(filename)
    handler.setFormatter(lg.Formatter(fmt))
    logger = lg.getLogger(name)
    logger.addHandler(handler)
    logger.setLevel(level)
    if set_as_current:
        _cur_logger = logger
    return logger

if __name__ == '__main__':
    lgr = makelogger(filename='tmp.txt', name='testlogger')
    lgr.debug('debug msg')
    try:
        1 / 0
    except Exception as e:
        lgr.exception('Test exception')