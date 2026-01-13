import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance, ImageFilter


root = tk.Tk()
root.title("Neon Pink Photo Editor")
root.geometry("1200x720")
root.configure(bg="#0b0b0f")


original_image = None
edited_image = None
preview_image = None
tk_image = None


def upload_image():
    global original_image, edited_image
    path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.png *.jpeg")]
    )
    if path:
        original_image = Image.open(path).convert("RGB")
        edited_image = original_image.copy()
        reset_sliders()
        update_preview()

def save_image():
    if edited_image:
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png")]
        )
        if path:
            edited_image.save(path, quality=100, subsampling=0)

def reset_image():
    global edited_image
    if original_image:
        edited_image = original_image.copy()
        reset_sliders()
        update_preview()

def update_preview():
    global tk_image
    if edited_image is None:
        return

    img = edited_image.copy()
    img.thumbnail((560, 420))
    tk_image = ImageTk.PhotoImage(img)
    image_label.config(image=tk_image)


def apply_adjustments(value=None):
    global edited_image
    if original_image is None:
        return

    img = original_image.copy()
    img = ImageEnhance.Brightness(img).enhance(brightness.get())
    img = ImageEnhance.Contrast(img).enhance(contrast.get())
    img = ImageEnhance.Color(img).enhance(saturation.get())
    img = ImageEnhance.Sharpness(img).enhance(sharpness.get())

    edited_image = img
    update_preview()

def blur_image():
    global edited_image
    if edited_image:
        edited_image = edited_image.filter(ImageFilter.GaussianBlur(3))
        update_preview()

def rotate_image():
    global edited_image
    if edited_image:
        edited_image = edited_image.rotate(90, expand=True)
        update_preview()

def resize_image():
    global edited_image
    if edited_image:
        w, h = edited_image.size
        edited_image = edited_image.resize((int(w * 0.75), int(h * 0.75)))
        update_preview()

def rounded_button(parent, text, command, width=200, height=42):
    canvas = tk.Canvas(
        parent,
        width=width,
        height=height,
        bg="#0b0b0f",
        highlightthickness=0
    )

    radius = 20
    color = "#ff4da6"
    hover = "#ff79c6"

    rect = canvas.create_round_rect(
        2, 2, width-2, height-2,
        radius=radius,
        fill=color,
        outline=""
    )

    label = canvas.create_text(
        width/2,
        height/2,
        text=text,
        fill="black",
        font=("Segoe UI Semibold", 10)
    )

    def on_enter(e):
        canvas.itemconfig(rect, fill=hover)

    def on_leave(e):
        canvas.itemconfig(rect, fill=color)

    def on_click(e):
        command()

    canvas.bind("<Enter>", on_enter)
    canvas.bind("<Leave>", on_leave)
    canvas.bind("<Button-1>", on_click)

    return canvas


def _create_round_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1+radius, y1,
        x2-radius, y1,
        x2, y1,
        x2, y1+radius,
        x2, y2-radius,
        x2, y2,
        x2-radius, y2,
        x1+radius, y2,
        x1, y2,
        x1, y2-radius,
        x1, y1+radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)

tk.Canvas.create_round_rect = _create_round_rect


def create_slider(parent, text):
    tk.Label(
        parent,
        text=text.upper(),
        bg="#0b0b0f",
        fg="#ff79c6",
        font=("Segoe UI", 9, "bold")
    ).pack(anchor="w", pady=(14, 0))

    s = tk.Scale(
        parent,
        from_=0.2, to=2.0,
        resolution=0.1,
        orient="horizontal",
        length=240,
        bg="#0b0b0f",
        fg="white",
        troughcolor="#ff4da6",
        highlightthickness=0,
        command=apply_adjustments
    )
    s.set(1.0)
    s.pack()
    return s

def reset_sliders():
    brightness.set(1.0)
    contrast.set(1.0)
    saturation.set(1.0)
    sharpness.set(1.0)


sidebar = tk.Frame(root, bg="#0b0b0f", width=320)
sidebar.pack(side="left", fill="y", padx=18)

main_area = tk.Frame(root, bg="#111118")
main_area.pack(side="right", expand=True, fill="both")

# Title
tk.Label(
    sidebar,
    text="NEON EDITOR",
    bg="#0b0b0f",
    fg="#ff4da6",
    font=("Segoe UI Black", 18)
).pack(pady=18)

# Buttons
rounded_button(sidebar, "Upload Image", upload_image).pack(pady=6)
rounded_button(sidebar, "Download Image", save_image).pack(pady=6)
rounded_button(sidebar, "Reset Image", reset_image).pack(pady=10)

# Sliders
brightness = create_slider(sidebar, "Brightness")
contrast = create_slider(sidebar, "Contrast")
saturation = create_slider(sidebar, "Saturation")
sharpness = create_slider(sidebar, "Sharpness")

# Tools
tk.Label(
    sidebar,
    text="TOOLS",
    bg="#0b0b0f",
    fg="#ff4da6",
    font=("Segoe UI", 12, "bold")
).pack(pady=18)

rounded_button(sidebar, "Blur", blur_image).pack(pady=4)
rounded_button(sidebar, "Rotate 90°", rotate_image).pack(pady=4)
rounded_button(sidebar, "Resize", resize_image).pack(pady=4)

# Image
image_label = tk.Label(main_area, bg="#111118")
image_label.pack(expand=True)

root.mainloop()
