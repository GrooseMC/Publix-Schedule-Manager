#######################################################
#     Publix Schedule Manager - By Yazheed Jeries     #
#                                                     #
#   The purpose of this program is to automatically   #
#   assign cashiers to a register for their shifts.   #
#######################################################

import tkinter as tk

# Adjusted Schedule Times
times = [
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

        self.create_schedule()
        self.create_keymap()

    def create_schedule(self):
        # Create a frame for each cashier's schedule
        for idx, cashier in enumerate(cashiers):
            label = tk.Label(self.root, text=f"{cashier[0]}'s Schedule:")
            label.grid(row=idx, column=0, sticky="w", padx=10, pady=5)

            # Create a canvas for schedule visualization
            canvas = tk.Canvas(self.root, width=len(times) * 10, height=30)
            canvas.grid(row=idx, column=1, padx=10, pady=5)

            # Draw hour labels and schedule bars
            for col, time in enumerate(times):
                if time.endswith("am") or time.endswith("pm"):
                    hour_label = time[:-2]  # Get the hour part
                    if idx == 0 and col % 4 == 0:  # Display hour label every 4th time slot for the top cashier
                        canvas.create_text(col * 10 + 5, 1, text=hour_label, anchor="n", fill="black", font=("Arial", 8, "bold"))
                    if col % 2 == 0:  # Draw vertical black line every half-hour
                        canvas.create_line(col * 10, 0, col * 10, 30, fill="black")

                color = self.get_color(cashier, col)
                canvas.create_rectangle(col * 10, 15, (col + 1) * 10, 30, fill=color, outline="")

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
        """ Create a styled keymap legend at the bottom of the window. """
        legend_frame = tk.Frame(self.root, bg="black", bd=1, relief="solid")
        legend_frame.grid(row=len(cashiers), column=0, columnspan=2, sticky="ew", padx=10, pady=5)

        colors = {
            "green": "Cashiering",
            "yellow": "Other Role",
            "blue": "On Break",
            "red": "Not Scheduled"
        }

        for color, description in colors.items():
            color_label = tk.Label(legend_frame, text=description, fg=color, bg="black")
            color_label.pack(side="left", padx=5, pady=2)

if __name__ == '__main__':
    root = tk.Tk()
    app = ScheduleApp(root)
    root.mainloop()
