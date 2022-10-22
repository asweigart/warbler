"""Warbler
By Al Sweigart al@inventwithpython.com

TODO_DESCRIPTION"""

__version__ = '0.1.0'

# Importing the Warbler wrappers
from .util import (
    _normalize_text_alignment,
    _normalize_vertical_alignment,
    _normalize_horizontal_alignment,
    _normalize_color,
    _normalize_hyphenation,
)
from .document import Document, Page, Paragraph
from .annotation import SquareAnnotation
from .shapes import Rectangle

# Importing directly from Borb:

# Color
from borb.pdf.canvas.color.color import (
    Color,
    RGBColor,
    CMYKColor,
    GrayColor,
    HSVColor,
    HexColor,
    HSVColor,
    X11Color,
)
from borb.pdf.canvas.color.pantone import Pantone

# Image
from borb.pdf.canvas.layout.image.barcode import Barcode
from borb.pdf.canvas.layout.image.barcode import BarcodeType
from borb.pdf.canvas.layout.image.chart import Chart
from borb.pdf.canvas.layout.image.image import Image
from borb.pdf.canvas.layout.layout_element import Alignment

# List
from borb.pdf.canvas.layout.list.list import List
from borb.pdf.canvas.layout.list.ordered_list import OrderedList
from borb.pdf.canvas.layout.list.roman_list import RomanNumeralOrderedList
from borb.pdf.canvas.layout.list.unordered_list import UnorderedList

# PageLayout
from borb.pdf.canvas.layout.page_layout.page_layout import PageLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import MultiColumnLayout
from borb.pdf.canvas.layout.page_layout.multi_column_layout import SingleColumnLayout

# TODO  Doesn't exist for some reason???
from borb.pdf.canvas.layout.page_layout.single_column_layout_with_overflow import (
    SingleColumnLayoutWithOverflow,
)

# Flow
from borb.pdf.canvas.layout.page_layout.inline_flow import InlineFlow
from borb.pdf.canvas.layout.page_layout.block_flow import BlockFlow

# Shape
from borb.pdf.canvas.layout.shape.connected_shape import ConnectedShape
from borb.pdf.canvas.layout.shape.disconnected_shape import DisconnectedShape
from borb.pdf.canvas.layout.smart_art.smart_art import SmartArt

# Table
from borb.pdf.canvas.layout.table.fixed_column_width_table import FixedColumnWidthTable
from borb.pdf.canvas.layout.table.flexible_column_width_table import FlexibleColumnWidthTable
from borb.pdf.canvas.layout.table.table import Table, TableCell
from borb.pdf.canvas.layout.table.table_util import TableUtil
from borb.pdf.canvas.layout.text.heading import Heading

# Forms
from borb.pdf.canvas.layout.forms.form_field import FormField
from borb.pdf.canvas.layout.forms.text_field import TextField
from borb.pdf.canvas.layout.forms.text_area import TextArea
from borb.pdf.canvas.layout.forms.drop_down_list import DropDownList
from borb.pdf.canvas.layout.forms.country_drop_down_list import CountryDropDownList
from borb.pdf.canvas.layout.forms.check_box import CheckBox
from borb.pdf.canvas.layout.forms.push_button import PushButton, JavaScriptPushButton

# Paragraph
# from borb.pdf.canvas.layout.text.paragraph import Paragraph
from borb.pdf.canvas.layout.text.heterogeneous_paragraph import HeterogeneousParagraph
from borb.pdf.canvas.layout.text.heading import Heading
from borb.pdf.canvas.layout.text.chunk_of_text import ChunkOfText
from borb.pdf.canvas.lipsum.lipsum import Lipsum

# Document, Page, PDF
# from borb.pdf.document.document import Document
# from borb.pdf.page.page import Page
from borb.pdf.pdf import PDF

# Additional imports:
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont
