import tkinter as tk
from random import randint

class Balloon:
    
    image_source = "./balloon.png"
    movement_speed = 1
    direction = -1
    width = 80
    height = 110

    ticks_passed = 0
    next_change = 0

    def __init__(self, x, y, canvas):
        self.x = x;
        self.y = y;
        self.canvas = canvas
        entities["balloon"] = self
    
    def draw(self):
        self.sprite = tk.PhotoImage(file=self.image_source)
        self.image = self.canvas.create_image(self.x, self.y, image=self.sprite)

    def move(self):
        x_offset = 0 * self.movement_speed * self.direction
        y_offset = 1 * self.movement_speed * self.direction
        self.x += x_offset
        self.y += y_offset
        if self.ticks_passed > self.next_change:
            self.direction = self.direction * -1
            self.ticks_passed = 0
            self.next_change = randint(50, 300)
        self.canvas.move(self.image, x_offset, y_offset)
        if (self.y >= self.canvas.winfo_height() - self.height / 2) or (self.y <= self.height / 2):
            self.direction = self.direction * -1
        self.canvas.after(10, self.move)
        self.ticks_passed += 1

    def hit(self):
        self.canvas.delete(self.image)

class Cannon:

    image_source = "./cannon.png"
    movement_speed = 2
    width = 80
    height = 110
    shot_counter = 0

    up_pressed = False
    down_pressed = False

    def __init__(self, x, y, canvas):
        self.x = x
        self.y = y
        self.canvas = canvas
        entities["cannon"] = self
        

    def draw(self):
        self.sprite = tk.PhotoImage(file=self.image_source)
        self.image = self.canvas.create_image(self.x, self.y, image=self.sprite)

    def move(self):
        y_offset = 0
        if self.up_pressed and not (self.y - self.height/2 < 0) and game_playing:
            y_offset = -1 * self.movement_speed
        elif self.down_pressed and not(self.y + self.height/2 > main_window.height) and game_playing:
            y_offset = self.movement_speed
        else:
            y_offset = 0
        self.y += y_offset
        self.canvas.move(self.image, 0, y_offset)
        self.canvas.after(10, self.move)
        

    def shoot(self, event):
        if game_playing:
            x = self.x - self.width / 2 + 5
            y = self.y + self.height / 2 - 5
            self.ball = Ball(self.shot_counter, self.x, self.y, self.canvas)
            self.ball.draw()
            self.ball.move()
            self.shot_counter += 1

    def upPress(self, event):
        if not self.down_pressed:
            self.up_pressed = True

    def downPress(self, event):
        if not self.up_pressed:
            self.down_pressed = True

    def upRelease(self, event):
        self.up_pressed = False

    def downRelease(self, event):
        self.down_pressed = False

class Ball:

    image_source = "./ball.png"
    movement_speed = 10
    hit_balloon = False

    def __init__(self, ball_id, x, y, canvas):
        self.ball_id = ball_id
        self.x = x
        self.y = y
        self.canvas = canvas

    def draw(self):
        self.sprite = tk.PhotoImage(file=self.image_source)
        self.image = self.canvas.create_image(self.x, self.y, image=self.sprite)
 
    def move(self):
        x_offset = -1 * self.movement_speed
        self.x += x_offset
        self.canvas.move(self.image, x_offset, 0)
        self.collision()
        if self.x > 0 or self.hit_balloon:
            canvas.after(10, self.move)

    def collision(self):
        global game_playing
        balloon = entities["balloon"]
        if (self.x >= balloon.x - balloon.width / 2) and\
           (self.x <= balloon.x + balloon.width / 2) and\
           (self.y >= balloon.y - balloon.height / 2) and\
           (self.y <= balloon.y + balloon.height / 2) and\
           game_playing:
            game_playing = False
            balloon.hit()
            self.canvas.delete(self.image)
            ui = EndUI(self.ball_id, main_window.width, main_window.height, canvas)
            ui.draw()

class MainWindow:

    def __init__(self):
        self.window = tk.Tk()
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.width = screen_width / 2
        self.height = screen_height / 2
        self.x = screen_width / 2 - self.width / 2
        self.y = screen_height / 2 - self.height / 2
        self.window.title("Junior Engineers Technical Assessment Option 1")
        self.window.geometry("%dx%d+%d+%d" % (self.width, self.height, self.x, self.y))
        self.canvas = tk.Canvas(self.window, bg="white", width=self.width, height=self.height)
        self.canvas.pack(expand=1, fill=tk.BOTH);
    
    def getWindow(self):
        return self.window

    def getCanvas(self):
        return self.canvas

class EndUI:

    def __init__(self, missed_shots, width, height, canvas):
        self.missed_shots = missed_shots
        self.width = width
        self.height = height
        self.canvas = canvas

    def draw(self):
        self.canvas.create_text(self.width / 2, self.height / 2 - 20, fill="black", font="Sans 40 bold", text="Game Over")
        self.canvas.create_text(self.width / 2, self.height / 2 + 50, fill="black", font="Sans 28", text="Missed shots: " + str(self.missed_shots))


if __name__ == "__main__":
    entities = {}
    game_playing = True
    main_window = MainWindow()
    root = main_window.getWindow()
    canvas = main_window.getCanvas()
    balloon = Balloon(80, 80, canvas)
    balloon.draw()
    balloon.move()
    cannon = Cannon(main_window.width - 40, 80, canvas)
    cannon.draw()
    cannon.move()
    root.bind("<KeyPress-Up>", cannon.upPress)
    root.bind("<KeyPress-Down>", cannon.downPress)
    root.bind("<KeyRelease-Up>", cannon.upRelease)
    root.bind("<KeyRelease-Down>", cannon.downRelease)
    root.bind("<KeyPress-space>", cannon.shoot)
    root.mainloop()
