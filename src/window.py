from include import *

import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import Tk, Event, Widget, Misc, StringVar
from tkinter import N, NW, NE, S, SE, SW, E, W, CENTER, TOP, LEFT, RIGHT, BOTTOM
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
import tkcalendar


def create_window(title: str, width: int, height: int) -> Tk:
    """Creates a window with a set title and size"""
    window = Tk()
    window.title(title)
    window.geometry("{}x{}".format(width, height))
    return window


def _geometry(widget: Widget, anchor: str, side: str, marginx: int, marginy: int, fill: str) -> None:
    if side is not None and anchor is not None:
        widget.pack(side=side, anchor=anchor,
                    padx=marginx, pady=marginy, fill=fill)
    elif side is not None:
        widget.pack(side=side, padx=marginx, pady=marginy, fill=fill)
    elif anchor is not None:
        widget.pack(anchor=anchor, padx=marginx, pady=marginy, fill=fill)
    else:
        widget.pack(padx=marginx, pady=marginy, fill=fill)


def _grid(widget: Widget, x: int, y: int, marginx: int, marginy: int) -> None:
    widget.grid(row=y, column=x, padx=marginx, pady=marginy)


def loop_window(window: Tk):
    """Runs the main loop of the window"""
    window.mainloop()


def frame(parent: Misc, *,
          anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
          marginx: int = 0, marginy: int = 20,
          grid: bool = False, gridx: int = 0, gridy: int = 0,
          **options) -> tk.Frame:
    widget = tk.Frame(parent, **options)
    if grid:
        _grid(widget, gridx, gridy, marginx, marginy)
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def text(parent: Misc, text: str, *,
         anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
         marginx: int = 10, marginy: int = 10,
         fontfamily: str = FONT_FAMILY, fontsize: int = FONT_SIZE,
         grid: bool = False, gridx: int = 0, gridy: int = 0,
         **options) -> tk.Label:
    """Text widget"""
    widget = tk.Label(parent, text=text,
                      font=(fontfamily, fontsize), **options)
    if grid:
        _grid(widget, gridx, gridy, marginx, marginy)
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def button(parent: Misc, text: str, onclick: Callable[[], Any] = lambda: None, *,
           anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
           marginx: int = 10, marginy: int = 10,
           fontfamily: str = FONT_FAMILY, fontsize: int = FONT_SIZE,
           grid: bool = False, gridx: int = 0, gridy: int = 0,
           **options) -> tk.Button:
    """Button widget"""
    widget = tk.Button(parent, text=text, command=onclick,
                       font=(fontfamily, fontsize), **options)
    if grid:
        _grid(widget, gridx, gridy, marginx, marginy)
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def entry(parent: Misc, textvariable: StringVar, *, password: bool = False,
          anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
          marginx: int = 10, marginy: int = 10,
          grid: bool = False, gridx: int = 0, gridy: int = 0,
          **options) -> tkcalendar.DateEntry:
    """Text entry widget"""
    widget = tk.Entry(parent, textvariable=textvariable,
                      show='*' if password else None, **options)

    if grid:
        _grid(widget, gridx, gridy, marginx, marginy)
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def date_entry(parent: Misc, *,
               anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
               marginx: int = 10, marginy: int = 10,
               grid: bool = False, gridx: int = 0, gridy: int = 0,
               **options) -> tkcalendar.DateEntry:
    """Date entry widget"""
    widget = tkcalendar.DateEntry(parent, **options)

    if grid:
        _grid(widget, gridx, gridy, marginx, marginy)
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def error_dialog(title: str, message: str) -> None:
    messagebox.showerror(title, message)


def info_dialog(title: str, message: str) -> None:
    messagebox.showinfo(title, message)


def input_dialog(title: str, message: str, password: bool = False) -> str:
    return askstring(title, message, show='*' if password else None)


def file_open_dialog(file_types: List[Tuple[str, str]] = [], initialfile: str = "") -> str:
    return askopenfilename(filetypes=file_types, initialfile=initialfile)


def file_save_dialog(file_types: List[Tuple[str, str]] = [], initialfile: str = "") -> str:
    return asksaveasfilename(filetypes=file_types, initialfile=initialfile)


def destroy_widget(widget: Widget):
    widget.destroy()


def bind_key_event(parent: Misc, function: Callable[[Event], Any]) -> str:
    """Binds key press event, returns identifier for the binding"""
    return parent.bind("<Key>", function)


def unbind_key_event(parent: Misc, id: str) -> None:
    """Unbinds key press event, with indentifier"""
    parent.unbind("<Key>", function)


def bind_date_selected_event(parent: Misc, function: Callable[[Event], Any]) -> str:
    """Binds date entry selected event, returns identifier for the binding"""
    return parent.bind("<<DateEntrySelected>>")


def unbind_date_selected_event(parent: Misc, id: str) -> None:
    """Unbinds date entry selected event, with indentifier"""
    parent.unbind("<<DateEntrySelected>>", function)


def test_key_event(event: Event):
    """Key handler for window test"""
    log("{}", event)


def test_window():
    """Test the TKinter window"""
    window = create_window("Test Window", 640, 320)
    t = text(window, "Hello, world!")
    b = button(window, "Press me",
               lambda: text.configure(text="Hola, mundo!"))

    window.bind("<Escape>", lambda _: window.withdraw())
    window.bind("<Key>", test_key_event)

    window.mainloop()


if __name__ == '__main__':
    test_window()
