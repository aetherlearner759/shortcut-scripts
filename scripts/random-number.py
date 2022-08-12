import argparse
import pyperclip
import random

def getArgumentParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('start', nargs='?', default='0', type=float, help="Starting value of the range to select the random number from. Inclusive")
    parser.add_argument('stop', type=float, help="Ending value of the range to select the random number from. Inclusive")
    parser.add_argument('-type', default='int', choices=['int', 'float'], help="Type of number to generate")
    return parser


def getRandomInteger(start, end):
    return random.randint(start, end)

def getRandomFloat(start, end):
    return random.uniform(start, end)


def main():
    Args = getArgumentParser()
    Args = Args.parse_args()

    num = None
    if Args.type == "int":
        num = getRandomInteger(Args.start, Args.stop)
    elif Args.type == "float":
        num = getRandomFloat(Args.start, Args.stop)
    else:
        raise Exception("Unknown Args.type given")

    print(num)


if __name__ == "__main__":
    main()