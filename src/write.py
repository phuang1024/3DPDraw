import argparse
import sys

import numpy as np
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from svgpathtools import parse_path

from convert import *


def main():
    parser = create_parser("Write lines.")
    parser.add_argument("--font", type=str, required=True, help="TTF font file.")
    parser.add_argument("--font-size", type=float, default=16, help="Font size.")
    parser.add_argument("--height", type=float, default=7.15, help="Line height in mm.")
    parser.add_argument("--resolution", type=float, default=0.01, help="Sampling resolution from 0 to 1.")
    args = parser.parse_args()

    final_path = []

    font = TTFont(args.font)
    glyphs = font.getGlyphSet()

    text = sys.stdin.read()
    for char in text:
        # Get path
        glyph = glyphs[char]
        pen = SVGPathPen(glyph)
        glyph.draw(pen)
        path = parse_path(pen.getCommands())
        path = path.continuous_subpaths()[0]
        points = [path.point(x) for x in np.arange(0, 1, args.resolution)]
        points = np.array([(p.real, p.imag) for p in points])
        points /= 10

        # Add to final path
        for i in range(points.shape[0] - 1):
            final_path.append((*points[i], *points[i+1]))

        break # TODO

    # Write
    lines_to_gcode(args, final_path)


if __name__ == "__main__":
    main()
