from robot.api.deco import keyword

class RobotTimeoutError(TimeoutError):
    ROBOT_CONTINUE_ON_FAILURE = False

class RobotRecvInvalidData(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = False

class RobotTestFlowException(RuntimeError):
    ROBOT_CONTINUE_ON_FAILURE = False