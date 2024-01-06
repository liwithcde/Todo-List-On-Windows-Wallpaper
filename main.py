# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import ctypes
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

# 文件路径
todo_file = 'todos.txt'
SPI_SETDESKWALLPAPER = 20

SPI_GETDESKWALLPAPER = 0x0073
MAX_PATH = 260
FONT_PATH="yhBold.ttf"

def load_todos():
    try:
        with open(todo_file, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError:
        return []

def save_todos(todos):
    with open(todo_file, 'w', encoding='utf-8') as file:
        file.writelines(todos)

def update_todos():
    todos = txt_todos.get("1.0", "end-1c").split('\n')
    save_todos([todo + '\n' for todo in todos if todo.strip()])  # 移除空行

    new_wallpaper = add_todo_list_with_box(current_wallpaper, todos)
    change_wallpaper(new_wallpaper)

def get_wallpaper():
    path = ctypes.create_unicode_buffer(MAX_PATH)
    ctypes.windll.user32.SystemParametersInfoW(SPI_GETDESKWALLPAPER, MAX_PATH, path, 0)
    return path.value

def change_wallpaper(image_path):
    ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, 3)

def get_screen_resolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    width, height = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)
    return width, height

def get_text_width(text, font_size):
    font = ImageFont.truetype(FONT_PATH, font_size)
    return font.getsize(text)[0]
def add_todo_list_with_box(image_path, todos):
    img = Image.open(image_path)
    width, height = img.size
    print(width,height)
    # 动态调整字体大小
    font_size = max(width // 50, 12)
    font = ImageFont.truetype(FONT_PATH, font_size)
    # 准备绘制
    draw = ImageDraw.Draw(img)
    line_height = font_size + 5
    box_height = line_height * len(todos) + 20
    box_width = max([get_text_width(s,font_size) for s in todos])  # 或者根据需要调整宽度

    # 确定矩形框位置
    box_x = width*4/5 - box_width
    box_y =height*1/5

    # 绘制白色矩形框
    draw.rectangle([box_x, box_y, box_x + box_width, box_y + box_height], fill="white")

    # 在矩形框内添加文字
    text_x, text_y = box_x + 10, box_y + 10
    for todo in todos:
        draw.text((text_x, text_y), todo, fill="black", font=font)
        text_y += line_height

    new_image_path = r"wall-sticker.jpg"
    img.save(new_image_path)
    return new_image_path

current_wallpaper = get_wallpaper()

root = tk.Tk()
root.title("Todo List")

txt_todos = tk.Text(root, height=10, width=50)
txt_todos.pack()

# 填充初始todos
initial_todos = load_todos()
txt_todos.insert(tk.END, ''.join(initial_todos))

# 创建保存按钮
btn_save = tk.Button(root, text="Save", command=update_todos)
btn_save.pack()

# 运行事件循环
root.mainloop()


