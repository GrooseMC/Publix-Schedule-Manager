#######################################################
#     Publix Schedule Manager - By Yazheed Jeries     #
#                                                     #
#   The purpose of this program is to automatically   #
#   assign cashiers to a register for their shifts.   #
#######################################################

import tkinter as tk
from tkinter import ttk

# Adjusted Schedule Times
times = [
    "6:30am", "6:45am",
    "7am", "7:15am", "7:30am", "7:45am",
    "8am", "8:15am", "8:30am", "8:45am",
    "9am", "9:15am", "9:30am", "9:45am",
    "10am", "10:15am", "10:30am", "10:45am",
    "11am", "11:15am", "11:30am", "11:45am",
    "12pm", "12:15pm", "12:30pm", "12:45pm",
    "1pm", "1:15pm", "1:30pm", "1:45pm",
    "2pm", "2:15pm", "2:30pm", "2:45pm",
    "3pm", "3:15pm", "3:30pm", "3:45pm",
    "4pm", "4:15pm", "4:30pm", "4:45pm",
    "5pm", "5:15pm", "5:30pm", "5:45pm",
    "6pm", "6:15pm", "6:30pm", "6:45pm",
    "7pm", "7:15pm", "7:30pm", "7:45pm",
    "8pm", "8:15pm", "8:30pm", "8:45pm",
    "9pm", "9:15pm", "9:30pm", "9:45pm",
    "10pm"
]

# [Name, [Break Start, Break End], [[Role1 Start, Role1 End, Role1 Type], [Role2 Start, Role2 End, Role2 Type]], ...]
# If Role Type is 0, that means the associate is cashiering during this interval. Otherwise, they are on break or other role.
cashiers = [
    ["Lori", [None, None], [["7am", "12pm", 0]]],
    ["Bobbie", ["1pm", "2pm"], [["9:30am", "1pm", 0], ["2pm", "4pm", 1], ["4pm", "5pm", 0]]],
    ["Nick", ["2pm", "3pm"], [["10:30am", "11:30am", 1], ["11:30am", "1:30pm", 0], ["1:30pm", "2pm", 1], ["3pm", "7:15pm", 0]]],
    ["Therese", ["4pm", "5pm"], [["12pm", "4pm", 0], ["5pm", "9pm", 0]]],
    ["Bonnie", ["5pm", "6pm"], [["1pm", "5pm", 0], ["6pm", "6:45pm", 1], ["6:45pm", "7:15pm", 1], ["7:15pm", "10pm", 1]]],
    ["Amanda", ["6:45pm", "7:15pm"], [["3:30pm", "6:45pm", 0], ["7:15pm", "9pm", 0], ["9pm", "9:15pm", 1]]]
]

class ScheduleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Publix Schedule Viewer")

        self.registers = []

        self.create_schedule_area()
        self.create_keymap()
        self.create_register_input_area()
        self.create_assign_button()

    def create_schedule_area(self):
        schedule_frame = tk.Frame(self.root)
        schedule_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        canvas = tk.Canvas(schedule_frame)
        h_scrollbar = tk.Scrollbar(schedule_frame, orient="horizontal", command=canvas.xview)
        v_scrollbar = tk.Scrollbar(schedule_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)

        canvas.grid(row=0, column=0, sticky="ew")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")

        for idx, cashier in enumerate(cashiers):
            label = tk.Label(scrollable_frame, text=f"{cashier[0]}'s Schedule:")
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

            # Create a canvas for schedule visualization
            schedule_canvas = tk.Canvas(scrollable_frame, width=len(times) * 15, height=30)
            schedule_canvas.grid(row=idx, column=1, padx=10, pady=5)

            # Draw vertical lines for every hour and half-hour
            for col, time in enumerate(times):
                if col % 2 == 0:  # Draw vertical black line every half-hour
                    schedule_canvas.create_line(col * 15, 0, col * 15, 30, fill="black")

                color = self.get_color(cashier, col)
                schedule_canvas.create_rectangle(col * 15, 15, (col + 1) * 15, 30, fill=color, outline="")

    def create_register_input_area(self):
        input_frame = tk.Frame(self.root)
        input_frame.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        tk.Label(input_frame, text="Total Number of Registers:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.num_registers_var = tk.IntVar()
        num_registers_entry = tk.Entry(input_frame, textvariable=self.num_registers_var)
        num_registers_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        add_registers_button = tk.Button(input_frame, text="Add Registers", command=self.add_registers)
        add_registers_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

        register_frame = tk.Frame(self.root)
        register_frame.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        self.register_canvas = tk.Canvas(register_frame)
        self.register_scrollbar = tk.Scrollbar(register_frame, orient="vertical", command=self.register_canvas.yview)
        self.register_scrollable_frame = tk.Frame(self.register_canvas)

        self.register_scrollable_frame.bind(
            "<Configure>",
            lambda e: self.register_canvas.configure(
                scrollregion=self.register_canvas.bbox("all")
            )
        )

        self.register_canvas.create_window((0, 0), window=self.register_scrollable_frame, anchor="nw")
        self.register_canvas.configure(yscrollcommand=self.register_scrollbar.set)

        self.register_canvas.grid(row=0, column=0, sticky="ew")
        self.register_scrollbar.grid(row=0, column=1, sticky="ns")

    def add_registers(self):
        for widget in self.register_scrollable_frame.winfo_children():
            widget.destroy()

        num_registers = self.num_registers_var.get()
        self.registers = []

        for i in range(num_registers):
            register = {
                "id": i + 1, 
                "type": tk.StringVar(value="Regular"), 
                "out_of_order": tk.BooleanVar()
            }
            self.registers.append(register)

            row = i
            tk.Label(self.register_scrollable_frame, text=f"Register {i + 1}").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            
            type_menu = ttk.Combobox(self.register_scrollable_frame, textvariable=register["type"], values=("Regular", "Express", "Backup"))
            type_menu.grid(row=row, column=1, padx=5, pady=5, sticky="w")

            out_of_order_check = tk.Checkbutton(self.register_scrollable_frame, text="Out of Order", variable=register["out_of_order"])
            out_of_order_check.grid(row=row, column=2, padx=5, pady=5, sticky="w")

        self.assign_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.check_requirements()

    def create_assign_button(self):
        self.assign_button = tk.Button(self.root, text="Assign", command=self.assign_registers)
        self.assign_button.grid(row=6, column=0, padx=10, pady=10, sticky="ew")
        self.assign_button.grid_remove()
        self.assign_button.bind("<Enter>", self.on_enter)
        self.assign_button.bind("<Leave>", self.on_leave)

    def assign_registers(self):
        if self.check_requirements():
            print("Assigning registers...")
            for register in self.registers:
                print(f"Register {register['id']} - Type: {register['type'].get()} - Out of Order: {register['out_of_order'].get()}")
        else:
            self.assign_button.configure(text="Assign (Requirements not met)")

    def check_requirements(self):
        has_express = any(register["type"].get() == "Express" for register in self.registers)
        has_backup = any(register["type"].get() == "Backup" for register in self.registers)
        if has_express and has_backup:
            self.assign_button.configure(state=tk.NORMAL, text="Assign")
            return True
        else:
            self.assign_button.configure(state=tk.DISABLED, text="Assign")
            return False

    def on_enter(self, event):
        if not self.check_requirements():
            self.assign_button.configure(text="Requirements not met")

    def on_leave(self, event):
        self.assign_button.configure(text="Assign")

    def get_color(self, cashier, time_index):
        """ Determine the color for the given time slot based on cashier's schedule. """
        for role in cashier[2]:
            start_time = times.index(role[0])
            end_time = times.index(role[1])
            if start_time <= time_index < end_time:
                if role[2] == 0:
                    return "green"  # Cashiering
                else:
                    return "yellow"  # Other role
        if self.is_on_break(cashier, time_index):
            return "blue"  # Break
        return "red"  # Not scheduled

    def is_on_break(self, cashier, time_index):
        """ Check if the cashier is on break at the given time. """
        break_start = cashier[1][0]
        break_end = cashier[1][1]

        if break_start is None or break_end is None:
            return False

        start_time = times.index(break_start)
        end_time = times.index(break_end)

        if start_time <= time_index < end_time:
            return True
        return False

    def create_keymap(self):
        """ Create a styled keymap legend above the register section. """
        legend_frame = tk.Frame(self.root, bg="black", bd=1, relief="solid")
        legend_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)

        colors = {
            "green": "Cashiering",
            "yellow": "Other Role",
            "blue": "On Break",
            "red": "Not Scheduled"
        }

        for color, description in colors.items():
            color_label = tk.Label(legend_frame, text=description, fg=color, bg="black")
            color_label.pack(side="left", padx=10, pady=2)

        for child in legend_frame.winfo_children():
            child.pack_configure(anchor="center")

if __name__ == '__main__':
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
