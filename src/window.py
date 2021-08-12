from include import *

import tkinter as tk
from tkinter import Tk, Event, Widget, Misc
from tkinter import N, NW, NE, S, SE, SW, E, W, CENTER, TOP, LEFT, RIGHT, BOTTOM
from tkinter.filedialog import askopenfile


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


def loop_window(window: Tk):
    """Runs the main loop of the window"""
    window.mainloop()


def frame(parent: Misc,
          anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
          marginx: int = 0, marginy: int = 20,
          place: bool = False, **options) -> tk.Frame:
    widget = tk.Frame(parent, **options)
    if place:
        pass
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def text(parent: Misc, text: str,
         anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
         marginx: int = 10, marginy: int = 10,
         fontfamily: str = FONT_FAMILY, fontsize: int = FONT_SIZE,
         place: bool = False, **options) -> tk.Label:
    """Text widget"""
    widget = tk.Label(parent, text=text,
                      font=(fontfamily, fontsize), **options)
    if place:
        pass
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def button(parent: Misc, text: str, onclick: Callable[[], Any] = lambda: None,
           anchor: Union[str, None] = None, side: Union[str, None] = None, fill: str = 'none',
           marginx: int = 10, marginy: int = 10,
           fontfamily: str = FONT_FAMILY, fontsize: int = FONT_SIZE,
           place: bool = False, **options) -> tk.Button:
    """Button widget"""
    widget = tk.Button(parent, text=text, command=onclick,
                       font=(fontfamily, fontsize), **options)
    if place:
        pass
    else:
        _geometry(widget, anchor, side, marginx, marginy, fill)
    return widget


def file_dialog(mode: str, file_types: List[Tuple[str, str]] = []) -> Union[IO, None]:
    return askopenfile(mode, filetypes=file_types)


def destroy_widget(widget: Widget):
    widget.destroy()


def bind_key_event(window: Tk, function: Callable[[Event], Any]) -> str:
    """Binds key press event to window, returns identifier for the binding"""
    return window.bind("<Key>", function)


def unbind_key_event(window: Tk, id: str) -> None:
    """Unbinds key press event, with indentifier"""
    window.unbind("<Key>", function)


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
