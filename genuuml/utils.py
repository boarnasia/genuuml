import sys


def exit(*args, exit_code=0, **kwargs):
    if exit_code == 0:
        # standerd exit
        print(*args, **kwargs)
    else:
        # on error occured
        print(*args, file=sys.stderr, **kwargs)

    sys.exit(exit_code)

