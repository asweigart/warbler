from borb.pdf.canvas.layout.annotation.square_annotation import SquareAnnotation as BorbSquareAnnotation
from borb.pdf.canvas.color.color import Color as BorbColor
from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

import typing
from typing import Optional, Union, Tuple
from decimal import Decimal

from .warblertypes import RectangleType, ColorType, NumberType
from .util import _normalize_rectangle, _normalize_color


class SquareAnnotation(BorbSquareAnnotation):
    def __init__(
        self,
        bounding_box: RectangleType,
        fill_color: Optional[ColorType] = None,
        stroke_color: Optional[ColorType] = None,
        rectangle_difference: Optional[Tuple[NumberType, NumberType, NumberType, NumberType]] = None,
    ):
        bounding_box = _normalize_rectangle(bounding_box)
        fill_color = _normalize_color(fill_color)
        stroke_color = _normalize_color(stroke_color)
        if rectangle_difference is not None:
            rectangle_difference = (
                Decimal(rectangle_difference[0]),
                Decimal(rectangle_difference[1]),
                Decimal(rectangle_difference[2]),
                Decimal(rectangle_difference[3]),
            )

        super().__init__(
            bounding_box=bounding_box,
            fill_color=fill_color,
            stroke_color=stroke_color,
            rectangle_difference=rectangle_difference,
        )
