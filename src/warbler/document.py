from borb.pdf import (
    Document as BorbDocument,
    PDF as BorbPDF,
    Page as BorbPage,
    Paragraph as BorbParagraph,
    Alignment as BorbAlignment,
    SingleColumnLayout as BorbSingleColumnLayout,
)
from borb.pdf.canvas.font.font import Font as BorbFont
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation as BorbHyphenation
from borb.pdf.canvas.color.color import Color as BorbColor, HexColor as BorbHexColor
from borb.pdf.page.page_size import PageSize as BorbPageSize

from .util import (
    _normalize_text_alignment,
    _normalize_alignment,
    _normalize_color,
    _normalize_hyphenation,
    _normalize_font,
)
from .warblertypes import NumberType, ColorType, OneNumForFourType, AlignmentType, OneBoolForFourType

from decimal import Decimal
from typing import Union, Tuple
import typing
from pathlib import Path


class Document(BorbDocument):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def add_page(self, *args, **kwargs) -> BorbPage:
        # (Overridden method)
        # If called with no arguments, we automatically create and return
        # a new Page object.
        # By default, the page is set to Letter sized instead of A4.
        if len(args) + len(kwargs) == 0:
            page = Page()
            self.add_page(page)
            return page
        else:
            return super().add_page(*args, **kwargs)

    def save(self, filename: str) -> None:
        # (New Warbler method that makes saving PDF files easier.)
        with open(filename, 'wb') as pdf_file_handle:
            BorbPDF.dumps(pdf_file_handle, self)


class Page(BorbPage):
    def __init__(self, width: NumberType = Decimal(612), height: NumberType = Decimal(792), size: str = ''):
        if size != '':
            width, height = _pageSizeFromName(size)

        super().__init__(width, height)

        self.default_layout_obj: BorbSingleColumnLayout = None

    def add(
        self,
        text: str,
        respect_newlines_in_text: bool = False,
        respect_spaces_in_text: bool = False,
        font: Union[BorbFont, str] = "Helvetica",
        font_size: NumberType = Decimal(12),
        text_alignment: AlignmentType = BorbAlignment.LEFT,
        alignment: AlignmentType = BorbAlignment.TOP,
        font_color: ColorType = BorbHexColor("000000"),
        border: OneBoolForFourType = False,
        border_radius: OneNumForFourType = Decimal(0),
        border_color: ColorType = BorbHexColor("000000"),
        border_width: NumberType = Decimal(1),
        padding: OneNumForFourType = Decimal(0),
        margin: typing.Optional[OneNumForFourType] = None,
        fixed_leading: typing.Optional[NumberType] = None,
        multiplied_leading: typing.Optional[NumberType] = None,
        background_color: typing.Optional[ColorType] = None,
        hyphenation: typing.Optional[Union[BorbHyphenation, str]] = None,
    ):
        # (New Warbler method)
        # Adds text in a Paragraph object to a default SingleColumnLayout
        # object that it generates if needed. Returns the default layout object.

        if self.default_layout_obj is None:
            self.default_layout_obj = BorbSingleColumnLayout(self)

        # Add text as a new Paragraph object. (The Paragraph object handles type casting.)
        self.default_layout_obj.add(
            Paragraph(
                text,
                respect_newlines_in_text=respect_newlines_in_text,
                respect_spaces_in_text=respect_spaces_in_text,
                font=font,
                font_size=font_size,
                text_alignment=text_alignment,
                alignment=alignment,
                font_color=font_color,
                border=border,
                border_radius=border_radius,
                border_color=border_color,
                border_width=border_width,
                padding=padding,
                margin=margin,
                fixed_leading=fixed_leading,
                multiplied_leading=multiplied_leading,
                background_color=background_color,
                hyphenation=hyphenation,
            )
        )

        return self.default_layout_obj  # Because Layout objects return self, this method returns the layout object.


class Paragraph(BorbParagraph):
    def __init__(
        self,
        text: str,
        respect_newlines_in_text: bool = False,
        respect_spaces_in_text: bool = False,
        font: Union[BorbFont, str, Path] = "Helvetica",
        font_size: NumberType = Decimal(12),
        text_alignment: AlignmentType = BorbAlignment.LEFT,
        alignment: AlignmentType = BorbAlignment.TOP,
        font_color: ColorType = BorbHexColor("000000"),
        border: OneBoolForFourType = False,
        border_radius: OneNumForFourType = Decimal(0),
        border_color: ColorType = BorbHexColor("000000"),
        border_width: NumberType = Decimal(1),
        padding: OneNumForFourType = Decimal(0),
        margin: typing.Optional[OneNumForFourType] = None,
        fixed_leading: typing.Optional[NumberType] = None,
        multiplied_leading: typing.Optional[NumberType] = None,
        background_color: typing.Optional[ColorType] = None,
        hyphenation: typing.Optional[Union[BorbHyphenation, str]] = None,
    ):
        font = _normalize_font(font)

        font_size = Decimal(font_size)
        border_width = Decimal(border_width)
        if fixed_leading is not None:
            fixed_leading = Decimal(fixed_leading)
        if multiplied_leading is not None:
            multiplied_leading = Decimal(multiplied_leading)

        text_alignment = _normalize_text_alignment(text_alignment)
        vertical_alignment, horizontal_alignment = _normalize_alignment(alignment)

        font_color = _normalize_color(font_color)
        border_color = _normalize_color(border_color)
        if background_color is not None:
            background_color = _normalize_color(background_color)

        if isinstance(border, bool):
            border_top = border_right = border_bottom = border_left = border
        else:
            border_top = border[0]
            border_right = border[1]
            border_bottom = border[2]
            border_left = border[3]

        if isinstance(border_radius, Decimal) or isinstance(border_radius, int) or isinstance(border_radius, float):
            border_radius = Decimal(border_radius)
            border_radius_top_left = border_radius
            border_radius_top_right = border_radius
            border_radius_bottom_right = border_radius
            border_radius_bottom_left = border_radius
        else:
            border_radius_top_left = Decimal(border_radius[0])
            border_radius_top_right = Decimal(border_radius[1])
            border_radius_bottom_right = Decimal(border_radius[2])
            border_radius_bottom_left = Decimal(border_radius[3])

        if isinstance(padding, Decimal) or isinstance(padding, int) or isinstance(padding, float):
            padding = Decimal(padding)
            padding_top = padding
            padding_right = padding
            padding_bottom = padding
            padding_left = padding
        else:
            padding_top = Decimal(padding[0])
            padding_right = Decimal(padding[1])
            padding_bottom = Decimal(padding[2])
            padding_left = Decimal(padding[3])

        if isinstance(margin, Decimal) or isinstance(margin, int) or isinstance(margin, float) or margin is None:
            if margin is not None:
                margin = Decimal(margin)
            margin_top = margin
            margin_right = margin
            margin_bottom = margin
            margin_left = margin
        else:
            margin_top = Decimal(margin[0])
            margin_right = Decimal(margin[1])
            margin_bottom = Decimal(margin[2])
            margin_left = Decimal(margin[3])

        if hyphenation is not None:
            hyphenation = _normalize_hyphenation(hyphenation)

        super().__init__(
            text,
            respect_newlines_in_text=respect_newlines_in_text,
            respect_spaces_in_text=respect_spaces_in_text,
            font=font,
            font_size=font_size,
            text_alignment=text_alignment,
            vertical_alignment=vertical_alignment,
            horizontal_alignment=horizontal_alignment,
            font_color=font_color,
            border_top=border_top,
            border_right=border_right,
            border_bottom=border_bottom,
            border_left=border_left,
            border_radius_top_left=border_radius_top_left,
            border_radius_top_right=border_radius_top_right,
            border_radius_bottom_right=border_radius_bottom_right,
            border_radius_bottom_left=border_radius_bottom_left,
            border_color=border_color,
            border_width=border_width,
            padding_top=padding_top,
            padding_right=padding_right,
            padding_bottom=padding_bottom,
            padding_left=padding_left,
            margin_top=margin_top,
            margin_right=margin_right,
            margin_bottom=margin_bottom,
            margin_left=margin_left,
            fixed_leading=fixed_leading,
            multiplied_leading=multiplied_leading,
            background_color=background_color,
            hyphenation=hyphenation,
        )  # TODO - pass the correct params here


def _pageSizeFromName(pageSizeName: str) -> Tuple[Decimal, Decimal]:
    pageSizeName = pageSizeName.upper()

    if pageSizeName in 'LETTER' or ('LETTER' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.LETTER_PORTRAIT.value[0], BorbPageSize.LETTER_PORTRAIT.value[1])
    elif 'LETTER' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.LETTER_LANDSCAPE.value[0], BorbPageSize.LETTER_LANDSCAPE.value[1])

    elif pageSizeName in 'LEGAL' or ('LEGAL' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.LEGAL_PORTRAIT.value[0], BorbPageSize.LEGAL_PORTRAIT.value[1])
    elif 'LEGAL' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.LEGAL_LANDSCAPE.value[0], BorbPageSize.LEGAL_LANDSCAPE.value[1])

    elif pageSizeName in 'TABLOID' or ('TABLOID' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.TABLOID_PORTRAIT.value[0], BorbPageSize.TABLOID_PORTRAIT.value[1])
    elif 'TABLOID' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.TABLOID_LANDSCAPE.value[0], BorbPageSize.TABLOID_LANDSCAPE.value[1])

    elif pageSizeName in 'LEDGER' or ('LEDGER' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.LEDGER_PORTRAIT.value[0], BorbPageSize.LEDGER_PORTRAIT.value[1])
    elif 'LEDGER' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.LEDGER_LANDSCAPE.value[0], BorbPageSize.LEDGER_LANDSCAPE.value[1])

    elif pageSizeName in 'EXECUTIVE' or ('EXECUTIVE' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.EXECUTIVE_PORTRAIT.value[0], BorbPageSize.EXECUTIVE_PORTRAIT.value[1])
    elif 'EXECUTIVE' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.EXECUTIVE_LANDSCAPE.value[0], BorbPageSize.EXECUTIVE_LANDSCAPE.value[1])

    elif pageSizeName in 'A0' or ('A0' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A0_PORTRAIT.value[0], BorbPageSize.A0_PORTRAIT.value[1])
    elif 'A0' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A0_LANDSCAPE.value[0], BorbPageSize.A0_LANDSCAPE.value[1])

    elif pageSizeName in 'A1' or ('A1' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A1_PORTRAIT.value[0], BorbPageSize.A1_PORTRAIT.value[1])
    elif 'A1' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A1_LANDSCAPE.value[0], BorbPageSize.A1_LANDSCAPE.value[1])

    elif pageSizeName in 'A2' or ('A2' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A2_PORTRAIT.value[0], BorbPageSize.A2_PORTRAIT.value[1])
    elif 'A2' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A2_LANDSCAPE.value[0], BorbPageSize.A2_LANDSCAPE.value[1])

    elif pageSizeName in 'A3' or ('A3' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A3_PORTRAIT.value[0], BorbPageSize.A3_PORTRAIT.value[1])
    elif 'A3' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A3_LANDSCAPE.value[0], BorbPageSize.A3_LANDSCAPE.value[1])

    elif pageSizeName in 'A4' or ('A4' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A4_PORTRAIT.value[0], BorbPageSize.A4_PORTRAIT.value[1])
    elif 'A4' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A4_LANDSCAPE.value[0], BorbPageSize.A4_LANDSCAPE.value[1])

    elif pageSizeName in 'A5' or ('A5' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A5_PORTRAIT.value[0], BorbPageSize.A5_PORTRAIT.value[1])
    elif 'A5' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A5_LANDSCAPE.value[0], BorbPageSize.A5_LANDSCAPE.value[1])

    elif pageSizeName in 'A6' or ('A6' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A6_PORTRAIT.value[0], BorbPageSize.A6_PORTRAIT.value[1])
    elif 'A6' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A6_LANDSCAPE.value[0], BorbPageSize.A6_LANDSCAPE.value[1])

    elif pageSizeName in 'A7' or ('A7' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A7_PORTRAIT.value[0], BorbPageSize.A7_PORTRAIT.value[1])
    elif 'A7' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A7_LANDSCAPE.value[0], BorbPageSize.A7_LANDSCAPE.value[1])

    elif pageSizeName in 'A8' or ('A8' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A8_PORTRAIT.value[0], BorbPageSize.A8_PORTRAIT.value[1])
    elif 'A8' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A8_LANDSCAPE.value[0], BorbPageSize.A8_LANDSCAPE.value[1])

    elif pageSizeName in 'A9' or ('A9' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A9_PORTRAIT.value[0], BorbPageSize.A9_PORTRAIT.value[1])
    elif 'A9' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A9_LANDSCAPE.value[0], BorbPageSize.A9_LANDSCAPE.value[1])

    elif pageSizeName in 'A10' or ('A10' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.A10_PORTRAIT.value[0], BorbPageSize.A10_PORTRAIT.value[1])
    elif 'A10' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.A10_LANDSCAPE.value[0], BorbPageSize.A10_LANDSCAPE.value[1])

    elif pageSizeName in 'B0' or ('B0' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B0_PORTRAIT.value[0], BorbPageSize.B0_PORTRAIT.value[1])
    elif 'B0' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B0_LANDSCAPE.value[0], BorbPageSize.B0_LANDSCAPE.value[1])

    elif pageSizeName in 'B1' or ('B1' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B1_PORTRAIT.value[0], BorbPageSize.B1_PORTRAIT.value[1])
    elif 'B1' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B1_LANDSCAPE.value[0], BorbPageSize.B1_LANDSCAPE.value[1])

    elif pageSizeName in 'B2' or ('B2' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B2_PORTRAIT.value[0], BorbPageSize.B2_PORTRAIT.value[1])
    elif 'B2' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B2_LANDSCAPE.value[0], BorbPageSize.B2_LANDSCAPE.value[1])

    elif pageSizeName in 'B3' or ('B3' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B3_PORTRAIT.value[0], BorbPageSize.B3_PORTRAIT.value[1])
    elif 'B3' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B3_LANDSCAPE.value[0], BorbPageSize.B3_LANDSCAPE.value[1])

    elif pageSizeName in 'B4' or ('B4' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B4_PORTRAIT.value[0], BorbPageSize.B4_PORTRAIT.value[1])
    elif 'B4' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B4_LANDSCAPE.value[0], BorbPageSize.B4_LANDSCAPE.value[1])

    elif pageSizeName in 'B5' or ('B5' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B5_PORTRAIT.value[0], BorbPageSize.B5_PORTRAIT.value[1])
    elif 'B5' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B5_LANDSCAPE.value[0], BorbPageSize.B5_LANDSCAPE.value[1])

    elif pageSizeName in 'B6' or ('B6' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B6_PORTRAIT.value[0], BorbPageSize.B6_PORTRAIT.value[1])
    elif 'B6' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B6_LANDSCAPE.value[0], BorbPageSize.B6_LANDSCAPE.value[1])

    elif pageSizeName in 'B7' or ('B7' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B7_PORTRAIT.value[0], BorbPageSize.B7_PORTRAIT.value[1])
    elif 'B7' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B7_LANDSCAPE.value[0], BorbPageSize.B7_LANDSCAPE.value[1])

    elif pageSizeName in 'B8' or ('B8' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B8_PORTRAIT.value[0], BorbPageSize.B8_PORTRAIT.value[1])
    elif 'B8' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B8_LANDSCAPE.value[0], BorbPageSize.B8_LANDSCAPE.value[1])

    elif pageSizeName in 'B9' or ('B9' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B9_PORTRAIT.value[0], BorbPageSize.B9_PORTRAIT.value[1])
    elif 'B9' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B9_LANDSCAPE.value[0], BorbPageSize.B9_LANDSCAPE.value[1])

    elif pageSizeName in 'B10' or ('B10' in pageSizeName and 'PORTRAIT' in pageSizeName):
        return (BorbPageSize.B10_PORTRAIT.value[0], BorbPageSize.B10_PORTRAIT.value[1])
    elif 'B10' in pageSizeName and 'LANDSCAPE' in pageSizeName:
        return (BorbPageSize.B10_LANDSCAPE.value[0], BorbPageSize.B10_LANDSCAPE.value[1])

    else:
        raise ValueError('page size must be a valid page size name')
