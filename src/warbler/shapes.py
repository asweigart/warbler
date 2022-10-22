from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

from .warblertypes import NumberType
from decimal import Decimal


class Rectangle(BorbRectangle):
    def __init__(
        self,
        lower_left_x: NumberType,
        lower_left_y: NumberType,
        width: NumberType,
        height: NumberType,
    ):
        lower_left_x = Decimal(lower_left_x)
        lower_left_y = Decimal(lower_left_y)
        width = Decimal(width)
        height = Decimal(height)

        super().__init__(lower_left_x=lower_left_x, lower_left_y=lower_left_y, width=width, height=height)

    # TODO add left, bottom, etc properties
