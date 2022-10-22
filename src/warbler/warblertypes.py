from typing import Union, Tuple
from decimal import Decimal

from borb.pdf.canvas.color.color import Color as BorbColor
from borb.pdf import Alignment as BorbAlignment
from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

# Borb tends to force us to use Decimal, so Warbler is more flexible and accepts ints and floats too:
NumberType = Union[Decimal, int, float]

# Borb forces us to use Color objects, so Warbler lets us use strs and RGB tuples:
ColorType = Union[BorbColor, str, Tuple[int, int, int]]

# Borb forces us to use Alignment objects, so Warbler lets us also use strs:
AlignmentType = Union[BorbAlignment, str]

# Borb forces us to use Rectangle objects, so Warbler lets us also use tuples of four numbers:
RectangleType = Union[BorbRectangle, Tuple[NumberType, NumberType, NumberType, NumberType]]

# This is used when you can specify one number to use for four related
# settings, like border for border_top, border_right, border_bottom,
# and border_left:
OneNumForFourType = Union[NumberType, Tuple[NumberType, NumberType, NumberType, NumberType]]
OneBoolForFourType = Union[bool, Tuple[bool, bool, bool, bool]]
