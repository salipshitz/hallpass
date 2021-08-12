from escpos.escpos import Escpos
from include import *

import usb.core
from escpos import printer
from PIL.Image import Image

# TODO: Add support for network printers


def get_usb_printer() -> Union[printer.Usb, None]:
    """Connects to a USB printer if one is connected to the computer."""
    # TODO: Add support for choosing multiple printers
    devs = usb.core.find(find_all=True, bDeviceClass=0x07)
    descs: list[tuple[str, str]] = []
    for dev in devs:
        descs.append((dev.idVendor, dev.idProduct))
    if len(descs) == 0:
        log("No USB printers connected.")
        return None
    else:
        return printer.Usb(*descs[0])


def print_image(dev: printer.Escpos, image: Union[str, Image]) -> None:
    """Prints an image through a receipt printer.
    The provided `image` argument may either be a Pillow image or a path to an image"""
    dev.image(image)


def print_text(dev: printer.Escpos, text: str, block: bool = False) -> None:
    """Prints a string through a receipt printer. If `block` is set to true, the text will wrap"""
    if block:
        dev.block_text(text)
    else:
        dev.text(text)

def cut(dev: printer.Escpos):
    """Cuts the receipt, when finished printing."""
    dev.cut()