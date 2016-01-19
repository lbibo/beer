import tkinter as tk
import tkMessageBox

class Main_Frame(tk.Frame):
    """Class for controlling the application frame"""

    def __init__(self, master = None):
        """initialize main frame, set frame variables, and start login process."""

        """Set variables"""
        self.HEIGHT = 400
        self.WIDTH = 600
        self.BGCOLOR = '#000000'
        self.TEXT_COLOR = '#FFFFFF'

        """Configure main frame"""
        tk.Frame.__init__(self, master)
        self.title("Beer")
        self.resizable(width = FALSE, height = FALSE)
        self.columnconfigure(0, minsize = int(WIDTH / 4), weight = 0)
        self.columnconfigure(1, minsize = int(WIDTH / 4), weight = 0)
        self.columnconfigure(2, minsize = int(WIDTH / 4), weight = 0)
        self.columnconfigure(3, minsize = int(WIDTH / 4), weight = 0)
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)

        """Methods run on startup"""
        create_widgets()

        return

    def create_widgets(self):
        """create all widgets"""
        self.login_frame = tk.Frame(self, background = self.BGCOLOR, padx = 5)
        self.user_input_frame = tk.Frame(self, background = self.BGCOLOR, padx = 5)
        self.console_output_frame = Frame(beerapp, background = BGCOLOR, padx = 15, pady = 15)
        return

    # Methods for making application state changes
    def show_login(self):
        self.login_frame.grid(row = 1, column = 0, columnspan = 1)
        self.login_frame.columnconfigure(0, minsize = int(WIDTH / 4), weight = 0)
        self.login_frame.rowconfigure(0, minsize = int(HEIGHT / 3), weight = 0)
        self.login_frame.rowconfigure(1, minsize = int(HEIGHT / 3), weight = 0)
        return

    def show_saved(self):
        return

    def show_input_new(self):
        return

    # Event handlers
    def login_existing(self, user):
        return

    # Methods for altering individual widgets
    def print_to_console(self, input):
        """Pass string input to label"""
        return

    def show_widget(self, widget):
        return