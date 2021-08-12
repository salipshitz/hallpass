# Hall Pass

Hall Pass is a program which scans the barcode on a student ID and prints out a hall pass from a receipt printer connected via USB. It is written entirely in Python, making use of the `python-escpos` library for use of ESC/POS printers (receipt printers).

## Dependencies & Installation

This application requires `libusb`. Some computers come with the library preinstalled, but many do not. To install `libusb`, go to <https://github.com/libusb/libusb/releases>.

The application was written in Python 3.8. Ensure you have that version installed and you can use it.

After downloading the files, enter the installed directory in a terminal and type:  
```python -m pip install -r requirements.txt```

To run the application, simply run the `main.py` file in the `src` directory. In the future, executable releases will be made to more easily install and run the application.
