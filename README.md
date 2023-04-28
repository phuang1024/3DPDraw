# 3DPDraw

Downgrade your 3D printer by using it as a 2D printer.

## Usage

```
$ python convert.py
```

Enter your line segments as `x1 y1 x2 y2`. Gcode is printed to stdout.

The other scripts call `convert.py` and generate cool stuff.

Somehow, fix your writing utensil to the 3D printer nozzle area, so that it moves
with the nozzle.

Manually level or adjust Z offset so the pen draws properly.

Be careful of the nozzle smashing into the paper and ripping it, if Z is not adjusted
properly.
