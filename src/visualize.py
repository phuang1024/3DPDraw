"""
Render gcode as image.
Only works for 3DPDraw gcode; doesn't have all gcode features.
"""

import argparse

import cv2
import numpy as np


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("gcode")
    parser.add_argument("-r", "--resolution", default=800, help="Pixel resolution of render.")
    parser.add_argument("-s", "--size", default=400, help="Side length of render in mm.")
    args = parser.parse_args()

    scale = args.resolution / args.size

    image = np.full((args.resolution, args.resolution), 255, dtype=np.uint8)
    pen_loc = np.array([0, 0])
    pen_state = False
    with open(args.gcode, "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("G1"):
                values = {}
                for part in line.split():
                    axis = part[0]
                    if axis in "XYZ":
                        values[axis] = float(part[1:])

                if "Z" in values:
                    pen_state = values["Z"] < 1e-2
                if "X" in values and "Y" in values:
                    new_loc = np.array([values["X"], values["Y"]]) * scale
                    if pen_state:
                        cv2.line(
                            image,
                            (int(pen_loc[0]), int(pen_loc[1])),
                            (int(new_loc[0]), int(new_loc[1])),
                            0,
                            1
                        )
                    pen_loc = new_loc

    cv2.imshow("image", image)
    cv2.waitKey(0)


if __name__ == "__main__":
    main()
