from escpos.exceptions import USBNotFoundError
from include import *

from escpos import printer as escpos
from PIL.Image import Image
from usb import core as usb

# TODO: Add support for network printers
# TODO: Add support for choosing printers/multiple printer brands


def get_usb_printer() -> Union[escpos.Escpos, None]:
    """Connects to a USB printer if one is connected to the computer."""
    try:
        return escpos.Usb(0x04b8, 0x0202)
    except USBNotFoundError:
        log("USB device not found")
        return None


def print_image(dev: escpos.Escpos, image: Union[str, Image]) -> None:
    """Prints an image through a receipt printer.
    The provided `image` argument may either be a Pillow image or a path to an image"""
    dev.image(image)


def print_text(dev: escpos.Escpos, text: str, block: bool = False, size: Union[int, None] = None) -> None:
    """Prints a string through a receipt printer. If `block` is set to true, the text will wrap"""
    if size != None:
        dev.set(width=size, height=size)

    if block:
        dev.block_text(text)
    else:
        dev.text(text)


def print_barcode(dev: escpos.Escpos, code: str) -> None:
    dev.barcode(code, 'CODE39')

def cut(dev: escpos.Escpos):
    """Cuts the receipt, when finished printing."""
    dev.cut()

if __name__ == '__main__':
    p = get_usb_printer()
    print_text(p, "Redwood High School\n", size=2)
    print_text(p, "Lipshitz, Sa'ar Liyam\n", size=1)
    print_image(p, "test/piggy.png")
    print_barcode(p, '116965')
    cut(p)