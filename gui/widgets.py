import logging
import tkinter as tk
from abc import abstractmethod

logger = logging.getLogger(__name__)


class Dialog(tk.Toplevel):
    def __init__(self, parent, title=None):
        super(Dialog, self).__init__(parent)
        self.parent = parent
        self.result = None
        self.transient(parent)
        if title:
            self.title(title)

        body = tk.Frame(self)
        self.initial_focus = self.body(body)

        body.pack(padx=5, pady=5)

        self.create_buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry(
            "+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 300)
        )

        self.initial_focus.focus_set()

        self.wait_window(self)

    @abstractmethod
    def body(self, master):
        """
        :param master: parent widget
        :return: tk widget which will be focused first
        """

        pass

    def create_buttonbox(self):
        """
        creates standard buttons, "cancel" and "ok"
        binds keys ECS and ENTER
        binds methods self.cancel and self.ok
        """

        box = tk.Frame(self)

        w = tk.Button(box, text="OK", width=10, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = tk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    def ok(self, event=None):
        """
        will run apply if validation passes, destroys dialog
        """

        if not self.validate():
            self.initial_focus.focus_set()  # put focus back
            return

        self.withdraw()
        self.update_idletasks()

        self.apply()

        self.cancel()

    def cancel(self, event=None):
        """
        refocus parent, destroy dialog
        """
        self.parent.focus_set()
        self.destroy()

    @abstractmethod
    def validate(self):
        """
        will keep in prompt until valid data
        :return: if valid data
        """
        pass

    @abstractmethod
    def apply(self):
        """
        sets field result
        :return:
        """
        pass


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""

    def __init__(self, text_widget):
        """
        :param text_widget: Tkinter Text or ScrolledText widget
        """
        super(TextHandler, self).__init__()

        self.text = text_widget

    def emit(self, record):
        msg = self.format(record)

        def append():
            self.text.configure(state="normal")
            self.text.insert(tk.END, msg + "\n", record.levelname)
            self.text.configure(state="disabled")
            # Autoscroll to the bottom
            self.text.yview(tk.END)

        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)


