from robot.api.deco import keyword

class RobotTimeoutError(TimeoutError):
    ROBOT_CONTINUE_ON_FAILURE = True