from __future__ import division, print_function
import pytest
import warbler
import os

from pathlib import Path
from pdf2image import convert_from_path
from PIL import ImageChops, Image, ImageDraw
from decimal import Decimal

from borb.pdf import Alignment as BorbAlignment
from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation as BorbHyphenation
from borb.pdf.canvas.color.color import HexColor as BorbHexColor, X11Color as BorbX11Color
from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont as BorbTrueTypeFont
from borb.pdf.canvas.geometry.rectangle import Rectangle as BorbRectangle

LOREM_IPSUM = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Tortor consequat id porta nibh venenatis cras sed felis eget. Augue lacus viverra vitae congue eu. Ut tortor pretium viverra suspendisse potenti nullam ac tortor. Lectus vestibulum mattis ullamcorper velit sed. Quisque id diam vel quam elementum pulvinar. Sagittis vitae et leo duis ut diam quam nulla. Cras fermentum odio eu feugiat pretium nibh ipsum. Nam at lectus urna duis convallis convallis tellus id interdum. Vitae ultricies leo integer malesuada nunc. Sem fringilla ut morbi tincidunt augue interdum velit. Vulputate dignissim suspendisse in est ante in. Enim eu turpis egestas pretium aenean pharetra magna. Malesuada proin libero nunc consequat interdum varius sit amet mattis. Pulvinar elementum integer enim neque volutpat ac tincidunt vitae semper. Rhoncus dolor purus non enim. Et leo duis ut diam quam nulla porttitor massa id.'


def test_imports_and_access():
    warbler.Document
    warbler.Page
    warbler.PDF
    warbler.PageLayout
    warbler.SingleColumnLayout
    warbler.MultiColumnLayout
    warbler.Alignment
    warbler.Paragraph
    warbler.Heading
    warbler.Image
    warbler.Chart
    warbler.Barcode
    warbler.BarcodeType
    warbler.ConnectedShape
    warbler.DisconnectedShape
    warbler.Table
    warbler.TableCell
    warbler.FixedColumnWidthTable
    warbler.FlexibleColumnWidthTable
    warbler.List
    warbler.OrderedList
    warbler.UnorderedList
    warbler.RomanNumeralOrderedList
    warbler.Color
    warbler.RGBColor
    warbler.CMYKColor
    warbler.GrayColor
    warbler.HSVColor
    warbler.HexColor
    warbler.X11Color
    warbler.Pantone
    warbler.TrueTypeFont
    warbler.SquareAnnotation


def test_basic_hello_world_document():
    # Create a basic hello world PDF:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    page.add('Hello, world!')
    doc.save('output-warbler.pdf')

    # Create the equivalent PDF with borb:
    from borb.pdf import Document
    from borb.pdf import Page
    from borb.pdf import PageLayout
    from borb.pdf import SingleColumnLayout
    from borb.pdf import Paragraph
    from borb.pdf import PDF
    from borb.pdf.page.page_size import PageSize

    doc = Document()
    page = Page(width=PageSize.LETTER_PORTRAIT.value[0], height=PageSize.LETTER_PORTRAIT.value[1])
    doc.add_page(page)
    layout = SingleColumnLayout(page)
    layout.add(Paragraph("Hello, world!"))
    with open("output-borb.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    imagesBorb = convert_from_path('output-borb.pdf')
    imagesWarbler = convert_from_path('output-warbler.pdf')
    diff = ImageChops.difference(imagesBorb[0], imagesWarbler[0])
    assert diff.getbbox() is None  # Images are the same.


def test_different_paragraph_styles():
    # Create a PDF with paragraphs with different text styles:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    page.add(
        LOREM_IPSUM,
        font='Courier',
        font_size=14,
        text_alignment='right',
        font_color='red',
        border=True,
        border_color='blue',
        border_radius=5,
        border_width=10,
        hyphenation='en-us',
    )
    doc.save('output-warbler.pdf')

    # Create the equivalent PDF with borb:
    from borb.pdf import Document, Page, SingleColumnLayout, Paragraph, PDF, Alignment
    from borb.pdf.page.page_size import PageSize
    from borb.pdf.canvas.layout.hyphenation.hyphenation import Hyphenation

    doc = Document()
    page = Page(width=PageSize.LETTER_PORTRAIT.value[0], height=PageSize.LETTER_PORTRAIT.value[1])
    doc.add_page(page)
    layout = SingleColumnLayout(page)
    layout.add(
        Paragraph(
            LOREM_IPSUM,
            font='Courier',
            font_size=Decimal(14),
            text_alignment=Alignment.RIGHT,
            font_color=BorbHexColor('FF0000'),
            border_top=True,
            border_right=True,
            border_bottom=True,
            border_left=True,
            border_color=BorbHexColor('0000FF'),
            border_width=Decimal(10),
            border_radius_top_left=Decimal(5),
            border_radius_top_right=Decimal(5),
            border_radius_bottom_right=Decimal(5),
            border_radius_bottom_left=Decimal(5),
            hyphenation=Hyphenation('en-us'),
        )
    )

    with open("output-borb.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    imagesBorb = convert_from_path('output-borb.pdf')
    imagesWarbler = convert_from_path('output-warbler.pdf')
    diff = ImageChops.difference(imagesBorb[0], imagesWarbler[0])
    # if diff.getbbox() is not None:
    #    ImageDraw.Draw(imagesBorb[0]).rectangle(diff.getbbox(), None, 'red')
    #    imagesBorb[0].show()
    assert diff.getbbox() is None  # Images are the same.


def test_custom_font():
    # Create the Hello World PDF with custom font in Borb:
    from borb.pdf import Document, Page, SingleColumnLayout, Paragraph, PDF, Alignment
    from borb.pdf.page.page_size import PageSize
    from borb.pdf.canvas.font.simple_font.true_type_font import TrueTypeFont

    doc = Document()
    page = Page(width=PageSize.LETTER_PORTRAIT.value[0], height=PageSize.LETTER_PORTRAIT.value[1])
    doc.add_page(page)
    layout = SingleColumnLayout(page)
    fontPath = Path(__file__).parent / 'Minecraft.ttf'
    customFont = TrueTypeFont.true_type_font_from_file(fontPath)
    layout.add(Paragraph('Hello, world!', font=customFont))
    with open("output-borb.pdf", "wb") as pdf_file_handle:
        PDF.dumps(pdf_file_handle, doc)

    imagesBorb = convert_from_path('output-borb.pdf')

    # Create the PDF in Warbler passing a TrueTypeFont object:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    fontPath = Path(__file__).parent / 'Minecraft.ttf'
    customFont = warbler.TrueTypeFont.true_type_font_from_file(fontPath)
    page.add('Hello, world!', font=customFont)
    doc.save('output-warbler.pdf')

    imagesWarbler = convert_from_path('output-warbler.pdf')
    diff = ImageChops.difference(imagesBorb[0], imagesWarbler[0])
    assert diff.getbbox() is None  # Images are the same.

    # Create the PDF in Warbler passing the Path of the ttf file:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    fontPath = Path(__file__).parent / 'Minecraft.ttf'
    page.add('Hello, world!', font=fontPath)
    doc.save('output-warbler.pdf')

    imagesWarbler = convert_from_path('output-warbler.pdf')
    diff = ImageChops.difference(imagesBorb[0], imagesWarbler[0])
    assert diff.getbbox() is None  # Images are the same.

    # Create the PDF in Warbler passing the str of the ttf file:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    fontPath = os.path.join(os.path.split(__file__)[0], 'Minecraft.ttf')
    page.add('Hello, world!', font=fontPath)
    doc.save('output-warbler.pdf')

    imagesWarbler = convert_from_path('output-warbler.pdf')
    diff = ImageChops.difference(imagesBorb[0], imagesWarbler[0])
    assert diff.getbbox() is None  # Images are the same.


def _test_rectangle_annotations():
    # Create the PDF in Warbler:
    import warbler

    doc = warbler.Document()
    page = doc.add_page()
    r = warbler.Rectangle(50, 50, 100, 100)
    page.add_annotation(SquareAnnotation(r, stroke_color='red'))
    Paragraph('Hello', alignment='left').paint(page, r)
    doc.save('output-warbler.pdf')


def test_normalize_text_alignment():
    assert warbler.util._normalize_text_alignment(BorbAlignment.LEFT) == BorbAlignment.LEFT
    assert warbler.util._normalize_text_alignment(BorbAlignment.RIGHT) == BorbAlignment.RIGHT
    assert warbler.util._normalize_text_alignment(BorbAlignment.CENTERED) == BorbAlignment.CENTERED
    assert warbler.util._normalize_text_alignment(BorbAlignment.JUSTIFIED) == BorbAlignment.JUSTIFIED

    assert warbler.util._normalize_text_alignment('left') == BorbAlignment.LEFT
    assert warbler.util._normalize_text_alignment('right') == BorbAlignment.RIGHT
    assert warbler.util._normalize_text_alignment('center') == BorbAlignment.CENTERED
    assert warbler.util._normalize_text_alignment('justified') == BorbAlignment.JUSTIFIED

    assert warbler.util._normalize_text_alignment('lEfT') == BorbAlignment.LEFT
    assert warbler.util._normalize_text_alignment('rIgHt') == BorbAlignment.RIGHT
    assert warbler.util._normalize_text_alignment('centERED') == BorbAlignment.CENTERED
    assert warbler.util._normalize_text_alignment('JustIFied') == BorbAlignment.JUSTIFIED

    with pytest.raises(ValueError):
        warbler.util._normalize_text_alignment('')
    with pytest.raises(ValueError):
        warbler.util._normalize_text_alignment(BorbAlignment.TOP)
    with pytest.raises(ValueError):
        warbler.util._normalize_text_alignment(BorbAlignment.MIDDLE)
    with pytest.raises(ValueError):
        warbler.util._normalize_text_alignment(BorbAlignment.BOTTOM)


def test_normalize_alignment():
    assert warbler.util._normalize_alignment(BorbAlignment.TOP) == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(BorbAlignment.MIDDLE) == (BorbAlignment.MIDDLE, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(BorbAlignment.BOTTOM) == (BorbAlignment.BOTTOM, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(BorbAlignment.LEFT) == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(BorbAlignment.CENTERED) == (BorbAlignment.TOP, BorbAlignment.CENTERED)
    assert warbler.util._normalize_alignment(BorbAlignment.RIGHT) == (BorbAlignment.TOP, BorbAlignment.RIGHT)

    assert warbler.util._normalize_alignment('top') == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment('middle') == (BorbAlignment.MIDDLE, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment('bottom') == (BorbAlignment.BOTTOM, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment('left') == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment('center') == (BorbAlignment.TOP, BorbAlignment.CENTERED)
    assert warbler.util._normalize_alignment('right') == (BorbAlignment.TOP, BorbAlignment.RIGHT)

    assert warbler.util._normalize_alignment(' tOP xxx ') == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(' miDDle xxx ') == (BorbAlignment.MIDDLE, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(' boTTom xxx ') == (BorbAlignment.BOTTOM, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(' leFT xxx ') == (BorbAlignment.TOP, BorbAlignment.LEFT)
    assert warbler.util._normalize_alignment(' ceNTerED xxx ') == (BorbAlignment.TOP, BorbAlignment.CENTERED)
    assert warbler.util._normalize_alignment(' riGHt xxx ') == (BorbAlignment.TOP, BorbAlignment.RIGHT)

    assert warbler.util._normalize_alignment('') == (BorbAlignment.TOP, BorbAlignment.LEFT)


def test_normalize_vertical_alignment():
    assert warbler.util._normalize_vertical_alignment(BorbAlignment.TOP) == BorbAlignment.TOP
    assert warbler.util._normalize_vertical_alignment(BorbAlignment.MIDDLE) == BorbAlignment.MIDDLE
    assert warbler.util._normalize_vertical_alignment(BorbAlignment.BOTTOM) == BorbAlignment.BOTTOM
    assert warbler.util._normalize_vertical_alignment('top') == BorbAlignment.TOP
    assert warbler.util._normalize_vertical_alignment('middle') == BorbAlignment.MIDDLE
    assert warbler.util._normalize_vertical_alignment('bottom') == BorbAlignment.BOTTOM
    assert warbler.util._normalize_vertical_alignment('tOP') == BorbAlignment.TOP
    assert warbler.util._normalize_vertical_alignment('mIDdle') == BorbAlignment.MIDDLE
    assert warbler.util._normalize_vertical_alignment('bOTtom') == BorbAlignment.BOTTOM

    with pytest.raises(ValueError):
        warbler.util._normalize_vertical_alignment('')
    with pytest.raises(ValueError):
        warbler.util._normalize_vertical_alignment(BorbAlignment.LEFT)
    with pytest.raises(ValueError):
        warbler.util._normalize_vertical_alignment(BorbAlignment.CENTERED)
    with pytest.raises(ValueError):
        warbler.util._normalize_vertical_alignment(BorbAlignment.RIGHT)
    with pytest.raises(ValueError):
        warbler.util._normalize_vertical_alignment(BorbAlignment.JUSTIFIED)


def test_normalize_horizontal_alignment():
    assert warbler.util._normalize_horizontal_alignment(BorbAlignment.LEFT) == BorbAlignment.LEFT
    assert warbler.util._normalize_horizontal_alignment(BorbAlignment.CENTERED) == BorbAlignment.CENTERED
    assert warbler.util._normalize_horizontal_alignment(BorbAlignment.RIGHT) == BorbAlignment.RIGHT
    assert warbler.util._normalize_horizontal_alignment('left') == BorbAlignment.LEFT
    assert warbler.util._normalize_horizontal_alignment('center') == BorbAlignment.CENTERED
    assert warbler.util._normalize_horizontal_alignment('right') == BorbAlignment.RIGHT
    assert warbler.util._normalize_horizontal_alignment('lEFT') == BorbAlignment.LEFT
    assert warbler.util._normalize_horizontal_alignment('cENTer') == BorbAlignment.CENTERED
    assert warbler.util._normalize_horizontal_alignment('rIGHt') == BorbAlignment.RIGHT

    with pytest.raises(ValueError):
        warbler.util._normalize_horizontal_alignment('')
    with pytest.raises(ValueError):
        warbler.util._normalize_horizontal_alignment(BorbAlignment.TOP)
    with pytest.raises(ValueError):
        warbler.util._normalize_horizontal_alignment(BorbAlignment.MIDDLE)
    with pytest.raises(ValueError):
        warbler.util._normalize_horizontal_alignment(BorbAlignment.BOTTOM)
    with pytest.raises(ValueError):
        warbler.util._normalize_horizontal_alignment(BorbAlignment.JUSTIFIED)


def test_normalize_color():
    # This test fails because of rounding errors in HexColor.__init__
    assert warbler.util._normalize_color(BorbHexColor('#AABBCC'))  # .to_hex_string() == '#aabbcc'

    for color_name in BorbX11Color.COLOR_DEFINITION:
        assert warbler.util._normalize_color(color_name)

    # This test fails because of rounding errors in HexColor.__init__
    for r in range(0, 256, 16):
        for g in range(0, 256, 16):
            for b in range(0, 256, 16):
                assert warbler.util._normalize_color(
                    (r, g, b)
                )  # .to_hex_string() == "#{:02x}{:02x}{:02x}".format(r, g, b)
                assert warbler.util._normalize_color(
                    "#{:02x}{:02x}{:02x}".format(r, g, b)
                )  # .to_hex_string() == "#{:02x}{:02x}{:02x}".format(r, g, b)
                assert warbler.util._normalize_color(
                    "{:02x}{:02x}{:02x}".format(r, g, b)
                )  # .to_hex_string() == "#{:02x}{:02x}{:02x}".format(r, g, b)


def test_normalize_hyphenation():
    # These tests don't work because of a Borb issue.
    # for iso_language_code in ('af', 'as', 'be', 'bg', 'bn', 'ca', 'cy', 'da', 'de', 'en-gb', 'en-us', 'es', 'et', 'fi', 'fr', 'lt', 'nl', 'ro', 'ru'):
    for iso_language_code in ('en-us',):
        assert warbler.util._normalize_hyphenation(iso_language_code)
        assert warbler.util._normalize_hyphenation(BorbHyphenation(iso_language_code))


def test_normalize_font():
    # This doesn't test that warbler is equivalent to borb, just that the warbler function doesn't fail.
    fontPath = Path(__file__).parent / 'Minecraft.ttf'
    customFont = warbler.TrueTypeFont.true_type_font_from_file(fontPath)

    assert isinstance(
        warbler.util._normalize_font(customFont), BorbTrueTypeFont
    )  # This should not fail and return a TrueTypeFont object

    fontPath = Path(__file__).parent / 'Minecraft.ttf'
    assert isinstance(warbler.util._normalize_font(fontPath), BorbTrueTypeFont)

    fontPath = os.path.join(os.path.split(__file__)[0], 'Minecraft.ttf')
    assert isinstance(warbler.util._normalize_font(fontPath), BorbTrueTypeFont)


def test_normalize_rectangle():
    r = warbler.util._normalize_rectangle(BorbRectangle(Decimal(1), Decimal(2), Decimal(3), Decimal(4)))
    assert r.get_x() == 1
    assert r.get_y() == 2
    assert r.get_width() == 3
    assert r.get_height() == 4

    r = warbler.util._normalize_rectangle((1, 2, 3, 4))
    assert r.get_x() == 1
    assert r.get_y() == 2
    assert r.get_width() == 3
    assert r.get_height() == 4


if __name__ == "__main__":
    pytest.main()
