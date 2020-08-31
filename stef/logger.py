from termcolor import colored, cprint

class Logger():
    @staticmethod
    def log(level, message, color=None):
        raw_text = level + ": " + message
        if color == "FAIL":
            text = colored(raw_text, 'red')
            print(text)
        elif color == "OK":
            text = colored(raw_text, 'green')
            print(text)
        elif color == "WARNING":
            text = colored(raw_text, 'yellow')
            print(text)
        elif color == "POINTS":
            text = colored(raw_text, 'magenta')
            print(text)
        elif color == "NEW_TEST":
            text = colored(raw_text, 'grey', 'on_green')
            print(text)
        elif color == "SUB_OUT_ERR":
            text = colored(raw_text, 'grey', 'on_red')
            print(text)
        elif color == "SUB_OUT":
            text = colored(raw_text, 'grey', 'on_yellow')
            print(text)
        elif color == "PRAISE":
            text = colored(raw_text, 'green', attrs=["blink", "bold"])
            print(text)
        else:
            print(raw_text)

    @staticmethod
    def log_points(points, max_points):
        Logger.log("POINTS", "Got " + str(points) + " out of " + str(max_points) + " points.", "POINTS")