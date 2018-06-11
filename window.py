import tkinter as tk
from virtual_world.gui import Dialog


class WorldSizeDialog(Dialog):
    def __init__(self, parent, title):
        super(WorldSizeDialog, self).__init__(parent, title)
        self.e1 = None
        self.e2 = None
        self.result = None

    def body(self, master):
        tk.Label(master, text="X:").grid(row=0)
        tk.Label(master, text="Y:").grid(row=1)

        self.e1 = tk.Entry(master)
        self.e2 = tk.Entry(master)

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1  # initial focus

    def validate(self):
        return int(self.e1.get()) > 0 and int(self.e2.get()) > 0

    def apply(self):
        x = int(self.e1.get())
        y = int(self.e2.get())

        self.result = (x, y)


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.quit_btn = None
        self.save_btn = None
        self.load_btn = None
        self.new_game_btn = None
        self.next_turn_btn = None
        self.create_widgets()

    def create_widgets(self):
        self.save_btn = tk.Button(self, text="SAVE", command=self.say_hi)
        self.save_btn.pack(side="left")
        self.load_btn = tk.Button(self, text="LOAD", command=self.say_hi)
        self.load_btn.pack(side="left")
        self.new_game_btn = tk.Button(self, text="NEW GAME", command=self.say_hi)
        self.new_game_btn.pack(side="left")
        self.next_turn_btn = tk.Button(self, text="NEXT TURN", command=self.say_hi)
        self.next_turn_btn.pack(side="left")
        self.quit_btn = tk.Button(self, text="QUIT", fg="red", command=root.destroy)
        self.quit_btn.pack(side="left")

    def say_hi(self):
        print("hi there, everyone!")


root = tk.Tk()
app = Application(master=root)
dialog = WorldSizeDialog(root, "Enter world size")
app.mainloop()
