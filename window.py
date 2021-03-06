import tkinter as tk
from virtual_world.gui import Dialog
from tkinter import scrolledtext

from virtual_world.organism_generator import OrganismGenerator
from virtual_world.location import Location
from virtual_world.world import World
from virtual_world.logger import logger


class WorldSizeDialog(Dialog):
    def __init__(self, parent, title):
        self.e1 = None
        self.e2 = None
        self.result = None
        super(WorldSizeDialog, self).__init__(parent, title)

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


class AddOrganismDialog(Dialog):
    def __init__(self, parent, title):
        self.file_name = None
        self.result = None
        super(AddOrganismDialog, self).__init__(parent, title)

    def body(self, master):
        self.tkvar = tk.StringVar(root)
        choices = ('Sheep', 'Antelope', 'Wolf', 'Turtle', 'CyberSheep', 'Human',
                   'belladonna', 'grass', 'guarana', 'sosnowskyBorshcht', 'dandelion')
        self.tkvar.set('Sheep')  # set the default option

        popupMenu = tk.OptionMenu(master, self.tkvar, *choices)
        tk.Label(master, text="Choose an organism").grid(row=1, column=1)
        popupMenu.grid(row=2, column=1)

        return popupMenu  # initial focus

    def apply(self):
        if str(self.tkvar.get()) == "guarana":
            self.result = str(self.tkvar.get())[1]

        else:
            self.result = str(self.tkvar.get())[0]

    def validate(self):
        return True


class FileNameDialog(Dialog):
    def __init__(self, parent, title):
        self.file_name = None
        self.result = None
        super(FileNameDialog, self).__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="File name:").grid(row=0)

        self.file_name = tk.Entry(master)
        self.file_name.grid(row=0, column=1)
        return self.file_name  # initial focus

    def apply(self):
        self.result = str(self.file_name.get())

    def validate(self):
        return True


class Application(tk.Frame):
    def __init__(self, master, dimentions):
        super().__init__(master)
        self.pack()
        self.quit_btn = None
        self.save_btn = None
        self.load_btn = None
        self.new_game_btn = None
        self.next_turn_btn = None
        self.logging_stext = None
        self.board = None
        self.game_frame = None
        self.world = World(dimentions[0], dimentions[1])
        self.create_widgets(master)

        def append_log(log):
            self.logging_stext.configure(state="normal")
            self.logging_stext.insert(tk.END, log + "\n")
            self.logging_stext.configure(state="disabled")
            # Autoscroll to the bottom
            self.logging_stext.yview(tk.END)

        logger.set_appender(append_log)
        self.create_board(master, dimentions)
        master.bind("<Escape>", lambda _: root.destroy())
        master.bind("<Up>", self.human_move)
        master.bind("<Down>", self.human_move)
        master.bind("<Right>", self.human_move)
        master.bind("<Left>", self.human_move)
        master.bind("p", self.human_move)
        master.bind("n", self.manage_key)
        master.bind("s", self.manage_key)
        master.bind("l", self.manage_key)
        master.bind("<space>", self.manage_key)

    def manage_key(self, e):
        key = e.keysym
        if key == "n":
            self.new_game()
        if key == "s":
            self.save()
        if key == "l":
            self.load()
        if key == "space":
            self.new_turn()

    def human_move(self, key):
        if self.world.get_human():
            self.world.get_human().key_typed(key)
            self.new_turn()
        else:
            logger.log("Human is dead")

    def new_turn(self):
        self.world.play_round()
        self.update_board()

    def save(self):
        dial = FileNameDialog(self.master, "Enter file name")
        self.world.save_to_file(dial.result)

    def load(self):
        dial = FileNameDialog(self.master, "Enter file name")
        self.world.load_from_file(dial.result)
        self.game_frame.destroy()
        self.create_board(self.master, (self.world.get_width(), self.world.get_height()))
        self.update_board()

    def new_game(self):
        self.world.create_new_world()
        self.update_board()

    def create_widgets(self, window):
        widget_frame = tk.Frame(window)
        self.save_btn = tk.Button(widget_frame, text="SAVE [s]", command=self.save)
        self.save_btn.pack(side="top", fill="x")
        self.load_btn = tk.Button(widget_frame, text="LOAD [l]", command=self.load)
        self.load_btn.pack(side="top", fill="x")
        self.new_game_btn = tk.Button(widget_frame, text="NEW GAME [n]", command=self.new_game)
        self.new_game_btn.pack(side="top", fill="x")
        self.next_turn_btn = tk.Button(widget_frame, text="NEXT TURN [space]", command=self.new_turn)
        self.next_turn_btn.pack(side="top", fill="x")
        self.quit_btn = tk.Button(widget_frame, text="QUIT [esc]", fg="red", command=root.destroy)
        self.quit_btn.pack(side="top", fill="x")
        self.logging_stext = scrolledtext.ScrolledText(widget_frame, state="disabled")
        self.logging_stext.configure(font="TkDefaultFont")
        self.logging_stext.tag_config("INFO", foreground="black")
        self.logging_stext.tag_config("DEBUG", foreground="gray")
        self.logging_stext.tag_config("WARNING", foreground="orange")
        self.logging_stext.tag_config("ERROR", foreground="red")
        self.logging_stext.tag_config("CRITICAL", foreground="red", underline=1)
        self.logging_stext.pack(side="bottom")
        widget_frame.pack(side="left")

    def create_board(self, window, dimentions):
        self.game_frame = tk.Frame(window, borderwidth=2, relief=tk.SUNKEN)

        def create_square(i, j):
            f = tk.Frame(self.game_frame, height=30, width=30)
            s = tk.Button(f, borderwidth=1, state="normal", foreground="#000000")
            s.pack(fill=tk.BOTH, expand=True)

            # buttons bindings
            def __handler(event, x=j, y=i):
                if not self.world.who_is_there(Location(x, y)):
                    dialog = AddOrganismDialog(self.master, "Choose an organism")
                    if not (dialog.result == "H" and self.world.get_human()):
                        o = OrganismGenerator.get_organism(dialog.result)
                        o.set_location(Location(x, y))
                        self.world.organisms.append(o)
                        self.update_board()
                    else:
                        logger.log("There can only be one human!")
                else:
                    logger.log("Field taken by " + self.world.who_is_there(Location(x, y)).get_name())

            s.bind("<Button-1>", __handler)
            s.bind("<Button-3>", __handler)

            f.pack_propagate(False)
            f.grid(row=i, column=j)
            return s

        self.board = [[create_square(i, j) for j in range(dimentions[0])]
                      for i in range(dimentions[1])]
        self.update_board()
        self.game_frame.pack(padx=10, pady=10, side="right")

    def update_board(self):
        for row in self.board:
            for button in row:
                button["text"] = ""
                button["state"] = "disabled"
        for o in self.world.organisms:
            self.board[o.get_location().y][o.get_location().x]["text"] = o.get_symbol()


if __name__ == "__main__":
    root = tk.Tk()
    root.wm_title("Anna Przybycien 172126")
    dialog = WorldSizeDialog(root, "Enter world size")
    app = Application(root, dialog.result)
    app.mainloop()
