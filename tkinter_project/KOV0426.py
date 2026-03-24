from tkinter import *
from tkinter import ttk
import time
from datetime import datetime
from style import apply_styles, BG, BLUE, ORANGE, GRAY, FRAME_BORDER, RED

class myApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Speedcubing Timer")
        self.root.geometry("1050x780")
        self.root.minsize(860,750)
        self.delete_confirmed = False

        menubar = Menu(root, bg=BG, fg=GRAY, activebackground=FRAME_BORDER, activeforeground=BLUE,
               borderwidth=0)
        filemenu = Menu(menubar, tearoff=0, bg=BG, fg=GRAY, activebackground=FRAME_BORDER, activeforeground=BLUE,
               borderwidth=0)
        filemenu.add_command(label="Info", command=self.new_win)
        filemenu.add_command(label="Přidat pokus", command=self.add_time_window)
        filemenu.add_command(label="Konec", command=root.quit)
        menubar.add_cascade(label="Menu", menu=filemenu)
        root.config(menu=menubar)
        
        self.selected_cube = StringVar(value="3x3")

        # STYLE
        style = ttk.Style()
        apply_styles(style)

        # SCRAMBLE
        self.scramble_frame = ttk.LabelFrame(root, text="SCRAMBLE")
        self.scramble_frame.pack(fill="x")

        self.top_info_frame = Frame(self.scramble_frame, bg=BG)
        self.top_info_frame.pack(fill="x")

        self.cube_label = Label(self.top_info_frame, text="3x3", bg=BLUE, fg="black", padx=5)
        self.cube_label.pack(side="left", padx=10, pady=(5, 0))

        self.new_scramble_label = Label(self.top_info_frame, text="Nový scramble", bg=BG, fg=GRAY, padx=5)
        self.new_scramble_label.pack(anchor="e", padx=10, pady=(5, 0))

        self.scramble_label = Label(self.scramble_frame, text="B L2 R B L2 D2 U' R2 F2 L2 D2 L2 B L D2 U B L F' L'", bg=BG, fg="white", font=("Arial", 20, "bold"))
        self.scramble_label.pack(pady=5, fill="x")

        # TIMER
        self.timer_frame = ttk.LabelFrame(root, text="TIMER")
        self.timer_frame.pack(fill="x")

        self.hint_label = Label(self.timer_frame, text="Drž MEZERNÍK pro start", bg=BG, fg=GRAY)
        self.hint_label.pack()

        self.timer_label = Label(self.timer_frame, text="0.000", bg=BG, fg="white", font=("Arial", 64, "bold"))
        self.timer_label.pack()

        self.timer_running = False
        self.timer_start = None
        self.timer_id = None
        self.just_stopped = False

        root.bind("<KeyPress-space>", self.on_space_press)
        root.bind("<KeyRelease-space>", self.on_space_release)

        self.cubes = ["2x2", "3x3", "4x4", "5x5", "6x6", "7x7", "Pyraminx", "Skewb"]
        self.buttons = {}

        self.btn_frame = Frame(self.timer_frame, bg=BG)
        self.btn_frame.pack()

        self.label2 = Label(self.btn_frame, text="Typ kostky:", bg=BG, fg=GRAY)
        self.label2.pack(side="left", padx=5)

        for cube in self.cubes:
            btn = Button(self.btn_frame, text=cube, borderwidth=0, highlightthickness=0,
                          command=lambda c=cube: self.select_cube(c))
            btn.pack(side="left", ipadx=5, padx=5, pady=3)
            self.buttons[cube] = btn

        # FILTER
        self.filter_frame = ttk.LabelFrame(root, text="FILTER", padding=10)
        self.filter_frame.pack(fill="x")

        self.sort_label = Label(self.filter_frame, text="Řadit: ", bg=BG, fg=GRAY)
        self.sort_label.grid(row=0, column=0, padx=(20,0))

        self.sort_type = StringVar(value="Nejnovější")
        sortfilter = ttk.Combobox(self.filter_frame, width=27, textvariable=self.sort_type, state="readonly")
        sortfilter['values'] = ('Nejnovější', 'Nejstarší', 'Nejrychlejší', 'Nejpomalejší')
        sortfilter.grid(row=0, column=1)

        self.penalty_label = Label(self.filter_frame, text="Penalizace: ", bg=BG, fg=GRAY)
        self.penalty_label.grid(row=0, column=2, padx=(20,0))

        self.penalty = StringVar(value="Vše")
        penaltyfilter = ttk.Combobox(self.filter_frame, width=27, textvariable=self.penalty, state="readonly")
        penaltyfilter['values'] = ('Vše', 'DNF', '+2s')
        penaltyfilter.grid(row=0, column=3)

        self.reset_filter_btn = Button(self.filter_frame, text="Zrušit filtry", bg=BG, fg=GRAY,
                                       font=("Arial", 10, "bold"), borderwidth=0, highlightthickness=0)
        self.reset_filter_btn.grid(row=0, column=4, padx=(30,20))

        # STATS
        self.stats_frame = ttk.LabelFrame(root, text="STATS")
        self.stats_frame.pack(fill="x", side="bottom")

        for i in range(5):
            self.stats_frame.columnconfigure(i, weight=1)

        Label(self.stats_frame, text="PB", bg=BG, fg=GRAY, font=("Arial", 12, "bold")).grid(row=0, column=0, sticky="n", pady=(0, 5))
        self.pb_label = Label(self.stats_frame, text="-", bg=BG, fg=ORANGE, font=("Arial", 28, "bold"))
        self.pb_label.grid(row=1, column=0, sticky="n")

        Label(self.stats_frame, text="AVG", bg=BG, fg=GRAY, font=("Arial", 12, "bold")).grid(row=0, column=1, sticky="n", pady=(0, 5))
        self.avg_label = Label(self.stats_frame, text="-", bg=BG, fg=ORANGE, font=("Arial", 28, "bold"))
        self.avg_label.grid(row=1, column=1, sticky="n")

        Label(self.stats_frame, text="Ao5", bg=BG, fg=GRAY, font=("Arial", 12, "bold")).grid(row=0, column=2, sticky="n", pady=(0, 5))
        self.ao5_label = Label(self.stats_frame, text="-", bg=BG, fg=ORANGE, font=("Arial", 28, "bold"))
        self.ao5_label.grid(row=1, column=2, sticky="n")

        Label(self.stats_frame, text="Ao12", bg=BG, fg=GRAY, font=("Arial", 12, "bold")).grid(row=0, column=3, sticky="n", pady=(0, 5))
        self.ao12_label = Label(self.stats_frame, text="-", bg=BG, fg=ORANGE, font=("Arial", 28, "bold"))
        self.ao12_label.grid(row=1, column=3, sticky="n")

        Label(self.stats_frame, text="POČET", bg=BG, fg=GRAY, font=("Arial", 12, "bold")).grid(row=0, column=4, sticky="n", pady=(0, 5))
        self.count_label = Label(self.stats_frame, text="-", bg=BG, fg=ORANGE, font=("Arial", 28, "bold"))
        self.count_label.grid(row=1, column=4, sticky="n")

        # MIDDLE FRAME
        self.frame = Frame(root)
        self.frame.pack(fill="both", expand=True)

        # TABLE
        self.table_frame = ttk.LabelFrame(self.frame, text="TABLE")
        self.table_frame.pack(side="left", fill="both", expand=True)

        self.table_frame.columnconfigure(0, weight=1)
        self.table_frame.rowconfigure(0, weight=1)

        self.table = ttk.Treeview(self.table_frame, columns=("date","cube","time","penalty","scramble"), show="headings")
        self.table.heading("date", text="Datum")
        self.table.heading("cube", text="Kostka")
        self.table.heading("time", text="Čas")
        self.table.heading("penalty", text="Penalizace")

        self.table.column("date", width=100, anchor="center")
        self.table.column("cube", width=80, anchor="center")
        self.table.column("time", width=80, anchor="center")
        self.table.column("penalty", width=80, anchor="center")
        self.table.column("scramble", width=0, stretch=False)

        self.table.bind("<<TreeviewSelect>>", self.on_row_select)

        self.table.grid(row=0, column=0, sticky=NSEW, padx=(10,0))

        self.scrollbar = ttk.Scrollbar(self.table_frame, orient=VERTICAL, command=self.table.yview)
        self.table.configure(yscroll=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky=NS)

        self.table.insert("", "end", values=("2024-01-05", "3x3", "36.295", "", "B L2 R B L2 D2 U' R2 F2 L2 D2 L2 B L D2 U B L F' L'"))
        self.table.insert("", "end", values=("2024-02-15", "3x3", "23.215", "", "R' U' F D2 L2 F R2 U2 R2 B D2 L B2 D' F2 R U' F' R'"))
        self.table.insert("", "end", values=("2024-03-25", "3x3", "40.245", "", "F U2 L2 B2 F' U2 R2 B2 D2 R2 U2 R' F' D L' U' B R2 F2"))
        self.table.insert("", "end", values=("2024-01-07", "3x3", "78.595", "", "D2 R' F2 L F2 R B2 L' U2 L2 D2 B' U' R F' D R2 U B2"))

        # DETAIL
        self.detail_frame = ttk.LabelFrame(self.frame, text="DETAIL POKUSU")
        self.detail_frame.pack(side="right", fill="both", expand=False)
        self.detail_frame.pack_propagate(False)
        self.detail_frame.config(width=300)

        self.detail_tabs = ttk.Notebook(self.detail_frame)
        self.detail_tabs.pack(fill="both", expand=True)

        self.info_tab = Frame(self.detail_tabs, bg=BG)
        self.edit_tab = Frame(self.detail_tabs, bg=BG)

        self.detail_tabs.add(self.info_tab, text="Info")
        self.detail_tabs.add(self.edit_tab, text="Upravit")

        # INFO
        self.detail_top = Frame(self.info_tab, bg=BG)
        self.detail_top.pack(fill="x", padx=10, pady=(10, 0))

        self.detail_header_row = Frame(self.detail_top, bg=BG)
        self.detail_header_row.pack(fill="x")

        self.detail_time_label = Label(self.detail_header_row, text="ČAS POKUSU", bg=BG, fg=GRAY, font=("Arial", 9, "bold"))
        self.detail_time_label.pack(side="left")

        self.detail_cube_label = Label(self.detail_header_row, text="TYP KOSTKY", bg=BG, fg=GRAY, font=("Arial", 9, "bold"))
        self.detail_cube_label.pack(side="right")

        self.detail_time_row = Frame(self.detail_top, bg=BG)
        self.detail_time_row.pack(fill="x")

        self.detail_time = Label(self.detail_time_row, text="", bg=BG, fg="white", font=("Arial", 28, "bold"))
        self.detail_time.pack(side="left")

        self.detail_cube = Label(self.detail_time_row, text="", bg=BG, fg=BLUE, font=("Arial", 19, "bold"))
        self.detail_cube.pack(side="right")

        self.detail_scramble_label = Label(self.info_tab, text="SCRAMBLE", bg=BG, fg=GRAY, font=("Arial", 9, "bold"))
        self.detail_scramble_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.detail_scramble = Label(self.info_tab, text="", bg=FRAME_BORDER, fg="white",
                                      font=("Arial", 10, "bold"), wraplength=250, justify="left", padx=8, pady=6)
        self.detail_scramble.pack(fill="x", padx=10, pady=(2, 0))

        self.detail_penalty_label = Label(self.info_tab, text="PENALIZACE", bg=BG, fg=GRAY, font=("Arial", 9, "bold"))
        self.detail_penalty_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.detail_penalty = Label(self.info_tab, text="", bg=FRAME_BORDER, fg="white",
                                      font=("Arial", 10, "bold"), padx=8, pady=6)
        self.detail_penalty.pack(fill="x", padx=10, pady=(2, 0))

        # EDIT
        self.detail_change_row = Frame(self.edit_tab, bg=BG)
        self.detail_change_row.pack(fill="x", padx=10, pady=(10, 0))

        self.detail_change_label = Label(self.detail_change_row, text="Změnit typ:", bg=BG, fg=GRAY, font=("Arial", 9))
        self.detail_change_label.pack(anchor="w", pady=(0, 4))

        self.change_cube_type = StringVar()
        self.change_cube_combobox = ttk.Combobox(self.detail_change_row, textvariable=self.change_cube_type,
                                                  values=self.cubes, state="readonly", width=20)
        self.change_cube_combobox.pack(anchor="w")

        self.detail_penalty_label = Label(self.edit_tab, text="PENALIZACE", bg=BG, fg=GRAY, font=("Arial", 9, "bold"))
        self.detail_penalty_label.pack(anchor="w", padx=10, pady=(10, 0))

        self.penalty_frame = Frame(self.edit_tab, bg=BG)
        self.penalty_frame.pack(anchor="w", padx=10)

        self.solve_penalty = StringVar(value="none")

        self.dnf_radio = Radiobutton(self.penalty_frame, text="DNF", variable=self.solve_penalty, value="DNF",
                                bg=BG, fg="white", selectcolor=BG,
                                activebackground=BG, activeforeground="white",
                                indicatoron=True, borderwidth=0, highlightthickness=0)
        self.dnf_radio.pack(anchor="w")

        self.plus2_radio = Radiobutton(self.penalty_frame, text="+2s", variable=self.solve_penalty, value="+2s",
                                bg=BG, fg="white", selectcolor=BG,
                                activebackground=BG, activeforeground="white",
                                indicatoron=True, borderwidth=0, highlightthickness=0)
        self.plus2_radio.pack(anchor="w")

        self.none_radio = Radiobutton(self.penalty_frame, text="Žádná", variable=self.solve_penalty, value="none",
                                bg=BG, fg="white", selectcolor=BG,
                                activebackground=BG, activeforeground="white",
                                borderwidth=0, highlightthickness=0)
        self.none_radio.pack(anchor="w")

        self.detail_btn_frame = Frame(self.edit_tab, bg=BG)
        self.detail_btn_frame.pack(fill="x", side="bottom", pady=10, padx=10)

        self.save_btn = Button(self.detail_btn_frame, text="ULOŽIT", bg=BLUE, fg="black",
                                font=("Arial", 12, "bold"), borderwidth=0, highlightthickness=0,
                                activebackground=BLUE, activeforeground="black",
                                padx=10, pady=8, command=self.on_save_click)
        self.save_btn.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.delete_btn = Button(self.detail_btn_frame, text="SMAZAT", bg=RED, fg="white",
                                  font=("Arial", 12, "bold"), borderwidth=0, highlightthickness=0,
                                  activebackground=RED, activeforeground="white",
                                  padx=10, pady=8, command=self.on_delete_click)
        self.delete_btn.pack(side="right", fill="x", expand=True, padx=(5, 0))

        self.select_cube("3x3")
        self.update_stats()

    def new_win(self):
        win = Toplevel()
        win.grab_set()
        win.focus_set()
        win.title("Info")
        win.config(bg=BG)
        win.geometry("300x200")
        win.resizable(False, False)

        Label(win, text="INFO", bg=BG, fg=BLUE, font=("Arial", 14, "bold")).pack(pady=(20, 10))
        Label(win, text="Speedcubing Timer", bg=BG, fg="white", font=("Arial", 11, "bold")).pack()
        Label(win, text="KOV0426", bg=BG, fg=GRAY, font=("Arial", 9)).pack(pady=(5, 0))

        Button(win, text="ZAVŘÍT", bg=FRAME_BORDER, fg="white",
               font=("Arial", 11, "bold"), borderwidth=0, highlightthickness=0,
               activebackground=BLUE, activeforeground="black",
               padx=10, pady=6, command=win.destroy).pack(pady=20)

    def select_cube(self, cube):
        self.selected_cube.set(cube)
        for name, btn in self.buttons.items():
            if name == cube:
                btn.config(bg=BLUE, fg="black", activebackground=BLUE, activeforeground="black")
            else:
                btn.config(bg="#1E1E1E", fg=GRAY, activebackground=BG, activeforeground=GRAY)
        self.cube_label.config(text=cube)

    def on_row_select(self, event):
        selected = self.table.focus()
        if not selected:
            return
        values = self.table.item(selected, "values")
        if values:
            self.detail_time.config(text=values[2])
            self.detail_cube.config(text=values[1])
            self.change_cube_type.set(values[1])
            self.solve_penalty.set(values[3] if values[3] else "none")
            self.detail_scramble.config(text=values[4])
            self.detail_penalty.config(text=values[3] if values[3] else "Žádná")

    def on_delete_click(self):
        if not self.delete_confirmed:
            self.delete_confirmed = True
            self.delete_btn.config(text="OPRAVDU?", bg=ORANGE)
            self.root.after(3000, self.reset_delete_btn)
        else:
            selected = self.table.focus()
            if selected:
                self.table.delete(selected)
            self.detail_time.config(text="")
            self.detail_cube.config(text="")
            self.detail_scramble.config(text="")
            self.detail_penalty.config(text="")
            self.reset_delete_btn()
        self.update_stats()

    def reset_delete_btn(self):
        self.delete_confirmed = False
        self.delete_btn.config(text="SMAZAT", bg=RED)

    def on_save_click(self):
        selected = self.table.focus()
        if not selected:
            return
        values = self.table.item(selected, "values")
        if not values:
            return

        penalty = self.solve_penalty.get()
        if penalty == "none":
            penalty = ""
        new_cube = self.change_cube_type.get()

        self.table.item(selected, values=(values[0], new_cube, values[2], penalty, values[4]))
        self.detail_penalty.config(text=penalty if penalty else "Žádná")
        self.detail_cube.config(text=new_cube)
        self.update_stats()

    def update_stats(self):
        times = []
        for row in self.table.get_children():
            values = self.table.item(row, "values")
            penalty = values[3]
            time_str = values[2]

            if penalty == "DNF":
                continue

            try:
                t = float(time_str)
                if penalty == "+2s":
                    t += 2
                times.append(t)
            except ValueError:
                continue

        count = len(self.table.get_children())
        pb = f"{min(times):.3f}" if times else "-"
        avg = f"{sum(times) / len(times):.3f}" if times else "-"

        ao5 = "-"
        if len(times) >= 5:
            last5 = times[-5:]
            ao5 = f"{(sum(last5) - min(last5) - max(last5)) / 3:.3f}"

        ao12 = "-"
        if len(times) >= 12:
            last12 = times[-12:]
            ao12 = f"{(sum(last12) - min(last12) - max(last12)) / 10:.3f}"

        self.pb_label.config(text=pb)
        self.avg_label.config(text=avg)
        self.ao5_label.config(text=ao5)
        self.ao12_label.config(text=ao12)
        self.count_label.config(text=str(count))

    def add_time_window(self):
        win = Toplevel()
        win.grab_set()
        win.focus_set()
        win.title("Přidat pokus")
        win.config(bg=BG)
        win.geometry("400x350")
        win.resizable(False, False)
        Label(win, text="PŘIDAT POKUS", bg=BG, fg=BLUE, font=("Arial", 14, "bold")).pack(pady=(15, 10))
        form = Frame(win, bg=BG)
        form.pack(fill="x", padx=20)

        Label(form, text="Čas (např. 36.295):", bg=BG, fg=GRAY, font=("Arial", 9, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        time_var = StringVar()
        Entry(form, textvariable=time_var, bg=FRAME_BORDER, fg="white", insertbackground="white",
              borderwidth=0, font=("Arial", 11)).grid(row=0, column=1, padx=(10,0), sticky="ew")

        Label(form, text="Datum:", bg=BG, fg=GRAY, font=("Arial", 9, "bold")).grid(row=1, column=0, sticky="w", pady=5)
        from datetime import datetime
        date_var = StringVar(value=datetime.now().strftime("%Y-%m-%d"))
        Entry(form, textvariable=date_var, bg=FRAME_BORDER, fg="white", insertbackground="white",
              borderwidth=0, font=("Arial", 11)).grid(row=1, column=1, padx=(10,0), sticky="ew")

        Label(form, text="Typ kostky:", bg=BG, fg=GRAY, font=("Arial", 9, "bold")).grid(row=2, column=0, sticky="w", pady=5)
        cube_var = StringVar(value=self.selected_cube.get())
        cube_combo = ttk.Combobox(form, textvariable=cube_var, values=self.cubes, state="readonly", width=18)
        cube_combo.grid(row=2, column=1, padx=(10,0), sticky="ew")

        Label(form, text="Penalizace:", bg=BG, fg=GRAY, font=("Arial", 9, "bold")).grid(row=3, column=0, sticky="w", pady=5)
        penalty_var = StringVar(value="none")
        penalty_frame = Frame(form, bg=BG)
        penalty_frame.grid(row=3, column=1, padx=(10,0), sticky="w")
        Radiobutton(penalty_frame, text="Žádná", variable=penalty_var, value="none",
                    bg=BG, fg="white", selectcolor=BG, activebackground=BG, activeforeground="white",
                    borderwidth=0, highlightthickness=0).pack(side="left")
        Radiobutton(penalty_frame, text="DNF", variable=penalty_var, value="DNF",
                    bg=BG, fg="white", selectcolor=BG, activebackground=BG, activeforeground="white",
                    borderwidth=0, highlightthickness=0).pack(side="left", padx=(10,0))
        Radiobutton(penalty_frame, text="+2s", variable=penalty_var, value="+2s",
                    bg=BG, fg="white", selectcolor=BG, activebackground=BG, activeforeground="white",
                    borderwidth=0, highlightthickness=0).pack(side="left", padx=(10,0))

        Label(form, text="Scramble:", bg=BG, fg=GRAY, font=("Arial", 9, "bold")).grid(row=4, column=0, sticky="w", pady=5)
        scramble_var = StringVar()
        Entry(form, textvariable=scramble_var, bg=FRAME_BORDER, fg="white", insertbackground="white",
              borderwidth=0, font=("Arial", 11)).grid(row=4, column=1, padx=(10,0), sticky="ew")
        form.columnconfigure(1, weight=1)

        error_label = Label(win, text="", bg=BG, fg=RED, font=("Arial", 9))
        error_label.pack()

        def on_add():
            time_str = time_var.get().strip()
            date_str = date_var.get().strip()
            cube_str = cube_var.get().strip()
            penalty_str = penalty_var.get()
            scramble_str = scramble_var.get().strip()
            if not time_str:
                error_label.config(text="Zadej čas!")
                return
            try:
                float(time_str)
            except ValueError:
                error_label.config(text="Čas musí být číslo (např. 36.295)")
                return
            if not date_str:
                error_label.config(text="Zadej datum!")
                return
            if penalty_str == "none":
                penalty_str = ""
            self.table.insert("", 0, values=(date_str, cube_str, time_str, penalty_str, scramble_str))
            self.update_stats()
            win.destroy()
        Button(win, text="PŘIDAT", bg=BLUE, fg="black", font=("Arial", 12, "bold"),
               borderwidth=0, highlightthickness=0, activebackground=BLUE, activeforeground="black",
               padx=10, pady=8, command=on_add).pack(fill="x", padx=20, pady=(5,0))

    def on_space_press(self, event):
        if isinstance(self.root.focus_get(), Entry):
            return

        if self.timer_running:
            self.timer_running = False
            self.just_stopped = True
            if self.timer_id:
                self.root.after_cancel(self.timer_id)

            elapsed = time.time() - self.timer_start
            final_time = f"{elapsed:.3f}"
            self.timer_label.config(text=final_time, fg="white")

            date = datetime.now().strftime("%Y-%m-%d")
            cube = self.selected_cube.get()
            scramble = self.scramble_label.cget("text")
            self.table.insert("", 0, values=(date, cube, final_time, "", scramble))
            self.update_stats()

    def on_space_release(self, event):
        if isinstance(self.root.focus_get(), Entry):
            return

        if self.just_stopped:
            self.just_stopped = False
            return

        if not self.timer_running:
            self.timer_running = True
            self.timer_start = time.time()
            self.timer_label.config(fg="#00D4FF")
            self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed = time.time() - self.timer_start
            self.timer_label.config(text=f"{elapsed:.3f}")
            self.timer_id = self.root.after(10, self.update_timer)

root = Tk()
app = myApp(root)
root.mainloop()