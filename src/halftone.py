import math

import cv2
import numpy as np

from convert import *


def generate_dots(args, angle, size):
    """
    Yields (x, y) positions of dots.
    """
    # First generate points as if angle = 0
    points = []
    dy = args.spacing * math.sqrt(3) / 2
    xy_max = 10 * max(size)
    y = -xy_max
    i = 0
    while y <= xy_max:
        x = -xy_max
        if i % 2 == 0:
            x += args.spacing / 2
        while x <= xy_max:
            points.append((x, y))
            x += args.spacing
        y += dy
        i += 1

    # Rotate with matmul
    mat = np.array([
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ])
    #points = np.matmul(points, mat)

    # Filter points outside of bounds
    for x, y in points:
        if 0 <= x <= size[0] and 0 <= y <= size[1]:
            yield x, y


def circle_at(lines, args, center, radius, iters, res=8):
    """
    Draws `iters` progressively larger rings to make full circle.
    """
    for i in range(iters):
        curr_rad = np.interp(i, [0, iters], [0, radius])
        curr_res = int(np.interp(i, [0, iters], [0, res]))
        curr_res = max(3, curr_res)

        pts = []
        for j in range(res):
            angle = j / res * 2 * math.pi
            vec = np.array([math.cos(angle), math.sin(angle)])
            pt = center + vec*curr_rad
            pts.append(pt)
        for j in range(res):
            before = pts[j]
            after = pts[(j+1) % res]
            lines.append((before[0], before[1], after[0], after[1]))


def main():
    parser = create_parser()
    parser.add_argument("image")
    parser.add_argument("--angle", type=float, default=30, help="Dot angle offset in degrees.")
    parser.add_argument("--stroke-width", type=float, default=1, help="Pen width in mm.")
    parser.add_argument("--spacing", type=float, default=2.5, help="Distance between dots in mm.")
    parser.add_argument("--dot-size", type=float, default=2, help="Radius of darkest dot.")
    parser.add_argument("--size", type=float, default=200, help="Output X drawing width in mm.")
    args = parser.parse_args()

    image = cv2.imread(args.image)
    image = image.astype(np.float32) / 255
    image = np.mean(image, axis=2)

    angle = math.radians(args.angle % 60)
    size = (args.size, args.size / image.shape[1] * image.shape[0])

    lines = []
    for x, y in generate_dots(args, angle, size):
        # Get average of this region
        x0 = int(x - args.spacing/2)
        x1 = int(x + args.spacing/2)
        y0 = int(y - args.spacing/2)
        y1 = int(y + args.spacing/2)
        region = image[y0:y1, x0:x1]
        if region.size == 0:
            continue
        avg = np.mean(region)

        center = np.array([x, y])
        radius = np.interp(avg, [0, 1], [args.dot_size, 0])
        circle_at(lines, args, center, radius, 3)

    lines_to_gcode(args, lines)


if __name__ == "__main__":
    main()
