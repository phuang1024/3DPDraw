from convert import *


def generate_tri(base, size, depth):
    """
    Generate line segments for upside down internal triangles.
    :param base: Bottom tip of triangle.
    :param size: Side length.
    """
    height = size * 3**0.5 / 2
    yield (base[0], base[1], base[0]+size/2, base[1]+height)
    yield (base[0]+size/2, base[1]+height, base[0]-size/2, base[1]+height)
    yield (base[0]-size/2, base[1]+height, base[0], base[1])

    if depth > 0:
        yield from generate_tri((base[0]-size/2, base[1]), size/2, depth-1)
        yield from generate_tri((base[0]+size/2, base[1]), size/2, depth-1)
        yield from generate_tri((base[0], base[1]+height), size/2, depth-1)


def main():
    parser = create_parser()
    parser.add_argument("--size", type=float, default=200, help="Side length in mm.")
    parser.add_argument("-d", "--depth", type=int, default=5, help="Depth of recursion.")
    args = parser.parse_args()

    height = args.size * 3**0.5 / 2

    # Initial triangle
    lines = [
        (0, 0, args.size, 0),
        (args.size, 0, args.size/2, height),
        (args.size/2, height, 0, 0),
    ]

    # Rest of the triangles
    for line in generate_tri((args.size/2, 0), args.size/2, args.depth-1):
        lines.append(line)

    lines_to_gcode(args, lines)


if __name__ == "__main__":
    main()
