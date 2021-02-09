import os
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw

root = Tk()
root.title('Label coordinate')
root.geometry('500x300')

# Define dataset path and labels here
label_folder = './data/training/cursor/seq_01/'

target_labels = {
    'cai': 0,
    'tro': 1,
    'giua': 2,
    'nhan': 3,
    'ut': 4
}

label_colors = {
    '0': 'red',
    '1': 'blue',
    '2': 'green',
    '3': 'yellow',
    '4': 'black'
}

image_index = 0

def load_image(image_file):
    global load, image_lbl
    load = Image.open(label_folder + image_file)

    with open(target_folder + current_image.split('.')[0] + '.txt', 'r') as label_file:
        r = label_file.read()
        r = r.strip().split(' ')
        i = 0
        for v in check_vars:
            v.delete(1.0, END)
            v.insert(1.0, '{} {}'.format(str(r[0+i*2]), str(r[1+i*2])))

            if str(r[0+i*2]) == '-1' or str(r[1+i*2]) == -1:
                render = ImageTk.PhotoImage(load)
                image_lbl.configure(image=render)
                image_lbl.image = render
            else:
                create_circle(x=int(r[0+i*2]), y=int(r[1+i*2]), color=label_colors[str(i)])

            i +=1

    return load.size

def render_image_holder(parent):
    global current_image, image_lbl
    image_frame = Frame(parent)
    image_frame.grid(row=0, column=0)

    image_lbl = Label(image_frame)
    image_lbl.pack()
    load_image(current_image)

    img_name_lbl = Label(image_frame)
    img_name_lbl.pack()
    img_shape = Label(image_frame)
    img_shape.pack()
    progress_lbl = Label(image_frame)
    progress_lbl.pack()
    
    return image_lbl, img_name_lbl, progress_lbl, img_shape

def render_label_box(parent):
    label_box_frame = Frame(parent)
    label_box_frame.grid(row=0, column=1)
    
    text_frame = Frame(label_box_frame)
    text_frame.pack(pady=20)

    vars = []
    for label in target_labels.keys():
        lbl = Label(text_frame, height=2, text=label)
        var = Text(text_frame, height=2, width=20)
        lbl.grid(row=target_labels[label], column=0)
        var.grid(row=target_labels[label], column=1)
        var.delete(1.0, END)
        var.insert(1.0, '-1 -1')
        vars.append(var)

    return vars

def next_image():
    global image_index, images, current_image, image_lbl
    global img_name_lbl, progress_lbl, img_shape
    if image_index < len(images):
        with open(target_folder + current_image.split('.')[0] + '.txt', 'w') as label_file:
            for v in check_vars:
                s = v.get(1.0, END).strip().split(' ')
                label_file.write('{} {}'.format(str(s[0]), str(s[1])))
                label_file.write(' ')

        image_index += 1
        current_image = images[image_index]
        s = load_image(current_image)
        img_shape.configure(text='shape: {}'.format(s))
        
    else:
        image_index -= 1

    img_name_lbl.configure(text=current_image)
    progress_lbl.configure(text='{} of {}'.format(image_index, len(images)))

def prev_image():
    global image_index, images, current_image, image_lbl
    global img_name_lbl, progress_lbl, img_shape
    image_index -= 1
    if image_index > -1:
        current_image = images[image_index]
        s = load_image(current_image)
        img_shape.configure(text='shape: {}'.format(s))
    else:
        image_index += 1

    img_name_lbl.configure(text=current_image)
    progress_lbl.configure(text='{} of {}'.format(image_index, len(images)))
    
def create_circle(x, y, color, r=3): #center coordinates, radius
    x0 = x - r
    y0 = y - r
    x1 = x + r
    y1 = y + r
    print("draw")
    draw = ImageDraw.Draw(load)
    draw.ellipse([(x0, y0), (x1, y1)], fill=color)
    render = ImageTk.PhotoImage(load)
    image_lbl.configure(image=render)
    image_lbl.image = render
    # return draw.ellipse((x0, y0, x1, y1), fill='red', width=2)

def printcoords(event, color):
    #outputting x and y coords to console
    x, y = event.x, event.y
    create_circle(int(x), int(y), color)
    return (x, y)

def key_stroke(event):
    # while True:
    c = event.char
    if c == 'a':
        prev_image()
        # break
    elif c == 'd':
        next_image()
        # break
    else:
        print(c)
        if c == '1':
            check_vars[0].delete(1.0, END)
            check_vars[0].insert(1.0, printcoords(event, 'red'))
        elif c == '2':
            check_vars[1].delete(1.0, END)
            check_vars[1].insert(1.0, printcoords(event, 'blue'))
        elif c == '3':
            check_vars[2].delete(1.0, END)
            check_vars[2].insert(1.0, printcoords(event, 'green'))
        elif c == '4':
            check_vars[3].delete(1.0, END)
            check_vars[3].insert(1.0, printcoords(event, 'yellow'))
        elif c == '5':
            check_vars[4].delete(1.0, END)
            check_vars[4].insert(1.0, printcoords(event, 'black'))

# get all images that need to be labeled
images = []
for image in os.listdir(label_folder):
    if any([f in image for f in ['.jpg', '.png']]):
        images.append(image)
print('Got a total of {} images'.format(len(images)))

# get labels
labels = {}
target_folder = label_folder + 'labels/'
if os.path.exists(target_folder):
    for label in os.listdir(target_folder):
        with open(target_folder + label, 'r') as label_file:
            labels[label.split('.')[0]] = label_file.read()
else:
    print('Creating label folder')
    os.mkdir(target_folder)
    for image in images:
        with open(target_folder + image[:-3]+'txt', 'w+') as f:
            f.write('-1 -1 -1 -1 -1 -1 -1 -1 -1 -1')
            f.close()

current_image = images[image_index]
image_lbl = None
load = None
check_vars = render_label_box(root)
image_lbl, img_name_lbl, progress_lbl, img_shape = render_image_holder(root)
root.bind('<Key>', key_stroke)

root.mainloop()