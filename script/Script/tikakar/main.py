import os
import json
import math
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk

img_paths = None

# Dev
# input_dir = "/Users/monirul/Downloads/ANPR/fazle2"
# output_dir = "/Users/monirul/Downloads/ANPR/fazle2_output"

# Prod
input_dir = ""
output_dir = ""

root = Tk()
root.title("Tikakar")
root.geometry("640x640")


def slope(p1, p2):
    return math.atan2(
        (p2[1] - p1[1]), (p2[0] - p1[0])
    )


def spherical_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y


def add_points(p1, p2):
    return int(p1[0] + p2[0]), int(p1[1] + p2[1])


def crop_resize_save(box, i):
    global img_path, output_dir
    filename = os.path.basename(img_path)
    name, ext = os.path.splitext(filename)
    output_filename = "{}_{}{}".format(name, i, ext)
    im = Image.open(img_path)

    cropped = im.crop(box=box)
    print("cropped image size: {}".format(cropped.size))
    resized = cropped.resize((1920, 1080), Image.Resampling.LANCZOS)
    print("resized image size: {}".format(resized.size))
    output_filepath = os.path.join(output_dir, output_filename)
    resized.save(output_filepath)
    print("saved at location: {}".format(output_filepath))
    status_label.config(text="{} - Saved".format(filename))


def image_on_click(event):
    global x, y, output_dir
    if not output_dir:
        messagebox.showwarning(title="Warning", message="Output directory not set")
        return

    x, y = event.x, event.y
    # xy1.config(text='{}, {}'.format(x, y))
    print("mouse position in thumb: {}, {}".format(x, y))

    clicked_point_x = x * 12
    clicked_point_y = y * 12
    print("mouse position in original: {}, {}".format(clicked_point_x, clicked_point_y))

    # For generating an extra crop
    user_clicked_point = [clicked_point_x, clicked_point_y]
    center_point = [2112, 2816]
    slp = slope(user_clicked_point, center_point)
    r = 800
    new_point = spherical_to_cartesian(r, slp)
    generated_clicked_point = add_points(user_clicked_point, new_point)

    clicked_points = []
    clicked_points.append(user_clicked_point)
    clicked_points.append(generated_clicked_point)

    for i, point in enumerate(clicked_points):
        new_left, new_top, new_right, new_bottom = -1, -1, -1, -1
        clicked_point_x = point[0]
        clicked_point_y = point[1]

        left = clicked_point_x - 1920
        if left < 0:
            new_left = 0
        else:
            new_left = left

        right = clicked_point_x + 1920
        if right > 4224:
            new_right = 4224
        else:
            new_right = right

        top = clicked_point_y - 1080
        if top < 0:
            new_top = 0
        else:
            new_top = top

        bottom = clicked_point_y + 1080
        if bottom > 5632:
            new_bottom = 5632
        else:
            new_bottom = bottom

        if new_left == 0:
            new_right = right + abs(left)

        if new_top == 0:
            new_bottom = bottom + abs(top)

        if new_right == 4224:
            new_left = left - (right - 4224)

        if new_bottom == 5632:
            new_top = top - (bottom - 5632)

        assert new_right - new_left == 3840, "wrong calculation: new_left, new_right"
        assert new_bottom - new_top == 2160, "wrong calculation: new_top, new_bottom"

        print("actual box: {}, {}, {}, {}".format(left, top, right, bottom))
        print("modified box: {}, {}, {}, {}".format(new_left, new_top, new_right, new_bottom))

        crop_resize_save((new_left, new_top, new_right, new_bottom), i)

        print("-----")


def select_input_dir():
    global input_dir
    input_dir = filedialog.askdirectory()
    lbl_input_dir.config(text=input_dir)


def select_output_dir():
    global output_dir
    output_dir = filedialog.askdirectory()
    lbl_output_dir.config(text=output_dir)


def select():
    global img_paths, img_path, img, input_dir
    if not input_dir:
        messagebox.showwarning(title="Warning", message="Input directory not set")
        return

    if img_paths is None:
        img_paths = [os.path.join(input_dir, filename) for filename in os.listdir(input_dir) if filename.endswith('.jpg')]

    try:
        img_path = img_paths.pop()
    except IndexError:
        messagebox.showinfo(title="Done", message="All Done. Thanks.")
        return

    filename = os.path.basename(img_path)
    img = Image.open(img_path)
    width, height = img.size
    thumb_width = width / 12
    thumb_height = height / 12
    img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
    img1 = ImageTk.PhotoImage(img)
    canvas2.config(width=thumb_width, height=thumb_height, bd=0, highlightthickness=0)
    canvas2.create_image(0, 0, image=img1, anchor="nw")
    canvas2.image = img1
    canvas2.pack()
    status_label.config(text=filename)

# def select():
#     global img_path, img, input_dir
#     if not input_dir:
#         messagebox.showwarning(title="Warning", message="Input directory not set")
#         return
#
#     img_path = filedialog.askopenfilename(initialdir=input_dir)
#     filename = os.path.basename(img_path)
#     img = Image.open(img_path)
#     width, height = img.size
#     thumb_width = width / 12
#     thumb_height = height / 12
#     img.thumbnail((thumb_width, thumb_height), Image.Resampling.LANCZOS)
#     img1 = ImageTk.PhotoImage(img)
#     canvas2.config(width=thumb_width, height=thumb_height, bd=0, highlightthickness=0)
#     canvas2.create_image(0, 0, image=img1, anchor="nw")
#     canvas2.image = img1
#     canvas2.pack()
#     status_label.config(text=filename)


# create canvas to display image
canvas2 = Canvas(root, width="600", height="480", relief=RIDGE, bd=1)
canvas2.place(x=15, y=30)

# create label for showing status
status_label = Label(root, text="")
status_label.place(x=300, y=30)
status_label.configure(anchor="center")
status_label.pack()

btn_input_dir = Button(root, text="Set input directory", relief=RAISED, command=select_input_dir)
btn_input_dir.place(x=15, y=520)

lbl_input_dir = Label(root, text="")
lbl_input_dir.place(x=200, y=520)

btn_output_dir = Button(root, text="Set output directory", relief=RAISED, command=select_output_dir)
btn_output_dir.place(x=15, y=550)

lbl_output_dir = Label(root, text="")
lbl_output_dir.place(x=200, y=550)

# create buttons
btn1 = Button(root, text="Select Image", width=10, relief=RAISED, command=select)
btn1.place(x=15, y=595)
btn2 = Button(root, text="Exit", width=10, relief=RAISED, command=root.destroy)
btn2.place(x=155, y=595)

# Execute Tkinter
canvas2.bind("<Button 1>", image_on_click)
root.mainloop()
