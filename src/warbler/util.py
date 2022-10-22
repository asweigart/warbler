from borb.pdf import Alignment as BorbAlignment
from borb.pdf.canvas.color.color import Color as BorbColor, HexColor as BorbHexColor, X11Color as BorbX11Color
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation as BorbHyphenation
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont as BorbTrueTypeFont
from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

import typing
from typing import Union, Sequence, Tuple, Dict, Optional
from pathlib import Path
from decimal import Decimal

from .warblertypes import ColorType, RectangleType, AlignmentType, NumberType

# For our copy of COLOR_DEFINITION, have a lowercase color name
COLOR_DEFINITION: Dict[str, str] = {str(k).lower(): str(v) for k, v in BorbX11Color.COLOR_DEFINITION.items()}


def _normalize_text_alignment(alignment: AlignmentType) -> BorbAlignment:
    # If alignment is already an enum object, just return it.
    if alignment in (
        BorbAlignment.LEFT,
        BorbAlignment.CENTERED,
        BorbAlignment.RIGHT,
        BorbAlignment.JUSTIFIED,
    ):
        return alignment

    if isinstance(alignment, BorbAlignment) and alignment not in (
        BorbAlignment.LEFT,
        BorbAlignment.CENTERED,
        BorbAlignment.RIGHT,
        BorbAlignment.JUSTIFIED,
    ):
        raise ValueError("text alignment must be 'left', 'center', 'right', or 'justified'")

    # Set alignment based on the string argument
    alignment = alignment.lower()
    if alignment == 'left':
        return BorbAlignment.LEFT
    elif alignment in ('center', 'centered'):
        return BorbAlignment.CENTERED
    elif alignment == 'right':
        return BorbAlignment.RIGHT
    elif alignment == 'justified':
        return BorbAlignment.JUSTIFIED
    else:
        raise ValueError("text alignment must be 'left', 'center', 'right', or 'justified'")


def _normalize_alignment(alignment: AlignmentType) -> Tuple[BorbAlignment, BorbAlignment]:
    if alignment == BorbAlignment.JUSTIFIED:
        raise ValueError("alignment must include 'top', 'middle', 'bottom', 'left', 'center', or 'right'")

    if alignment in (
        BorbAlignment.TOP,
        BorbAlignment.MIDDLE,
        BorbAlignment.BOTTOM,
    ):
        return (alignment, BorbAlignment.LEFT)

    if alignment in (
        BorbAlignment.LEFT,
        BorbAlignment.CENTERED,
        BorbAlignment.RIGHT,
    ):
        return (BorbAlignment.TOP, alignment)

    vertical_alignment = BorbAlignment.TOP
    horizontal_alignment = BorbAlignment.LEFT

    alignment = alignment.lower()

    if 'top' in alignment:
        vertical_alignment = BorbAlignment.TOP
    elif 'middle' in alignment:
        vertical_alignment = BorbAlignment.MIDDLE
    elif 'bottom' in alignment:
        vertical_alignment = BorbAlignment.BOTTOM

    if 'left' in alignment:
        horizontal_alignment = BorbAlignment.LEFT
    elif 'center' in alignment:
        horizontal_alignment = BorbAlignment.CENTERED
    elif 'right' in alignment:
        horizontal_alignment = BorbAlignment.RIGHT

    return (vertical_alignment, horizontal_alignment)


def _normalize_vertical_alignment(alignment: AlignmentType) -> BorbAlignment:
    # If alignment is already an enum object, just return it.
    if alignment in (
        BorbAlignment.TOP,
        BorbAlignment.MIDDLE,
        BorbAlignment.BOTTOM,
    ):
        return alignment

    if isinstance(alignment, BorbAlignment) and alignment not in (
        BorbAlignment.TOP,
        BorbAlignment.MIDDLE,
        BorbAlignment.BOTTOM,
    ):
        raise ValueError("vertical alignment must be 'top', 'middle', or 'bottom'")

    # Set alignment based on the string argument
    alignment = alignment.lower()
    if alignment == 'top':
        return BorbAlignment.TOP
    elif alignment == 'middle':
        return BorbAlignment.MIDDLE
    elif alignment == 'bottom':
        return BorbAlignment.BOTTOM
    else:
        raise ValueError("vertical alignment must be 'top', 'middle', or 'bottom'")


def _normalize_horizontal_alignment(alignment: AlignmentType) -> BorbAlignment:
    # If alignment is already an enum object, just return it.
    if alignment in (
        BorbAlignment.LEFT,
        BorbAlignment.CENTERED,
        BorbAlignment.RIGHT,
    ):
        return alignment

    if isinstance(alignment, BorbAlignment) and alignment not in (
        BorbAlignment.LEFT,
        BorbAlignment.CENTERED,
        BorbAlignment.RIGHT,
    ):
        raise ValueError("horizontal alignment must be 'left', 'centered', or 'right'")

    # Set alignment based on the string argument
    alignment = alignment.lower()
    if alignment == 'left':
        return BorbAlignment.LEFT
    elif alignment in ('center', 'centered'):
        return BorbAlignment.CENTERED
    elif alignment == 'right':
        return BorbAlignment.RIGHT
    else:
        raise ValueError("horizontal alignment must be 'left', 'centered', or 'right'")


def _normalize_color(color: ColorType) -> BorbColor:
    # color that can either be:
    #   - a BorbColor object
    #   - the x11 name string of a color
    #   - the hex string of an RGB color, optionally prefixed with #
    if isinstance(color, BorbColor):
        return color
    elif isinstance(color, str):
        color = color.lower()
        if color in COLOR_DEFINITION:
            return BorbHexColor(COLOR_DEFINITION[color])
        else:
            return BorbHexColor(color)
    else:
        if len(color) != 3:
            raise ValueError('invalid value used for color, must be a color name str or a str of the RGB hex value')
        return BorbHexColor(hex(color[0])[2:].zfill(2) + hex(color[1])[2:].zfill(2) + hex(color[2])[2:].zfill(2))


def _normalize_hyphenation(iso_language_code: Union[BorbHyphenation, str]) -> BorbHyphenation:
    if isinstance(iso_language_code, BorbHyphenation):
        return iso_language_code

    return BorbHyphenation(iso_language_code)


def _normalize_font(fontFile: Union[BorbTrueTypeFont, str, Path]) -> Union[BorbTrueTypeFont, str]:
    if isinstance(fontFile, BorbTrueTypeFont):
        return fontFile

    if isinstance(fontFile, str):
        # Check if the name is one of the 16 standard PDF fonts:
        if fontFile.lower() in (
            'courier',
            'courier-bold',
            'courier-bold-oblique',
            'helvetica',
            'helvetica-bold',
            'helvetical-bold-oblique',
            'helvetica-oblique',
            'times-bold',
            'times-bold-oblique',
            'times-oblique',
            'times-roman',
            'symbol',
            'zapfdingbats',
        ):
            # Return the properly cased name of the font:
            return fontFile[0].upper() + fontFile[1:].lower()
        else:
            # Or else, the string represents a .ttf file path and name.
            fontFile = Path(fontFile)

    if isinstance(fontFile, Path):
        return BorbTrueTypeFont.true_type_font_from_file(fontFile)


def _normalize_rectangle(rect: RectangleType) -> BorbRectangle:
    if isinstance(rect, BorbRectangle):
        return rect

    return BorbRectangle(Decimal(rect[0]), Decimal(rect[1]), Decimal(rect[2]), Decimal(rect[3]))


# TODO - add NormalizeFont that makes it easy to add in custom fonts?
