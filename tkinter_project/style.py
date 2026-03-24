# styles.py
from tkinter import ttk

BG = "#16161D"
BLUE = "#00D4FF"
RED = "#FF1744"
ORANGE = "#FF7034"
GRAY = "#7B7B7B"
FRAME_BORDER = "#2A2A38"

def apply_styles(style: ttk.Style):
    style.theme_use("clam")

    style.configure("TLabelframe", background=BG, foreground="#16161D", bordercolor="#000000",
                    lightcolor=FRAME_BORDER, darkcolor=FRAME_BORDER)
    style.configure("TLabelframe.Label", background=BG, foreground=BLUE)

    style.configure("TCombobox",
        foreground="white",
        arrowcolor=BLUE,
        bordercolor=FRAME_BORDER,
        lightcolor=FRAME_BORDER,
        darkcolor="black",
    )
    style.map("TCombobox",
        fieldbackground=[("readonly", BG), ("disabled", BG), ("active", BG), ("!disabled", BG)],
        foreground=[("readonly", "white"), ("disabled", "white"), ("active", "white"), ("!disabled", "white")],
        background=[("readonly", FRAME_BORDER), ("active", FRAME_BORDER), ("!disabled", FRAME_BORDER)],
        selectbackground=[("readonly", BG)],
        selectforeground=[("readonly", "white")],
    )

    style.configure("Treeview",
        background=BG, foreground=BLUE, fieldbackground=BG,
        bordercolor=FRAME_BORDER, rowheight=25, relief="flat",
        lightcolor=FRAME_BORDER, darkcolor=FRAME_BORDER,
        font= ("Arial", 11, "bold")
    )
    style.configure("Treeview.Heading",
        background=FRAME_BORDER, foreground=BLUE, relief="flat",
        font= ("Arial", 11, "bold")
    )
    style.map("Treeview",
        background=[("selected", "!focus", FRAME_BORDER), ("selected", FRAME_BORDER)],
        foreground=[("selected", "!focus", BLUE), ("selected", BLUE)]
    )

    style.configure("Vertical.TScrollbar",
        background=FRAME_BORDER, troughcolor=BG, bordercolor=BG,
        arrowcolor=BLUE, darkcolor=FRAME_BORDER, lightcolor=FRAME_BORDER, arrowsize=0
    )
    style.map("Vertical.TScrollbar",
        background=[("active", BLUE), ("!active", GRAY)],
    )

    style.configure("TNotebook", background=BG, bordercolor=BG, lightcolor=BG, darkcolor=BG,
                    tabmargins=[0, 0, 0, 0], borderwidth=0)
    style.configure("TNotebook.Tab", background=FRAME_BORDER, foreground=GRAY, lightcolor=FRAME_BORDER, darkcolor=FRAME_BORDER,
                    padding=[10, 4], borderwidth=0, focusthickness=0, focuscolor=BG)
    style.map("TNotebook.Tab",
        background=[("selected", BG)],
        foreground=[("selected", BLUE)],
        lightcolor=[("selected", BG), ("!selected", FRAME_BORDER)],
        darkcolor=[("selected", BG), ("!selected", FRAME_BORDER)],
        bordercolor=[("selected", BG), ("!selected", FRAME_BORDER)]
    )
    style.layout("TNotebook", [("TNotebook.client", {"sticky": "nswe"})])
    style.configure("TNotebook.client", background=BG, bordercolor=BG,
                    lightcolor=BG, darkcolor=BG, borderwidth=0)