import customtkinter as ctk
import sys
from CTK_Alert.window_position import center_window, place_frame
from PIL import Image
import os

CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))
ICON_DIR = os.path.join(CURRENT_PATH, "icons")

ICON_PATH = {
    "close": (os.path.join(ICON_DIR, "close_black.png"), os.path.join(ICON_DIR, "close_white.png")),
    "images": list(os.path.join(ICON_DIR, f"image{i}.jpg") for i in range(1, 4)),
    "eye1": (os.path.join(ICON_DIR, "eye1_black.png"), os.path.join(ICON_DIR, "eye1_white.png")),
    "eye2": (os.path.join(ICON_DIR, "eye2_black.png"), os.path.join(ICON_DIR, "eye2_white.png")),
    "info": os.path.join(ICON_DIR, "info.png"),
    "warning": os.path.join(ICON_DIR, "warning.png"),
    "error": os.path.join(ICON_DIR, "error.png"),
    "left": os.path.join(ICON_DIR, "left.png"),
    "right": os.path.join(ICON_DIR, "right.png"),
    "warning2": os.path.join(ICON_DIR, "warning2.png"),
    "loader": os.path.join(ICON_DIR, "loader.gif"),
    "icon": os.path.join(ICON_DIR, "icon.png"),
    "arrow": os.path.join(ICON_DIR, "arrow.png"),
    "image": os.path.join(ICON_DIR, "image.png"),
}

DEFAULT_BTN = {
    "fg_color": "transparent",
    "hover": False,
    "compound": "left",
    "anchor": "w",
}

LINK_BTN = {**DEFAULT_BTN, "width": 70, "height": 25, "text_color": "#3574F0"}


class CTkAlert(ctk.CTkToplevel):
    def __init__(self, state: str = "info", title: str = "Информация",
                 body_text: str = "Body text", btn1: str = "OK",  height=200):
        super().__init__()
        self.old_y = None
        self.old_x = None
        self.width = 420
        self.height = height
        center_window(self, self.width, self.height)
        self.resizable(False, False)
        self.overrideredirect(True)
        self.grab_set()
        self.lift()

        self.x = self.winfo_x()
        self.y = self.winfo_y()
        self.event = None

        if sys.platform.startswith("win"):
            self.transparent_color = self._apply_appearance_mode(self.cget("fg_color"))
            self.attributes("-transparentcolor", self.transparent_color)

        self.bg_color = self._apply_appearance_mode(ctk.ThemeManager.theme["CTkFrame"]["fg_color"])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.frame_top = ctk.CTkFrame(self, corner_radius=5, width=self.width,
                                      border_width=1,
                                      bg_color=self.transparent_color, fg_color=self.bg_color)
        self.frame_top.grid(sticky="nsew")
        self.frame_top.bind("<B1-Motion>", self.move_window)
        self.frame_top.bind("<ButtonPress-1>", self.old_xy_set)
        self.frame_top.grid_columnconfigure(0, weight=1)
        self.frame_top.grid_rowconfigure(1, weight=1)

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (30, 30))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (30, 30))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.title_label = ctk.CTkLabel(self.frame_top, text=f"  {title}", font=("", 18), image=self.icon,
                                        compound="left")
        self.title_label.grid(row=0, column=0, sticky="w", padx=15, pady=20)
        self.title_label.bind("<B1-Motion>", self.move_window)
        self.title_label.bind("<ButtonPress-1>", self.old_xy_set)

        self.close_btn = ctk.CTkButton(self.frame_top, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.button_event)
        self.close_btn.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        self.message = ctk.CTkLabel(self.frame_top,
                                    text=body_text,
                                    justify="left", anchor="w", wraplength=self.width - 30)
        self.message.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="nsew", columnspan=2)

        self.btn_1 = ctk.CTkButton(self.frame_top, text=btn1, width=200, height=30, text_color="white",
                                   command=lambda: self.button_event(btn1))
        self.btn_1.grid(row=2, column=1, padx=20, pady=20, sticky="e")

        # self.btn_2 = ctk.CTkButton(self.frame_top, text=btn2, width=120, fg_color="transparent", border_width=1,
        #                            command=lambda: self.button_event(btn2), text_color=("black", "white"))
        # self.btn_2.grid(row=2, column=1, padx=(5, 10), pady=20, sticky="e")

        self.bind("<Escape>", lambda e: self.button_event())

    def get(self):
        if self.winfo_exists():
            self.master.wait_window(self)
        return self.event

    def old_xy_set(self, event):
        self.old_x = event.x
        self.old_y = event.y

    def move_window(self, event):
        self.y = event.y_root - self.old_y
        self.x = event.x_root - self.old_x
        self.geometry(f'+{self.x}+{self.y}')

    def button_event(self, event=None):
        self.grab_release()
        self.destroy()
        self.event = event


class CTkBanner(ctk.CTkFrame):
    def __init__(self, master, state: str = "info", title: str = "Title", btn1: str = "Action A",
                 btn2: str = "Action B", side: str = "right_bottom"):
        self.root = master
        self.width = 400
        self.height = 100
        super().__init__(self.root, width=self.width, height=self.height, corner_radius=5, border_width=1)

        self.grid_propagate(False)
        self.grid_columnconfigure(1, weight=1)
        self.event = None
        self.grab_set()

        self.horizontal, self.vertical = side.split("_")

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (24, 24))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (24, 24))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.title_label = ctk.CTkLabel(self, text=f"  {title}", font=("", 16), image=self.icon,
                                        compound="left")
        self.title_label.grid(row=0, column=0, sticky="w", padx=15, pady=10)

        self.close_btn = ctk.CTkButton(self, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.button_event)
        self.close_btn.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

        self.btn_1 = ctk.CTkButton(self, text=btn1, **LINK_BTN, command=lambda: self.button_event(btn1))
        self.btn_1.grid(row=1, column=0, padx=(40, 5), pady=10, sticky="w")

        self.btn_2 = ctk.CTkButton(self, text=btn2, **LINK_BTN,
                                   command=lambda: self.button_event(btn2))
        self.btn_2.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        place_frame(self.root, self, self.horizontal, self.vertical)
        self.root.bind("<Configure>", self.update_position, add="+")

    def update_position(self, event):
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.update_idletasks()
        self.root.update_idletasks()

    def get(self):
        if self.winfo_exists():
            self.master.wait_window(self)
        return self.event

    def button_event(self, event=None):
        self.root.unbind("<Configure>")
        self.grab_release()
        self.destroy()
        self.event = event


class CTkNotification(ctk.CTkFrame):
    def __init__(self, master, state: str = "info", message: str = "message", side: str = "right_bottom"):
        self.root = master
        self.width = 400
        self.height = 60
        super().__init__(self.root, width=self.width, height=self.height, corner_radius=5, border_width=1)
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grab_set()

        self.horizontal, self.vertical = side.split("_")

        if state not in ICON_PATH or ICON_PATH[state] is None:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH["info"]), Image.open(ICON_PATH["info"]), (24, 24))
        else:
            self.icon = ctk.CTkImage(Image.open(ICON_PATH[state]), Image.open(ICON_PATH[state]), (24, 24))

        self.close_icon = ctk.CTkImage(Image.open(ICON_PATH["close"][0]), Image.open(ICON_PATH["close"][1]), (20, 20))

        self.message_label = ctk.CTkLabel(self, text=f"  {message}", font=("", 13), image=self.icon, compound="left")
        self.message_label.grid(row=0, column=0, sticky="nsw", padx=15, pady=10)

        self.close_btn = ctk.CTkButton(self, text="", image=self.close_icon, width=20, height=20, hover=False,
                                       fg_color="transparent", command=self.close_notification)
        self.close_btn.grid(row=0, column=1, sticky="nse", padx=10, pady=10)

        place_frame(self.root, self, self.horizontal, self.vertical)
        self.root.bind("<Configure>", self.update_position, add="+")

    def update_position(self, event):
        place_frame(self.root, self, self.horizontal, self.vertical)
        self.update_idletasks()
        self.root.update_idletasks()

    def close_notification(self):
        self.root.unbind("<Configure>")
        self.destroy()
