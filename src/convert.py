__all__ = (
    "create_parser",
    "lines_to_gcode",
)

import argparse
import math


def create_parser():
    """
    Create default parser.
    """
    parser = argparse.ArgumentParser(description="Line segments to gcode")
    parser.add_argument("--ox", type=float, default=0, help="Additive offset X.")
    parser.add_argument("--oy", type=float, default=0, help="Additive offset Y.")
    parser.add_argument("--oz", type=float, default=0, help="Additive offset Z.")
    parser.add_argument("-u", "--up", type=float, default=1.2, help="Pen up height.")
    parser.add_argument("-s", "--speed", type=float, default=200, help="Speed in mm/sec.")
    parser.add_argument("-m", "--margin", type=float, default=1, help="Max move distance w/o pen up.")
    return parser


def lines_to_gcode(args, lines):
    """
    :param lines: List of (x1, y1, x2, y2)
    Prints gcode to stdout.
    """

    print("; Generated by 3DPDraw")
    print("G21 ; Set units to mm")
    print("G90 ; Absolute positioning")
    print(f"G1 F{args.speed*60} ; Set speed")
    print("G28 ; Home")

    curr_x = 0
    curr_y = 0
    is_first_iter = True
    for x1, y1, x2, y2 in lines:
        x1 += args.ox
        y1 += args.oy
        x2 += args.ox
        y2 += args.oy

        dist = math.hypot(x1-curr_x, y1-curr_y)
        needs_up = is_first_iter or dist > args.margin
        if needs_up:
            print(f"G1 Z{args.up+args.oz}")
        print(f"G1 X{x1} Y{y1}")
        if needs_up:
            print(f"G1 Z{args.oz}")
        print(f"G1 X{x2} Y{y2}")

        curr_x = x2
        curr_y = y2
        is_first_iter = False

    print("G28 ; Home", flush=True)


def main():
    parser = create_parser()
    args = parser.parse_args()

    lines = []
    while True:
        try:
            line = input()
        except EOFError:
            break
        x1, y1, x2, y2 = map(float, line.split())
        lines.append((x1, y1, x2, y2))

    lines_to_gcode(args, lines)


if __name__ == "__main__":
    main()
