import sys

from hydt.commands import start, migrate, how_to, build_database
from hydt.options import options


if __name__ == '__main__':
    args = sys.argv[1:]

    options.parse_command_line(args)

    if not len(args):
        print(how_to())
    elif args[0] == 'start':
        start(*args[1:])
    elif args[0] == 'build_database':
        build_database(*args[1:])
    elif args[0] == 'migrate':
        migrate(*args[1:])
    else:
        print(how_to())
