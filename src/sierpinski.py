import argparse
import sys
from subprocess import Popen, PIPE

PY = sys.executable


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
    parser = argparse.ArgumentParser()
    parser.add_argument("output", help="Output gcode file.")
    parser.add_argument("--ox", type=float, default=0, help="Offset x.")
    parser.add_argument("--oy", type=float, default=0, help="Offset y.")
    parser.add_argument("-s", "--size", type=float, default=200, help="Side length in mm.")
    parser.add_argument("-d", "--depth", type=int, default=5, help="Depth of recursion.")
    args = parser.parse_args()

    with open(args.output, "wb") as f:
        proc = Popen([PY, "convert.py", "--ox", str(args.ox), "--oy", str(args.oy)], stdin=PIPE, stdout=f)

        # Draw initial triangle
        height = args.size * 3**0.5 / 2
        proc.stdin.write(f"0 0 {args.size} 0\n".encode())
        proc.stdin.write(f"{args.size} 0 {args.size/2} {height}\n".encode())
        proc.stdin.write(f"{args.size/2} {height} 0 0\n".encode())

        # Draw the rest
        for line in generate_tri((args.size/2, 0), args.size/2, args.depth-1):
            proc.stdin.write(" ".join(map(str, line)).encode())
            proc.stdin.write("\n".encode())

        proc.stdin.flush()
        proc.stdin.close()
        proc.wait()


if __name__ == "__main__":
    main()
