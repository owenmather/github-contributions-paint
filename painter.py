import tkinter
import os

WHITE = "white"
INPUT_IMAGE_PATH = os.environ.get("INPUT_IMAGE_PATH", "image.txt")

color0 = "#161b22"
color1 = "#0e4429"
color2 = "#006d32"
color3 = "#26a641"
color4 = "#39d353"

colors = [color0, color1, color2, color3, color4]

next_color = {
    color0: color1,
    color1: color2,
    color2: color3,
    color3: color4,
    color4: color0
}


class Painter:
    canvas: tkinter.Canvas

    def __init__(self, margin=20, square_size=30, horizontal_squares=30, vertical_squares=7):
        self.MARGIN = margin
        self.SQUARE_SIZE = square_size
        self.HORIZONTAL_SQUARES = horizontal_squares
        self.VERTICAL_SQUARES = vertical_squares
        self.HEIGHT = self.VERTICAL_SQUARES * self.SQUARE_SIZE + self.MARGIN * 2
        self.WIDTH = self.HORIZONTAL_SQUARES * self.SQUARE_SIZE + self.MARGIN * 2
        self.grid = []
        self.drag_color = color1

    def get_square(self, event):
        return int((event.x - self.MARGIN) / self.SQUARE_SIZE) + ((int((event.y - self.MARGIN) / self.SQUARE_SIZE)) *
                                                                  self.HORIZONTAL_SQUARES)

    def change_square_color(self, event):
        target = self.get_square(event)
        color = next_color[self.canvas.itemconfig(self.grid[target])['fill'][-1]]
        self.canvas.itemconfig(self.grid[target], fill=color)
        self.drag_color = color

    def paint_square(self, event):
        col = int((event.x - self.MARGIN) / self.SQUARE_SIZE)
        row = int((event.y - self.MARGIN) / self.SQUARE_SIZE)
        if 0 <= col < self.HORIZONTAL_SQUARES and 0 <= row < self.VERTICAL_SQUARES:
            target = col + row * self.HORIZONTAL_SQUARES
            self.canvas.itemconfig(self.grid[target], fill=self.drag_color)

    def clear_grid(self):
        for rect in self.grid:
            self.canvas.itemconfig(rect, fill=color0)

    def save_grid(self):
        image_data = ""
        for idx, rect in enumerate(self.grid):
            if idx > 0 and idx % self.HORIZONTAL_SQUARES == 0:
                image_data += "\n"
            image_data += str(colors.index(self.canvas.itemconfig(rect)['fill'][-1]))

        with open(INPUT_IMAGE_PATH, "w") as csv_file:
            csv_file.write(image_data)

    def load_grid(self):
        self.clear_grid()
        with open(INPUT_IMAGE_PATH, "r") as image_file:
            data = image_file.read().split("\n")
            data = "".join(data)

        for idx, code in enumerate(list(data)):
            self.canvas.itemconfig(self.grid[idx], fill=colors[int(code)])

    def run(self):
        top = tkinter.Tk()
        top.resizable(False, False)
        self.canvas = tkinter.Canvas(top, bg=WHITE, height=self.HEIGHT, width=self.WIDTH)

        for y in range(7):
            for i in range(self.HORIZONTAL_SQUARES):
                rect = self.canvas.create_rectangle((i * self.SQUARE_SIZE) + self.MARGIN,
                                                    (y * self.SQUARE_SIZE) + self.MARGIN,
                                                    ((i + 1) * self.SQUARE_SIZE) + self.MARGIN,
                                                    ((y + 1) * self.SQUARE_SIZE) + self.MARGIN,
                                                    fill=color0,
                                                    outline=WHITE)
                self.grid.append(rect)
        self.canvas.bind("<Button-1>", self.change_square_color)
        self.canvas.bind("<B1-Motion>", self.paint_square)
        # Code to add widgets will go here...
        self.canvas.pack()
        frame = tkinter.Frame(top)
        frame.pack()
        # flat, groove, raised, ridge, solid, or sunken
        load_button = tkinter.Button(frame, text="Load", command=self.load_grid, fg=WHITE, bg="blue", width=10,
                                     height=2, relief="raised", bd=1)
        clear_button = tkinter.Button(frame, text="Clear", command=self.clear_grid, fg=WHITE, bg="red", width=10,
                                      height=2, relief="raised", bd=1)
        save_button = tkinter.Button(frame, text="Save", command=self.save_grid, width=10, height=2, relief="raised",
                                     bd=1)

        load_button.pack({"side": "left"})
        clear_button.pack({"side": "left"})
        save_button.pack({"side": "left"})

        top.mainloop()


if __name__ == '__main__':
    p = Painter()
    p.run()
