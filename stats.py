import tkinter as tk


class Stats(tk.Frame):
    def __init__(self, root, width, height):
        container = tk.Frame(root)
        self.canvas = tk.Canvas(container, bg="black",
                                highlightbackground="black")
        scrollbar = tk.Scrollbar(
            container, orient="vertical", command=self.canvas.yview, bg="black")
        self.scrollable_frame = tk.Frame(self.canvas, bg="black")
        # self.scrollable_frame.pack_propagate(0)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame)

        self.canvas.configure(yscrollcommand=scrollbar.set,
                              width=width, height=height)

        container.pack(side="bottom")
        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add(self, stringToAdd):
        tk.Label(self.scrollable_frame, text=stringToAdd,  # font=("Helvetica", 3),
                 fg="white", bg="black").pack(side="bottom")
        # self.canvas.yview_moveto(0) # Scrolls to the top
