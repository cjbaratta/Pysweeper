from tkinter import Button, Label, messagebox
import random
import settings
import sys

class Cell:

    all = []
    cell_count = settings.SAFE_COUNT
    cell_count_label_object = None
    def __init__(self, x, y, is_mine=False):

        self.is_mine = is_mine
        self.is_opened = False
        self.is_flagged = False
        self.cell_btn_object = None
        self.x = x
        self.y = y
        # Append object to Cell.all list
        Cell.all.append(self)

    def create_btn_object(self, location):
        btn = Button(
            location,
            width = 12,
            height = 4,
        )
        btn.bind('<Button-1>', self.left_click_actions)  # Left click
        # Replace button-2 with button-3 on Windows and Linux)
        btn.bind('<Button-3>', self.right_click_actions)  # Right click
        self.cell_btn_object = btn

    @staticmethod
    def create_cell_count_label(location):
        lbl = Label(
            location,
            font=("Arial", 24),
            bg='black',
            fg='white',
            text=f"Cells Left:{Cell.cell_count}",
        )
        Cell.cell_count_label_object = lbl

    def left_click_actions(self, event):
        if self.is_mine:
            self.show_mine()
        else:
            if self.surrounded_cells_mines_length == 0:
                for cell_obj in self.surrounded_cells:
                    cell_obj.show_cell()
                    self.cell_btn_object.configure(highlightbackground='black')
            self.show_cell()
            self.cell_btn_object.configure(highlightbackground='black')
        # Unbind events on opened cells
        self.cell_btn_object.unbind('<Button-1>')
        self.cell_btn_object.unbind('<Button-2>')

    def get_cell_by_axis(self, x, y):
        # Return cell object based on value of x, y
        for cell in Cell.all:
            if cell.x == x and cell.y == y:
                return cell

    @property
    def surrounded_cells(self):
        cells = [
            self.get_cell_by_axis(self.x - 1, self.y - 1),
            self.get_cell_by_axis(self.x - 1, self.y),
            self.get_cell_by_axis(self.x - 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y - 1),
            self.get_cell_by_axis(self.x + 1, self.y),
            self.get_cell_by_axis(self.x + 1, self.y + 1),
            self.get_cell_by_axis(self.x, self.y + 1)
        ]

        cells = [cell for cell in cells if cell is not None]
        return cells

    @property
    def surrounded_cells_mines_length(self):
        counter = 0
        for cell in self.surrounded_cells:
            if cell.is_mine:
                counter += 1
        return counter

    def show_cell(self):
        if not self.is_opened:
            Cell.cell_count -= 1
            self.cell_btn_object.configure(text=self.surrounded_cells_mines_length)
            # Replace text of cell count label with the newer count
            if Cell.cell_count_label_object:
                Cell.cell_count_label_object.configure(
                    text=f"Cells Left:{Cell.cell_count}"
                )
            # Mark cell as opened (use as last line of method)
            self.is_opened = True
        if Cell.cell_count == 0:
            messagebox.showinfo(
                "You won!",
                "Congratulations!\nYou won!"
            )
            sys.exit()

    def show_mine(self):
        # Using outlines to display mines due to macOS click handling.
        self.cell_btn_object.configure(bg='red')
        messagebox.showinfo(
            "You lost!",
            "You blew up!\nTry again?"
        )
        sys.exit()

    def right_click_actions(self, event):
        if not self.is_flagged:
            self.cell_btn_object.configure(highlightbackground='orange')
            self.is_flagged = True
        else:
            self.cell_btn_object.configure(highlightbackground='white')
            self.is_flagged = False

    @staticmethod
    def randomize_mines():
        picked_cells = random.sample(Cell.all, settings.MINES_COUNT)
        for picked_cell in picked_cells:
            picked_cell.is_mine = True

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"
