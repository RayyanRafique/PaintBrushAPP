from tkinter import *
from tkinter import Button, Scale, Canvas, Label, StringVar, messagebox, Entry, Toplevel
from tkinter.colorchooser import askcolor
from tkinter import filedialog
from tkinter import colorchooser
from PIL import ImageGrab
from PIL import Image, ImageDraw, ImageTk
from tkinter import ttk
import math
import os


class FilenamePopup:
    def __init__(self, master):
        top = self.top = Toplevel(master)
        self.lbl = Label(top, text="Choose a file name:")
        self.lbl.grid(row=0, column=0, padx=10, pady=10)
        self.ent_filename = Entry(top)
        self.ent_filename.grid(row=1, column=0, padx=10, pady=10)
        self.btn_ok = Button(top, text='Ok', command=self.cleanup)
        self.btn_ok.grid(row=2, column=0, padx=10, pady=10)

    def cleanup(self):
        self.filename = self.ent_filename.get().strip()
        self.top.destroy()


class CNCCanvas(Canvas, object):
    # Calculate arguments for antialiasing
    def antialias_args(self, args, winc=0.5, cw=2):
        nargs = {}

        # Set defaults
        nargs['width'] = 1
        nargs['fill'] = "#000"

        # Get original args
        for arg in args:
            nargs[arg] = args[arg]
        if nargs['width'] == 0:
            nargs['width'] = 1

        # Calculate width
        nargs['width'] += winc

        # Calculate color
        cbg = self.winfo_rgb(self.cget("bg"))
        cfg = list(self.winfo_rgb(nargs['fill']))
        cfg[0] = (cfg[0] + cbg[0] * cw) / (cw + 1)
        cfg[1] = (cfg[1] + cbg[1] * cw) / (cw + 1)
        cfg[2] = (cfg[2] + cbg[2] * cw) / (cw + 1)
        nargs['fill'] = '#%02x%02x%02x' % (cfg[0] // 256, cfg[1] // 256, cfg[2] // 256)

        return nargs

    # Override create_line method if antialiasing is enabled
    def create_line(self, *args, **kwargs):
        nkwargs = self.antialias_args(kwargs)
        super(CNCCanvas, self).create_line(*args, **nkwargs)
        return super(CNCCanvas, self).create_line(*args, **kwargs)


class Paint(object):
    DEFAULT_PEN_SIZE = 5.0
    DEFAULT_COLOR = 'black'

    def __init__(self, width=1550, height=840):
        self.root = Tk()
        self.root.title("Paint Application")
        self.root.geometry(f"{width}x{height}")

        self.button_area = Frame(self.root)
        self.button_area.grid(row=0, columnspan=9)

        #Save Button
        self.save =PhotoImage(file = "D:\Python\save.png")

        self.save_button = ttk.Button(self.button_area, text="Save", command=self.save_file, image=self.save)
        self.save_button.grid(row=0, column=0)

        #Load Button
        self.load =PhotoImage(file = "D:\Python\load.png")
        self.load_button = ttk.Button(self.button_area, text="load", command=self.loadImage, image= self.load)
        self.load_button.grid(row=0, column=1)

        #Pen Button
        self.pen =PhotoImage(file = "D:\Python\pen.png")
        self.pen_button = ttk.Button(self.button_area, text='Pen', command=self.use_pen, image=self.pen )
        self.pen_button.grid(row=0, column=2)

        #Brush Button
        self.brush =PhotoImage(file = "D:\Python\OBrush.png")
        self.brush_button = ttk.Button(self.button_area, text='Brush', command=self.use_brush, image = self.brush)
        self.brush_button.grid(row=0, column=3)

        #Color Button
        self.colors =PhotoImage(file = "D:\Python\potato.png")
        self.color_button = ttk.Button(self.button_area, text='Select color', command=self.choose_color, image = self.colors)
        self.color_button.grid(row=0, column=5)

        #Eraser Button
        self.eraser =PhotoImage(file = "D:\Python\eraser.png")
        self.eraser_button = ttk.Button(self.button_area, text='Eraser', command=self.use_eraser, image = self.eraser)
        self.eraser_button.grid(row=0, column=4)

        #Fill Button
        self.fill =PhotoImage(file = "D:\Python\illbucket.png")
        self.fill_button = ttk.Button(self.button_area, text='Fill', command=self.select_fill_color,image=self.fill)
        self.fill_button.grid(row=0, column=6)

        #Clear Button
        self.clear =PhotoImage(file = "D:\Python\clear.png")
        self.clear_button = ttk.Button(self.button_area, text='Clear', command=self.clear_screen,image=self.clear)
        self.clear_button.grid(row=0, column=7)

        #Select Size Bar
        self.choose_size_button = Scale(self.button_area, from_=2, to=15, orient=HORIZONTAL)
        self.choose_size_button.grid(row=0, column=20)

         #Circle button
        self.circle =PhotoImage(file = "D:\Python\cir.png")
        self.circle_button = ttk.Button(self.button_area, text = "Circle", command = self.on_circleButton_pressed,image=self.circle)
        self.circle_button.grid(row=0, column =8)

        #Oval button
        self.oval =PhotoImage(file = "D:\Python\oval.png")
        self.oval_button = ttk.Button(self.button_area, text = "Oval", command = self.on_ovalButton_pressed, image=self.oval)
        self.oval_button.grid(row=0, column = 9)

        #rectangle button
        self.rect =PhotoImage(file = "D:\Python\ect.png")
        self.rectangle_button = ttk.Button(self.button_area, text = "Rectangle", command = self.on_rectangleButton_pressed,image=self.rect)
        self.rectangle_button.grid(row=0, column = 10)

        #square button
        self.sq =PhotoImage(file = "D:\Python\sq.png")
        self.square_button = ttk.Button(self.button_area, text = "Square", command = self.on_squareButton_pressed,image= self.sq)
        self.square_button.grid(row=0, column = 11)

        #triangle button
        self.tri =PhotoImage(file = "D:\Python\i.png")
        self.triangle_button = ttk.Button(self.button_area, text = "Triangle", command = self.on_triangleButton_pressed,image=self.tri)
        self.triangle_button.grid(row=0, column = 12)

        #line button
        self.line =PhotoImage(file = "D:\Python\line.png")
        self.line_button = ttk.Button(self.button_area, text = "Line", command = self.on_lineButton_pressed,image = self.line)
        self.line_button.grid(row=0, column = 13)

        # pentagon button
        self.pentagon =PhotoImage(file = "D:\Python\pentagon.png")
        self.pentagon_button = ttk.Button(self.button_area, text='Pentagon', command=self.on_pentagonButton_pressed,image=self.pentagon)
        self.pentagon_button.grid(row=0, column=14)

        # Star button
        self.star =PhotoImage(file = "D:\Python\star.png")
        self.star_button = ttk.Button(self.button_area, text='star', command=self.on_star_pressed,image=self.star)
        self.star_button.grid(row=0, column=15)

         # Selection button
        self.select =PhotoImage(file = "D:\Python\select.png")
        self.select_button = ttk.Button(self.button_area, text='Select', command=self.on_select_pressed,image=self.select)
        self.select_button.grid(row=0, column=16)

        self.color_buttons_area = Frame(self.root)
        self.color_buttons_area.grid(row=1, columnspan=18)

        #Magnify/Zoom
        self.magnify =PhotoImage(file = "D:\Python\magnify.png")
        self.magnify_button = ttk.Button(self.button_area, text="Magnify", command=self.magnify_canvas,image=self.magnify)
        self.magnify_button.grid(row=0, column=17)

        #Random Colors
        self.color_buttons = []
        for index, color in enumerate(["black", "red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "gray"]):
            button = Button(self.color_buttons_area, bg=color, width=2, relief=FLAT, command=lambda c=color: self.select_color(c))
            button.grid(row=0, column=index, padx=2, pady=2)
            self.color_buttons.append(button)

        self.c = Canvas(self.root, bg='white', width=width, height=height - 100)
        self.c.grid(row=2, columnspan=9, sticky="nsew")

        self.setup()
        self.root.mainloop()

    #initial
    def setup(self):
        self.old_x = None   
        self.old_y = None
        self.line_width = self.choose_size_button.get()
        self.color = self.DEFAULT_COLOR
        self.eraser_on = False
        self.fill_color = None
        self.shape_id = None
        self.active_button = self.pen_button
        self.c.bind('<B1-Motion>', self.paint)
        self.c.bind('<ButtonRelease-1>', self.reset)
        self.magnified_image = None
        self.start_x = None
        self.start_y = None

    #pen
    def use_pen(self):
        self.activate_button(self.pen_button)

    #brush
    def use_brush(self):
        self.activate_button(self.brush_button)

    #Choose color
    def choose_color(self):
        self.eraser_on = False
        color = askcolor(color=self.color)[1]
        if color is not None:
            self.color = color

    #eraser
    def use_eraser(self):
        self.activate_button(self.eraser_button, eraser_mode=True)

    #clearScreen
    def clear_screen(self):
        self.c.delete('all')

    def activate_button(self, some_button, eraser_mode=False):
        self.active_button.config(relief=RAISED)
        some_button.config(relief=SUNKEN)
        self.active_button = some_button
        self.eraser_on = eraser_mode

    #paint
    def paint(self, event):
        self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        if self.old_x and self.old_y:
            self.c.create_line(
                self.old_x, self.old_y, event.x, event.y,
                width=self.line_width, fill=paint_color,
                capstyle=ROUND, smooth=TRUE, splinesteps=36
            )
        self.old_x = event.x
        self.old_y = event.y

    #Reset
    def reset(self, event):
        self.old_x, self.old_y = None, None

    #Select Color
    def select_color(self, color):
        self.color = color

    #Fill Color
    def select_fill_color(self):
        
        color = colorchooser.askcolor()[1]
        self.fill_color = color
        self.c.bind("<Button-1>",self.fill_color_at_position)
    
    def fill_color_at_position(self,event):
        self.fill(event)

    #Magnify
    def magnify_canvas(self):
        self.c.unbind('<Button-1>')  # Unbind the previous binding
        self.c.bind('<Button-1>', self.magnify)

    def magnify(self, event):
        x, y = event.x, event.y
        window_size = 400  

        window_x1 = max(x - window_size // 2 + 120, 0)
        window_y1 = max(y - window_size // 2 + 200, 0)
        window_x2 = min(x + window_size // 2 + 120, self.c.winfo_width())
        window_y2 = min(y + window_size // 2 + 200, self.c.winfo_height())

        actual_window_size = min(window_x2 - window_x1, window_y2 - window_y1)

        if actual_window_size < window_size:
            window_x1 = max(x - actual_window_size // 2, 0)
            window_y1 = max(y - actual_window_size // 2, 0)
            window_x2 = min(x + actual_window_size // 2, self.c.winfo_width())
            window_y2 = min(y + actual_window_size // 2, self.c.winfo_height())

        
        image = ImageGrab.grab(bbox=(window_x1, window_y1, window_x2, window_y2))
        image = image.resize((actual_window_size*1 , actual_window_size*1), Image.ANTIALIAS)

        magnified_window = Toplevel(self.root)
        magnified_window.title("Magnified View")
        self.magnified_image = ImageTk.PhotoImage(image)  # Store the image to prevent it from being garbage collected
        magnified_canvas = Canvas(magnified_window, width=actual_window_size, height=actual_window_size)
        magnified_canvas.create_image(0, 0, anchor="nw", image=self.magnified_image)
        magnified_canvas.pack()

        self.c.unbind('<Button-1>')

    #Fill
    def fill(self, event):
        x, y = event.x, event.y
        item = self.c.find_closest(x,y)[0]
        self.c.itemconfig(item, fill=self.fill_color)

    #Circle
    def on_circleButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_circle) 
        self.c.bind("<ButtonRelease-1>", self.draw_circle_end) 

    def draw_circle(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y  
            return
        radius = abs(self.last_x - event.x) + abs(self.last_y - event.y)

        x1, y1 = (self.last_x - radius), (self.last_y - radius)
        x2, y2 = (self.last_x + radius), (self.last_y + radius)
        self.shape_id = self.c.create_oval(x1, y1, x2, y2, outline="black", width=2, fill="")

    def draw_circle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None
        

    #Oval
    def on_ovalButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_oval) 
        self.c.bind("<ButtonRelease-1>", self.draw_oval_end) 

    def draw_oval(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        self.shape_id = self.c.create_oval(x1, y1, x2, y2, outline="black", width=2, fill="")
            
    def draw_oval_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None


    #Rectangle
    def on_rectangleButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_rectangle)
        self.c.bind("<ButtonRelease-1>", self.draw_rectangle_end)

    def draw_rectangle(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        self.shape_id = self.c.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill="")

    def draw_rectangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 


    #Square
    def on_squareButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_square)
        self.c.bind("<ButtonRelease-1>", self.draw_square_end)

    def draw_square(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        side = min(abs(event.x - self.last_x), abs(event.y - self.last_y))
        if event.x < self.last_x:
            x1 = self.last_x - side
            x2 = self.last_x
        else:
            x1 = self.last_x
            x2 = self.last_x + side
        if event.y < self.last_y:
            y1 = self.last_y - side
            y2 = self.last_y
        else:
            y1 = self.last_y
            y2 = self.last_y + side
        self.shape_id = self.c.create_rectangle(x1, y1, x2, y2, outline="black", width=2, fill="")

    def draw_square_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None  


    #Triangle
    def on_triangleButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_triangle)
        self.c.bind("<ButtonRelease-1>", self.draw_triangle_end)

    def draw_triangle(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        x3, y3 = (2 * self.last_x) - event.x, event.y
        self.shape_id = self.c.create_polygon(x1, y1, x2, y2, x3, y3, outline="black", width=2, fill="")

    def draw_triangle_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None  


    #Line
    def on_lineButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")

        self.c.bind("<B1-Motion>", self.draw_line)
        self.c.bind("<ButtonRelease-1>", self.draw_line_end)

    def draw_line(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            self.last_x, self.last_y = event.x, event.y
            return
        x1, y1 = self.last_x, self.last_y
        x2, y2 = event.x, event.y
        self.shape_id = self.c.create_line(x1, y1, x2, y2, width=4)

    def draw_line_end(self, event):
        self.last_x, self.last_y = None, None
        self.shape_id = None 


    #Pentagon 
    def on_pentagonButton_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")
        self.c.bind("<Button-1>", self.start_pentagon_drawing)

    def start_pentagon_drawing(self, event):
        self.last_x = event.x
        self.last_y = event.y
        self.c.bind("<B1-Motion>", self.draw_pentagon)
        self.c.bind("<ButtonRelease-1>", self.end_pentagon_drawing)

    def draw_pentagon(self, event):
        if self.shape_id is not None:
            self.c.delete(self.shape_id)
        if self.last_x is None:
            return
        cx, cy = (self.last_x + event.x) / 2, (self.last_y + event.y) / 2
        radius = math.sqrt((event.x - cx) ** 2 + (event.y - cy) ** 2)
        points = self.calculate_pentagon_points(cx, cy, radius)
        self.shape_id = self.c.create_polygon(points, outline="black", width=2, fill="")

    def end_pentagon_drawing(self, event):
        self.last_x , self.last_y = None, None
        self.shape_id = None

    def calculate_pentagon_points(self, cx, cy, radius):
        angle = 2 * math.pi / 5
        points = []
        for i in range(5):
            point_x = cx + math.cos(i * angle) * radius
            point_y = cy + math.sin(i * angle) * radius
            points.extend([point_x, point_y])
        return points
    
    #star
    def on_star_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")
        self.c.bind("<Button-1>", self.start_star)

    def start_star(self, event):
        self.star_start_x = event.x
        self.star_start_y = event.y
        self.c.bind("<B1-Motion>", self.draw_star_shape)
        self.c.bind("<ButtonRelease-1>", self.stop_star)

    def calculate_star_points(self, x1, y1, x2, y2):
        radius = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        inner_radius = radius / 2
        angle = 2 * math.pi / 5
        points = []
        for i in range(5):
            outer_x = x1 + radius * math.cos(i * angle)
            outer_y = y1 + radius * math.sin(i * angle)
            inner_x = x1 + inner_radius * math.cos((i + 0.5) * angle)
            inner_y = y1 + inner_radius * math.sin((i + 0.5) * angle)
            points.extend([outer_x, outer_y, inner_x, inner_y])
        return points

    def draw_star_shape(self, event):
        x1, y1 = self.star_start_x, self.star_start_y
        x2, y2 = event.x, event.y
        points = self.calculate_star_points(x1, y1, x2, y2)

        if self.shape_id:
            self.c.delete(self.shape_id)
        self.shape_id = self.c.create_polygon(*points, fill="", outline="black", width=4)

    def stop_star(self, event):
        if self.shape_id:
            star_coords = self.c.coords(self.shape_id)
            star_action = {"type": "star", "item": self.shape_id, "coordinates": star_coords}

        self.shape_id = None
                      
    #selection tool
    def on_select_pressed(self):
        self.c.unbind("<B1-Motion>")
        self.c.unbind("<ButtonRelease-1>")
        self.c.bind("<Button-1>", self.start_selection)

    def start_selection(self, event):
        self.start_x = event.x
        self.start_y = event.y
        self.c.bind("<B1-Motion>", self.update_selection)
        self.c.bind("<ButtonRelease-1>", self.end_selection)

    def update_selection(self, event):
        self.end_x = event.x
        self.end_y = event.y

        if self.selection:
            self.c.delete(self.selection)

        self.selection = self.c.create_rectangle(
            self.start_x, self.start_y, self.end_x, self.end_y,
            outline="red", dash=(4, 4))

    def end_selection(self, event):
        if self.selection:
            self.c.delete(self.selection)
            self.selection = None

        # Move the selected area to a new position
        if self.start_x is not None and self.start_y is not None:
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.c.move(Tk.ALL, dx, dy)

        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
    



    #save / load
    def save_file(self):
        self.popup = FilenamePopup(self.root)
        self.save_button["state"] = "disabled"
        self.root.wait_window(self.popup.top)

        if self.popup.filename:
            filepng = self.popup.filename + '.png'
            filepath = os.path.abspath(filepng) 

            if not os.path.exists(filepng) or messagebox.askyesno("File already exists", "Overwrite?"):
                self.c.update()
                x = self.c.winfo_rootx()
                y = self.c.winfo_rooty()
                width = self.c.winfo_width()
                height = self.c.winfo_height()
                border = -25  

                ImageGrab.grab(bbox=( x - border, y - border, x + width + border, y + height + border)).save(filepng, 'png')

                messagebox.showinfo("File Save", f"File saved!\n\nPath: {filepath}")
            else:
                messagebox.showwarning("File Save", "File not saved!")

        self.save_button["state"] = "normal"

    def loadImage(self):
        self.clear_screen()
        filepng = filedialog.askopenfilename()
        if filepng != '':
            self.img = ImageTk.PhotoImage(Image.open(filepng))
            self.c.create_image(0, 0, anchor=NW, image=self.img)

if __name__ == '__main__':
    Paint()



