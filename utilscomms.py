import comms
from utilslog import get_cur_logger 

def loginfo_and_alert(msg: str):
    print(msg)
    get_cur_logger().info(msg)
    comms.alert(msg)

def logdebug_and_alert(msg: str):
    print(msg)
    get_cur_logger().debug(msg)
    comms.alert(msg)