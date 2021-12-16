from termcolor import colored, cprint

class Logger():

    COLOR_MAP = {
        "FAIL":        lambda t: colored(t, 'red'),
        "OK":          lambda t: colored(t, 'green'),
        "WARNING":     lambda t: colored(t, 'yellow'),
        "POINTS":      lambda t: colored(t, 'magenta'),
        "NEW_TEST":    lambda t: colored(t, 'grey', 'on_green'),
        "SUB_OUT_ERR": lambda t: colored(t, 'grey', 'on_red'),
        "SUB_OUT":     lambda t: colored(t, 'grey', 'on_yellow'),
        "PRAISE":      lambda t: colored(t, 'green', attrs=["blink", "bold"]),
    }

    @staticmethod
    def log(level, message, color=None):
        raw_text = f"{level}: {message}"

        if color in Logger.COLOR_MAP.keys():
            text = Logger.COLOR_MAP[color](raw_text)
        else:
            text = raw_text

        print(text)

    @staticmethod
    def log_points(points, max_points):
        Logger.log("POINTS", Logger.points_fmt(points, max_points), "POINTS")

    @staticmethod
    def points_fmt(points, max_points):
        return f"Got {points} out of {max_points} point{'' if points == 1 else 's'}."
