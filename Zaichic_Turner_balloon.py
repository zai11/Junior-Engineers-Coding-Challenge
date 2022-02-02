import tkinter as tk

class Balloon:
    
    image_source = "./balloon.png"
    movement_speed = 1

    def __init__(self, x, y):
        self.x = x;
        self.y = y;
    
    def draw(self, canvas):
        self.sprite = tk.PhotoImage(file=self.image_source)
        canvas.create_image(self.x, self.y, anchor=tk.NW, image=self.sprite)

class MainWindow:

    def __init__(self):
        self.window = tk.Tk()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.width = screen_width / 2
        self.height = screen_height / 2
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height / 2 - self.height / 2
        self.window.title("Junior Engineers Coding Challenge Option 1")
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
    
    def getWindow(self):
        return self.window


if __name__ == "__main__":
    root = MainWindow().getWindow()
    balloon = Balloon(20, 20)
    balloon.draw(root)
    root.mainloop()