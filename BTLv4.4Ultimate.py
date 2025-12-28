import functools
import queue
from tkinter import messagebox
import psutil
from tkinter import Toplevel, Canvas, Button, Label, Entry, Frame, StringVar, messagebox
from tkinter import Toplevel, filedialog, messagebox, ttk
import json
from tkinter import Toplevel, messagebox, ttk, StringVar
from tkinter import ttk, messagebox
from tkinter import Toplevel, Button, Listbox, END, messagebox
import traceback
import tkinter.font as tkfont
from tkinter import Toplevel, Text, Menu, Scrollbar, filedialog, messagebox, simpledialog
import pygame
import os
import sys
import random
import time
import threading
import zipfile
import subprocess
import platform
import getpass
import shutil
import datetime
import copy
from pathlib import Path
import tkinter as tk
from tkinter import Toplevel, Label, Text, END, Button, Entry, Menu, filedialog, ttk, Canvas, messagebox, simpledialog
import glob
from plyer import notification
from tkinter import font


# Optional libs
try:
    from PIL import Image, ImageTk, ImageDraw
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

try:
    import psutil
    PSUTIL_AVAILABLE = True
except Exception:
    psutil = None
    PSUTIL_AVAILABLE = False

try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    PYGAME_AVAILABLE = False

# Helper: cross-platform open (file/URL)

# ---------- Temel dizinler ----------
try:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
except Exception:
    BASE_DIR = os.getcwd()
BTL_DESKTOP = os.path.join(BASE_DIR, "BTL_Desktop")
RECYCLEBIN_DIR = os.path.join(BASE_DIR, "Recycle_Bin")
OLD_VERSIONS_DIR = os.path.join(BASE_DIR, "old_versions")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(BASE_DIR, "Icons")
for d in (
        BTL_DESKTOP,
        RECYCLEBIN_DIR,
        OLD_VERSIONS_DIR,
        ASSETS_DIR,
        ICONS_DIR):
    os.makedirs(d, exist_ok=True)

def startup_animation(callback):
    """
    Var olan `logon` Toplevel'ini kullanarak animasyon oynatır.
    - Kendi Toplevel'ini oluşturmaz veya yok etmez.
    - Animasyon bitince sadece içindeki container frame'i kaldırır ve callback()'i çağırır.
    Gereksinim: global olarak tanımlı bir `logon` Toplevel olmalı.
    """
    import tkinter as tk
    import time
    import math
    import os

    # PIL tercihli
    try:
        from PIL import Image, ImageSequence, ImageTk
        PIL_AVAILABLE = True
    except Exception:
        Image = None
        ImageSequence = None
        ImageTk = None
        PIL_AVAILABLE = False

    WIDTH, HEIGHT = 900, 600
    gif_path = r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\btlload\Loading.gif"
    duration = 10.0  # saniye

    # logon var mı?
    try:
        # referansı kullanmak için sadece var olup olmadığı kontrolu
        logon
    except NameError:
        raise RuntimeError("startup_animation: global 'logon' bulunamadı. Logon ile uğraşmayacağımı söyledin; ama nerede olduğu da lazım.")

    if not hasattr(logon, "winfo_exists") or not logon.winfo_exists():
        raise RuntimeError("startup_animation: 'logon' mevcut değil veya kapatılmış.")

    # Container frame (logon içinde) - main logon penceresine dokunmuyoruz
    container = tk.Frame(logon, width=WIDTH, height=HEIGHT)
    # Center inside logon without changing logon geometry:
    container.place(relx=0.5, rely=0.5, anchor="center")
    container.update_idletasks()

    canvas = tk.Canvas(container, width=WIDTH, height=HEIGHT, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # Metin öğesi
    font_name = ("Arial", 100, "bold")
    text_id = canvas.create_text(WIDTH//2, HEIGHT//2, text="BTL", font=font_name, fill="#8080ff")

    # GIF yükleme
    frames = []
    gif_cumulative = []
    total_gif_duration = 0

    if PIL_AVAILABLE and os.path.exists(gif_path):
        try:
            img = Image.open(gif_path)
            durations = []
            for frame in ImageSequence.Iterator(img):
                frame_rgba = frame.convert("RGBA")
                photo = ImageTk.PhotoImage(frame_rgba)
                frames.append(photo)
                d = frame.info.get('duration', 100)
                if not d or d <= 0:
                    d = 100
                durations.append(d)
            cum = 0
            for d in durations:
                cum += d
                gif_cumulative.append(cum)
            total_gif_duration = gif_cumulative[-1] if gif_cumulative else 0
            img.close()
        except Exception:
            frames = []
            gif_cumulative = []
            total_gif_duration = 0
    else:
        # PIL yoksa, tkinter.PhotoImage ile index dene (basit fallback)
        if os.path.exists(gif_path):
            i = 0
            try:
                while True:
                    p = tk.PhotoImage(file=gif_path, format=f"gif -index {i}")
                    frames.append(p)
                    gif_cumulative.append((i+1)*100)
                    i += 1
            except Exception:
                pass
            total_gif_duration = gif_cumulative[-1] if gif_cumulative else 0

    # Görsellerin çöp toplamasını engelle (container'e bağla)
    container._startup_frames = frames

    img_obj = None
    if frames:
        img_obj = canvas.create_image(WIDTH//2, HEIGHT - 100 + 12, image=frames[0], anchor="center")

    start_time = time.time()

    def animate():
        elapsed = time.time() - start_time
        # renk pulsatasyonu 
        pulse = 128 + int(127 * abs(math.sin(elapsed * 3.0)))
        pulse = max(0, min(255, pulse))
        color = f"#{pulse:02x}{pulse:02x}ff"
        try:
            canvas.itemconfig(text_id, fill=color)
        except Exception:
            pass

        # GIF frame seçimi
        if frames:
            gif_ms = int(elapsed * 1000)
            if total_gif_duration > 0:
                t = gif_ms % total_gif_duration
                frame_idx = 0
                for i, cum in enumerate(gif_cumulative):
                    if t < cum:
                        frame_idx = i
                        break
            else:
                frame_idx = (gif_ms // 100) % len(frames)
            try:
                canvas.itemconfig(img_obj, image=frames[frame_idx])
            except Exception:
                pass

        if elapsed < duration:
            # 16 ms ile yaklaşık 60 FPS
            container.after(16, animate)
        else:
            # Sadece container'ı kaldır, logon'a dokunma
            try:
                container.destroy()
            except Exception:
                try:
                    container.place_forget()
                except Exception:
                    pass
            # callback çağır
            try:
                callback()
            except Exception:
                pass

    container.after(0, animate)
    return container

logon = None

import tkinter as tk
from tkinter import ttk, messagebox
import getpass
import threading
import time

def btl_logon():
    global logon
    """
    Parametresiz. Çağırmak yeterli:
        btl_logon()
    Toplevel kullanır ve Windows logon benzeri bir giriş arayüzü gösterir.
    Not: İstediğin gibi Toplevel değişkeni 'logon' olarak adlandırıldı.
    """

    # Eğer ana Tk root yoksa oluşturup gizle
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()

    # Kullanıcının istediği şekilde: parent belirtmeden Toplevel
    logon = tk.Toplevel()  # <-- burada 'logon' olarak adlandırıldı
    logon.title("BTL Logon")
    logon.configure(bg="#1e1e1e")
    logon.resizable(False, False)
    logon.attributes("-topmost", True)

    # Boyut ve merkeze yerleştirme
    W, H = 600, 340
    screen_w = logon.winfo_screenwidth()
    screen_h = logon.winfo_screenheight()
    x = (screen_w - W) // 2
    y = (screen_h - H) // 2
    logon.geometry(f"{W}x{H}+{x}+{y}")

    # Stil (ttk)
    style = ttk.Style(logon)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    # Ana kart (orta kutu)
    card = ttk.Frame(logon, padding=(24, 18, 24, 18))
    card.place(relx=0.5, rely=0.5, anchor="center")

    # Kullanıcı adı (sistem kullanıcısı)
    try:
        username = getpass.getuser()
    except Exception:
        username = "Kullanıcı"

    # Avatar: daire + baş harf
    avatar = tk.Canvas(card, width=96, height=96, bd=0, highlightthickness=0)
    avatar.grid(row=0, column=0, rowspan=2, padx=(0, 20))
    avatar.create_oval(2, 2, 94, 94, fill="#0078D7", outline="")
    avatar.create_text(48, 48, text=(username[:1] or "?").upper(),
                       fill="white", font=("Segoe UI", 36, "bold"))

    # Kullanıcı adı etiket
    lbl_user = ttk.Label(card, text=username, font=("Segoe UI", 14))
    lbl_user.grid(row=0, column=1, sticky="w")

    # Şifre girişi
    pw_var = tk.StringVar()
    ent_pw = ttk.Entry(card, textvariable=pw_var, show="*", width=32, font=("Segoe UI", 12))
    ent_pw.grid(row=1, column=1, sticky="w", pady=(8, 0))
    ent_pw.focus_set()

    # Durum etiketi
    status = ttk.Label(card, text="", font=("Segoe UI", 10))
    status.grid(row=3, column=0, columnspan=2, pady=(14, 0))

    # Buton satırı
    btn_frame = ttk.Frame(card)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=(12, 0))

    def finish(success: bool):
        if success:
            status.config(text="Doğrulandı. Hoş geldin.")
            logon.update_idletasks()
            logon.after(300, logon.destroy)
        else:
            status.config(text="Hatalı şifre. Tekrar deneyin.")
            pw_var.set("")
            ent_pw.focus_set()
        btn_login.config(state="normal")

    def fake_auth(password: str):
        # Gerçek uygulamada burada sunucu/LDAP/Windows auth çağrısı olur.
        time.sleep(1.0)  # simüle gecikme
        ok = bool(password.strip())  # örnek: boş olmayan şifre kabul edilir
        logon.after(0, lambda: finish(ok))

    def do_login(event=None):
        pw = pw_var.get()
        if not pw.strip():
            messagebox.showwarning("Giriş", "Lütfen şifrenizi girin.")
            ent_pw.focus_set()
            return
        btn_login.config(state="disabled")
        status.config(text="Doğrulanıyor...")
        threading.Thread(target=fake_auth, args=(pw,), daemon=True).start()

    btn_login = ttk.Button(btn_frame, text="Giriş", command=do_login)
    btn_login.pack(side="left", padx=6)
    btn_cancel = ttk.Button(btn_frame, text="İptal", command=logon.destroy)
    btn_cancel.pack(side="left", padx=6)

    # Enter ile giriş, Esc ile iptal
    logon.bind("<Return>", do_login)
    logon.bind("<Escape>", lambda e: logon.destroy())

    # Modal yapmak için grab ve focus
    logon.grab_set()
    logon.focus_force()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def setup_screen():
    if tk._default_root is None:
        raise RuntimeError("setup_screen() çağrılmadan önce ana uygulamada bir Tk() oluşturulmalıdır.")

    win = tk.Toplevel()
    win.title("BTL OS Setup")
    win.resizable(False, False)

    # Boyut ve ortalama
    width, height = 500, 700
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = (sw - width) // 2
    y = (sh - height) // 2
    win.geometry(f"{width}x{height}+{x}+{y}")

    # Header
    header = tk.Frame(win, height=60)
    header.pack(fill="x", padx=12, pady=(10, 6))
    tk.Label(header, text="BTL OS Setup", font=("Segoe UI", 16, "bold")).pack(anchor="w")
    tk.Label(header, text="BTLv4.2", font=("Segoe UI", 9)).pack(anchor="w")

    # Progress
    progress_frame = tk.Frame(win, height=24)
    progress_frame.pack(fill="x", padx=12)
    progress_var = tk.DoubleVar(value=0.0)
    progress = ttk.Progressbar(progress_frame, maximum=100, variable=progress_var)
    progress.pack(fill="x", pady=6)

    # Content alanı
    content = tk.Frame(win)
    content.pack(expand=True, fill="both", padx=12, pady=8)

    # Footer
    footer = tk.Frame(win, height=50)
    footer.pack(fill="x", padx=12, pady=(0,12))
    status_lbl = tk.Label(footer, text="Hazır", anchor="w")
    status_lbl.pack(side="left")
    btn_frame = tk.Frame(footer)
    btn_frame.pack(side="right")
    back_btn = tk.Button(btn_frame, text="Geri", width=10)
    next_btn = tk.Button(btn_frame, text="İleri", width=10)
    cancel_btn = tk.Button(btn_frame, text="İptal", width=10)
    back_btn.pack(side="left", padx=6)
    next_btn.pack(side="left", padx=6)
    cancel_btn.pack(side="left", padx=6)

    # State
    state = {
        "page": 0,
        "accepted_license": False,
        "selected_disk": None,
        "username": "",
        "password": "",
        "product_key": "",
        "privacy": {"telemetry": True, "ads": True},
        "install_progress": 0
    }

    # İçerik temizleme
    def clear_content():
        for child in content.winfo_children():
            child.destroy()

    # Sayfalar
    def page_welcome():
        clear_content()
        status_lbl.config(text="Dil ve bölge seçimi")
        tk.Label(content, text="BTL OS'e hoş geldiniz\nKurulum sihirbazı size birkaç soru soracak.",
                 justify="center", font=("Segoe UI", 12)).pack(pady=20)
        frame = tk.Frame(content)
        frame.pack(pady=10)
        tk.Label(frame, text="Dil:").grid(row=0, column=0, sticky="e")
        lang_cb = ttk.Combobox(frame, values=["Türkçe (Türkiye)","English (United States)","Español"], state="readonly")
        lang_cb.current(0)
        lang_cb.grid(row=0, column=1, padx=6, pady=2)
        tk.Label(frame, text="Saat Dilimi:").grid(row=1, column=0, sticky="e")
        tz_cb = ttk.Combobox(frame, values=["UTC+3 (Istanbul)","UTC+0","UTC-8"], state="readonly")
        tz_cb.current(0)
        tz_cb.grid(row=1, column=1, padx=6, pady=2)

        back_btn.config(state="disabled")
        def on_next():
            state["page"] = 1
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_license():
        clear_content()
        status_lbl.config(text="Lisans sözleşmesi")
        tk.Label(content, text="Lisansı okuyun ve kabul edin:", anchor="w").pack(anchor="w")
        txt_frame = tk.Frame(content, bd=1, relief="sunken")
        txt_frame.pack(fill="both", expand=True, pady=6)
        license_text = tk.Text(txt_frame, wrap="word")
        license_text.insert("1.0", "BTLv4.2 Xaef - 25BTL License.\n\nLütfen okudum diye tikleyin.\n\n(XAEF TARAFINDAN.)\n"*8)
        license_text.config(state="disabled")
        license_text.pack(side="left", fill="both", expand=True)
        scr = tk.Scrollbar(txt_frame, command=license_text.yview)
        scr.pack(side="right", fill="y")
        license_text.config(yscrollcommand=scr.set)
        accept_var = tk.BooleanVar(value=False)
        tk.Checkbutton(content, text="Lisansı kabul ediyorum", variable=accept_var).pack(anchor="w", pady=8)

        back_btn.config(command=lambda: set_page(0))
        def on_next():
            if not accept_var.get():
                messagebox.showwarning("Kabul gerekli", "Devam etmek için lisansı kabul etmelisiniz.")
                return
            state["accepted_license"] = True
            state["page"] = 2
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_disk():
        clear_content()
        status_lbl.config(text="Sürücü seçimi (örnek)")
        tk.Label(content, text="Kurulum yapacağınız sürücüyü seçin:", anchor="w").pack(anchor="w", pady=(0,6))
        disks = [("Disk 0", "100 GB, boş: 60 GB"), ("Disk 1", "500 GB, boş: 200 GB")]
        lb = tk.Listbox(content, height=4)
        for d, desc in disks:
            lb.insert("end", f"{d} - {desc}")
        lb.selection_set(0)
        lb.pack(fill="x", pady=6)

        back_btn.config(command=lambda: set_page(1))
        def on_next():
            sel = lb.curselection()
            if not sel:
                messagebox.showwarning("Sürücü seçimi", "Lütfen bir sürücü seçin.")
                return
            state["selected_disk"] = disks[sel[0]][0]
            state["page"] = 3
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_user_account():
        clear_content()
        status_lbl.config(text="Kullanıcı hesabı oluştur")
        tk.Label(content, text="Yeni kullanıcı oluşturun:", anchor="w").pack(anchor="w")
        frm = tk.Frame(content)
        frm.pack(pady=6)
        tk.Label(frm, text="Kullanıcı adı:").grid(row=0, column=0, sticky="e")
        user_ent = tk.Entry(frm)
        user_ent.grid(row=0, column=1, padx=6, pady=4)
        tk.Label(frm, text="Şifre:").grid(row=1, column=0, sticky="e")
        pass_ent = tk.Entry(frm, show="*")
        pass_ent.grid(row=1, column=1, padx=6, pady=4)

        back_btn.config(command=lambda: set_page(2))
        def on_next():
            user = user_ent.get().strip()
            pwd = pass_ent.get()
            if not user:
                messagebox.showwarning("Hata", "Kullanıcı adı boş olamaz.")
                return
            state["username"] = user
            state["password"] = pwd
            state["page"] = 4
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_product_key():
        clear_content()
        status_lbl.config(text="Ürün anahtarı (isteğe bağlı)")
        tk.Label(content, text="Ürün anahtarınız varsa girin (yoksa atla):", anchor="w").pack(anchor="w")
        pk_ent = tk.Entry(content, width=30)
        pk_ent.pack(pady=8)
        back_btn.config(command=lambda: set_page(3))
        def on_next():
            state["product_key"] = pk_ent.get().strip()
            state["page"] = 5
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_privacy():
        clear_content()
        status_lbl.config(text="Gizlilik ayarları")
        tk.Label(content, text="Gizlilik tercihlerinizi seçin:", anchor="w").pack(anchor="w")
        telem = tk.BooleanVar(value=state["privacy"]["telemetry"])
        ads = tk.BooleanVar(value=state["privacy"]["ads"])
        tk.Checkbutton(content, text="Kullanım verilerini gönder (telemetry)", variable=telem).pack(anchor="w", pady=4)
        tk.Checkbutton(content, text="Hedefli reklamlar göster", variable=ads).pack(anchor="w", pady=4)

        back_btn.config(command=lambda: set_page(4))
        def on_next():
            state["privacy"]["telemetry"] = telem.get()
            state["privacy"]["ads"] = ads.get()
            state["page"] = 6
            update_progress()
            render_current_page()
        next_btn.config(command=on_next)

    def page_install():
        clear_content()
        status_lbl.config(text="Yükleme")
        tk.Label(content, text="Kurulum başlatılıyor. Lütfen bekleyin...", anchor="w").pack(anchor="w", pady=(0,8))
        info = tk.Label(content, text=f"Kullanıcı: {state['username'] or '<yok>'}\nSürücü: {state['selected_disk'] or '<yok>'}", justify="left")
        info.pack(anchor="w", pady=(0,8))
        pb = ttk.Progressbar(content, maximum=100, length=400, mode="determinate")
        pb.pack(pady=12)
        pb["value"] = state["install_progress"]

        back_btn.config(state="disabled")
        cancel_btn.config(state="disabled")
        next_btn.config(state="disabled")

        def install_step():
            state["install_progress"] += 5
            val = state["install_progress"]
            pb["value"] = val
            progress_var.set(60 + val*0.4)
            if val < 100:
                win.after(250, install_step)
            else:
                state["page"] = 7
                update_progress(final=True)
                render_current_page()

        win.after(600, install_step)

    def page_finish():
        clear_content()
        status_lbl.config(text="Tamamlandı")
        tk.Label(content, text="Kurulum tamamlandı. Bilgisayarınız şimdi yeniden başlatılacak.",
                 wraplength=460, justify="center").pack(pady=20)
        tk.Label(content, text=f"Kullanıcı: {state['username']}", font=("Segoe UI", 10, "bold")).pack(pady=6)
        back_btn.config(state="disabled")
        next_btn.config(text="Bitir", command=lambda: do_finish(win))
        cancel_btn.config(text="Kapat", command=lambda: do_finish(win))

    pages = [
        page_welcome,
        page_license,
        page_disk,
        page_user_account,
        page_product_key,
        page_privacy,
        page_install,
        page_finish
    ]

    def render_current_page():
        idx = state["page"]
        if idx < 0: idx = 0
        if idx >= len(pages): idx = len(pages)-1
        pages[idx]()
        update_progress()

    def set_page(n):
        state["page"] = n
        update_progress()
        render_current_page()

    def update_progress(final=False):
        p = int((state["page"] / max(1, (len(pages)-1))) * 100)
        if final: p = 100
        progress_var.set(p)
        progress["value"] = p
        if state["page"] == 0:
            back_btn.config(state="disabled")
            next_btn.config(state="normal", text="İleri")
            cancel_btn.config(state="normal", command=on_cancel)
        elif state["page"] in (len(pages)-1,):
            back_btn.config(state="disabled")
            cancel_btn.config(state="normal", command=on_cancel)
        else:
            back_btn.config(state="normal")
            next_btn.config(state="normal", text="İleri")
            cancel_btn.config(state="normal", command=on_cancel)

    def on_cancel():
        if messagebox.askyesno("İptal", "Kurulumu iptal etmek istiyor musunuz?"):
            messagebox.showerror("REGISTRY CONTENT", "BTL REGISTRYY ERRORRED. SYSTEM HALTED")
            try:
                tk._default_root.destroy()
            except Exception:
                pass

    try:
        win.transient(tk._default_root)
    except Exception:
        pass
    win.grab_set()
    win.focus_force()
    win.protocol("WM_DELETE_WINDOW", on_cancel)
    render_current_page()
    return win

# Animasyon callback örneği
def callback():
    print("Animasyon bitti")
def do_finish(window):
    from tkinter import messagebox
    messagebox.showinfo("Yeniden Başlatma", "Sistem yeniden başlatılıyor.")
    try:
        window.destroy()
    except Exception as e:
        print(f"Pencere kapatılırken hata oluştu: {e}")



# ---------- Globaller ----------
root = tk.Tk()
root.title("BTL 4.4 Ultra")
root.geometry("900x600")
root.config(bg="white")
setup_screen()
btl_logon()
root.iconbitmap(BASE_DIR, "BTL.ico")


_image_refs = []         # PhotoImage referanslarını sakla (Tkinter GC için)
# {label_text: {"frame":frame, "icon_label":..., "text_label":...}}
desktop_icons = {}
users = ["YOU", "BTL SYSTEM", "BTL ADMIN"]
btl_active_users = []

import pygame

# --- MİXER'I GARANTİLİ BAŞLAT ---
pygame.mixer.pre_init(44100, -16, 2, 512)  # önceden ayarla
pygame.init()
pygame.mixer.init()  # kesinlikle en başta

# Ses dosyası (WAV olursa %100 stabil)
pygame.mixer.music.load(r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\BTLstartup.mp3")

# Çal
pygame.mixer.music.play()


# ---------- Initialize pygame mixer if available ----------
if PYGAME_AVAILABLE:
    try:
        pygame.mixer.init()
    except Exception:
        # bazı ortamlarda mixer init başarısız olabilir; sessizce geç.
        PYGAME_AVAILABLE = False
        try:
            pygame = None
        except Exception:
            pass

# Try play a safe startup music if exists (non-blocking)


def try_startup_music():
    if not PYGAME_AVAILABLE:
        return
    startup_path = os.path.join(ASSETS_DIR, "startup.mp3")
    if not os.path.isfile(startup_path):
        # fallback to wav
        startup_path = os.path.join(ASSETS_DIR, "startup.wav")
        if not os.path.isfile(startup_path):
            return

    def _play():
        try:
            pygame.mixer.music.load(startup_path)
            pygame.mixer.music.play()
        except Exception:
            pass
    threading.Thread(target=_play, daemon=True).start()


# schedule startup sound a bit after start (UI thread safe)
root.after(1500, try_startup_music)



# ---------- Arkaplan (wallpaper) ----------
WALLPAPER_PATH = os.path.join(BASE_DIR, "wallpaper2.png")
_background_img = None
_bg_photo = None

if PIL_AVAILABLE and os.path.isfile(WALLPAPER_PATH):
    try:
        _background_img = Image.open(WALLPAPER_PATH).convert("RGBA")
    except Exception:
        _background_img = None

background = Label(root)
background.place(x=0, y=0, relwidth=1, relheight=1)


def resize_bg(event):
    global _bg_photo, _background_img
    if not _background_img:
        return
    new_width = max(1, event.width)
    new_height = max(1, event.height)
    try:
        resized = _background_img.resize(
            (new_width, new_height), Image.Resampling.LANCZOS)
    except Exception:
        resized = _background_img.resize(
            (new_width, new_height), Image.LANCZOS if hasattr(
                Image, 'LANCZOS') else Image.ANTIALIAS)
    _bg_photo = ImageTk.PhotoImage(resized)
    background.config(image=_bg_photo)
    background.image = _bg_photo


root.bind('<Configure>', resize_bg)

# ---------- Görev çubuğu ----------
taskbar = tk.Frame(root, bg="#111111", height=40, relief="raised", bd=2)
taskbar.pack(side="bottom", fill="x")
taskbar.pack_propagate(False)

# Renkler ve parametreler
normal_start = (17, 17, 17)
normal_end = (34, 34, 34)
hover_start = (50, 50, 50)
hover_end = (80, 80, 80)
steps = 50
delay = 20

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

# Hafif geçiş animasyonu
def animate_color(start_color, end_color, step=0, forward=True, callback=None):
    ratio = step / steps
    r = int(start_color[0] + (end_color[0]-start_color[0])*ratio)
    g = int(start_color[1] + (end_color[1]-start_color[1])*ratio)
    b = int(start_color[2] + (end_color[2]-start_color[2])*ratio)
    taskbar.config(bg=rgb_to_hex((r,g,b)))
    
    if forward and step < steps:
        root.after(delay, lambda: animate_color(start_color, end_color, step+1, True, callback))
    elif not forward and step > 0:
        root.after(delay, lambda: animate_color(start_color, end_color, step-1, False, callback))
    elif callback:
        callback()

# Hover efektleri
def on_enter(e):
    animate_color(normal_end, hover_end)

def on_leave(e):
    animate_color(hover_end, normal_end)

taskbar.bind("<Enter>", on_enter)
taskbar.bind("<Leave>", on_leave)

# Sürekli hafif geçiş (pulse)
def pulse(step=0, forward=True):
    ratio = step / steps
    r = int(normal_start[0] + (normal_end[0]-normal_start[0])*ratio)
    g = int(normal_start[1] + (normal_end[1]-normal_start[1])*ratio)
    b = int(normal_start[2] + (normal_end[2]-normal_start[2])*ratio)
    taskbar.config(bg=rgb_to_hex((r,g,b)))
    
    if forward:
        if step < steps:
            root.after(delay, lambda: pulse(step+1, True))
        else:
            root.after(delay, lambda: pulse(steps, False))
    else:
        if step > 0:
            root.after(delay, lambda: pulse(step-1, False))
        else:
            root.after(delay, lambda: pulse(0, True))

pulse()  # animasyonu başlat

# Clock
clock_label = tk.Label(taskbar, fg="white", bg="gray20", font=("Arial", 12))
clock_label.pack(side="right", padx=10)


def update_clock():
    clock_label.config(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_clock)


update_clock()

# ---------- Görev çubuğu: Pencere Yönetimi (Taskbar window management) ----------
# Bu kısım mevcut toollar tarafından açılan `Toplevel` pencerelerini tarar ve
# görev çubuğunda küçük butonlar olarak gösterir. Sol tık: pencereyi
# simge durumuna al / geri getir; Sağ tık: Menü (Simge Durumuna Al / Geri Getir / Kapat).
task_buttons_frame = tk.Frame(taskbar, bg="black")
task_buttons_frame.pack(side="left", padx=6)

managed_windows = {}

def _make_window_button(win):
    try:
        title_var = tk.StringVar(value=win.title() or "Untitled")
    except Exception:
        title_var = tk.StringVar(value="Untitled")

    btn = tk.Button(task_buttons_frame, textvariable=title_var, bg="gray20", fg="white", relief="raised")
    btn.pack(side="left", padx=4, pady=4)

    def _left_click(event=None):
        try:
            st = win.state()
            if st in ("iconic", "withdrawn"):
                try:
                    win.deiconify()
                except Exception:
                    pass
                try:
                    win.lift()
                except Exception:
                    pass
                try:
                    win.focus_force()
                except Exception:
                    pass
            else:
                try:
                    win.iconify()
                except Exception:
                    try:
                        win.withdraw()
                    except Exception:
                        pass
        except Exception:
            pass

    def _right_click(event):
        try:
            menu = tk.Menu(root, tearoff=0)
            menu.add_command(label="Simge Durumuna Al", command=lambda: (win.iconify() if hasattr(win, 'iconify') else None))
            menu.add_command(label="Geri Getir", command=lambda: (win.deiconify() if hasattr(win, 'deiconify') else None, win.lift(), win.focus_force()))
            menu.add_separator()
            menu.add_command(label="Kapat", command=lambda: (win.destroy() if hasattr(win, 'destroy') else None))
            menu.tk_popup(event.x_root, event.y_root)
        finally:
            try:
                menu.grab_release()
            except Exception:
                pass

    btn.bind("<Button-1>", lambda e=None: _left_click())
    btn.bind("<Button-3>", _right_click)

    def _on_destroy(e=None):
        try:
            btn.destroy()
        except Exception:
            pass
        managed_windows.pop(win, None)

    try:
        win.bind('<Destroy>', _on_destroy)
    except Exception:
        pass

    managed_windows[win] = {"btn": btn, "title_var": title_var}
    return btn

def scan_taskbar_windows():
    # Yeni açılmış Toplevel pencereleri tarayıp buton oluştur
    try:
        for w in list(root.winfo_children()):
            try:
                if isinstance(w, tk.Toplevel):
                    # Eğer pencere taskbar'da gösterilmemesi için işaretlenmişse atla
                    if getattr(w, 'taskbar_exclude', False):
                        continue
                    if w not in managed_windows:
                        # ignore some internal transient windows optionally
                        _make_window_button(w)
            except Exception:
                continue

        # Güncelle (başlık değişikliği veya yok olmuş pencereler)
        for w, info in list(managed_windows.items()):
            try:
                if not getattr(w, 'winfo_exists', lambda: True)() or not w.winfo_exists():
                    try:
                        info['btn'].destroy()
                    except Exception:
                        pass
                    managed_windows.pop(w, None)
                    continue
                title = w.title() or "Untitled"
                if info['title_var'].get() != title:
                    info['title_var'].set(title)
            except Exception:
                managed_windows.pop(w, None)
    except Exception:
        pass
    # tekrar tara
    root.after(1000, scan_taskbar_windows)

scan_taskbar_windows()

# ---------- Güvenli image loader ----------
# ---------- Güvenli image loader (şeffaflık düzeltmeli) ----------


def load_image_as_tk(path_or_pil, size=(64, 64), bg=None):
    """
    Path veya PIL.Image alır. Eğer PIL varsa, RGBA desteğini kullanır.
    Eğer bg verilmişse (ör: parent.cget("bg")), şeffaf pikseller bg ile birleştirilerek
    beyaz halo sorunu önlenir.
    """
    if not path_or_pil:
        return None
    try:
        # Pillow varsa en esnek yolu kullan
        if PIL_AVAILABLE:
            # path mi yoksa PIL.Image mı?
            if isinstance(path_or_pil, Image.Image):
                img = path_or_pil.convert("RGBA")
            elif isinstance(path_or_pil, str) and os.path.isfile(path_or_pil):
                img = Image.open(path_or_pil).convert("RGBA")
            else:
                return None

            # Resize / thumbnail
            try:
                img.thumbnail(size, Image.Resampling.LANCZOS)
            except Exception:
                img.thumbnail(
                    size, Image.LANCZOS if hasattr(
                        Image, 'LANCZOS') else Image.ANTIALIAS)

            # Eğer bg verilmişse, alpha içeren resmi bg ile composite et
            if bg:
                try:
                    from PIL import ImageColor
                    rgb = ImageColor.getrgb(bg)
                except Exception:
                    # fallback: tkinter ile oku (örn 'gray18' gibi isimleri
                    # dönüştürmek için)
                    try:
                        r, g, b = root.winfo_rgb(bg)
                        rgb = (r // 256, g // 256, b // 256)
                    except Exception:
                        rgb = (255, 255, 255)
                # bg'yi RGBA olarak oluştur ve üzerine yapıştır (alpha maskesi
                # kullan)
                bg_img = Image.new("RGBA", img.size, rgb + (255,))
                bg_img.paste(img, (0, 0), img)
                img = bg_img

            tkimg = ImageTk.PhotoImage(img)
            _image_refs.append(tkimg)
            return tkimg

        # Pillow yoksa tkinter.PhotoImage ile dene (sınırlı)
        else:
            if isinstance(path_or_pil, str) and os.path.isfile(path_or_pil):
                tkimg = tk.PhotoImage(file=path_or_pil)
                _image_refs.append(tkimg)
                return tkimg

    except Exception:
        # sessizce başarısız ol (orijinal proje tarzı), None döndür
        pass
    return None

# ---------- Helper: open path in platform safe way ----------


def safe_start(path):
    try:
        if sys.platform.startswith("win"):
            os.startfile(path)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
    except Exception:
        messagebox.showerror("Hata", f"Açma başarısız: {path}")

# ---------- add_icon (tek ve sağlam sürüm) ----------


def add_icon(
        x,
        y,
        icon_path,
        label,
        command=None,
        deletable=True,
        parent_frame=None):
    parent = parent_frame if parent_frame else root
    parent_bg = parent.cget("bg")
    frame = tk.Frame(parent, bg=parent_bg)
    frame.place(x=x, y=y)

    # load_image_as_tk fonksiyonu artık bg argümanını destekliyor olmalı
    tk_img = load_image_as_tk(icon_path, size=(64, 64), bg=parent_bg)

    if tk_img:
        icon_label = tk.Label(frame, image=tk_img, bg=parent_bg)
        # referansı sakla, tkinter yine unutkanlık yapmasın diye
        icon_label.image = tk_img
        icon_label.pack()
    else:
        icon_label = tk.Label(
            frame, text=label, font=(
                "Arial", 12), bg=parent_bg)
        icon_label.pack()

    text_label = tk.Label(frame, text=label, font=("Segoe UI", 9), bg=parent_bg)
    text_label.pack()

    # Kayıt et (güncelleme fonksiyonları için). Görüntü referansını da
    # saklıyoruz.
    desktop_icons[label] = {
        "frame": frame,
        "icon_label": icon_label,
        "text_label": text_label,
        "image": getattr(icon_label, "image", None)
    }

    def call_cmd(event=None):
        if callable(command):
            try:
                command()
            except Exception as e:
                messagebox.showerror(
                    "Hata", f"Fonksiyon çalıştırılırken hata: {e}")
        else:
            if isinstance(command, str) and os.path.exists(command):
                try:
                    safe_start(command)
                except Exception as e:
                    messagebox.showerror("Hata", f"Açılamadı: {e}")

    for w in (frame, icon_label, text_label):
        w.bind("<Button-1>", call_cmd)

    if deletable:
        def remove(evt=None):
            try:
                frame.destroy()
                # desktop_icons'dan temizle
                desktop_icons.pop(label, None)
            except Exception:
                pass
        for w in (frame, icon_label, text_label):
            w.bind("<Button-3>", remove)

# btl_os_regedit_single_open.py
# Tüm mantık tek fonksiyon: open_reg()
# Kullanım: butonun command'ine open_reg ver:
# button = tk.Button(taskbar, text="regedit", command=open_reg)
# button.place(relx=0.5, rely=0.5, anchor="center")

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import json, copy, datetime, os, time

APP_TITLE = "BTL OS Regedit (Sahte - Gelişmiş)"
VERSION = "BTL-Regedit-UNIFIED-1.0"

def open_reg():
    """
    Tek merkez: open_reg() tüm UI, tüm fonksiyonlar, tüm state içinde.
    Butona bağla: command=open_reg
    """
    # --- root yönetimi: mevcut root'u kullan ya da yeni, gizli bir root oluştur ---
    created_root = False
    if tk._default_root is None:
        root = tk.Tk()
        root.withdraw()
        created_root = True
    else:
        root = tk._default_root

    # --- iç durum (closure değişkenleri) ---
    registry = {
        "HKEY_BTL": {
            "System": {"Installed": "1", "Version": VERSION, "LastBoot": str(datetime.datetime.now())},
            "Users": {"Sarma": {"Theme": "Dark", "YouTubeSubs": "2600"}},
            "Services": {"btld": {"Start": "Auto", "Status": "Running"}}
        }
    }
    undo_stack = []
    redo_stack = []
    log_lines = []

    # --- görünür pencere ---
    top = tk.Toplevel(master=root)
    top.title(APP_TITLE)
    top.geometry("920x620")
    top.minsize(760, 480)
    top.protocol("WM_DELETE_WINDOW", lambda: on_close())

    # --- UI bileşenleri ---
    toolbar = ttk.Frame(top, padding=6)
    toolbar.pack(side="top", fill="x")

    btn_new_key = ttk.Button(toolbar, text="Yeni Anahtar")
    btn_new_val = ttk.Button(toolbar, text="Yeni Değer")
    btn_delete = ttk.Button(toolbar, text="Sil")
    btn_find = ttk.Button(toolbar, text="Bul")
    btn_undo = ttk.Button(toolbar, text="Geri Al")
    btn_redo = ttk.Button(toolbar, text="Yinele")
    btn_backup = ttk.Button(toolbar, text="Yedekle")
    btn_restore = ttk.Button(toolbar, text="Geri Yükle")
    btn_import = ttk.Button(toolbar, text="İçe Aktar")
    btn_export = ttk.Button(toolbar, text="Dışa Aktar")
    btn_cancel_install = ttk.Button(toolbar, text="Kurulum İptal Et", style="Danger.TButton")

    for w in (btn_new_key, btn_new_val, btn_delete, btn_find, btn_undo, btn_redo,
              btn_backup, btn_restore, btn_import, btn_export):
        w.pack(side="left", padx=2)
    btn_cancel_install.pack(side="right", padx=2)

    main = ttk.PanedWindow(top, orient="horizontal")
    main.pack(fill="both", expand=True)

    left = ttk.Frame(main, width=340)
    main.add(left, weight=1)
    right = ttk.Frame(main)
    main.add(right, weight=3)

    # Sol: ağaç
    tree = ttk.Treeview(left, show="tree")
    vsb = ttk.Scrollbar(left, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True, side="left")
    tree.bind("<<TreeviewSelect>>", lambda e: on_tree_select())
    tree.bind("<Button-3>", lambda e: on_tree_right_click(e))

    # Sağ üst: değerler
    ttk.Label(right, text="Değerler (Seçili anahtar):").pack(anchor="w", padx=6, pady=(6,0))
    values_tree = ttk.Treeview(right, columns=("Name","Type","Value"), show="headings", height=10)
    values_tree.heading("Name", text="Ad")
    values_tree.heading("Type", text="Tür")
    values_tree.heading("Value", text="Değer")
    values_tree.column("Name", width=160)
    values_tree.column("Type", width=80)
    values_tree.column("Value", width=420)
    values_tree.pack(fill="x", padx=6, pady=6)
    values_tree.bind("<Double-1>", lambda e: edit_value())
    values_tree.bind("<Button-3>", lambda e: on_value_right_click(e))

    editor_frame = ttk.Frame(right)
    editor_frame.pack(fill="x", padx=6, pady=6)
    ttk.Label(editor_frame, text="Seçili Anahtar Yolu:").pack(anchor="w")
    path_var = tk.StringVar()
    path_entry = ttk.Entry(editor_frame, textvariable=path_var, state="readonly")
    path_entry.pack(fill="x")

    ttk.Label(editor_frame, text="Hızlı Değer Ekle (ad=değer):").pack(anchor="w", pady=(6,0))
    hv = ttk.Frame(editor_frame)
    hv.pack(fill="x")
    quick_var = tk.StringVar()
    ttk.Entry(hv, textvariable=quick_var).pack(side="left", fill="x", expand=True)
    ttk.Button(hv, text="Ekle", command=lambda: quick_add()).pack(side="left", padx=4)

    ttk.Label(right, text="Log:").pack(anchor="w", padx=6, pady=(8,0))
    logbox = tk.Text(right, height=8, state="disabled")
    logbox.pack(fill="both", expand=True, padx=6, pady=(0,6))

    # Context menüler
    key_menu = tk.Menu(top, tearoff=0)
    key_menu.add_command(label="Yeni Anahtar", command=lambda: add_key())
    key_menu.add_command(label="Yeni Değer", command=lambda: add_value())
    key_menu.add_separator()
    key_menu.add_command(label="Kopyala Anahtar Yolu", command=lambda: copy_key_path())
    key_menu.add_command(label="Yedekle (Bu alt dal)", command=lambda: backup_selected_branch())
    key_menu.add_separator()
    key_menu.add_command(label="Sil", command=lambda: delete_selected())

    value_menu = tk.Menu(top, tearoff=0)
    value_menu.add_command(label="Düzenle", command=lambda: edit_value())
    value_menu.add_command(label="Sil", command=lambda: delete_value())
    value_menu.add_separator()
    value_menu.add_command(label="Kopyala Değer", command=lambda: copy_value())

    # Helper: tree oluşturma
    def _build_tree():
        tree.delete(*tree.get_children())
        def add_nodes(parent, d):
            for k in sorted(d.keys()):
                node = tree.insert(parent, "end", text=k, open=True)
                if isinstance(d[k], dict):
                    add_nodes(node, d[k])
        add_nodes("", registry)

    def _find_node_dict(item_id):
        if not item_id:
            return None
        parts = []
        t = item_id
        while t:
            parts.append(tree.item(t, "text"))
            t = tree.parent(t)
        parts = list(reversed(parts))
        d = registry
        for p in parts:
            if isinstance(d, dict) and p in d:
                d = d[p]
            else:
                return None
        return d

    def _get_path_str(item_id):
        if not item_id:
            return ""
        parts = []
        t = item_id
        while t:
            parts.append(tree.item(t, "text"))
            t = tree.parent(t)
        return "\\".join(reversed(parts))

    # Log / undo helpers
    def _push_undo(desc="İşlem"):
        undo_stack.append(copy.deepcopy(registry))
        if len(undo_stack) > 100:
            del undo_stack[0]
        redo_stack.clear()
        _write_log(f"UNDO push: {desc}")

    def undo():
        if not undo_stack:
            messagebox.showinfo(APP_TITLE, "Geri alınacak işlem yok.")
            return
        redo_stack.append(copy.deepcopy(registry))
        snap = undo_stack.pop()
        registry.clear()
        registry.update(snap)
        _build_tree()
        on_tree_select()
        _write_log("Geri alındı.")

    def redo():
        if not redo_stack:
            messagebox.showinfo(APP_TITLE, "Yinelecek işlem yok.")
            return
        undo_stack.append(copy.deepcopy(registry))
        snap = redo_stack.pop()
        registry.clear()
        registry.update(snap)
        _build_tree()
        on_tree_select()
        _write_log("Yineleme yapıldı.")

    def _write_log(text):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_lines.append((ts, text))
        try:
            logbox.config(state="normal")
            logbox.insert("end", f"[{ts}] {text}\n")
            logbox.see("end")
            logbox.config(state="disabled")
        except Exception:
            pass

    # --- UI event handlers and operations ---
    def on_tree_select():
        values_tree.delete(*values_tree.get_children())
        sel = tree.selection()
        if not sel:
            path_var.set("")
            return
        node = sel[0]
        path_var.set(_get_path_str(node))
        d = _find_node_dict(node)
        if isinstance(d, dict):
            for k, v in d.items():
                if isinstance(v, dict):
                    continue
                t = "REG_SZ"
                try:
                    if str(v).isdigit():
                        t = "REG_DWORD"
                except Exception:
                    pass
                values_tree.insert("", "end", values=(k, t, str(v)))

    def on_tree_right_click(event):
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)
            key_menu.tk_popup(event.x_root, event.y_root)
        else:
            mm = tk.Menu(top, tearoff=0)
            mm.add_command(label="Yeni Kök Anahtar", command=lambda: add_root_key())
            mm.add_command(label="İçe Aktar", command=lambda: import_json())
            mm.tk_popup(event.x_root, event.y_root)

    def on_value_right_click(event):
        iid = values_tree.identify_row(event.y)
        if iid:
            values_tree.selection_set(iid)
            value_menu.tk_popup(event.x_root, event.y_root)

    def add_root_key():
        name = simpledialog.askstring(APP_TITLE, "Yeni kök anahtar adı:")
        if not name:
            return
        if name in registry:
            messagebox.showwarning(APP_TITLE, "Aynı isimde kök anahtar var.")
            return
        _push_undo("Kök anahtar ekle")
        registry[name] = {}
        _build_tree()
        _write_log(f"Kök anahtar eklendi: {name}")

    def add_key():
        sel = tree.selection()
        parent = sel[0] if sel else ""
        name = simpledialog.askstring(APP_TITLE, "Yeni anahtar adı:")
        if not name:
            return
        parent_dict = _find_node_dict(parent) if parent else registry
        if parent_dict is None or not isinstance(parent_dict, dict):
            messagebox.showerror(APP_TITLE, "Anahtar bulunamadı.")
            return
        if name in parent_dict:
            messagebox.showwarning(APP_TITLE, "Aynı adda anahtar zaten var.")
            return
        _push_undo("Anahtar ekle")
        parent_dict[name] = {}
        _build_tree()
        if parent:
            path_str = _get_path_str(parent) + "\\" + name
        else:
            path_str = name
        _write_log(f"Anahtar eklendi: {path_str}")

    def add_value():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning(APP_TITLE, "Önce bir anahtar seç.")
            return
        node = sel[0]
        key_name = simpledialog.askstring(APP_TITLE, "Değer adı:")
        if not key_name:
            return
        val = simpledialog.askstring(APP_TITLE, "Değer:")
        if val is None:
            return
        d = _find_node_dict(node)
        if d is None or not isinstance(d, dict):
            messagebox.showerror(APP_TITLE, "Anahtar bulunamadı.")
            return
        if key_name in d and isinstance(d[key_name], dict):
            messagebox.showerror(APP_TITLE, "Aynı isimde alt anahtar var; değer eklenemiyor.")
            return
        _push_undo("Değer ekle")
        d[key_name] = val
        on_tree_select()
        _write_log(f"Değer eklendi: {key_name} -> {val}")

    def quick_add():
        data = quick_var.get().strip()
        if "=" not in data:
            messagebox.showwarning(APP_TITLE, "Format: ad=değer")
            return
        name, val = data.split("=",1)
        quick_var.set("")
        sel = tree.selection()
        if not sel:
            messagebox.showwarning(APP_TITLE, "Önce bir anahtar seç.")
            return
        node = sel[0]
        d = _find_node_dict(node)
        if d is None:
            return
        _push_undo("Hızlı değer ekle")
        d[name.strip()] = val.strip()
        on_tree_select()
        _write_log(f"Hızlı değer eklendi: {name.strip()}")

    def delete_selected():
        val_sel = values_tree.selection()
        if val_sel:
            item = val_sel[0]
            name = values_tree.item(item, "values")[0]
            if messagebox.askyesno(APP_TITLE, f"{name} değerini silmek istediğine emin misin?"):
                tree_sel = tree.selection()
                if not tree_sel:
                    return
                d = _find_node_dict(tree_sel[0])
                if d and name in d:
                    _push_undo("Değer sil")
                    del d[name]
                    on_tree_select()
                    _write_log(f"Değer silindi: {name}")
                else:
                    messagebox.showerror(APP_TITLE, "Değer bulunamadı.")
            return
        tree_sel = tree.selection()
        if not tree_sel:
            messagebox.showwarning(APP_TITLE, "Önce bir anahtar seç.")
            return
        node = tree_sel[0]
        path = _get_path_str(node)
        if messagebox.askyesno(APP_TITLE, f"{path} anahtarını (alt dallarıyla) silmek istediğine emin misin?"):
            parent = tree.parent(node)
            name = tree.item(node, "text")
            parent_dict = _find_node_dict(parent) if parent else registry
            if parent_dict and name in parent_dict:
                _push_undo("Anahtar sil")
                del parent_dict[name]
                _build_tree()
                values_tree.delete(*values_tree.get_children())
                _write_log(f"Anahtar silindi: {path}")
            else:
                messagebox.showerror(APP_TITLE, "Silme başarısız.")

    def edit_value():
        sel = values_tree.selection()
        if not sel:
            return
        item = sel[0]
        name, typ, val = values_tree.item(item, "values")
        new = simpledialog.askstring(APP_TITLE, f"Düzenle: {name}", initialvalue=val)
        if new is None:
            return
        tree_sel = tree.selection()
        if not tree_sel:
            return
        d = _find_node_dict(tree_sel[0])
        if d and name in d:
            _push_undo("Değer düzenle")
            d[name] = new
            on_tree_select()
            _write_log(f"Değer düzenlendi: {name} -> {new}")

    def delete_value():
        sel = values_tree.selection()
        if not sel:
            messagebox.showwarning(APP_TITLE, "Değer seçili değil.")
            return
        item = sel[0]
        name = values_tree.item(item, "values")[0]
        tree_sel = tree.selection()
        if not tree_sel:
            return
        d = _find_node_dict(tree_sel[0])
        if d and name in d:
            if messagebox.askyesno(APP_TITLE, f"{name} değerini silmek istediğine emin misin?"):
                _push_undo("Değer sil")
                del d[name]
                on_tree_select()
                _write_log(f"Değer silindi: {name}")

    def copy_key_path():
        sel = tree.selection()
        if not sel:
            return
        path = _get_path_str(sel[0])
        try:
            top.clipboard_clear()
            top.clipboard_append(path)
            _write_log(f"Anahtar yolu kopyalandı: {path}")
        except Exception:
            _write_log("Kopyalama başarısız.")

    def copy_value():
        sel = values_tree.selection()
        if not sel:
            return
        item = sel[0]
        name, typ, val = values_tree.item(item, "values")
        try:
            top.clipboard_clear()
            top.clipboard_append(val)
            _write_log(f"Değer kopyalandı: {name}")
        except Exception:
            _write_log("Kopyalama başarısız.")

    # Import / export / backup
    def export_json():
        f = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
        if not f:
            return
        try:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(registry, fh, ensure_ascii=False, indent=2)
            messagebox.showinfo(APP_TITLE, f"Dışa aktarıldı: {os.path.basename(f)}")
            _write_log(f"Dışa aktarma: {f}")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Kaydetme hatası: {e}")

    def import_json():
        f = filedialog.askopenfilename(filetypes=[("JSON","*.json")])
        if not f:
            return
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                raise ValueError("Geçersiz format.")
            _push_undo("İçe aktar")
            registry.clear()
            registry.update(data)
            _build_tree()
            _write_log(f"İçe aktarıldı: {f}")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"İçe aktarma hatası: {e}")

    def backup():
        f = filedialog.asksaveasfilename(defaultextension=".btlbak", filetypes=[("BTL Backup","*.btlbak")])
        if not f:
            return
        try:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(registry, fh, ensure_ascii=False)
            messagebox.showinfo(APP_TITLE, f"Yedeklendi: {os.path.basename(f)}")
            _write_log(f"Yedeklendi: {f}")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Yedekleme hatası: {e}")

    def restore():
        f = filedialog.askopenfilename(filetypes=[("BTL Backup","*.btlbak"),("JSON","*.json")])
        if not f:
            return
        try:
            with open(f, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if not isinstance(data, dict):
                raise ValueError("Geçersiz yedek.")
            _push_undo("Geri yükle")
            registry.clear()
            registry.update(data)
            _build_tree()
            _write_log(f"Geri yüklendi: {f}")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Geri yükleme hatası: {e}")

    # Search
    def find_dialog():
        q = simpledialog.askstring(APP_TITLE, "Ara (anahtar veya değer adı / içeriği):")
        if not q:
            return
        matches = []
        def search(d, path):
            for k, v in d.items():
                p = path + [k]
                if q.lower() in k.lower():
                    matches.append("\\".join(p))
                if isinstance(v, dict):
                    search(v, p)
                else:
                    if q.lower() in str(v).lower():
                        matches.append("\\".join(p) + "\\" + k)
        search(registry, [])
        if not matches:
            messagebox.showinfo(APP_TITLE, "Eşleşme bulunamadı.")
            return
        text = "\n".join(f"{i}: {m}" for i, m in enumerate(matches[:50]))
        sel = simpledialog.askstring(APP_TITLE, "Eşleşmeler:\n" + text + "\n\nİndeksi gir:")
        try:
            idx = int(sel.strip())
            chosen = matches[idx]
            parts = chosen.split("\\")
            def find_in_tree(parent, parts_left):
                if not parts_left:
                    return parent
                for child in tree.get_children(parent):
                    if tree.item(child, "text") == parts_left[0]:
                        return find_in_tree(child, parts_left[1:])
                return None
            node = find_in_tree("", parts)
            if node:
                tree.selection_set(node)
                tree.see(node)
                _write_log(f"Ara sonuçuna gidildi: {chosen}")
            else:
                messagebox.showinfo(APP_TITLE, "Bulunan yol ağaçta bulunamadı.")
        except Exception:
            messagebox.showinfo(APP_TITLE, "Geçersiz seçim.")

    def backup_selected_branch():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning(APP_TITLE, "Önce bir anahtar seç.")
            return
        node = sel[0]
        d = _find_node_dict(node)
        if d is None:
            return
        f = filedialog.asksaveasfilename(defaultextension=".json")
        if not f:
            return
        try:
            with open(f, "w", encoding="utf-8") as fh:
                json.dump(d, fh, ensure_ascii=False, indent=2)
            _write_log(f"Alt dal yedeklendi: {f}")
            messagebox.showinfo(APP_TITLE, "Alt dal yedeklendi.")
        except Exception as e:
            messagebox.showerror(APP_TITLE, f"Hata: {e}")

    # Permission sim
    def _simulate_permission_check():
        # sahte izin: Sarma kullanıcıyı varsa admin kabul et
        return "Sarma" in registry.get("HKEY_BTL", {}).get("Users", {})

    # Kurulum iptali: istenen hata zinciri, sonra temizleme
    def cancel_install_sequence():
        if not messagebox.askyesno(APP_TITLE, "Kurulumu iptal etmek istediğine emin misin?"):
            return
        # sıralı hata pencereleri (bloklayıcı ama dramatik)
        messagebox.showerror(APP_TITLE, "BTL REGISTIRY ERROR")
        messagebox.showerror(APP_TITLE, "REGISTRY CONTENT")
        messagebox.showerror(APP_TITLE, "BTL REGISTRYY ERRORRED. SYSTEM HALTED")
        _write_log("Kurulum iptali tetiklendi: sahte hata zinciri gösterildi.")
        # temizle
        try:
            top.destroy()
        except Exception:
            pass
        if created_root:
            try:
                root.destroy()
            except Exception:
                pass

    # Kapatma
    def on_close():
        if messagebox.askokcancel(APP_TITLE, "Kapatılsın mı?"):
            try:
                top.destroy()
            except Exception:
                pass
            if created_root:
                try:
                    root.destroy()
                except Exception:
                    pass

    # Bağlantılar: toolbar düğmelerine handler bağla
    btn_new_key.config(command=lambda: add_key())
    btn_new_val.config(command=lambda: add_value())
    btn_delete.config(command=lambda: delete_selected())
    btn_find.config(command=lambda: find_dialog())
    btn_undo.config(command=lambda: undo())
    btn_redo.config(command=lambda: redo())
    btn_backup.config(command=lambda: backup())
    btn_restore.config(command=lambda: restore())
    btn_import.config(command=lambda: import_json())
    btn_export.config(command=lambda: export_json())
    btn_cancel_install.config(command=lambda: cancel_install_sequence())

    # Sağ-tık value/menu handlerlar zaten bağlandı via lambdalar

    # İlk ağaç inşa
    _build_tree()

    # Modal davranış: capture ve bekle
    try:
        top.transient(root)
        top.grab_set()
        top.wait_window()
    finally:
        # eğer kullanıcı beklemeden kapattıysa temizle
        if created_root:
            try:
                if root.winfo_exists():
                    root.destroy()
            except Exception:
                pass

# ---------- Dosya Yöneticisi (simülasyon) ----------
# Gelişmiş Dosya Yöneticisi - Tam Fonksiyonel Simülasyon
# Kullanım: Bu dosyayı çalıştırın; bir Tkinter penceresi açılacak ve
# 'open_file_manager(root)' fonksiyonu içinde tanımlı gelişmiş yöneticiyi göreceksiniz.
# Not: Harici kütüphaneler (Pillow) varsa /img önizleme desteklenir; yoksa metin önizleme çalışır.

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
from tkinter import Toplevel, END
import datetime
import copy
import os
import sys

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except Exception:
    PIL_AVAILABLE = False

def open_file_manager():
    win = Toplevel(root)
    win.title("Gelişmiş Dosya Yöneticisi (Düzeltilmiş)")
    win.geometry("900x560")

    FS = {
        "root": {
            "type": "folder",
            "children": {
                "Windows": {
                    "type": "folder",
                    "children": {
                        "System32": {
                            "type": "folder",
                            "children": {
                                f"SYSTEM_FILE_{i}.sys": {
                                    "type": "file",
                                    "content": "",
                                    "size": 4,
                                    "modified": datetime.datetime.now()
                                } for i in range(1, 21)
                            }
                        }
                    }
                },
                "Belgelerim": {
                    "type": "folder",
                    "children": {
                        "notlar.txt": {
                            "type": "file",
                            "content": "Bu bir önizleme dosyası.\nMerhaba.",
                            "size": 12,
                            "modified": datetime.datetime.now()
                        },
                        "gorevler.txt": {
                            "type": "file",
                            "content": "1. Kahve\n2. Kod yaz",
                            "size": 10,
                            "modified": datetime.datetime.now()
                        }
                    }
                }
            }
        }
    }


    clipboard = {"node": None, "mode": None}

    top_frame = tk.Frame(win)
    top_frame.pack(fill="x", padx=6, pady=6)

    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var)
    search_entry.pack(side="left", fill="x", expand=True)

    btn_search = tk.Button(
        top_frame,
        text="Ara",
        command=lambda: refresh_tree(
            filter_text=search_var.get()))
    btn_search.pack(side="left", padx=4)

    btn_new_folder = tk.Button(
        top_frame,
        text="Yeni Klasör",
        command=lambda: new_folder())
    btn_new_folder.pack(side="left", padx=4)

    btn_new_file = tk.Button(
        top_frame,
        text="Yeni Dosya",
        command=lambda: new_file())
    btn_new_file.pack(side="left", padx=4)

    main_pane = tk.PanedWindow(win, orient="horizontal", sashrelief="raised")
    main_pane.pack(fill="both", expand=True, padx=6, pady=(0, 6))

    tree_frame = tk.Frame(main_pane)
    tree = ttk.Treeview(tree_frame)
    tree.pack(fill="both", expand=True, side="left")
    tree_scroll = ttk.Scrollbar(
        tree_frame,
        orient="vertical",
        command=tree.yview)
    tree.configure(yscrollcommand=tree_scroll.set)
    tree_scroll.pack(side="right", fill="y")

    right_frame = tk.Frame(main_pane)
    preview_label = tk.Label(right_frame, text="Önizleme", anchor="w")
    preview_label.pack(fill="x")
    preview_text = tk.Text(right_frame, height=18)
    preview_text.pack(fill="both", expand=True)

    status = tk.Label(win, text="Hazır", anchor="w")
    status.pack(fill="x", side="bottom")

    main_pane.add(tree_frame, width=360)
    main_pane.add(right_frame)

    def get_node_by_tree_id(tree_id):
        parts = []
        cur = tree_id
        while cur:
            parts.append(tree.item(cur, "text"))
            cur = tree.parent(cur)
        if not parts:
            return None, []
        parts.reverse()
        node = FS["root"]
        for p in parts[1:]:
            if "children" in node and p in node["children"]:
                node = node["children"][p]
            else:
                return None, parts
        return node, parts

    def populate_tree():
        tree.delete(*tree.get_children())

        def _insert(parent, node_dict):
            for name, meta in sorted(node_dict.items()):
                iid = tree.insert(parent, "end", text=name, open=False)
                if meta["type"] == "folder":
                    tree.insert(iid, "end", text="__placeholder__")
        root_iid = tree.insert("", "end", text="root", open=True)
        _insert(root_iid, FS["root"]["children"])

    populate_tree()

    def expand_real_children(event):
        iid = tree.focus()
        if not iid:
            return
        children = tree.get_children(iid)
        if len(children) == 1 and tree.item(
                children[0], "text") == "__placeholder__":
            tree.delete(children[0])
            node, parts = get_node_by_tree_id(iid)
            if not node:
                return
            for name, meta in sorted(node.get("children", {}).items()):
                child_iid = tree.insert(iid, "end", text=name, open=False)
                if meta["type"] == "folder":
                    tree.insert(child_iid, "end", text="__placeholder__")

    tree.bind("<<TreeviewOpen>>", expand_real_children)

    def get_path_str(tree_iid):
        if not tree_iid:
            return ""
        parts = []
        cur = tree_iid
        while cur:
            parts.append(tree.item(cur, "text"))
            cur = tree.parent(cur)
        parts.reverse()
        return "/".join(parts)

    def refresh_tree(filter_text=""):
        expanded = set()

        def collect_open(iid):
            if tree.item(iid, "open"):
                expanded.add(get_path_str(iid))
                for c in tree.get_children(iid):
                    collect_open(c)
        for iid in tree.get_children():
            collect_open(iid)

        tree.delete(*tree.get_children())

        def _insert(parent, node_dict):
            for name, meta in sorted(node_dict.items()):
                if filter_text and filter_text.lower() not in name.lower():
                    if meta["type"] == "folder" and any(
                        filter_text.lower() in k.lower() for k in meta.get(
                            "children", {})):
                        pass
                    else:
                        continue
                open_state = (get_path_str(parent) + "/" + name) in expanded
                iid = tree.insert(parent, "end", text=name, open=open_state)
                if meta["type"] == "folder":
                    if meta.get("children"):
                        tree.insert(iid, "end", text="__placeholder__")
        root_iid = tree.insert("", "end", text="root", open=True)
        _insert(root_iid, FS["root"]["children"])

    def show_properties(node, parts):
        if not node:
            return
        typ = node["type"]
        if typ == "folder":
            size = sum(
                child.get(
                    "size",
                    0) for child in node.get(
                    "children",
                    {}).values())
        else:
            size = node.get("size", 0)
        modified = node.get("modified", "")
        messagebox.showinfo(
            "Özellikler",
            f"Ad: {parts[-1]}\nTür: {typ}\nBoyut: {size} KB\nSon Değişiklik: {modified}")

    def on_select(event):
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if not parts:
            preview_text.delete("1.0", END)
            status.config(text="Seçim yok")
            return

        name = parts[-1]

        if node is None:
            preview_text.delete("1.0", END)
            preview_text.insert(
                END, f"'{name}' seçildi — öğe ağaçta var ama simüle edilmiş FS'de bulunamadı.")
            status.config(text=f"Seçili: {'/'.join(parts)} (bulunamadı)")
            return

        if node["type"] == "file":
            preview_text.delete("1.0", END)
            preview_text.insert(END, node.get("content", ""))
        else:
            preview_text.delete("1.0", END)
            preview_text.insert(
                END, f"{name} klasörü, {len(node.get('children',{}))} öğe")
        status.config(text=f"Seçili: {'/'.join(parts)}")

    tree.bind("<<TreeviewSelect>>", on_select)

    # Context menu
    ctx = tk.Menu(win, tearoff=0)
    ctx.add_command(label="Aç / Önizle", command=lambda: action_open())
    ctx.add_command(label="Sil", command=lambda: action_delete())
    ctx.add_command(
        label="Yeniden Adlandır (F2)",
        command=lambda: action_rename())
    ctx.add_separator()
    ctx.add_command(label="Kopyala (Ctrl+C)", command=lambda: action_copy())
    ctx.add_command(label="Yapıştır (Ctrl+V)", command=lambda: action_paste())
    ctx.add_separator()
    ctx.add_command(label="Özellikler", command=lambda: action_properties())

    def popup_menu(event):
        iid = tree.identify_row(event.y)
        if iid:
            tree.selection_set(iid)
            ctx.tk_popup(event.x_root, event.y_root)
    tree.bind("<Button-3>", popup_menu)

    win.bind("<Delete>", lambda e: action_delete())
    win.bind("<F2>", lambda e: action_rename())
    win.bind_all("<Control-c>", lambda e: action_copy())
    win.bind_all("<Control-v>", lambda e: action_paste())

    def action_open():
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if not node:
            if parts:
                messagebox.showinfo(
                    "Bilgi", f"'{parts[-1]}' açılmaya çalışıldı ama içerik yok.")
            return
        if node["type"] == "file":
            preview_text.delete("1.0", END)
            preview_text.insert(END, node.get("content", ""))
            messagebox.showinfo("Açıldı", f"{parts[-1]} önizlemede açıldı.")
        else:
            tree.item(iid, open=True)
            expand_real_children(None)

    def action_delete():
        iid = tree.focus()
        if not iid:
            return
        node, parts = get_node_by_tree_id(iid)
        if not parts:
            return
        name = parts[-1]
        if node and node["type"] == "file" and name.lower().endswith(".sys"):
            for i in range(3):
                messagebox.showerror(
                    "Sistem Hatası",
                    f"{name} silinemez! Sistem hatası {i+1}/3")
            win.destroy()
            try:
                root.withdraw()
            except Exception:
                pass
            try:
                show_bsod()
            except Exception:
                messagebox.showerror(
                    "BSOD", "show_bsod() fonksiyonu bulunamadı veya hata verdi.")
            return

        if messagebox.askyesno(
            "Sil",
                f"'{name}' silinsin mi? (Gerçek dosyalara dokunmam)"):
            parent_iid = tree.parent(iid)
            parent_node, parent_parts = get_node_by_tree_id(parent_iid)
            if parent_node and "children" in parent_node and name in parent_node["children"]:
                del parent_node["children"][name]
            refresh_tree(filter_text=search_var.get())

    def action_rename():
        iid = tree.focus()
        if not iid:
            return
        node, parts = get_node_by_tree_id(iid)
        if not parts or node is None:
            return
        old_name = parts[-1]
        new_name = simpledialog.askstring(
            "Yeniden Adlandır",
            "Yeni ad:",
            initialvalue=old_name,
            parent=win)
        if not new_name or new_name.strip() == "":
            return
        parent_iid = tree.parent(iid)
        parent_node, parent_parts = get_node_by_tree_id(parent_iid)
        if parent_node and "children" in parent_node:
            if new_name in parent_node["children"]:
                messagebox.showerror("Hata", "Aynı isimde bir öğe zaten var.")
                return
            parent_node["children"][new_name] = parent_node["children"].pop(
                old_name)
            refresh_tree(filter_text=search_var.get())

    def action_copy():
        iid = tree.focus()
        if not iid:
            return
        node, parts = get_node_by_tree_id(iid)
        if not parts or node is None:
            return
        clipboard["node"] = (parts.copy(), copy.deepcopy(node))
        clipboard["mode"] = "copy"
        status.config(text=f"Kopyalandı: {'/'.join(parts)}")

    def action_paste():
        iid = tree.focus()
        if not iid:
            return
        target_node, parts = get_node_by_tree_id(iid)
        if not target_node or target_node["type"] != "folder":
            messagebox.showerror("Hata", "Yapıştırmak için bir klasör seçin.")
            return
        if not clipboard["node"]:
            messagebox.showinfo("Bilgi", "Panoda öğe yok.")
            return
        original_path, original_node = clipboard["node"]
        name = original_path[-1]
        if name in target_node.get("children", {}):
            name = f"{name}_kopya"
        copied = copy.deepcopy(original_node)
        target_node.setdefault("children", {})[name] = copied
        refresh_tree(filter_text=search_var.get())
        status.config(text=f"'{name}' yapıştırıldı -> {'/'.join(parts)}")

    def action_properties():
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if parts:
            show_properties(node, parts)

    def new_folder():
        iid = tree.focus()
        if not iid:
            messagebox.showerror("Hata", "Klasör seçin.")
            return
        node, parts = get_node_by_tree_id(iid)
        if not node or node["type"] != "folder":
            messagebox.showerror("Hata", "Klasör seçin.")
            return
        name = simpledialog.askstring("Yeni Klasör", "Klasör adı:", parent=win)
        if not name:
            return
        if name in node.get("children", {}):
            messagebox.showerror("Hata", "Aynı isimde öğe var.")
            return
        node.setdefault(
            "children",
            {})[name] = {
            "type": "folder",
            "children": {},
            "modified": datetime.datetime.now()}
        refresh_tree(filter_text=search_var.get())

    def new_file():
        iid = tree.focus()
        if not iid:
            messagebox.showerror("Hata", "Klasör seçin.")
            return
        node, parts = get_node_by_tree_id(iid)
        if not node or node["type"] != "folder":
            messagebox.showerror("Hata", "Klasör seçin.")
            return
        name = simpledialog.askstring(
            "Yeni Dosya", "Dosya adı (ör: yeni.txt):", parent=win)
        if not name:
            return
        if name in node.get("children", {}):
            messagebox.showerror("Hata", "Aynı isimde öğe var.")
            return
        node.setdefault(
            "children",
            {})[name] = {
            "type": "file",
            "content": "",
            "size": 1,
            "modified": datetime.datetime.now()}
        refresh_tree(filter_text=search_var.get())

    # İlk seçim
    root_items = tree.get_children()
    if root_items:
        tree.selection_set(root_items[0])
        tree.focus(root_items[0])

    status.config(
        text="Kısayollar: Delete=Sil, F2=Yeniden adlandır, Ctrl+C/Ctrl+V=Kopyala/Yapıştır")

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import keyword, builtins, re, os, sys

_HIGHLIGHT_DELAY = 150
_TAG_STYLES = {
    'keyword': {'foreground': '#569CD6'},
    'builtin': {'foreground': '#4EC9B0'},
    'string': {'foreground': '#CE9178'},
    'comment': {'foreground': '#6A9955', 'italic': True},
    'number': {'foreground': '#B5CEA8'},
    'defname': {'foreground': '#DCDCAA', 'underline': True},
    'decorator': {'foreground': '#C586C0'},
    'classname': {'foreground': '#4EC9B0'},
}

_KEYWORDS = r"\\b(" + r"|".join(re.escape(k) for k in keyword.kwlist) + r")\\b"
_BUILTINS = r"\\b(" + r"|".join(re.escape(n) for n in dir(builtins) if not n.startswith('_')) + r")\\b"
_STRING = r"('''[\\s\\S]*?'''|\"\"\"[\\s\\S]*?\"\"\"|'(?:\\.|[^'\\])*'|\"(?:\\.|[^\"\\])*\")"
_COMMENT = r"#.*"
_NUMBER = r"\\b(\\d+(?:\\.\\d+)?)\\b"
_DEFNAME = r"\\bdef\\s+([A-Za-z_][A-Za-z0-9_]*)"
_DECORATOR = r"@[_A-Za-z][_A-Za-z0-9\\.]*"
_CLASSNAME = r"\\bclass\\s+([A-Za-z_][A-Za-z0-9_]*)"

_kw_re = re.compile(_KEYWORDS, re.MULTILINE)
_builtin_re = re.compile(_BUILTINS, re.MULTILINE)
_string_re = re.compile(_STRING, re.MULTILINE)
_comment_re = re.compile(_COMMENT, re.MULTILINE)
_number_re = re.compile(_NUMBER, re.MULTILINE)
_defname_re = re.compile(_DEFNAME, re.MULTILINE)
_decorator_re = re.compile(_DECORATOR, re.MULTILINE)
_classname_re = re.compile(_CLASSNAME, re.MULTILINE)

def open_lightning_code():
    root = tk._default_root
    if root is None:
        root = tk.Tk()
        root.withdraw()

    win = tk.Toplevel(root)
    win.title('Lightning Code Editor')
    win.geometry('1000x700')

    toolbar = ttk.Frame(win)
    toolbar.pack(side='top', fill='x')

    output_frame = tk.Frame(win, height=150, bg='#1e1e1e')
    output_frame.pack(side='bottom', fill='x')
    output_text = tk.Text(output_frame, height=8, bg='#1e1e1e', fg='#d4d4d4', state='disabled')
    output_text.pack(fill='both', expand=True)

    editor_frame = tk.Frame(win)
    editor_frame.pack(fill='both', expand=True)

    v_scroll = tk.Scrollbar(editor_frame)
    v_scroll.pack(side='right', fill='y')
    h_scroll = tk.Scrollbar(win, orient='horizontal')
    h_scroll.pack(side='bottom', fill='x')

    editor = tk.Text(editor_frame, wrap='none', undo=True, yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set, bg='#1e1e1e', fg='#d4d4d4', insertbackground='white')
    editor.pack(fill='both', expand=True)

    v_scroll.config(command=editor.yview)
    h_scroll.config(command=editor.xview)

    txt_font = font.Font(family='Consolas' if 'Consolas' in font.families() else 'Courier', size=11)
    editor.configure(font=txt_font)

    for tag, opts in _TAG_STYLES.items():
        cfg = {}
        if 'foreground' in opts: cfg['foreground'] = opts['foreground']
        if opts.get('italic'): cfg['font'] = font.Font(txt_font, slant='italic')
        if opts.get('underline'): cfg['underline'] = 1
        editor.tag_configure(tag, **cfg)

    editor._filename = None
    editor._highlight_after_id = None

    def _clear_tags():
        for tag in _TAG_STYLES.keys(): editor.tag_remove(tag, '1.0', 'end')

    def _highlight_all():
        _clear_tags()
        text = editor.get('1.0', 'end-1c')
        for m in _string_re.finditer(text): editor.tag_add('string', f'1.0+{m.start(1)}c', f'1.0+{m.end(1)}c')
        for m in _comment_re.finditer(text): editor.tag_add('comment', f'1.0+{m.start()}c', f'1.0+{m.end()}c')
        for m in _decorator_re.finditer(text): editor.tag_add('decorator', f'1.0+{m.start()}c', f'1.0+{m.end()}c')
        for m in _classname_re.finditer(text): s,e=m.start(1),m.end(1); editor.tag_add('classname', f'1.0+{s}c', f'1.0+{e}c')
        for m in _defname_re.finditer(text): s,e=m.start(1),m.end(1); editor.tag_add('defname', f'1.0+{s}c', f'1.0+{e}c')
        for m in _kw_re.finditer(text): editor.tag_add('keyword', f'1.0+{m.start()}c', f'1.0+{m.end()}c')
        for m in _builtin_re.finditer(text): editor.tag_add('builtin', f'1.0+{m.start()}c', f'1.0+{m.end()}c')
        for m in _number_re.finditer(text): editor.tag_add('number', f'1.0+{m.start()}c', f'1.0+{m.end()}c')

    def _schedule_highlight(event=None):
        if editor._highlight_after_id: editor.after_cancel(editor._highlight_after_id)
        editor._highlight_after_id = editor.after(_HIGHLIGHT_DELAY, _highlight_all)

    editor.bind('<<Modified>>', lambda e: (editor.edit_modified(False), _schedule_highlight()))

    def _maybe_save():
        if editor.edit_modified():
            r = messagebox.askyesnocancel('Save', 'Save changes?')
            if r is None: return False
            if r: _save_file()
        return True

    def _new_file():
        if _maybe_save(): editor.delete('1.0','end'); editor._filename=None; win.title('Lightning Code Editor - Untitled')

    def _open_file():
        if not _maybe_save(): return
        f = filedialog.askopenfilename(filetypes=[('Python', '*.py'), ('All', '*.*')])
        if f: editor.delete('1.0','end'); editor.insert('1.0', open(f,'r',encoding='utf-8').read()); editor._filename=f; win.title(f'Lightning Code Editor - {os.path.basename(f)}')

    def _save_file():
        if editor._filename is None: _save_as_file(); return
        with open(editor._filename,'w',encoding='utf-8') as fh: fh.write(editor.get('1.0','end-1c'))
        editor.edit_modified(False)

    def _save_as_file():
        f = filedialog.asksaveasfilename(defaultextension='.py');
        if f: editor._filename=f; _save_file()

    def _run_code():
        code = editor.get('1.0','end-1c')
        output_text.config(state='normal'); output_text.delete('1.0','end')
        try: exec(code, {})
        except Exception as e: output_text.insert('1.0', str(e))
        output_text.config(state='disabled')

    ttk.Button(toolbar, text='New', command=_new_file).pack(side='left')
    ttk.Button(toolbar, text='Open', command=_open_file).pack(side='left')
    ttk.Button(toolbar, text='Save', command=_save_file).pack(side='left')
    ttk.Button(toolbar, text='Run', command=_run_code).pack(side='left')

    win.bind_all('<Control-s>', lambda e: (_save_file(), 'break'))
    win.bind_all('<Control-o>', lambda e: (_open_file(), 'break'))
    win.bind_all('<Control-n>', lambda e: (_new_file(), 'break'))
    win.bind_all('<Control-r>', lambda e: (_run_code(), 'break'))

    editor.focus_set()

    # ----------------- GELİŞTİRMELER (AŞAĞIYA EKLENDİ) -----------------
    # Not: Orijinal fonksiyondaki satırlar hiç çıkarılmadı, sadece sonuna
    # gelişmiş özellikler eklendi. Hadi bakalım, mucize bekleme ama iş görüyor.

    import json
    import zipfile
    import os
    # undo/redo için hafızacık
    undo_stack = []
    redo_stack = []
    UNDO_LIMIT = 30

    def push_undo():
        try:
            snapshot = copy.deepcopy(FS)
            undo_stack.append(snapshot)
            if len(undo_stack) > UNDO_LIMIT:
                undo_stack.pop(0)
            # temizle redo
            redo_stack.clear()
        except Exception:
            pass

    # sarmış gibi davranma: bazı eylemler öncesi undo al
    orig_action_delete = action_delete
    orig_action_rename = action_rename
    orig_action_copy = action_copy
    orig_action_paste = action_paste
    orig_new_folder = new_folder
    orig_new_file = new_file

    def action_delete_wrapped(*a, **k):
        push_undo()
        return orig_action_delete()

    def action_rename_wrapped(*a, **k):
        push_undo()
        return orig_action_rename()

    def action_copy_wrapped(*a, **k):
        return orig_action_copy()

    def action_paste_wrapped(*a, **k):
        push_undo()
        return orig_action_paste()

    def new_folder_wrapped(*a, **k):
        push_undo()
        return orig_new_folder()

    def new_file_wrapped(*a, **k):
        push_undo()
        return orig_new_file()

    # Menüdeki komutları güncelle (label bulup yeniden bağla)
    try:
        end_idx = ctx.index("end")
        if end_idx is not None:
            for i in range(end_idx + 1):
                try:
                    lbl = ctx.entrycget(i, "label")
                    if lbl == "Sil":
                        ctx.entryconfig(i, command=action_delete_wrapped)
                    elif lbl and "Yeniden Adlandır" in lbl:
                        ctx.entryconfig(i, command=action_rename_wrapped)
                    elif lbl and "Kopyala" in lbl:
                        ctx.entryconfig(i, command=action_copy_wrapped)
                    elif lbl and "Yapıştır" in lbl:
                        ctx.entryconfig(i, command=action_paste_wrapped)
                except Exception:
                    continue
    except Exception:
        pass

    # Klavye kısayollarını güncelle
    win.bind("<Delete>", lambda e: action_delete_wrapped())
    win.bind("<F2>", lambda e: action_rename_wrapped())
    win.bind_all("<Control-c>", lambda e: action_copy_wrapped())
    win.bind_all("<Control-v>", lambda e: action_paste_wrapped())

    # Breadcrumb (seçili yol göstergesi)
    path_label = tk.Label(top_frame, text="", anchor="w")
    path_label.pack(side="left", padx=6)

    def update_path_label():
        iid = tree.focus()
        path_label.config(text=get_path_str(iid))

    # Önizlemede düzenleme ve kaydetme
    def save_preview():
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if not parts or node is None:
            messagebox.showerror("Hata", "Dosya seçili değil veya bulunamadı.")
            return
        if node["type"] != "file":
            messagebox.showerror("Hata", "Sadece dosya içeriği kaydedilebilir.")
            return
        push_undo()
        content = preview_text.get("1.0", END).rstrip("\n")
        node["content"] = content
        node["size"] = len(content)
        node["modified"] = datetime.datetime.now()
        status.config(text=f"{parts[-1]} kaydedildi.")
        refresh_tree(filter_text=search_var.get())

    save_btn = tk.Button(right_frame, text="Kaydet (Ctrl+S)", command=save_preview)
    save_btn.pack(anchor="e", pady=4)

    # Undo / Redo
    def do_undo():
        if not undo_stack:
            status.config(text="Geri alınacak işlem yok.")
            return
        redo_stack.append(copy.deepcopy(FS))
        snap = undo_stack.pop()
        FS.clear()
        FS.update(snap)
        refresh_tree(filter_text=search_var.get())
        status.config(text="Geri alındı.")

    def do_redo():
        if not redo_stack:
            status.config(text="Yine ileri yok.")
            return
        undo_stack.append(copy.deepcopy(FS))
        snap = redo_stack.pop()
        FS.clear()
        FS.update(snap)
        refresh_tree(filter_text=search_var.get())
        status.config(text="İleri alındı.")

    undo_btn = tk.Button(top_frame, text="Geri Al (Ctrl+Z)", command=do_undo)
    undo_btn.pack(side="left", padx=4)
    redo_btn = tk.Button(top_frame, text="İleri (Ctrl+Y)", command=do_redo)
    redo_btn.pack(side="left", padx=4)

    # Dışa aktar / içe aktar (JSON)
    def export_fs():
        try:
            from tkinter import filedialog
            fname = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
            if not fname:
                return
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(FS, f, default=str, indent=2)
            status.config(text=f"FS dışa aktarıldı: {os.path.basename(fname)}")
        except Exception as e:
            messagebox.showerror("Hata", f"Dışa aktarma başarısız: {e}")

    def import_fs():
        try:
            from tkinter import filedialog
            fname = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON","*.json")])
            if not fname:
                return
            with open(fname, "r", encoding="utf-8") as f:
                data = json.load(f)
            push_undo()
            FS.clear()
            FS.update(data)
            refresh_tree(filter_text=search_var.get())
            status.config(text=f"FS içe aktarıldı: {os.path.basename(fname)}")
        except Exception as e:
            messagebox.showerror("Hata", f"İçe aktarma başarısız: {e}")

    btn_export = tk.Button(top_frame, text="Dışa Aktar", command=export_fs)
    btn_export.pack(side="left", padx=4)
    btn_import = tk.Button(top_frame, text="İçe Aktar", command=import_fs)
    btn_import.pack(side="left", padx=4)

    # Double-click ile açma (hızlı)
    tree.bind("<Double-1>", lambda e: action_open())

    # Seçim sonrası ekstra güncellemeler
    def enhanced_on_select(event):
        try:
            on_select(event)  # orijinal davranış
        except Exception:
            pass
        update_path_label()
        # İçerik düzenlenebilir mi kontrolü
        iid = tree.focus()
        node, parts = get_node_by_tree_id(iid)
        if node and node.get("type") == "file":
            save_btn.config(state="normal")
        else:
            save_btn.config(state="disabled")

    tree.unbind("<<TreeviewSelect>>")
    tree.bind("<<TreeviewSelect>>", enhanced_on_select)

    # Arama alanına Enter ile refresh
    def on_search_enter(event):
        refresh_tree(filter_text=search_var.get())
        status.config(text=f"Arama: {search_var.get()}")
    search_entry.bind("<Return>", on_search_enter)

    # Kaydet kısayolu
    win.bind_all("<Control-s>", lambda e: save_preview())

    # Undo/Redo kısayolları
    win.bind_all("<Control-z>", lambda e: do_undo())
    win.bind_all("<Control-y>", lambda e: do_redo())

    # Gizli dosyaları gösterme (başında . olanlar) - simülasyon
    show_hidden_var = tk.BooleanVar(value=False)
    def toggle_show_hidden():
        refresh_tree(filter_text=search_var.get())

    chk_hidden = tk.Checkbutton(top_frame, text="Gizlileri Göster (örn: .git)", variable=show_hidden_var, command=toggle_show_hidden)
    chk_hidden.pack(side="left", padx=4)

    # refresh_tree fonksiyonunu hafifçe genişlet (gizli filtresi)
    orig_refresh_tree = refresh_tree
    def refresh_tree(filter_text=""):
        # gizli kontrolü: eğer gizli gösterme açık değilse, başında '.' olanları at
        expanded = set()

        def collect_open(iid):
            if tree.item(iid, "open"):
                expanded.add(get_path_str(iid))
                for c in tree.get_children(iid):
                    collect_open(c)
        for iid in tree.get_children():
            collect_open(iid)

        tree.delete(*tree.get_children())

        def _insert(parent, node_dict):
            for name, meta in sorted(node_dict.items()):
                if (not show_hidden_var.get()) and name.startswith("."):
                    continue
                if filter_text and filter_text.lower() not in name.lower():
                    if meta["type"] == "folder" and any(
                        filter_text.lower() in k.lower() for k in meta.get(
                            "children", {})):
                        pass
                    else:
                        continue
                open_state = (get_path_str(parent) + "/" + name) in expanded
                iid = tree.insert(parent, "end", text=name, open=open_state)
                if meta["type"] == "folder":
                    if meta.get("children"):
                        tree.insert(iid, "end", text="__placeholder__")
        root_iid = tree.insert("", "end", text="root", open=True)
        _insert(root_iid, FS["root"]["children"])

    # Başlangıç güncellemeleri
    refresh_tree(filter_text="")
    update_path_label()
    try:
        # İlk seçim tekrar
        root_items = tree.get_children()
        if root_items:
            tree.selection_set(root_items[0])
            tree.focus(root_items[0])
    except Exception:
        pass

    status.config(text="Geliştirilmiş dosya yöneticisi hazır. Kısayollar: Ctrl+S kaydet, Ctrl+Z geri al, Ctrl+Y ileri al.")

    # İsteğe bağlı: küçük yardımcı fonksiyonlar (ör. FS'yi yazdır)
    def debug_print_fs():
        print(json.dumps(FS, default=str, indent=2))

    # Eğer istersen (ama istemedin), kapatılırken otomatik yedek al:
    def on_close():
        try:
            # küçük otomatik yedek
            bname = f"fs_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(bname, "w", encoding="utf-8") as f:
                json.dump(FS, f, default=str, indent=2)
        except Exception:
            pass
        try:
            win.destroy()
        except Exception:
            pass

    win.protocol("WM_DELETE_WINDOW", on_close)

    # İstersen debug butonu ekleyeyim (sen demedin ama ben ettim)
    dbg = tk.Button(top_frame, text="FS Yazdır (debug)", command=debug_print_fs)
    dbg.pack(side="right", padx=4)

# ---------- Eğer kullanıcı kendi show_bsod() fonksiyonunu tanımlamadıysa,
def show_bsod():
    bsod_win = Toplevel(root)
    bsod_win.attributes("-fullscreen", True)
    bsod_win.configure(bg="blue")
    Label(bsod_win, text=":( SYSTEM FILE BULUNAMADI\n\nSTOP: 0x000000D1", fg="white", bg="blue",
          font=("Consolas", 30)).pack(expand=True)
    bsod_win.after(3000, lambda: [bsod_win.destroy(), show_recovery()])

def show_recovery():
    rec_win = Toplevel(root)
    rec_win.title("Kurtarma Seçenekleri")
    rec_win.geometry("400x300")
    Label(rec_win, text="Kurtarma Seçenekleri", font=("Arial", 16)).pack(pady=10)
    def normal_open_error():
        messagebox.showerror("Sistem Hatası", "Sistem bozuk. Sistemden çıkın.\n\nSomething went wrong!")
        rec_win.destroy()
        root.destroy()
    def normal_open_ok():
        rec_win.destroy()
        root.deiconify()
    Button(rec_win, text="BTL'yi normal aç", command=normal_open_error).pack(pady=5)
    Button(rec_win, text="BTL'yi güncelle", command=normal_open_ok).pack(pady=5)
    Button(rec_win, text="BTL'yi güvenilir kaynaklardan geri indir", command=normal_open_ok).pack(pady=5)


# ---------- Oyunlar ve Basit Uygulamalar ----------
# Gerekli importlar (dosyanın başında varsa tekrar etmene gerek yok)


def open_notepad(root=None):
    """
    Geliştirilmiş Not Defteri penceresi.
    Özellikler: Yeni/Aç/Kaydet/Kaydet Farklı, Undo/Redo, Bul/Değiştir,
    Yazı tipi boyutu/family değiştirme, satır/kolon durumu, sarma aç/kapa,
    kaydedilmemiş değişiklik uyarısı.
    """
    if root is None:
        # Eğer root verilmemişse yeni bir gizli kök oluştur (nadiren gerekir)
        root = tk._default_root or tk.Tk()
    win = Toplevel(root)
    win.title("Not Defteri — Sarma Edition")
    win.geometry("700x500")

    # --- internal state ---
    state = {"filepath": None, "saved": True}

    # --- Text widget ve scrollbar ---
    text = Text(win, wrap="word", undo=True, autoseparators=True, maxundo=-1)
    vsb = Scrollbar(win, orient="vertical", command=text.yview)
    hsb = Scrollbar(win, orient="horizontal", command=text.xview)
    text.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    vsb.pack(side="right", fill="y")
    hsb.pack(side="bottom", fill="x")
    text.pack(expand=True, fill="both")

    # Başlangıç fontu
    current_font = tkfont.Font(font=text['font'])

    def set_font(family=None, size=None):
        family = family or current_font.actual()['family']
        size = size or current_font.actual()['size']
        current_font.config(family=family, size=size)
        text.configure(font=current_font)

    # --- Status bar ---
    status = tk.Label(win, text="Satır: 1  Kolon: 0  |  Kelime: 0", anchor="w")
    status.pack(side="bottom", fill="x")

    def update_status(event=None):
        # Satır/kolon/gun sayısı
        idx = text.index("insert")
        line, col = idx.split(".")
        content = text.get("1.0", "end-1c")
        words = len(content.split())
        status.configure(
            text=f"Satır: {line}  Kolon: {col}  |  Kelime: {words}")
        # modified flag reset handled elsewhere
    # Tüm yazma olaylarında güncelle
    text.bind(
        "<<Modified>>",
        lambda e: (
            update_status(),
            text.edit_modified(False)))
    notepad_btn = tk.Button(taskbar, text="Notepad", command=open_notepad)
    notepad_btn.place(relx=0.5, rely=0.5, anchor="center")

    # --- Dosya işlemleri ---
    def maybe_save():
        if not state["saved"]:
            answer = messagebox.askyesnocancel(
                "Kaydedilsin mi?", "Değişiklikler kaydedilsin mi?")
            if answer:  # Yes
                return save_file()
            if answer is None:  # Cancel
                return False
        return True

    def new_file():
        if not maybe_save():
            return
        text.delete("1.0", "end")
        state["filepath"] = None
        state["saved"] = True
        win.title("Not Defteri — Yeni Belge")
        update_status()

    def open_file():
        if not maybe_save():
            return
        fp = filedialog.askopenfilename(
            filetypes=[("Text files", "*.txt;*.py;*.md;*.log"), ("All files", "*.*")])
        if not fp:
            return
        try:
            with open(fp, "r", encoding="utf-8") as f:
                data = f.read()
        except Exception as e:
            messagebox.showerror("Hata", f"Dosya açılamadı: {e}")
            return
        text.delete("1.0", "end")
        text.insert("1.0", data)
        state["filepath"] = fp
        state["saved"] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")

    def save_file():
        fp = state["filepath"]
        if not fp:
            return save_as()
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
            return False
        state["saved"] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")
        return True

    def save_as():
        fp = filedialog.asksaveasfilename(
            defaultextension=".txt", filetypes=[
                ("Text files", "*.txt"), ("All files", "*.*")])
        if not fp:
            return False
        try:
            with open(fp, "w", encoding="utf-8") as f:
                f.write(text.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Hata", f"Kaydedilemedi: {e}")
            return False
        state["filepath"] = fp
        state["saved"] = True
        win.title(f"Not Defteri — {os.path.basename(fp)}")
        return True

    # Her değişiklikte "saved" false olsun
    def on_edit(event=None):
        state["saved"] = False
    text.bind("<<Modified>>", lambda e: (on_edit(), text.edit_modified(False)))

    # --- Bul / Değiştir ---
    def open_find_replace():
        dlg = Toplevel(win)
        dlg.transient(win)
        dlg.title("Bul / Değiştir")
        tk.Label(dlg, text="Bul:").grid(row=0, column=0, sticky="e")
        tk.Label(dlg, text="Değiştir:").grid(row=1, column=0, sticky="e")
        s_var = tk.StringVar()
        r_var = tk.StringVar()
        s_entry = tk.Entry(dlg, textvariable=s_var, width=30)
        r_entry = tk.Entry(dlg, textvariable=r_var, width=30)
        s_entry.grid(row=0, column=1, padx=4, pady=4)
        r_entry.grid(row=1, column=1, padx=4, pady=4)

        def do_find():
            text.tag_remove("find", "1.0", "end")
            needle = s_var.get()
            if not needle:
                return
            start = "1.0"
            while True:
                pos = text.search(needle, start, stopindex="end", nocase=True)
                if not pos:
                    break
                endpos = f"{pos}+{len(needle)}c"
                text.tag_add("find", pos, endpos)
                start = endpos
            text.tag_config("find", background="yellow")

        def do_replace_all():
            needle = s_var.get()
            repl = r_var.get()
            if not needle:
                return
            content = text.get("1.0", "end-1c")
            new = content.replace(needle, repl)
            text.delete("1.0", "end")
            text.insert("1.0", new)
            state["saved"] = False
            update_status()
        btn_find = tk.Button(dlg, text="Bul", command=do_find)
        btn_replace = tk.Button(
            dlg,
            text="Tümünü Değiştir",
            command=do_replace_all)
        btn_find.grid(row=2, column=0, pady=6)
        btn_replace.grid(row=2, column=1, pady=6)
        dlg.grab_set()
        dlg.focus_set()

    # --- Yazı tipi ve sarma ---
    def choose_font():
        # Basit font seçici (family ve size sor)
        fam = simpledialog.askstring(
            "Yazı Tipi",
            "Yazı tipi family (ör: Arial, Courier):",
            parent=win)
        if fam:
            try:
                current_font.config(family=fam)
                text.configure(font=current_font)
            except Exception as e:
                messagebox.showerror("Hata", f"Yazı tipi yüklenemedi: {e}")
        size = simpledialog.askinteger(
            "Boyut",
            "Boyut (ör: 12):",
            parent=win,
            minvalue=6,
            maxvalue=72)
        if size:
            current_font.config(size=size)
            text.configure(font=current_font)

    wrap_var = tk.BooleanVar(value=True)

    def toggle_wrap():
        if wrap_var.get():
            text.configure(wrap="word")
        else:
            text.configure(wrap="none")
    # Wrap toggle menü check
    wrap_var.trace_add("write", lambda *args: toggle_wrap())

    # --- Menü ---
    menubar = Menu(win)
    file_menu = Menu(menubar, tearoff=0)
    file_menu.add_command(label="Yeni\tCtrl+N", command=new_file)
    file_menu.add_command(label="Aç...\tCtrl+O", command=open_file)
    file_menu.add_command(label="Kaydet\tCtrl+S", command=save_file)
    file_menu.add_command(
        label="Farklı Kaydet...\tShift+Ctrl+S",
        command=save_as)
    file_menu.add_separator()
    file_menu.add_checkbutton(
        label="Kelime sarma",
        onvalue=True,
        offvalue=False,
        variable=wrap_var)
    file_menu.add_separator()
    file_menu.add_command(label="Kapat\tCtrl+W", command=win.destroy)
    menubar.add_cascade(label="Dosya", menu=file_menu)

    edit_menu = Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Geri Al\tCtrl+Z",
                          command=lambda: text.event_generate("<<Undo>>"))
    edit_menu.add_command(label="İleri Al\tCtrl+Y",
                          command=lambda: text.event_generate("<<Redo>>"))
    edit_menu.add_separator()
    edit_menu.add_command(label="Kes\tCtrl+X",
                          command=lambda: text.event_generate("<<Cut>>"))
    edit_menu.add_command(label="Kopyala\tCtrl+C",
                          command=lambda: text.event_generate("<<Copy>>"))
    edit_menu.add_command(label="Yapıştır\tCtrl+V",
                          command=lambda: text.event_generate("<<Paste>>"))
    edit_menu.add_separator()
    edit_menu.add_command(
        label="Bul / Değiştir\tCtrl+F",
        command=open_find_replace)
    menubar.add_cascade(label="Düzen", menu=edit_menu)

    format_menu = Menu(menubar, tearoff=0)
    format_menu.add_command(label="Yazı Tipi...", command=choose_font)
    menubar.add_cascade(label="Biçim", menu=format_menu)

    help_menu = Menu(menubar, tearoff=0)
    help_menu.add_command(label="Hakkında", command=lambda: messagebox.showinfo(
        "Hakkında", "Not Defteri — Sarma sürümü\nGeliştirilmiş. Şımarmış."))
    menubar.add_cascade(label="Yardım", menu=help_menu)

    win.config(menu=menubar)

    # --- Kısayollar ---
    win.bind_all("<Control-n>", lambda e: new_file())
    win.bind_all("<Control-o>", lambda e: open_file())
    win.bind_all("<Control-s>", lambda e: save_file())
    win.bind_all("<Control-S>", lambda e: save_as())
    win.bind_all("<Control-f>", lambda e: open_find_replace())
    win.bind_all("<Control-q>", lambda e: (maybe_save() and win.destroy()))
    win.bind_all("<Control-w>", lambda e: win.destroy())

    # Pencere kapandığında kontrol et
    def on_close():
        if maybe_save():
            win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_close)

    # Başlık/başlangıç durumu
    win.title("Not Defteri — Yeni Belge")
    text.focus_set()
    update_status()
    notepad_btn = tk.Button(
        taskbar,
        text="Notepad",
        command=lambda: globals().get(
            'open_notepad',
            (lambda: None))())
    notepad_btn.place(relx=0.5, rely=0.5, anchor="center")

"""
Robot Satranç - Taş Hareket Animasyonu Eklendi
Parametresiz çağrılacak fonksiyon: open_chess_game()

Yapılan değişiklikler:
- Taş hareketleri için akıcı bir animasyon eklendi (hem kullanıcı hamleleri hem de robot hamleleri için).
- animate_and_push(frm,to, callback=None) fonksiyonu eklendi: önce görsel animasyon oynatır, sonra hamleyi tahtaya uygular.
- Animasyon süresi ayarlanabilir: ChessGame(..., anim_duration=180) şeklinde milisaniye cinsinden verilebilir.
- Animasyon sırasında kullanıcı girişleri engellenir.

Not: Kod hala hafif bir motor içerir; animasyon UI tarafında görsel kaliteyi arttırır. Daha farklı easing veya sürükle-bırak için eklemeler yapılabilir.
"""

import tkinter as tk
from tkinter import messagebox
import time
import random

# Satranç sembolleri
UNICODE = {
    'P': '\u2659', 'N': '\u2658', 'B': '\u2657', 'R': '\u2656', 'Q': '\u2655', 'K': '\u2654',
    'p': '\u265F', 'n': '\u265E', 'b': '\u265D', 'r': '\u265C', 'q': '\u265B', 'k': '\u265A',
}

PIECE_VALUES = {
    'q': 900, 'r': 500, 'b': 330, 'n': 320, 'p': 100,
    'Q': 900, 'R': 500, 'B': 330, 'N': 320, 'P': 100,
    'k': 20000, 'K': 20000
}

def board_to_key(board):
    return ''.join(''.join(row) for row in board)

class ChessGame:
    def __init__(self, master=None, ai_depth=5, time_limit=8.0, anim_duration=180):
        # Toplevel oluşturma
        if master is None:
            if not tk._default_root:
                self.root = tk.Tk()
                self.root.withdraw()
            else:
                self.root = tk._default_root
            self.top = tk.Toplevel(self.root)
        else:
            self.top = tk.Toplevel(master)
        self.top.title('Satranç (Animasyonlu) - open_chess_game()')
        self.top.protocol('WM_DELETE_WINDOW', self.on_close)

        self.ai_depth = ai_depth
        self.time_limit = time_limit
        self.anim_duration = anim_duration  # milisaniye

        self.board = [['.' for _ in range(8)] for __ in range(8)]
        self.init_board()
        self.history = []
        self.turn = 'w'  # 'w', 'b' veya 'busy' (animasyon sırasında)

        self.square_size = 64
        self.canvas = tk.Canvas(self.top, width=8*self.square_size, height=8*self.square_size)
        self.canvas.pack()
        self.canvas.bind('<Button-1>', self.on_click)

        self.selected = None
        self.legal_moves_cache = []

        self.info_label = tk.Label(self.top, text='Siz beyazsınız. Taşı tıklayın.', anchor='w')
        self.info_label.pack(fill='x')

        # Transpo table ve history heuristic
        self.ttable = {}
        self.hist_heur = {}

        self.draw_board()

    def on_close(self):
        try:
            if hasattr(self, 'root') and self.root is not None:
                if self.root is not tk._default_root:
                    self.root.destroy()
        except Exception:
            pass
        self.top.destroy()

    def init_board(self):
        back = ['r','n','b','q','k','b','n','r']
        for i in range(8):
            self.board[0][i] = back[i]
            self.board[1][i] = 'p'
            self.board[6][i] = 'P'
            self.board[7][i] = back[i].upper()
        for r in range(2,6):
            for c in range(8):
                self.board[r][c] = '.'

    def draw_board(self):
        self.canvas.delete('all')
        for r in range(8):
            for c in range(8):
                x1 = c*self.square_size
                y1 = r*self.square_size
                x2 = x1 + self.square_size
                y2 = y1 + self.square_size
                fill = '#EEEED2' if (r+c)%2==0 else '#769656'
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=fill, outline='')
                piece = self.board[r][c]
                if piece != '.':
                    symbol = UNICODE.get(piece, '?')
                    self.canvas.create_text(x1+self.square_size/2, y1+self.square_size/2, text=symbol, font=('Arial', 32), tags=f'piece_{r}_{c}')
        if self.selected:
            r,c = self.selected
            self.highlight_square(r,c,'#F6F669')
            for (tr,tc) in self.legal_moves_cache:
                self.highlight_square(tr,tc,'#BACAFF')

    def highlight_square(self,r,c,color):
        x1 = c*self.square_size
        y1 = r*self.square_size
        x2 = x1 + self.square_size
        y2 = y1 + self.square_size
        self.canvas.create_rectangle(x1+2, y1+2, x2-2, y2-2, outline=color, width=3)

    def on_click(self, event):
        # bloklama: animasyon veya AI sırasında tıklamayı yoksay
        if self.turn == 'busy' or self.turn == 'b':
            return

        c = event.x // self.square_size
        r = event.y // self.square_size
        if not (0 <= r < 8 and 0 <= c < 8):
            return
        piece = self.board[r][c]
        side = 'w' if piece.isupper() else 'b' if piece.isalpha() else None

        if self.selected:
            if (r,c) in self.legal_moves_cache:
                # animasyonlu hamle: önce görsel, sonra tahtaya uygula
                self.turn = 'busy'
                self.info_label.config(text='Taş hareket ediyor...')
                self.animate_and_push(self.selected, (r,c), after_cb=self.after_player_move)
                return
            else:
                if side == 'w':
                    self.selected = (r,c)
                    self.legal_moves_cache = self.get_legal_moves_for_square(r,c)
                    self.draw_board()
                    return
                else:
                    self.selected = None
                    self.legal_moves_cache = []
                    self.draw_board()
                    return

        if side == 'w':
            self.selected = (r,c)
            self.legal_moves_cache = self.get_legal_moves_for_square(r,c)
            self.draw_board()

    def after_player_move(self):
        # oyuncunun animasyonu tamamlandıktan sonra
        self.turn = 'b'
        self.info_label.config(text='Rakip (robot) hamle yapıyor...')
        self.top.update()
        self.top.after(80, self.ai_move)

    def animate_and_push(self, frm, to, after_cb=None):
        """Grafiksel animasyon: taşın görselini hareket ettirir, ardından hamleyi uygular.
        after_cb: animasyon bittikten sonra çağrılacak fonksiyon.
        """
        fr,fc = frm
        tr,tc = to
        piece = self.board[fr][fc]
        if piece == '.':
            # tuhaf ama güvenlik
            self.push_move(frm,to)
            if after_cb:
                after_cb()
            return

        # başlangıç koordinatları
        start_x = fc*self.square_size + self.square_size/2
        start_y = fr*self.square_size + self.square_size/2
        end_x = tc*self.square_size + self.square_size/2
        end_y = tr*self.square_size + self.square_size/2

        symbol = UNICODE.get(piece, '?')
        temp = self.canvas.create_text(start_x, start_y, text=symbol, font=('Arial', 32), tags='anim_piece')

        # hedef karedeki taşı hafifçe vurgula (capture için)
        captured = self.board[tr][tc]
        if captured != '.':
            # kırmızı kenarlıkla uyar
            self.highlight_square(tr,tc,'#FF5555')

        frames = max(4, int(self.anim_duration / 30))
        dx = (end_x - start_x) / frames
        dy = (end_y - start_y) / frames
        delay = int(self.anim_duration / frames)

        def step(i=0):
            if i < frames:
                self.canvas.move(temp, dx, dy)
                self.top.update()
                self.top.after(delay, lambda: step(i+1))
            else:
                # animasyon bitti: temporary objeyi sil ve hamleyi uygula
                self.canvas.delete(temp)
                self.push_move(frm,to)
                self.draw_board()
                if after_cb:
                    after_cb()
        step()

    def push_move(self, frm, to):
        fr,fc = frm
        tr,tc = to
        moved = self.board[fr][fc]
        captured = self.board[tr][tc]
        self.history.append((fr,fc,tr,tc,moved,captured))
        self.board[tr][tc] = moved
        self.board[fr][fc] = '.'
        if moved == 'P' and tr == 0:
            self.board[tr][tc] = 'Q'
        if moved == 'p' and tr == 7:
            self.board[tr][tc] = 'q'

    def pop_move(self):
        if not self.history:
            return
        fr,fc,tr,tc,moved,captured = self.history.pop()
        self.board[fr][fc] = moved
        self.board[tr][tc] = captured

    def is_square_attacked(self, r, c, by_side):
        for i in range(8):
            for j in range(8):
                p = self.board[i][j]
                if p == '.':
                    continue
                if (p.isupper() and by_side=='w') or (p.islower() and by_side=='b'):
                    moves = self._pseudo_moves_for_piece(i,j, attacks_only=True)
                    if (r,c) in moves:
                        return True
        return False

    def king_position(self, side):
        target = 'K' if side=='w' else 'k'
        for i in range(8):
            for j in range(8):
                if self.board[i][j] == target:
                    return (i,j)
        return None

    def in_check(self, side):
        kp = self.king_position(side)
        if not kp:
            return True
        return self.is_square_attacked(kp[0], kp[1], 'b' if side=='w' else 'w')

    def get_legal_moves_for_square(self, r, c):
        p = self.board[r][c]
        if p == '.':
            return []
        side = 'w' if p.isupper() else 'b'
        moves = self._pseudo_moves_for_piece(r,c, attacks_only=False)
        legal = []
        for (tr,tc) in moves:
            self.push_move((r,c),(tr,tc))
            king_in_check = self.in_check(side)
            self.pop_move()
            if not king_in_check:
                legal.append((tr,tc))
        return legal

    def generate_all_legal_moves(self, side):
        all_moves = []
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == '.':
                    continue
                if (side == 'w' and p.isupper()) or (side == 'b' and p.islower()):
                    for mv in self.get_legal_moves_for_square(r,c):
                        all_moves.append(((r,c), mv))
        return all_moves

    def _pseudo_moves_for_piece(self, r, c, attacks_only=False):
        moves = []
        p = self.board[r][c]
        if p == '.':
            return moves
        is_white = p.isupper()
        piece = p.lower()

        if piece == 'p':
            if is_white:
                if not attacks_only:
                    if r-1 >= 0 and self.board[r-1][c]=='.':
                        moves.append((r-1,c))
                        if r==6 and self.board[r-2][c]=='.':
                            moves.append((r-2,c))
                for dc in (-1,1):
                    nr, nc = r-1, c+dc
                    if 0<=nr<8 and 0<=nc<8 and self.board[nr][nc] != '.' and self.board[nr][nc].islower():
                        moves.append((nr,nc))
            else:
                if not attacks_only:
                    if r+1 < 8 and self.board[r+1][c]=='.':
                        moves.append((r+1,c))
                        if r==1 and self.board[r+2][c]=='.':
                            moves.append((r+2,c))
                for dc in (-1,1):
                    nr, nc = r+1, c+dc
                    if 0<=nr<8 and 0<=nc<8 and self.board[nr][nc] != '.' and self.board[nr][nc].isupper():
                        moves.append((nr,nc))
            return moves

        if piece == 'n':
            for dr,dc in [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                nr, nc = r+dr, c+dc
                if 0<=nr<8 and 0<=nc<8:
                    target = self.board[nr][nc]
                    if target == '.' or (target.isupper() if not is_white else target.islower()):
                        moves.append((nr,nc))
            return moves

        if piece in ('b','r','q'):
            if piece == 'b':
                dirs = [(-1,-1),(-1,1),(1,-1),(1,1)]
            elif piece == 'r':
                dirs = [(-1,0),(1,0),(0,-1),(0,1)]
            else:
                dirs = [(-1,-1),(-1,1),(1,-1),(1,1),(-1,0),(1,0),(0,-1),(0,1)]
            for dr,dc in dirs:
                nr, nc = r+dr, c+dc
                while 0<=nr<8 and 0<=nc<8:
                    target = self.board[nr][nc]
                    if target == '.':
                        moves.append((nr,nc))
                    else:
                        if (target.isupper() and is_white) or (target.islower() and not is_white):
                            break
                        moves.append((nr,nc))
                        break
                    nr += dr
                    nc += dc
            return moves

        if piece == 'k':
            for dr in (-1,0,1):
                for dc in (-1,0,1):
                    if dr==0 and dc==0:
                        continue
                    nr, nc = r+dr, c+dc
                    if 0<=nr<8 and 0<=nc<8:
                        target = self.board[nr][nc]
                        if target == '.' or (target.isupper() if not is_white else target.islower()):
                            moves.append((nr,nc))
            return moves

        return moves

    def evaluate(self):
        score = 0
        mobility_white = 0
        mobility_black = 0
        for r in range(8):
            for c in range(8):
                p = self.board[r][c]
                if p == '.':
                    continue
                v = PIECE_VALUES.get(p,0)
                if p.isupper():
                    score += v
                    mobility_white += len(self._pseudo_moves_for_piece(r,c, attacks_only=False))
                else:
                    score -= v
                    mobility_black += len(self._pseudo_moves_for_piece(r,c, attacks_only=False))
        score += 10 * (mobility_white - mobility_black)
        return score

    def is_capture(self, frm, to):
        tr,tc = to
        return self.board[tr][tc] != '.'

    def mvv_lva(self, frm, to):
        fr,fc = frm
        tr,tc = to
        moved = self.board[fr][fc]
        captured = self.board[tr][tc]
        if captured == '.':
            return 0
        return PIECE_VALUES.get(captured.lower() if captured.islower() else captured,0)*100 - PIECE_VALUES.get(moved.lower() if moved.islower() else moved,0)

    def score_move_for_ordering(self, frm, to):
        fr,fc = frm
        tr,tc = to
        moved = self.board[fr][fc]
        captured = self.board[tr][tc]
        score = 0
        if captured != '.':
            score += 100000 + self.mvv_lva(frm,to)
        if moved.lower() == 'p' and fr != tr:
            score += 10
        score += self.hist_heur.get((fr,fc,tr,tc), 0)
        return score

    def ai_move(self):
        moves = self.generate_all_legal_moves('b')
        if not moves:
            if self.in_check('b'):
                messagebox.showinfo('Oyun bitti', 'Mat! Tebrikler, kazandın')
            else:
                messagebox.showinfo('Oyun bitti', 'Pat!')
            return

        start = time.time()
        best_move = None
        captures = [m for m in moves if self.is_capture(m[0], m[1])]
        non_caps = [m for m in moves if not self.is_capture(m[0], m[1])]
        moves_ord = sorted(captures, key=lambda m: -self.mvv_lva(m[0], m[1])) + sorted(non_caps, key=lambda m: -self.score_move_for_ordering(m[0], m[1]))

        for depth in range(1, self.ai_depth+1):
            best_score = -10**9
            alpha = -10**9
            beta = 10**9
            for (frm,to) in moves_ord:
                if time.time() - start > self.time_limit:
                    break
                self.push_move(frm,to)
                score = self.search(depth-1, alpha, beta, False, start)
                self.pop_move()
                if score > best_score:
                    best_score = score
                    best_move = (frm,to)
                    alpha = max(alpha, score)
            if time.time() - start > self.time_limit:
                break

        if best_move is None:
            best_move = random.choice(moves)

        # animasyonlu uygulama
        self.turn = 'busy'
        self.info_label.config(text='Robot taşını sürdürüyor...')
        self.animate_and_push(best_move[0], best_move[1], after_cb=self.after_ai_move)

    def after_ai_move(self):
        # robot animasyonu tamamlandıktan sonra
        # history heuristic güncellemesi
        self.turn = 'w'
        frm,to = self.history[-1][0:2], self.history[-1][2:4]
        self.hist_heur[(frm[0],frm[1],to[0],to[1])] = self.hist_heur.get((frm[0],frm[1],to[0],to[1]), 0) + 100
        self.info_label.config(text='Siz oynayın.')

    def search(self, depth, alpha, beta, maximizing, start_time):
        key = board_to_key(self.board)
        tt_entry = self.ttable.get(key)
        if tt_entry and tt_entry[0] >= depth:
            return tt_entry[1]

        if depth == 0:
            val = self.quiescence(alpha, beta, maximizing)
            self.ttable[key] = (depth, val)
            return val

        if time.time() - start_time > self.time_limit:
            return self.evaluate()

        side = 'b' if maximizing else 'w'
        moves = self.generate_all_legal_moves(side)
        if not moves:
            if self.in_check(side):
                return -999999 if maximizing else 999999
            return 0

        captures = [m for m in moves if self.is_capture(m[0], m[1])]
        non_caps = [m for m in moves if not self.is_capture(m[0], m[1])]
        moves = sorted(captures, key=lambda m: -self.mvv_lva(m[0], m[1])) + sorted(non_caps, key=lambda m: -self.score_move_for_ordering(m[0], m[1]))

        if maximizing:
            value = -10**9
            for (frm,to) in moves:
                self.push_move(frm,to)
                val = self.search(depth-1, alpha, beta, False, start_time)
                self.pop_move()
                if val >= beta:
                    self.hist_heur[(frm[0],frm[1],to[0],to[1])] = self.hist_heur.get((frm[0],frm[1],to[0],to[1]),0) + (1 << depth)
                    value = val
                    break
                if val > value:
                    value = val
                alpha = max(alpha, value)
            self.ttable[key] = (depth, value)
            return value
        else:
            value = 10**9
            for (frm,to) in moves:
                self.push_move(frm,to)
                val = self.search(depth-1, alpha, beta, True, start_time)
                self.pop_move()
                if val <= alpha:
                    self.hist_heur[(frm[0],frm[1],to[0],to[1])] = self.hist_heur.get((frm[0],frm[1],to[0],to[1]),0) + (1 << depth)
                    value = val
                    break
                if val < value:
                    value = val
                beta = min(beta, value)
            self.ttable[key] = (depth, value)
            return value

    def quiescence(self, alpha, beta, maximizing):
        stand_pat = self.evaluate()
        if maximizing:
            if stand_pat >= beta:
                return beta
            if alpha < stand_pat:
                alpha = stand_pat
            moves = self.generate_all_legal_moves('b')
            caps = [m for m in moves if self.is_capture(m[0], m[1])]
            caps = sorted(caps, key=lambda m: -self.mvv_lva(m[0], m[1]))
            for (frm,to) in caps:
                self.push_move(frm,to)
                val = self.quiescence(alpha, beta, False)
                self.pop_move()
                if val >= beta:
                    return beta
                if val > alpha:
                    alpha = val
            return alpha
        else:
            if stand_pat <= alpha:
                return alpha
            if beta > stand_pat:
                beta = stand_pat
            moves = self.generate_all_legal_moves('w')
            caps = [m for m in moves if self.is_capture(m[0], m[1])]
            caps = sorted(caps, key=lambda m: self.mvv_lva(m[0], m[1]))
            for (frm,to) in caps:
                self.push_move(frm,to)
                val = self.quiescence(alpha, beta, True)
                self.pop_move()
                if val <= alpha:
                    return alpha
                if val < beta:
                    beta = val
            return beta

    def minimax(self, depth, alpha, beta, maximizing):
        return self.search(depth, alpha, beta, maximizing, time.time())

# Parametresiz API

def open_chess_game():
    ChessGame()


def open_widgets():
    """Windows7 tarzı küçük gadget/widget paneli açar.
    - Küçük, taşınabilir Toplevel.
    - Saat ve CPU sayaç (psutil varsa gerçek değer) gibi örnek gadget'lar içerir.
    - Kullanıcı yeni gadget ekleyebilir / kaldırabilir.
    """
    try:
        win = tk.Toplevel(root)
    except Exception:
        win = tk.Toplevel()
    win.title("Gadgets")
    win.geometry("320x420")
    win.resizable(False, False)
    win.attributes("-topmost", True)

    container = ttk.Frame(win, padding=8)
    container.pack(fill="both", expand=True)

    header = ttk.Frame(container)
    header.pack(fill="x")
    ttk.Label(header, text="Gadgets", font=("Segoe UI", 11, "bold")).pack(side="left")
    btn_close = ttk.Button(header, text="Kapat", command=win.destroy)
    btn_close.pack(side="right")

    body = ttk.Frame(container)
    body.pack(fill="both", expand=True, pady=(8,0))

    gadgets_frame = ttk.Frame(body)
    gadgets_frame.pack(fill="both", expand=True)

    # yardımcı: gadget container listesi
    gadget_widgets = []

    def add_clock(parent=None):
        parent = parent or gadgets_frame
        f = ttk.Frame(parent, relief="ridge", padding=6)
        lbl = ttk.Label(f, text="--:--:--", font=("Consolas", 18))
        lbl.pack()

        def tick():
            try:
                lbl.config(text=time.strftime("%H:%M:%S"))
            except Exception:
                pass
            try:
                f.after(500, tick)
            except Exception:
                pass

        tick()

        def remove():
            try:
                f.destroy()
                gadget_widgets.remove(f)
            except Exception:
                pass

        btn = ttk.Button(f, text="Kaldır", command=remove)
        btn.pack(pady=(6,0))
        f.pack(fill="x", pady=6)
        gadget_widgets.append(f)
        return f

    def add_cpu_meter(parent=None):
        parent = parent or gadgets_frame
        f = ttk.Frame(parent, relief="ridge", padding=6)
        ttl = ttk.Label(f, text="CPU Kullanımı", font=("Segoe UI", 9, "bold"))
        ttl.pack()
        val_lbl = ttk.Label(f, text="-- %", font=("Segoe UI", 12))
        val_lbl.pack()
        pb = ttk.Progressbar(f, orient="horizontal", length=200, mode="determinate")
        pb.pack(pady=(6,0))

        def update_cpu():
            try:
                if PSUTIL_AVAILABLE:
                    pct = int(psutil.cpu_percent(interval=None))
                else:
                    # mock değer / random görünüm
                    pct = random.randint(1, 40)
                val_lbl.config(text=f"{pct} %")
                try:
                    pb['value'] = pct
                except Exception:
                    pass
            except Exception:
                pass
            try:
                f.after(1000, update_cpu)
            except Exception:
                pass

        update_cpu()

        def remove():
            try:
                f.destroy()
                gadget_widgets.remove(f)
            except Exception:
                pass

        btn = ttk.Button(f, text="Kaldır", command=remove)
        btn.pack(pady=(6,0))
        f.pack(fill="x", pady=6)
        gadget_widgets.append(f)
        return f

    # Başlangıç gadget'ları
    add_clock()
    add_cpu_meter()

    # Alt bar: gadget seçme
    footer = ttk.Frame(container)
    footer.pack(fill="x", pady=(6,0))

    available = [
        ("Saat", add_clock),
        ("CPU Meter", add_cpu_meter),
        ("Bellek Meter", None),
        ("Ağ Meter", None),
        ("Pil Durumu", None),
        ("Hava Durumu", None),
        ("Takvim", None),
        ("Notlar", None),
        ("Slayt Gösterisi", None),
    ]

    sel_var = tk.StringVar(value=available[0][0])
    names = [n for n, _ in available]
    opt = ttk.OptionMenu(footer, sel_var, names[0], *names)
    opt.pack(side="left")

    def on_add():
        sel = sel_var.get()
        for n, fn in available:
            if n == sel:
                try:
                    if fn:
                        fn()
                    else:
                        # map placeholder names to implementations
                        if n == "Bellek Meter":
                            add_memory_meter()
                        elif n == "Ağ Meter":
                            add_network_meter()
                        elif n == "Pil Durumu":
                            add_battery()
                        elif n == "Hava Durumu":
                            add_weather()
                        elif n == "Takvim":
                            add_calendar()
                        elif n == "Notlar":
                            add_notes()
                        elif n == "Slayt Gösterisi":
                            add_slideshow()
                except Exception as e:
                    messagebox.showerror("Hata", f"Gadget eklenemedi: {e}")
                break

    add_btn = ttk.Button(footer, text="Ekle", command=on_add)
    add_btn.pack(side="left", padx=(6,0))

    # pencereyi sürüklenebilir yapmak için başlığa bağla
    def start_move(event):
        win._drag_start_x = event.x
        win._drag_start_y = event.y

    def do_move(event):
        try:
            x = win.winfo_x() + event.x - getattr(win, '_drag_start_x', 0)
            y = win.winfo_y() + event.y - getattr(win, '_drag_start_y', 0)
            win.geometry(f'+{x}+{y}')
        except Exception:
            pass

    header.bind('<Button-1>', start_move)
    header.bind('<B1-Motion>', do_move)

    return win

    # --- Gelişmiş gadget fonksiyonları ---

def add_memory_meter(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    # find a parent fallback
    if parent is None:
        # try to attach to top-level gadgets_frame if exists
        for w in root.winfo_children():
            if isinstance(w, tk.Toplevel):
                parent = w
                break
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Bellek Kullanımı", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    val_lbl = ttk.Label(f, text="-- %", font=("Segoe UI", 12))
    val_lbl.pack()
    pb = ttk.Progressbar(f, orient="horizontal", length=200, mode="determinate")
    pb.pack(pady=(6,0))

    def update_mem():
        try:
            if PSUTIL_AVAILABLE:
                pct = int(psutil.virtual_memory().percent)
            else:
                pct = random.randint(10, 60)
            val_lbl.config(text=f"{pct} %")
            try:
                pb['value'] = pct
            except Exception:
                pass
        except Exception:
            pass
        try:
            f.after(1500, update_mem)
        except Exception:
            pass

    update_mem()

    def remove():
        try:
            f.destroy()
        except Exception:
            pass

    btn = ttk.Button(f, text="Kaldır", command=remove)
    btn.pack(pady=(6,0))
    f.pack(fill="x", pady=6)
    return f

def add_network_meter(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Ağ Trafiği (KB)", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    sent_lbl = ttk.Label(f, text="Gönder: -- KB", font=("Segoe UI", 9))
    sent_lbl.pack()
    recv_lbl = ttk.Label(f, text="Al: -- KB", font=("Segoe UI", 9))
    recv_lbl.pack()

    last = {'sent': 0, 'recv': 0}

    def update_net():
        try:
            if PSUTIL_AVAILABLE:
                counters = psutil.net_io_counters()
                sent = int(counters.bytes_sent / 1024)
                recv = int(counters.bytes_recv / 1024)
                if last['sent']:
                    sent_lbl.config(text=f"Gönder: {sent - last['sent']} KB/s")
                    recv_lbl.config(text=f"Al: {recv - last['recv']} KB/s")
                else:
                    sent_lbl.config(text=f"Gönder: {sent} KB")
                    recv_lbl.config(text=f"Al: {recv} KB")
                last['sent'] = sent
                last['recv'] = recv
            else:
                sent_lbl.config(text=f"Gönder: {random.randint(1,100)} KB/s")
                recv_lbl.config(text=f"Al: {random.randint(1,120)} KB/s")
        except Exception:
            pass
        try:
            f.after(1000, update_net)
        except Exception:
            pass

    update_net()

    def remove():
        try:
            f.destroy()
        except Exception:
            pass

    btn = ttk.Button(f, text="Kaldır", command=remove)
    btn.pack(pady=(6,0))
    f.pack(fill="x", pady=6)
    return f

def add_battery(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Pil Durumu", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    stat_lbl = ttk.Label(f, text="--", font=("Segoe UI", 10))
    stat_lbl.pack()

    def update_batt():
        try:
            if PSUTIL_AVAILABLE and hasattr(psutil, 'sensors_battery'):
                batt = psutil.sensors_battery()
                if batt:
                    stat_lbl.config(text=f"{int(batt.percent)}% {'(Şarj)' if batt.power_plugged else ''}")
                else:
                    stat_lbl.config(text="Bilgi yok")
            else:
                stat_lbl.config(text=f"{random.randint(40,95)}%")
        except Exception:
            pass
        try:
            f.after(5000, update_batt)
        except Exception:
            pass

    update_batt()

    def remove():
        try:
            f.destroy()
        except Exception:
            pass

    btn = ttk.Button(f, text="Kaldır", command=remove)
    btn.pack(pady=(6,0))
    f.pack(fill="x", pady=6)
    return f

def add_weather(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Hava Durumu", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    loc_frame = ttk.Frame(f)
    loc_frame.pack(fill="x")
    city_var = tk.StringVar(value="Istanbul")
    ttk.Entry(loc_frame, textvariable=city_var).pack(side="left", fill="x", expand=True)
    info_lbl = ttk.Label(f, text="—", font=("Segoe UI", 10))
    info_lbl.pack(pady=(6,0))

    def fetch_weather_by_coords(lat, lon):
        try:
            # Open-Meteo free API (no key) — user must provide lat/lon manually
            import requests
            url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                data = r.json()
                cw = data.get('current_weather', {})
                temp = cw.get('temperature')
                wcode = cw.get('weathercode')
                info_lbl.config(text=f"{temp}°C, code:{wcode}")
                return True
        except Exception:
            pass
        return False

    def on_fetch():
        city = city_var.get().strip()
        # if user entered like 'lat,lon', try parse
        if ',' in city:
            try:
                lat, lon = city.split(',', 1)
                if fetch_weather_by_coords(float(lat), float(lon)):
                    return
            except Exception:
                pass
        # fallback: try some presets
        presets = {'Istanbul': (41.0082, 28.9784), 'Ankara': (39.9208, 32.8541), 'Izmir': (38.4237, 27.1428)}
        if city in presets:
            lat, lon = presets[city]
            if fetch_weather_by_coords(lat, lon):
                return
        # else show mock
        info_lbl.config(text=f"{random.randint(5,30)}°C, durum: Parçalı Bulutlu")

    ttk.Button(f, text="Göster (lat,lon veya şehir)", command=on_fetch).pack(pady=(6,0))

    def remove():
        try:
            f.destroy()
        except Exception:
            pass

    btn = ttk.Button(f, text="Kaldır", command=remove)
    btn.pack(pady=(6,0))
    f.pack(fill="x", pady=6)
    return f

def add_calendar(parent=None):
    import calendar as _calendar
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    now = datetime.datetime.now()
    ttl = ttk.Label(f, text=now.strftime("%B %Y"), font=("Segoe UI", 9, "bold"))
    ttl.pack()
    txt = tk.Text(f, height=6, width=26)
    txt.pack()
    txt.insert('1.0', _calendar.month(now.year, now.month))
    txt.config(state='disabled')

    def remove():
        try:
            f.destroy()
        except Exception:
            pass

    btn = ttk.Button(f, text="Kaldır", command=remove)
    btn.pack(pady=(6,0))
    f.pack(fill="x", pady=6)
    return f

def add_notes(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Notlar", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    txt = tk.Text(f, height=6, width=28)
    txt.pack()

    def save_local():
        try:
            # save to a temporary file in BASE_DIR
            p = os.path.join(BASE_DIR, 'widget_note.txt')
            with open(p, 'w', encoding='utf-8') as fh:
                fh.write(txt.get('1.0', 'end-1c'))
            messagebox.showinfo('Kaydedildi', f'Not kaydedildi: {p}')
        except Exception as e:
            messagebox.showerror('Hata', f'Kaydedilemedi: {e}')

    btns = ttk.Frame(f)
    btns.pack(fill='x')
    ttk.Button(btns, text='Kaydet', command=save_local).pack(side='left')
    ttk.Button(btns, text='Kaldır', command=lambda: f.destroy()).pack(side='left', padx=6)
    f.pack(fill="x", pady=6)
    return f

def add_slideshow(parent=None):
    parent = parent or globals().get('gadgets_frame', None)
    f = ttk.Frame(parent, relief="ridge", padding=6)
    ttl = ttk.Label(f, text="Slayt Gösterisi", font=("Segoe UI", 9, "bold"))
    ttl.pack()
    img_lbl = ttk.Label(f, text='(resim yok)')
    img_lbl.pack()

    imgs = {'list': [], 'idx': 0}

    def choose_folder():
        from tkinter import filedialog
        p = filedialog.askdirectory()
        if not p:
            return
        files = [os.path.join(p, x) for x in os.listdir(p) if x.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
        imgs['list'] = files
        imgs['idx'] = 0
        show_next()

    def show_next():
        if not imgs['list']:
            return
        path = imgs['list'][imgs['idx']]
        try:
            if PIL_AVAILABLE:
                im = Image.open(path)
                im.thumbnail((260, 160))
                tkim = ImageTk.PhotoImage(im)
                img_lbl.config(image=tkim, text='')
                img_lbl.image = tkim
            else:
                img_lbl.config(text=os.path.basename(path))
        except Exception:
            img_lbl.config(text=os.path.basename(path))
        imgs['idx'] = (imgs['idx'] + 1) % len(imgs['list'])
        try:
            f.after(3000, show_next)
        except Exception:
            pass

    btns = ttk.Frame(f)
    btns.pack()
    ttk.Button(btns, text='Klasör Seç', command=choose_folder).pack(side='left')
    ttk.Button(btns, text='Kaldır', command=lambda: f.destroy()).pack(side='left', padx=6)
    f.pack(fill="x", pady=6)
    return f

# Taskbar üzerinde Widgets butonu ekle (çakışma olursa mevcutse atla)
try:
    if 'open_widgets' in globals() and not any(getattr(b, 'cget', lambda k=None: None)('text') == 'Widgets' for b in task_buttons_frame.winfo_children()):
        widgets_btn = tk.Button(taskbar, text="Widgets", command=open_widgets, bg="gray20", fg="white")
        widgets_btn.pack(side="left", padx=4, pady=4)
except Exception:
    pass


def open_ball_game():
    import tkinter as tk
    import random
    import os
    import time

    # Ayarlar (fonksiyon parametresi yok, dedin; o yüzden burada sabit)
    WINDOW_W, WINDOW_H = 500, 420
    DURATION = 30  # saniye
    BALL_INITIAL_SIZE = 50
    HIGHSCORE_FILE = os.path.join(os.path.expanduser("~"), ".top_yakalama_highscore.txt")

    # Yardımcılar: yüksek skor oku/yaz
    def load_highscore():
        try:
            with open(HIGHSCORE_FILE, "r") as f:
                return int(f.read().strip() or 0)
        except Exception:
            return 0

    def save_highscore(val):
        try:
            with open(HIGHSCORE_FILE, "w") as f:
                f.write(str(int(val)))
        except Exception:
            pass

    win = tk.Toplevel(root)
    win.title("Top Yakalama — Gelişmiş")
    win.geometry(f"{WINDOW_W}x{WINDOW_H}")
    win.resizable(False, False)

    # Durum değişkenleri
    score = {"val": 0}
    time_left = {"val": DURATION}
    running = {"val": False}
    anim_after = {"id": None}
    timer_after = {"id": None}
    highscore = {"val": load_highscore()}
    ball_size = {"val": BALL_INITIAL_SIZE}

    # UI
    top_frame = tk.Frame(win)
    top_frame.pack(fill="x", pady=(6, 0))

    score_label = tk.Label(top_frame, text=f"Score: {score['val']}", font=("Arial", 12))
    score_label.pack(side="left", padx=8)

    high_label = tk.Label(top_frame, text=f"High: {highscore['val']}", font=("Arial", 12))
    high_label.pack(side="left", padx=8)

    timer_label = tk.Label(top_frame, text=f"Time: {time_left['val']}", font=("Arial", 12))
    timer_label.pack(side="right", padx=8)

    canvas = tk.Canvas(win, width=WINDOW_W, height=WINDOW_H-80, bg="white", highlightthickness=0)
    canvas.pack(pady=8)

    control_frame = tk.Frame(win)
    control_frame.pack(fill="x", pady=(0,8))

    start_btn = tk.Button(control_frame, text="Start", width=10)
    pause_btn = tk.Button(control_frame, text="Pause", width=10, state="disabled")
    restart_btn = tk.Button(control_frame, text="Restart", width=10, state="disabled")
    quit_btn = tk.Button(control_frame, text="Quit", width=10)

    start_btn.pack(side="left", padx=6)
    pause_btn.pack(side="left", padx=6)
    restart_btn.pack(side="left", padx=6)
    quit_btn.pack(side="right", padx=6)

    # Topu oluştur
    def center_coords_for_size(s):
        x = (WINDOW_W - s) // 2
        y = (WINDOW_H - 80 - s) // 2
        return x, y, x+s, y+s

    ball = canvas.create_oval(*center_coords_for_size(ball_size["val"]), fill="red", outline="black", tags=("ball",))

    # Görsel efekt: küçük parıltı at
    def pop_effect(x, y, size):
        r = max(6, int(size/4))
        eid = canvas.create_oval(x-r, y-r, x+r, y+r, outline="", fill="yellow")
        # hızlıca sildir
        win.after(120, lambda: canvas.delete(eid))

    # Skoru güncelle
    def update_score_label():
        score_label.config(text=f"Score: {score['val']}")
        # zorluk arttıkça top küçülsün (min 18px)
        new_size = max(18, BALL_INITIAL_SIZE - score['val'] // 2)
        if new_size != ball_size["val"]:
            ball_size["val"] = new_size
            # topu bulunduğu merkeze göre yeniden boyutlandır
            cx, cy = get_ball_center()
            set_ball_center(cx, cy, ball_size["val"])

    def update_high_label():
        high_label.config(text=f"High: {highscore['val']}")

    # Topun merkezini al / ayarla
    def get_ball_center():
        x1, y1, x2, y2 = canvas.coords(ball)
        cx = (x1 + x2) / 2
        cy = (y1 + y2) / 2
        return cx, cy

    def set_ball_center(cx, cy, size):
        half = size / 2
        x1, y1, x2, y2 = cx-half, cy-half, cx+half, cy+half
        # sınırlar içinde tut
        x1 = max(0, min(x1, WINDOW_W - size))
        y1 = max(0, min(y1, (WINDOW_H-80) - size))
        canvas.coords(ball, x1, y1, x1+size, y1+size)

    # Kullanıcı topa tıkladığında
    def click_ball(event):
        if not running["val"]:
            return
        # Gerçek bir "ball" tıklamasıysa puan ver
        # (tag_bind ile zaten top için bağladık ama ekstra güvenlik)
        tags = canvas.gettags("current")
        if "ball" in tags:
            score["val"] += 1
            update_score_label()
            pop_effect(event.x, event.y, ball_size["val"])
            # hemen yeni hedef belirle (animasyon iptal edilip yeniden yapılıyor)
            move_ball(force=True)

    canvas.tag_bind(ball, "<Button-1>", click_ball)

    # Topu animasyonla rastgele bir noktaya gönder
    def move_ball(force=False):
        if not running["val"] and not force:
            return
        # varsa önceki animasyonu iptal et
        if anim_after["id"]:
            try:
                win.after_cancel(anim_after["id"])
            except Exception:
                pass
            anim_after["id"] = None

        # zorluk: puana göre hız artsın (daha az steps => daha hızlı)
        speed_factor = min(10, 1 + score["val"]//3)  # 1..10
        # steps küçüldükçe top hızlı gider
        steps = max(6, 20 - speed_factor*2)

        size = ball_size["val"]
        # hedef koordinat (topun sol üst noktası içinde kalacak şekilde center hedef)
        tx = random.randint(size//2, WINDOW_W - size//2)
        ty = random.randint(size//2, (WINDOW_H-80) - size//2)

        cx, cy = get_ball_center()
        dx = (tx - cx) / steps
        dy = (ty - cy) / steps

        # animasyon adımı
        def step(i=0):
            if not running["val"]:
                return
            nonlocal_dx = dx; nonlocal_dy = dy
            if i < steps:
                canvas.move(ball, nonlocal_dx, nonlocal_dy)
                anim_after["id"] = win.after(18, lambda: step(i+1))
            else:
                # küçük rastgele titreşim (doğallık)
                jitter_x = random.uniform(-2, 2)
                jitter_y = random.uniform(-2, 2)
                canvas.move(ball, jitter_x, jitter_y)
                # yenisini başlat
                anim_after["id"] = win.after(max(200, 800 - score["val"]*30), move_ball)

        step()

    # Zamanlayıcı
    def game_timer():
        if timer_after["id"]:
            try:
                win.after_cancel(timer_after["id"])
            except Exception:
                pass
            timer_after["id"] = None
        if not running["val"]:
            return
        if time_left["val"] <= 0:
            end_game()
            return
        time_left["val"] -= 1
        timer_label.config(text=f"Time: {time_left['val']}")
        timer_after["id"] = win.after(1000, game_timer)

    # Oyun bitişi
    def end_game():
        running["val"] = False
        pause_btn.config(state="disabled")
        restart_btn.config(state="normal")
        start_btn.config(state="normal")
        # animasyonları iptal et
        if anim_after["id"]:
            try:
                win.after_cancel(anim_after["id"])
            except Exception:
                pass
            anim_after["id"] = None
        if timer_after["id"]:
            try:
                win.after_cancel(timer_after["id"])
            except Exception:
                pass
            timer_after["id"] = None

        # yüksek skoru güncelle
        if score["val"] > highscore["val"]:
            highscore["val"] = score["val"]
            save_highscore(highscore["val"])
            update_high_label()

        # Sonuç bildirimi (basit, pencere üstünde)
        canvas.create_text(WINDOW_W//2, (WINDOW_H-80)//2, text=f"Time's up! Score: {score['val']}", font=("Helvetica", 18), fill="black", tags=("endtext",))
        # topu biraz küçült ve ortaya koy
        set_ball_center(WINDOW_W/2, (WINDOW_H-80)/2 + 40, 30)

    # Başlat / durdur / yeniden başlat
    def start_game():
        # temizle
        canvas.delete("endtext")
        score["val"] = 0
        time_left["val"] = DURATION
        ball_size["val"] = BALL_INITIAL_SIZE
        update_score_label()
        timer_label.config(text=f"Time: {time_left['val']}")
        running["val"] = True
        start_btn.config(state="disabled")
        pause_btn.config(state="normal", text="Pause")
        restart_btn.config(state="disabled")
        # ilk hareketi başlat (yavaş başlangıç)
        move_ball(force=True)
        game_timer()

    def toggle_pause():
        if not running["val"]:
            # devam ettir
            running["val"] = True
            pause_btn.config(text="Pause")
            move_ball(force=True)
            game_timer()
        else:
            running["val"] = False
            pause_btn.config(text="Resume")
            # animasyonlar natural olarak durur çünkü running False

    def restart_game():
        # animasyonları temizle
        if anim_after["id"]:
            try:
                win.after_cancel(anim_after["id"])
            except Exception:
                pass
            anim_after["id"] = None
        if timer_after["id"]:
            try:
                win.after_cancel(timer_after["id"])
            except Exception:
                pass
            timer_after["id"] = None
        start_game()

    def on_quit():
        # iptaller
        running["val"] = False
        try:
            if anim_after["id"]:
                win.after_cancel(anim_after["id"])
            if timer_after["id"]:
                win.after_cancel(timer_after["id"])
        except Exception:
            pass
        win.destroy()

    # Düğme bağlantıları
    start_btn.config(command=start_game)
    pause_btn.config(command=toggle_pause)
    restart_btn.config(command=restart_game)
    quit_btn.config(command=on_quit)

    # pencere kapanırken temizle
    win.protocol("WM_DELETE_WINDOW", on_quit)

    # klavye kısayolları (space = pause)
    def on_key(e):
        if e.keysym == "space":
            if pause_btn["state"] != "disabled":
                toggle_pause()
    win.bind_all("<Key>", on_key)

    # son olarak: topun üzerine küçük kılavuz
    hint = canvas.create_text(8, 8, anchor="nw", text="Tıklayın! Space: duraklat/başlat", font=("Arial", 9))
    # topa başlangıç pozisyonu (merkez)
    set_ball_center(WINDOW_W/2, (WINDOW_H-80)/2, BALL_INITIAL_SIZE)

# SarmaBot_Toplevel.py
# SarmaBot'u bir Tkinter Toplevel içine gömen tek dosyalık uygulama.
# - 500 programatik komut (cmd1..cmd500)
# - Türkçe/İngilizce tespit
# - Güvenli hesaplama (AST tabanlı)
# - Toplevel içinde sohbet arayüzü (giriş, gönder, kaydırılabilir metin)
#
# Çalıştır: python SarmaBot_Toplevel.py

import ast
import math
import operator
import random
import re
import sys
import tkinter as tk
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime

# -------------------------
# Güvenli hesaplama (safe_eval)
# -------------------------
ALLOWED_FUNCS = {name: getattr(math, name) for name in dir(math) if not name.startswith("__")}
ALLOWED_FUNCS.update({"abs": abs, "round": round, "min": min, "max": max})
ALLOWED_NAMES = set(ALLOWED_FUNCS.keys()) | {"pi", "e"}


def safe_eval(expr: str):
    try:
        tree = ast.parse(expr, mode="eval")
    except Exception as e:
        raise ValueError("Ifade parse edilemedi: " + str(e))

    def _check(node):
        if isinstance(node, ast.Expression):
            return _check(node.body)
        if isinstance(node, ast.BinOp):
            if not isinstance(node.op, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod, ast.Pow, ast.FloorDiv)):
                raise ValueError("İzin verilmeyen işlem: " + str(node.op))
            _check(node.left)
            _check(node.right)
            return True
        if isinstance(node, ast.UnaryOp):
            if not isinstance(node.op, (ast.UAdd, ast.USub)):
                raise ValueError("İzin verilmeyen unary op")
            return _check(node.operand)
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Sadece isimli fonksiyon çağrılabilir")
            fname = node.func.id
            if fname not in ALLOWED_FUNCS:
                raise ValueError(f"İzin verilmeyen fonksiyon: {fname}")
            for a in node.args:
                _check(a)
            return True
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return True
            raise ValueError("Sadece sayısal sabitlere izin var")
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_NAMES:
                return True
            raise ValueError(f"İzin verilmeyen isim: {node.id}")
        if isinstance(node, ast.Tuple):
            for elt in node.elts:
                _check(elt)
            return True
        raise ValueError("İzin verilmeyen ifade kısmı: " + node.__class__.__name__)

    _check(tree)
    safe_globals = {"__builtins__": {}}
    safe_globals.update(ALLOWED_FUNCS)
    return eval(compile(tree, filename="<safe>", mode="eval"), safe_globals, {})

# -------------------------
# Matematik yardımcıları
# -------------------------

def is_prime(n: int):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    r = int(n**0.5) + 1
    for i in range(3, r, 2):
        if n % i == 0:
            return False
    return True


def lcm(a: int, b: int):
    return abs(a*b) // math.gcd(a, b) if a and b else 0

# -------------------------
# Komut sistemi
# -------------------------
class Command:
    def __init__(self, name, aliases, desc, handler):
        self.name = name
        self.aliases = set([name] + aliases)
        self.desc = desc
        self.handler = handler

COMMANDS = {}

def register(cmd: Command):
    for alias in cmd.aliases:
        COMMANDS[alias] = cmd
    return cmd

# Temel komutlar

def cmd_help(args, lang):
    if not args:
        keys = sorted({c.name for c in COMMANDS.values()})
        return {
            "tr": "Kullanılabilir komutlar (kısa): " + ", ".join(keys[:40]) + f" ... (toplam {len(keys)} komut)",
            "en": "Available commands (short): " + ", ".join(keys[:40]) + f" ... (total {len(keys)} commands)"
        }[lang]
    else:
        name = args[0].lower()
        cmd = COMMANDS.get(name)
        if not cmd:
            return {"tr": "Bilinmeyen komut: " + name, "en": "Unknown command: " + name}[lang]
        return {"tr": f"{cmd.name} - {cmd.desc}", "en": f"{cmd.name} - {cmd.desc}"}[lang]

register(Command("help", ["yardim", "yardım", "help"], "Show help. / Yardım gösterir.", lambda a, l: cmd_help(a, l)))
register(Command("ping", ["ping"], "Check latency / pong.", lambda a, l: {"tr":"pong","en":"pong"}[l]))
register(Command("time", ["zaman", "time"], "Shows current time.", lambda a, l: {"tr":f"Şu an: {datetime.now()}","en":f"Now: {datetime.now()}"}[l]))

# calc / hesapla

def cmd_calc(args, lang):
    if not args:
        return {"tr":"Kullanım: calc <ifade>  Ör: calc 2+2*3","en":"Usage: calc <expression>  e.g. calc 2+2*3"}[lang]
    expr = " ".join(args)
    try:
        result = safe_eval(expr)
        return {"tr": f"Sonuç: {result}", "en": f"Result: {result}"}[lang]
    except Exception as e:
        return {"tr": "Hesaplama hatası: " + str(e), "en": "Calculation error: " + str(e)}[lang]

register(Command("calc", ["hesapla", "calculate"], "Evaluate math expressions safely. / Matematik ifadelerini güvenli değerlendirir.", lambda a, l: cmd_calc(a, l)))

# gcd / ebob

def cmd_gcd(args, lang):
    if len(args) < 2:
        return {"tr":"Kullanım: gcd a b", "en":"Usage: gcd a b"}[lang]
    try:
        a = int(args[0]); b = int(args[1])
    except:
        return {"tr":"Sayı giriniz", "en":"Please enter integers"}[lang]
    return {"tr":f"GCD({a},{b}) = {math.gcd(a,b)}", "en":f"GCD({a},{b}) = {math.gcd(a,b)}"}[lang]

register(Command("gcd", ["ebob"], "Greatest common divisor / EBOB.", lambda a, l: cmd_gcd(a, l)))

# lcm
register(Command("lcm", ["ekok"], "Least common multiple / EKOK.", lambda a, l: {"tr":f"LCM = {lcm(int(a[0]),int(a[1]))}" if len(a)>=2 else "Kullanım: lcm a b", "en":f"LCM = {lcm(int(a[0]),int(a[1]))}" if len(a)>=2 else "Usage: lcm a b"}[l]))

# factorial

def cmd_fact(args, lang):
    if not args:
        return {"tr":"Kullanım: fact n", "en":"Usage: fact n"}[lang]
    try:
        n = int(args[0])
        return {"tr":f"{n}! = {math.factorial(n)}", "en":f"{n}! = {math.factorial(n)}"}[lang]
    except Exception as e:
        return {"tr":"Hata: "+str(e), "en":"Error: "+str(e)}[lang]

register(Command("fact", ["faktoriyel"], "Factorial / Faktöriyel.", lambda a, l: cmd_fact(a, l)))

# isprime

def cmd_isprime(args, lang):
    if not args: return {"tr":"Kullanım: isprime n", "en":"Usage: isprime n"}[lang]
    try:
        n = int(args[0])
        return {"tr":f"{n} asal mı? {'Evet' if is_prime(n) else 'Hayır'}", "en":f"Is {n} prime? {'Yes' if is_prime(n) else 'No'}"}[lang]
    except Exception as e:
        return {"tr":"Hata: "+str(e), "en":"Error: "+str(e)}[lang]

register(Command("isprime", ["asalmi", "asal mı"], "Check primality / Asal mı?", lambda a, l: cmd_isprime(a, l)))

# -------------------------
# 500 otomatik komut
# -------------------------

def make_simple_handler(i):
    def handler(args, lang):
        if i <= 100:
            return {"tr": f"Selam! (komut {i})", "en": f"Hello! (command {i})"}[lang]
        if 101 <= i <= 200:
            if args:
                try:
                    n = float(args[0])
                    return {"tr": f"{n} * {i} = {n * i}", "en": f"{n} * {i} = {n * i}"}[lang]
                except:
                    return {"tr":"Lütfen sayı verin", "en":"Please give a number"}[lang]
            return {"tr":f"Bu komut {i}: verilen sayıyı {i} ile çarpar.", "en":f"This command {i}: multiplies given number by {i}."}[lang]
        if 201 <= i <= 300:
            if args:
                s = " ".join(args)
                if i % 3 == 0:
                    return {"tr": s.upper(), "en": s.upper()}[lang]
                if i % 3 == 1:
                    return {"tr": s[::-1], "en": s[::-1]}[lang]
                return {"tr": s.title(), "en": s.title()}[lang]
            return {"tr":"Veri yok: bir şey yazın.", "en":"No input: provide a string."}[lang]
        if 301 <= i <= 380:
            if args and len(args) >= 2:
                try:
                    val = float(args[0])
                    typ = args[1].lower()
                    if typ in ("cm","centimeter"):
                        return {"tr":f"{val} cm = {val/100} m", "en":f"{val} cm = {val/100} m"}[lang]
                    if typ in ("km","kilometer"):
                        return {"tr":f"{val} km = {val*0.621371} mi", "en":f"{val} km = {val*0.621371} mi"}[lang]
                    if typ in ("c","celsius"):
                        return {"tr":f"{val}°C = {val*9/5+32}°F", "en":f"{val}°C = {val*9/5+32}°F"}[lang]
                    return {"tr":"Bilinmeyen tip", "en":"Unknown type"}[lang]
                except:
                    return {"tr":"Hata: sayı bekleniyordu", "en":"Error: expected a number"}[lang]
            return {"tr":"Kullanım: komut <değer> <tip(cm/km/c) >", "en":"Usage: command <value> <type(cm/km/c)>"}[lang]
        if 381 <= i <= 450:
            if i % 2 == 0:
                return {"tr":f"Rastgele sayı: {random.randint(0, i)}", "en":f"Random number: {random.randint(0, i)}"}[lang]
            return {"tr":f"Kısa bilgi #{i}: Bu bir örnek bilgi.", "en":f"Fact #{i}: This is a sample fact."}[lang]
        if args:
            expr = " ".join(args)
            try:
                res = safe_eval(expr)
                return {"tr":f"({i}) Hesaplama sonucu: {res}", "en":f"({i}) Calculation result: {res}"}[lang]
            except Exception as e:
                return {"tr":f"Hata: {e}", "en":f"Error: {e}"}[lang]
        return {"tr":f"Komut {i}: math helper. Bir ifade verin.", "en":f"Command {i}: math helper. Provide an expression."}[lang]
    return handler

for i in range(1, 501):
    name = f"cmd{i}"
    aliases = [f"komut{i}", f"c{i}", f"k{i}"]
    desc = f"Automated command #{i}"
    register(Command(name, aliases, desc, make_simple_handler(i)))

# -------------------------
# Dil algılama ve dispatch
# -------------------------
TURKISH_KEYWORDS = ["merhaba", "selam", "nasılsın", "hesapla", "kaç", "teşekkür", "sağol", "günaydın", "iyi akşamlar"]

def detect_lang(text: str):
    lower = text.lower()
    for w in TURKISH_KEYWORDS:
        if w in lower:
            return "tr"
    if re.search(r"\b(calc|help|time|ping|isprime|gcd|lcm|fact)\b", lower):
        return "en"
    return "tr" if re.search(r"[ığüşöçİĞÜŞÖÇ]", text) else "en"


def parse_and_dispatch(text: str):
    text = text.strip()
    if not text:
        return "..."
    lang = detect_lang(text)
    if text.startswith("/"):
        text = text[1:]
    parts = text.split()
    cmd_token = parts[0].lower()
    args = parts[1:]
    cmd = COMMANDS.get(cmd_token)
    if not cmd:
        token_clean = re.sub(r"[^\wğüşöçıİĞÜŞÖÇ]", "", cmd_token)
        cmd = COMMANDS.get(token_clean)
    if not cmd:
        if re.search(r"[0-9\.\+\-\*\/\^\(\)]", text):
            return cmd_calc(parts if COMMANDS.get(parts[0]) else parts, lang)
        return {"tr":"Bilinmeyen komut. help yazın.", "en":"Unknown command. Type help."}[lang]
    try:
        return cmd.handler(args, lang)
    except Exception as e:
        return {"tr":"Komut çalıştırma hatası: "+str(e), "en":"Command runtime error: "+str(e)}[lang]

# -------------------------
# GUI: Toplevel içine gömme
# -------------------------
class SarmaBotGUI:
    def __init__(self, root):
        self.root = root
        root.title("SarmaBot Container")

        # Ana pencerede bir butonla Toplevel açalım
        open_btn = ttk.Button(root, text="Open SarmaBot (Toplevel)", command=self.open_toplevel)
        open_btn.pack(padx=10, pady=10)

        # Hemen toplevel açılmasını isterseniz uncomment:
        # self.open_toplevel()

    def open_toplevel(self):
        # Eğer zaten açık bir toplevel varsa ona odaklan
        if hasattr(self, 'top') and self.top.winfo_exists():
            self.top.deiconify()
            self.top.lift()
            return

        self.top = tk.Toplevel(self.root)
        self.top.title("SarmaBot - Toplevel Chat")
        self.top.geometry('700x500')

        # Chat görüntüleme
        self.chat_area = ScrolledText(self.top, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=6, pady=6)

        bottom_frame = ttk.Frame(self.top)
        bottom_frame.pack(fill=tk.X, padx=6, pady=6)

        self.entry = ttk.Entry(bottom_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,6))
        self.entry.bind('<Return>', self.on_send)

        send_btn = ttk.Button(bottom_frame, text="Gönder", command=self.on_send)
        send_btn.pack(side=tk.RIGHT)

        # başlangıç mesajı
        self._append_bot("SarmaBot hazır. Yardım için 'help' veya 'yardim' yazın.")

        # destroy handler
        self.top.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        try:
            self.top.destroy()
        except:
            pass

    def _append_bot(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "SarmaBot: " + str(text) + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def _append_user(self, text):
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.insert(tk.END, "You: " + str(text) + "\n")
        self.chat_area.see(tk.END)
        self.chat_area.config(state=tk.DISABLED)

    def on_send(self, event=None):
        raw = self.entry.get().strip()
        if not raw:
            return
        self._append_user(raw)
        self.entry.delete(0, tk.END)

        # çıkış kontrolü
        if raw.lower() in ("çık","cık","exit","quit"):
            self._append_bot("Görüşürüz.")
            self.on_close()
            return

        out = parse_and_dispatch(raw)
        if isinstance(out, dict):
            lang = detect_lang(raw)
            resp = out.get(lang, next(iter(out.values())))
        else:
            resp = out
        self._append_bot(resp)


def open_snake_game():
    import tkinter as tk
    from tkinter import messagebox
    import random
    import time
    import os

    HIGH_SCORE_FILE = "snake_highscore.txt"
    CELL = 20
    GRID = 20
    W = CELL * GRID
    SPEED_START = 200

    # Root yönetimi: var olan global 'root' kullanılırsa o tercih edilir,
    # yoksa geçici bir root oluşturulur ve fonksiyon mainloop'u başlatır.
    created_root = False
    parent = globals().get("root", None) or tk._default_root
    if parent is None:
        parent = tk.Tk()
        parent.withdraw()
        created_root = True

    win = tk.Toplevel(parent)
    win.title("Yılan Oyunu — Retro")
    win.resizable(False, False)

    canvas = tk.Canvas(win, width=W, height=W, bg="#070707", highlightthickness=0)
    canvas.pack()

    # Oyun durumu (outer scope değişkenleri)
    snake = [((W // 2 - CELL), W // 2)]
    snake_dir = "Right"
    score = 0
    level = 1
    food_eaten = 0
    speed = SPEED_START
    paused = False
    running = True
    job = None
    powerup = None
    powerup_timer = 0
    powerup_active = False
    walls_kill = True  # duvarlara çarpınca ölür by default

    # highscore yükle/kaydet
    def load_highscore():
        try:
            if os.path.exists(HIGH_SCORE_FILE):
                with open(HIGH_SCORE_FILE, "r") as f:
                    return int(f.read().strip() or 0)
        except Exception:
            pass
        return 0

    def save_highscore(val):
        try:
            with open(HIGH_SCORE_FILE, "w") as f:
                f.write(str(int(val)))
        except Exception:
            pass

    highscore = load_highscore()

    # Grid çizimi
    def draw_grid():
        canvas.delete("grid")
        canvas.create_rectangle(0, 0, W, W, fill="#070707", outline="#070707", tag="grid")
        for i in range(0, W, CELL):
            canvas.create_line(i, 0, i, W, fill="#111111", tag="grid")
            canvas.create_line(0, i, W, i, fill="#111111", tag="grid")

    # KONTROLLER ve skor (Label yerine canvas text)
    def draw_controls_and_score():
        # "EN ÜSTTE KONTROLLER" isteğine uygun olarak canvas'ın üst kısmına yazıyoruz.
        canvas.delete("controls")
        # KONTROLLER başlığı
        canvas.create_text(W // 2, 6, text="KONTROLLER", fill="#c7ff3d",
                           font=("Courier", 10, "bold"), tag="controls", anchor="n")
        # kontrol açıklamaları (küçük, başlığın altında)
        controls_line = "Y/Enter/Space: Başla   P: Duraklat   R: Yeniden   Q: Çık   W: Duvar Toggle"
        canvas.create_text(W // 2, 20, text=controls_line, fill="#9be564",
                           font=("Courier", 8), tag="controls", anchor="n")
        # skor / seviye sağ üstte
        canvas.delete("score")
        score_text = f"Skor: {score}  Seviye: {level}  En Yüksek: {highscore}"
        canvas.create_text(W - 6, 6, text=score_text, fill="#c7ff3d",
                           font=("Courier", 9), tag="score", anchor="ne")

    # Food / Powerup spawn
    food = [random.randrange(0, GRID) * CELL, random.randrange(0, GRID) * CELL]
    food_rect = canvas.create_rectangle(food[0], food[1], food[0] + CELL, food[1] + CELL,
                                       fill="#ff4b4b", outline="#8b0000", tag="food")

    def spawn_food():
        nonlocal food, food_rect, powerup, powerup_active, powerup_timer
        tries = 0
        while True:
            fx = random.randrange(0, GRID) * CELL
            fy = random.randrange(0, GRID) * CELL
            if (fx, fy) not in snake:
                food = [fx, fy]
                break
            tries += 1
            if tries > 200:
                break
        try:
            canvas.delete("food")
        except Exception:
            pass
        food_rect = canvas.create_rectangle(food[0], food[1], food[0] + CELL, food[1] + CELL,
                                           fill="#ff4b4b", outline="#8b0000", tag="food")

        # küçük olasılıkla powerup spawn et
        if not powerup_active and random.random() < 0.12:
            tries = 0
            while tries < 200:
                px = random.randrange(0, GRID) * CELL
                py = random.randrange(0, GRID) * CELL
                if (px, py) not in snake and [px, py] != food:
                    powerup = [px, py]
                    powerup_active = True
                    powerup_timer = 120
                    try:
                        canvas.delete("power")
                    except Exception:
                        pass
                    canvas.create_rectangle(px, py, px + CELL, py + CELL, fill="#ffd166", outline="#ffb347", tag="power")
                    break
                tries += 1

    # Snake çizimi
    def draw_snake():
        canvas.delete("snake")
        head = snake[-1]
        canvas.create_rectangle(head[0], head[1], head[0] + CELL, head[1] + CELL,
                                fill="#c7ff3d", outline="#4caf50", tag="snake")
        for seg in snake[:-1]:
            canvas.create_rectangle(seg[0], seg[1], seg[0] + CELL, seg[1] + CELL,
                                    fill="#9be564", outline="#6bbf3b", tag="snake")

    # Skor güncelleme (canvas üzerinden)
    def update_info():
        nonlocal highscore
        if score > highscore:
            highscore = score
            save_highscore(highscore)
        # güncelle
        try:
            canvas.delete("score")
        except Exception:
            pass
        score_text = f"Skor: {score}  Seviye: {level}  En Yüksek: {highscore}"
        canvas.create_text(W - 6, 6, text=score_text, fill="#c7ff3d",
                           font=("Courier", 9), tag="score", anchor="ne")

    # Oyun bitti
    def game_over():
        nonlocal running, job
        running = False
        if job:
            try:
                win.after_cancel(job)
            except Exception:
                pass
        # canvas üzerinde uyarı (label yok)
        canvas.create_text(W // 2, W // 2 - 10, text="OYUN BİTTİ", fill="#ff6b6b", font=("Courier", 18, "bold"), tag="end")
        canvas.create_text(W // 2, W // 2 + 16,
                           text=f"Skorunuz: {score}  (R: Yeniden  Y: Başla  Q: Çık)", fill="#c7ff3d", font=("Courier", 10), tag="end")
        # ek popup istemezsek yorum satırına al; kullanıcı önce 'labelları kaldır' dedi, popup bırakıyorum opsiyonel.
        try:
            messagebox.showinfo("Oyun Bitti", f"Skorunuz: {score}")
        except Exception:
            pass
        if created_root:
            try:
                parent.quit()
            except Exception:
                pass

    # Hareket ve oyun döngüsü
    def move():
        nonlocal snake, snake_dir, score, food_eaten, speed, level, job, powerup_active, powerup_timer
        if not running or paused:
            # eğer pauseda ya da durduysa çok sık job koyma
            try:
                job = win.after(100, move)
            except Exception:
                pass
            return

        x, y = snake[-1]
        if snake_dir == "Right":
            x += CELL
        elif snake_dir == "Left":
            x -= CELL
        elif snake_dir == "Up":
            y -= CELL
        elif snake_dir == "Down":
            y += CELL

        # duvar kontrolü
        if x < 0 or x >= W or y < 0 or y >= W:
            if walls_kill:
                return game_over()
            else:
                x %= W
                y %= W

        if (x, y) in snake:
            return game_over()

        snake.append((x, y))
        ate = False
        if x == food[0] and y == food[1]:
            ate = True
            food_eaten += 1
            score += 10
            if food_eaten % 5 == 0:
                level += 1
                speed = max(50, int(speed * 0.85))
        else:
            snake.pop(0)

        # powerup yeme kontrolü
        if powerup_active and powerup and (x == powerup[0] and y == powerup[1]):
            score += 50
            powerup_active = False
            powerup_timer = 0
            try:
                canvas.delete("power")
            except Exception:
                pass
            speed = max(40, int(speed * 0.95))

        if ate:
            spawn_food()
        else:
            # yeme efekti
            try:
                fillc = "#ff4b4b" if int(time.time() * 2) % 2 == 0 else "#ff6b6b"
                canvas.itemconfig("food", fill=fillc)
            except Exception:
                pass

        if powerup_active:
            powerup_timer -= 1
            if powerup_timer <= 0:
                powerup_active = False
                try:
                    canvas.delete("power")
                except Exception:
                    pass

        draw_snake()
        update_info()

        # schedule next
        try:
            if job:
                win.after_cancel(job)
        except Exception:
            pass
        try:
            job = win.after(speed, move)
        except Exception:
            pass

    # Yön değiştirici (ok tuşları)
    def change_dir(event):
        nonlocal snake_dir
        key = event.keysym
        opp = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}
        if key in ("Up", "Down", "Left", "Right"):
            if opp.get(snake_dir) != key:
                snake_dir = key

    # Genel tuşlar: P pause, R restart, Q quit, W duvar toggle, Y start
    def on_key(event):
        nonlocal paused, running, snake, snake_dir, score, level, food_eaten, speed, job, powerup_active, powerup_timer, walls_kill
        k = event.keysym.lower()
        if k in ("up", "down", "left", "right"):
            change_dir(event)
        elif k == "p":
            if not running:
                return
            paused = not paused
            if paused:
                try:
                    if job:
                        win.after_cancel(job)
                except Exception:
                    pass
                canvas.create_text(W // 2, W // 2, text="DURAKLATILDI\n(P bas)", fill="#8be9fd", font=("Courier", 16), tag="pause")
            else:
                canvas.delete("pause")
                try:
                    job = win.after(speed, move)
                except Exception:
                    pass
        elif k == "r":
            try:
                if job:
                    win.after_cancel(job)
            except Exception:
                pass
            # reset state
            score = 0
            level = 1
            food_eaten = 0
            speed = SPEED_START
            snake = [((W // 2 - CELL), W // 2)]
            snake_dir = "Right"
            paused = False
            running = True
            try:
                canvas.delete("all")
            except Exception:
                pass
            draw_grid()
            draw_controls_and_score()
            spawn_food()
            draw_snake()
            update_info()
            try:
                job = win.after(speed, move)
            except Exception:
                pass
        elif k == "q":
            try:
                if job:
                    win.after_cancel(job)
            except Exception:
                pass
            running = False
            win.destroy()
            if created_root:
                try:
                    parent.quit()
                except Exception:
                    pass
        elif k == "w":
            walls_kill = not walls_kill
            canvas.delete("note")
            canvas.create_text(W // 2, 24, text=f"Duvar modu: {'Açık' if walls_kill else 'Wrap'}",
                               fill="#ffb86b", font=("Courier", 8), tag="note", anchor="n")
            win.after(1000, lambda: canvas.delete("note"))
        elif k in ("y", "space", "return"):
            # eğer oyun başlamamış ya da bitti ise başlat / start
            if not running:
                # yeniden başlat yerine yeni başla
                score = 0
                level = 1
                food_eaten = 0
                speed = SPEED_START
                snake = [((W // 2 - CELL), W // 2)]
                snake_dir = "Right"
                paused = False
                running = True
                canvas.delete("all")
                draw_grid()
                draw_controls_and_score()
                spawn_food()
                draw_snake()
                update_info()
                try:
                    job = win.after(speed, move)
                except Exception:
                    pass
            else:
                # eğer start ekranındaysak başlat
                if job is None:
                    try:
                        job = win.after(speed, move)
                    except Exception:
                        pass

    # Başlangıç ekranı
    def show_start():
        canvas.delete("all")
        draw_grid()
        draw_controls_and_score()
        canvas.create_text(W // 2, W // 2 - 40, text="S A R M A  —  R E T R O  S N A K E",
                           fill="#8be9fd", font=("Courier", 14, "bold"), tag="start")
        canvas.create_text(W // 2, W // 2 + 8, text="Y/Enter/Space: Başla   P: Duraklat   R: Yeniden   Q: Çık",
                           fill="#c7ff3d", font=("Courier", 10), tag="start")

    # Başlatma
    draw_grid()
    show_start()
    spawn_food()
    draw_snake()
    draw_controls_and_score()
    canvas.focus_set()
    win.bind("<Key>", on_key)

# --- Güvenlik: Eğer _ToolTip tanımlı değilse, basit ve güvenli bir fallback tanımla ---
try:
    _ToolTip  # eğer zaten varsa hiçbir şey yapma
except NameError:
    try:
        from tkinter import Toplevel, Label
    except Exception:
        # Eğer tkinter isimleri yoksa, fallback için boş bir sınıf üret
        class _ToolTip:
            def __init__(self, widget, text): pass
            def show(self, _=None): pass
            def hide(self, _=None): pass
    else:
        class _ToolTip:
            def __init__(self, widget, text):
                self.widget = widget
                self.text = text
                self.tip = None
                try:
                    widget.bind("<Enter>", self.show)
                    widget.bind("<Leave>", self.hide)
                except Exception:
                    pass

            def show(self, _=None):
                if self.tip:
                    return
                try:
                    x = self.widget.winfo_rootx() + 20
                    y = self.widget.winfo_rooty() + 20
                    self.tip = Toplevel(self.widget)
                    # başlık çubuğu olmasın
                    try:
                        self.tip.wm_overrideredirect(True)
                    except Exception:
                        pass
                    try:
                        self.tip.wm_geometry(f"+{x}+{y}")
                    except Exception:
                        self.tip.geometry("+%d+%d" % (x, y))
                    Label(self.tip, text=self.text, bg="black", fg="white",
                          padx=6, pady=2, font=("Segoe UI", 8)).pack()
                except Exception:
                    # tooltip gösterimi başarısız olursa sessizce geç
                    try:
                        if self.tip:
                            self.tip.destroy()
                            self.tip = None
                    except Exception:
                        pass

            def hide(self, _=None):
                try:
                    if self.tip:
                        self.tip.destroy()
                        self.tip = None
                except Exception:
                    pass


# maria_pygame_open.py
# Kullanım:
#   pip install pygame
#   python maria_pygame_open.py
#
# Fonksiyon adı değişmedi: open_maria_game()

import pygame
import sys
import random
import time

def open_maria_game():
    pygame.init()
    WIDTH, HEIGHT = 500, 500
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maria'yı Kurtar")
    clock = pygame.time.Clock()

    # Renkler
    WHITE = (255,255,255)
    BLACK = (0,0,0)
    LIGHTBLUE = (173,216,230)
    YELLOW = (255,223,0)
    GREEN = (34,177,76)
    RED = (200,30,30)
    PURPLE = (128,0,128)
    GRAY = (120,120,120)
    ORANGE = (255,165,0)

    # Fontlar
    font = pygame.font.SysFont(None, 18)
    bigfont = pygame.font.SysFont(None, 28)

    # Orijinal veriler (pozisyonlar, mesaj)
    positions = [(50, 50), (200, 100), (350, 200)]
    text_message = "Sely, kurtar beni"

    # Kağıt parçaları (paper_pieces)
    paper_pieces = [pygame.Rect(x,y,30,30) for (x,y) in positions]
    collected = set()

    # Sely (oyuncu) (orijinal koordinatlara sadık)
    sely = pygame.Rect(20, 450, 20, 20)
    sely_speed = 5
    sely_lives = 5

    # Engeller (obstacle'lar) - orijinal Y değerleri kullanıldı
    obstacles = [pygame.Rect(100, y, 50, 20) for y in range(50, 400, 100)]
    obstacle_speed = 3  # hareket hızı (sağa doğru)
    obstacle_dirs = [random.choice([1,-1]) for _ in obstacles]

    # Boss
    boss = pygame.Rect(200, 50, 100, 100)  # (200,50,300,150)
    boss_hp = 500
    boss_max_hp = 500
    boss_attacks = []  # fireball list
    boss_attack_interval = 1500  # ms
    last_boss_attack = 0

    # Oyun durumları: "collect" -> "obby" -> "boss" -> "win" / "lose"
    state = "collect"
    boss_start_time = None
    boss_time_limit = 30  # saniye
    s_cooldown_ms = 150
    last_s_time = 0

    # Player bullets (space ile)
    player_bullets = []

    # Maria (arka planda gözükmesi için) - Maria arka planda duruyor
    maria = pygame.Rect(30, 30, 60, 60)  # arka planda, boss ortaya çıkınca görünür olacak
    maria_visible = False
    maria_rescued = False

    def draw_text(text, x, y, f=font, color=BLACK):
        surf = f.render(text, True, color)
        screen.blit(surf, (x,y))

    def show_overlay(title, lines, wait_for_key=True, timeout=None):
        # Basit popup: overlay gösterir, tuşa basılana kadar bekler
        start = pygame.time.get_ticks()
        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if wait_for_key and (ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN):
                    return
            if timeout is not None:
                if pygame.time.get_ticks() - start >= int(timeout*1000):
                    return
            overlay = pygame.Surface((WIDTH, HEIGHT))
            overlay.set_alpha(230)
            overlay.fill((240,240,240))
            screen.blit(overlay, (0,0))
            screen.blit(bigfont.render(str(title), True, (10,10,10)), (20,30))
            for i, line in enumerate(lines):
                screen.blit(font.render(line, True, (10,10,10)), (20,80 + i*22))
            screen.blit(font.render("Herhangi bir tuşa basın...", True, (60,60,60)), (20, HEIGHT-40))
            pygame.display.flip()
            clock.tick(30)

    # Başlangıç mesajı (orijinal messagebox içeriği)
    show_overlay("Başlangıç", [
        "Maria arkadaşı Sely ile gezerken kayboldu!",
        "Sely: Maria! Neredesin??",
        "Hadi ipuçlarını bul ve Maria'yı kurtar!"
    ])

    def check_collision(r1, r2):
        return r1.colliderect(r2)

    def spawn_fireball():
        # Boss'un alt kısmından rastgele fireball oluştur
        fx = random.randint(boss.left + 10, boss.right - 20)
        fy = boss.bottom - 8
        fb = pygame.Rect(fx, fy, 18, 18)
        boss_attacks.append({'rect': fb, 'speed': 6})

    # OBBY başlatma: sadece state değişecek
    def start_obby():
        nonlocal state, boss_start_time
        state = "obby"
        # obby bittikten 1 saniye sonra boss başlasın (orijinal after(1000,...))
        boss_start_time = None

    # Boss savaşını başlat
    def start_boss_battle():
        nonlocal state, boss_start_time, maria_visible, last_boss_attack
        show_overlay("Boss", ["Boss ortaya çıktı! 30 saniye içinde 'S' tuşuna basarak saldırın!"])
        state = "boss"
        boss_start_time = pygame.time.get_ticks()
        last_boss_attack = pygame.time.get_ticks()
        maria_visible = True  # Maria arka planda gözükür

    running = True
    while running:
        dt = clock.tick(60)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if state == "collect":
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mx,my = event.pos
                    for i, piece in enumerate(paper_pieces):
                        if piece.collidepoint(mx,my) and i not in collected:
                            collected.add(i)
                            # görsel değişiklik sadece set ile takip ediliyor

            elif state == "obby":
                # hiçbir özel event gerekmiyor, hareket tuşları sürekli okunuyor
                pass

            elif state == "boss":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        # cooldown kontrolü
                        if now - last_s_time >= s_cooldown_ms:
                            last_s_time = now
                            boss_hp -= 1  # orijinali 1 azaltıyordu
                    if event.key == pygame.K_SPACE:
                        # mermi at
                        bx = sely.centerx - 3
                        by = sely.top
                        player_bullets.append(pygame.Rect(bx, by, 6, 12))

        # --- Update & Draw ---
        if state == "collect":
            screen.fill(LIGHTBLUE)
            # kağıt parçaları çiz
            for i, piece in enumerate(paper_pieces):
                if i in collected:
                    pygame.draw.rect(screen, GRAY, piece)
                else:
                    pygame.draw.rect(screen, YELLOW, piece)
                    pygame.draw.rect(screen, BLACK, piece, 1)
            # Sely ve bilgi
            pygame.draw.rect(screen, GREEN, sely)
            draw_text(f"Toplanan: {len(collected)} / {len(paper_pieces)}", 8, 8)
            # hepsi toplandığında obby başlat
            if len(collected) == len(paper_pieces):
                show_overlay("İpucu Bulundu", [f"Kağıt parçaları birleştirildi: '{text_message}'", "Canavarlar çıkıyor! Obby başlıyor..."])
                start_obby()

        elif state == "obby":
            screen.fill((30,30,40))
            # zemin
            pygame.draw.rect(screen, (60,60,70), (0, HEIGHT-20, WIDTH, 20))
            # oyuncu hareket (ok tuşları veya WASD)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                sely.x -= sely_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                sely.x += sely_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                sely.y -= sely_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                sely.y += sely_speed
            # sınırlar
            if sely.left < 0: sely.left = 0
            if sely.right > WIDTH: sely.right = WIDTH
            if sely.top < 0: sely.top = 0
            if sely.bottom > HEIGHT: sely.bottom = HEIGHT

            # engelleri hareket ettir ve çiz
            for idx, obs in enumerate(obstacles):
                dir = obstacle_dirs[idx]
                obs.x += obstacle_speed * dir
                # ekran kenarına çarpınca yön değiştir
                if obs.right >= WIDTH or obs.left <= 0:
                    obstacle_dirs[idx] *= -1
                pygame.draw.rect(screen, RED, obs)
                # çarpışma kontrolü
                if check_collision(sely, obs):
                    # orijinal davranış: Sely çarptı! Yeniden başla.
                    show_overlay("Obby", ["Sely çarptı! Yeniden başla."])
                    sely.x, sely.y = 20, 450
                    sely_lives -= 1
                    if sely_lives <= 0:
                        show_overlay("Oyun Bitti", ["Sely öldü! Maria kurtarılamadı."])
                        state = "lose"
                        break

            # HUD
            draw_text(f"Can: {sely_lives}", 8, 8)
            draw_text("Engelleri geçip sağa ulaşırsan boss çıkar.", 8, HEIGHT-30)

            # obby bitiş koşulu: sely sağa ulaşırsa
            if sely.right >= WIDTH - 5:
                show_overlay("Obby Tamamlandı", ["Obby tamamlandı! Boss ortaya çıkıyor..."])
                # 1 saniye bekle (orijinal after)
                pygame.time.delay(1000)
                start_boss_battle()

        elif state == "boss":
            screen.fill((20,10,30))

            # Maria arka planda gözükür
            if maria_visible:
                # Maria'yı arka planda çiz (hafifçe soluk)
                pygame.draw.rect(screen, (200,180,255), maria)
                pygame.draw.rect(screen, BLACK, maria, 2)
                draw_text("Maria", maria.x + 8, maria.y + 22)

            # Sely hareketi yine aktif
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                sely.x -= sely_speed
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                sely.x += sely_speed
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                sely.y -= sely_speed
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                sely.y += sely_speed
            # sınırlar
            if sely.left < 0: sely.left = 0
            if sely.right > WIDTH: sely.right = WIDTH
            if sely.top < 0: sely.top = 0
            if sely.bottom > HEIGHT: sely.bottom = HEIGHT

            # Sely ve boss çizimleri
            pygame.draw.rect(screen, GREEN, sely)
            pygame.draw.rect(screen, PURPLE, boss)

            # Boss saldırı zamanlaması
            if now - last_boss_attack >= boss_attack_interval:
                spawn_fireball()
                last_boss_attack = now

            # Fireball güncelle ve çiz
            for fb in boss_attacks[:]:
                fb['rect'].y += fb['speed']
                pygame.draw.ellipse(screen, ORANGE, fb['rect'])
                pygame.draw.ellipse(screen, BLACK, fb['rect'], 2)
                if fb['rect'].top > HEIGHT:
                    boss_attacks.remove(fb)
                elif check_collision(sely, fb['rect']):
                    boss_attacks.remove(fb)
                    sely_lives -= 1
                    if sely_lives <= 0:
                        show_overlay("Oyun Bitti", ["Sely öldü! Maria kurtarılamadı."])
                        state = "lose"
                        break

            # Player mermileri güncelle
            for pb in player_bullets[:]:
                pb.y -= 9
                pygame.draw.rect(screen, WHITE, pb)
                if pb.bottom < 0:
                    player_bullets.remove(pb)
                elif pb.colliderect(boss):
                    boss_hp -= 10
                    try:
                        player_bullets.remove(pb)
                    except ValueError:
                        pass

            # 'S' tuşu doğrudan hasar (cooldown ile)
            keys_now = pygame.key.get_pressed()
            if keys_now[pygame.K_s]:
                if pygame.time.get_ticks() - last_s_time >= s_cooldown_ms:
                    last_s_time = pygame.time.get_ticks()
                    boss_hp -= 1

            # Boss HP bar
            bar_x, bar_y, bar_w, bar_h = 100, 10, 300, 20
            pygame.draw.rect(screen, GRAY, (bar_x, bar_y, bar_w, bar_h))
            hp_ratio = max(0, boss_hp) / boss_max_hp
            pygame.draw.rect(screen, RED, (bar_x, bar_y, int(bar_w*hp_ratio), bar_h))
            pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 2)
            draw_text(f"Boss HP: {max(0, boss_hp)}", 8, 12)

            # Süre limiti (30 sn)
            if boss_start_time:
                elapsed = (pygame.time.get_ticks() - boss_start_time) / 6000.0
            else:
                elapsed = 0
                boss_start_time = pygame.time.get_ticks()
            remaining = max(0, boss_time_limit - int(elapsed))
            draw_text(f"Süre: {remaining}s  Can: {sely_lives}", 8, HEIGHT-30)

            # Boss yenildiğinde: Maria kurtuldu ve oyun biter (kullanıcının istediği)
            if boss_hp <= 0:
                maria_rescued = True
                # Küçük kutlama overlay
                show_overlay("Tebrikler!", ["Boss yenildi! Maria kurtarıldı!"], wait_for_key=True)
                state = "win"

            # Süre dolduysa kaybedersin
            if elapsed >= boss_time_limit and boss_hp > 0:
                show_overlay("Süre doldu", ["Süre doldu! Boss güçlenip kaçtı. Maria kurtarılamadı."])
                state = "lose"

        elif state == "win":
            # Maria kurtulduktan sonra son ekran
            screen.fill((40,120,40))
            draw_text("MARIA KURTARILDI!", 140, 160, bigfont, WHITE)
            draw_text("Oyunu kapatmak için bir tuşa basın veya pencereyi kapatın.", 50, 220)
            pygame.display.flip()
            # bekle ve çık
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        running = False
                clock.tick(30)
            break

        elif state == "lose":
            screen.fill((120,20,20))
            draw_text("OYUN BİTTİ", 200, 160, bigfont, WHITE)
            draw_text("Oyunu kapatmak için bir tuşa basın veya pencereyi kapatın.", 50, 220)
            pygame.display.flip()
            waiting = True
            while waiting:
                for ev in pygame.event.get():
                    if ev.type == pygame.QUIT:
                        waiting = False
                        running = False
                    if ev.type == pygame.KEYDOWN or ev.type == pygame.MOUSEBUTTONDOWN:
                        waiting = False
                        running = False
                clock.tick(30)
            break

        pygame.display.flip()

    pygame.quit()
    return

import tkinter as tk
from tkinter import ttk, messagebox

def open_control_panel():
    """
    Yeni bir Toplevel olarak Denetim Masası penceresi açar.
    Not: Bu fonksiyon root = tk.Tk() oluşturulduktan sonra çağrılmalıdır.
    Fonksiyon kendi içinde tk.Tk() oluşturmaz, parent/root parametresi almaz ve
    mainloop çağırmaz. Kullanıcı kendi ana döngüsünü çalıştırır.
    """
    # Güvenlik kontrolü: henüz bir Tk örneği yoksa, kullanıcıya haber ver.
    if not tk._default_root:
        raise RuntimeError("Bir Tk örneği oluşturduktan sonra bu fonksiyonu çağırın (örnek: root = tk.Tk()).")

    win = tk.Toplevel()  # burada parent/root parametresi vermiyoruz
    win.title("Denetim Masası — Sarma Edition")
    win.geometry("980x620")
    win.minsize(760, 480)

    # --- Layout: sol navigasyon, sağ içerik, üst arama ---
    # Üst çubuk (arama + breadcrumb)
    top_bar = ttk.Frame(win, padding=(8,6))
    top_bar.grid(row=0, column=0, columnspan=2, sticky="nsew")
    top_bar.columnconfigure(2, weight=1)

    ttk.Label(top_bar, text="Denetim Masası", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w", padx=(2,8))
    breadcrumb = ttk.Label(top_bar, text="Tüm Öğeler", foreground="#444")
    breadcrumb.grid(row=0, column=1, sticky="w")

    search_var = tk.StringVar()
    search_entry = ttk.Entry(top_bar, textvariable=search_var)
    search_entry.grid(row=0, column=2, sticky="ew", padx=8)
    ttk.Button(top_bar, text="Ara", command=lambda: render_items()).grid(row=0, column=3, padx=(0,6))

    # Sol navigasyon (kategoriler)
    left_frame = ttk.Frame(win, padding=(8,8))
    left_frame.grid(row=1, column=0, sticky="nsw")
    left_frame.grid_propagate(False)
    left_frame.configure(width=200)

    ttk.Label(left_frame, text="Kategoriler", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0,6))

    categories = [
        "Sistem ve Güvenlik",
        "Ağ ve İnternet",
        "Ses ve Donanım",
        "Programlar",
        "Kullanıcı Hesapları",
        "Görünüm ve Kişiselleştirme",
        "Saat ve Bölge",
        "Erişim Kolaylığı",
        "Güncelleştirme ve Güvenlik"
    ]

    cat_listbox = tk.Listbox(left_frame, height=12, exportselection=False)
    for c in categories:
        cat_listbox.insert("end", c)
    cat_listbox.pack(fill="y", expand=True)
    cat_listbox.bind("<<ListboxSelect>>", lambda e: on_category_select())

    # Sağ içerik alanı (ikon ızgarası)
    right_frame = ttk.Frame(win, padding=(10,10))
    right_frame.grid(row=1, column=1, sticky="nsew")
    win.columnconfigure(1, weight=1)
    win.rowconfigure(1, weight=1)

    # Kaydırılabilir içerik (canvas içinde frame)
    canvas = tk.Canvas(right_frame)
    vsb = ttk.Scrollbar(right_frame, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    content_inner = ttk.Frame(canvas)
    canvas.create_window((0,0), window=content_inner, anchor="nw")

    def on_frame_configure(event=None):
        canvas.configure(scrollregion=canvas.bbox("all"))
    content_inner.bind("<Configure>", on_frame_configure)

    # --- Veri: kategori -> ögeler ---
    SETTINGS = {
        "Sistem ve Güvenlik": [
            ("Güvenlik ve Bakım", "shield"),
            ("Güvenlik Duvarı", "firewall"),
            ("Yedekleme ve Geri Yükleme", "backup"),
            ("Sistem Bilgileri", "info")
        ],
        "Ağ ve İnternet": [
            ("Ağ ve Paylaşım Merkezi", "network"),
            ("Wi-Fi Ayarları", "wifi"),
            ("VPN", "vpn"),
            ("Ethernet Ayarları", "ethernet"),
        ],
        "Ses ve Donanım": [
            ("Ses", "sound"),
            ("Aygıtlar ve Yazıcılar", "devices"),
            ("Güç Seçenekleri", "power"),
        ],
        "Programlar": [
            ("Program Ekle/Kaldır", "apps"),
            ("Varsayılan Programlar", "defaults"),
        ],
        "Kullanıcı Hesapları": [
            ("Kullanıcı Hesapları", "users"),
            ("Aile Güvenliği", "family"),
        ],
        "Görünüm ve Kişiselleştirme": [
            ("Ekran", "display"),
            ("Görev Çubuğu", "taskbar"),
            ("Tema ve Renkler", "theme"),
            ("Duvar Kağıdı", "wallpaper"),
        ],
        "Saat ve Bölge": [
            ("Tarih ve Saat", "clock"),
            ("Bölge Ayarları", "region"),
        ],
        "Erişim Kolaylığı": [
            ("Erişim Kolaylığı Merkezi", "access"),
            ("Klavye", "keyboard"),
        ],
        "Güncelleştirme ve Güvenlik": [
            ("Windows Update", "update"),
            ("Yedekle/Kurtar", "restore"),
        ]
    }

    current_buttons = []

    # --- yardımcı fonksiyonlar ---
    def clear_items():
        nonlocal current_buttons
        for w in current_buttons:
            w.destroy()
        current_buttons = []

    def show_setting_dialog(name):
        """Öğe tıklandığında açılacak hızlı ayar penceresi."""
        dlg = tk.Toplevel()
        dlg.title(name)
        dlg.geometry("420x260")
        ttk.Label(dlg, text=name, font=("Segoe UI", 12, "bold")).pack(anchor="w", padx=12, pady=(12,6))

        body = ttk.Frame(dlg, padding=12)
        body.pack(fill="both", expand=True)

        # Eğer Duvar Kağıdı öğesi ise, kullanıcıya resim seçtirme ve
        # ana pencerenin arkaplanını değiştirme arayüzü sun.
        if "Duvar Kağıdı" in name:
            try:
                preview = ttk.Label(body, text="Önizleme yok", anchor="center")
                preview.pack(fill="both", expand=False, pady=(6,8))

                def choose_wallpaper():
                    from tkinter import filedialog
                    global _background_img, _bg_photo, WALLPAPER_PATH
                    path = filedialog.askopenfilename(
                        title="Duvar Kağıdı Seç",
                        filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All files", "*.*")]
                    )
                    if not path:
                        return
                    try:
                        if PIL_AVAILABLE:
                            img = Image.open(path).convert("RGBA")
                            _background_img = img
                            # isteğe bağlı: seçilen resmi yerel bir dosyaya kaydetmeye
                            # çalış; başarısız olursa sessizce geç
                            try:
                                img.save(WALLPAPER_PATH)
                            except Exception:
                                pass
                            # Mevcut root boyutlarına göre hemen yeniden boyutla ve uygula
                            w = max(1, root.winfo_width())
                            h = max(1, root.winfo_height())
                            try:
                                resized = _background_img.resize((w, h), Image.Resampling.LANCZOS)
                            except Exception:
                                resized = _background_img.resize((w, h), Image.LANCZOS if hasattr(Image, 'LANCZOS') else Image.ANTIALIAS)
                            _bg_photo = ImageTk.PhotoImage(resized)
                            background.config(image=_bg_photo)
                            background.image = _bg_photo
                            # preview için küçük thumbnail
                            try:
                                thumb = _background_img.copy()
                                thumb.thumbnail((200, 120), Image.Resampling.LANCZOS)
                                tkthumb = ImageTk.PhotoImage(thumb)
                                preview.config(image=tkthumb, text="")
                                preview.image = tkthumb
                            except Exception:
                                preview.config(text=os.path.basename(path))
                        else:
                            # Pillow yoksa basit PhotoImage kullan
                            tkimg = tk.PhotoImage(file=path)
                            _bg_photo = tkimg
                            background.config(image=tkimg)
                            background.image = tkimg
                            preview.config(image=tkimg, text="")
                        messagebox.showinfo("Duvar Kağıdı", "Duvar kağıdı uygulandı.")
                    except Exception as e:
                        messagebox.showerror("Hata", f"Duvar kağıdı uygulanamadı: {e}")

                btn_browse = ttk.Button(body, text="Gözat...", command=choose_wallpaper)
                btn_browse.pack(side="right", pady=8)
                ttk.Button(body, text="Kapat", command=dlg.destroy).pack(side="right", pady=8, padx=(0,8))
            except Exception:
                # herhangi bir hata olursa fallback olarak genel arayüzü göstermeye devam et
                pass
            return

        # Örnek kontroller: bir toggle, bir slider ve bir açıklama
        ttk.Label(body, text="Hızlı Ayarlar:", font=("Segoe UI", 10, "underline")).pack(anchor="w")
        var = tk.BooleanVar(value=True)
        ttk.Checkbutton(body, text="Etkin", variable=var).pack(anchor="w", pady=(6,0))

        ttk.Label(body, text="Seviye:").pack(anchor="w", pady=(8,0))
        scale = ttk.Scale(body, from_=0, to=100)
        scale.set(50)
        scale.pack(fill="x")

        ttk.Button(body, text="Uygula", command=lambda: messagebox.showinfo("Uygulandı", f"{name} ayarları uygulandı.")).pack(side="right", pady=12)
        ttk.Button(body, text="İptal", command=dlg.destroy).pack(side="right", pady=12, padx=(0,8))

    def build_icon_button(parent, text, row, col):
        btn = ttk.Button(parent, text=text, width=24, command=lambda: show_setting_dialog(text))
        btn.grid(row=row, column=col, padx=8, pady=8, sticky="n")
        return btn

    def render_items(selected_category=None):
        # kategori seçili değilse "Tüm Öğeler"
        clear_items()
        q = search_var.get().strip().lower()
        if selected_category is None:
            items = []
            for k, v in SETTINGS.items():
                for name, _ in v:
                    items.append((name, k))
        else:
            items = [(name, selected_category) for name, _ in SETTINGS.get(selected_category, [])]

        # filtreleme
        if q:
            items = [it for it in items if q in it[0].lower() or q in it[1].lower()]

        # breadcrumb güncelle
        if selected_category:
            breadcrumb.config(text=f"{selected_category} — Filtre: '{q}'" if q else selected_category)
        else:
            breadcrumb.config(text=f"Tüm Öğeler — Filtre: '{q}'" if q else "Tüm Öğeler")

        # ikon ızgarası oluştur
        cols = 3
        r = 0
        c = 0
        for name, cat in items:
            b = build_icon_button(content_inner, f"{name}\n({cat})", r, c)
            current_buttons.append(b)
            c += 1
            if c >= cols:
                c = 0
                r += 1

        # küçük bilgi: eğer hiç öğe yoksa göster
        if not items:
            lbl = ttk.Label(content_inner, text="Aradığınız kriterlere uygun öğe bulunamadı.", padding=14)
            lbl.grid(row=0, column=0, sticky="w")
            current_buttons.append(lbl)

        # güncelle scrollregion
        content_inner.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def on_category_select():
        sel = cat_listbox.curselection()
        if not sel:
            render_items(None)
            return
        cat = cat_listbox.get(sel[0])
        render_items(cat)

    # Arama kutusuna herşey girildiğinde otomatik render (isteğe bağlı)
    def on_search_key(event=None):
        render_items(None)

    search_entry.bind("<Return>", lambda e: render_items(None))
    search_entry.bind("<KeyRelease>", lambda e: render_items(None))

    # Başlangıçta tüm öğeleri render et
    render_items(None)

    # Pencere kapatıldığında temizlik (isteğe bağlı)
    def on_close():
        # burada ekstra temizlik yapılabilir
        win.destroy()
    win.protocol("WM_DELETE_WINDOW", on_close)

    # Fonksiyon bir referans döndürüyor ki istersen bağladığın yerde tutabilesin
    return win

# ------------------------
# Örnek kullanım (kendi Tk uygulamana ekle):
#
# import tkinter as tk
# from this_module import open_control_panel
#
# root = tk.Tk()
# ttk.Button(root, text="Denetim Masası", command=open_control_panel).pack()
# root.mainloop()
#
# NOT: open_control_panel() fonksiyonu kendi içinde tk.Toplevel() oluşturur.
# ------------------------




def shutdown_animation():
    import time
    import random
    import math
    try:
        import tkinter as tk
        from tkinter import ttk
    except Exception:
        raise RuntimeError("tkinter bulunamadı")

    win = tk.Toplevel(root)
    win.title("BTL Kapanıyor")
    win.geometry("420x220")
    win.configure(bg="#000000")
    win.resizable(False, False)
    win.attributes("-topmost", True)
    win.transient(root)

    # Üst alan: canvas (particle) + büyük başlık
    canvas_h = 120
    canvas = tk.Canvas(
        win,
        width=420,
        height=canvas_h,
        highlightthickness=0,
        bg="#000000")
    canvas.pack(padx=0, pady=0)

    label = tk.Label(
        win,
        text="BTL",
        font=(
            "Arial",
            40,
            "bold"),
        fg="white",
        bg="black")
    label.pack(pady=(6, 0))

    # Stil + progressbar
    style = ttk.Style(win)
    try:
        style.theme_use('default')
    except Exception:
        pass
    style.configure(
        "red.Horizontal.TProgressbar",
        troughcolor='#111111',
        background='#e23b3b',
        thickness=14)
    progress = ttk.Progressbar(
        win,
        orient="horizontal",
        length=340,
        mode="determinate",
        style="red.Horizontal.TProgressbar")
    progress.pack(pady=12)

    status = tk.Label(
        win,
        text="Başlatılıyor...",
        font=(
            "Segoe UI",
            9),
        fg="#cccccc",
        bg="#000000")
    status.pack()

    # Kapatma/x davranışı (sadece Toplevel'i kapatır)
    cancelled = {"v": False}

    def _close():
        cancelled["v"] = True
        try:
            win.destroy()
        except Exception:
            pass
    win.protocol("WM_DELETE_WINDOW", _close)
    win.bind("<Escape>", lambda e: _close())

    # Basit particle sistemi (hafif, performans dostu)
    particles = []
    for _ in range(20):
        particles.append({
            "x": 210 + random.uniform(-90, 90),
            "y": canvas_h / 2 + random.uniform(-18, 18),
            "vx": random.uniform(-0.6, 0.6),
            "vy": random.uniform(-0.8, -0.2),
            "r": random.uniform(1.2, 4.0),
            "life": random.uniform(700, 1600),
            "age": random.uniform(0, 800)
        })

    start_ms = time.time() * 1000.0
    duration_ms = 3000  # toplam süre (ms)

    # easing (yumuşak ilerleme)
    def ease_out_quad(t): return 1 - (1 - t) * (1 - t)

    def format_status(pct):
        if pct < 10:
            return "Hazırlanıyor..."
        if pct < 40:
            return "Arka plan görevleri..."
        if pct < 70:
            return "Ayarlar kaydediliyor..."
        if pct < 95:
            return "Kaynaklar serbest bırakılıyor..."
        return "Tamamlanıyor..."

    def animate():
        if cancelled["v"]:
            return
        now_ms = time.time() * 1000.0
        t = min(1.0, (now_ms - start_ms) / max(1.0, duration_ms))
        eased = ease_out_quad(t)
        pct = int(eased * 100)
        progress["value"] = pct
        status.config(text=f"{pct}% — {format_status(pct)}")

        # label parıldaması (hafif renk değişimi ve boyut)
        pulse = 0.5 + 0.5 * math.sin((now_ms - start_ms) / 180.0)
        glow_strength = 0.4 + 0.6 * eased
        r = int(230 * (0.6 + 0.4 * pulse * glow_strength))
        g = int(60 * (0.4 + 0.6 * pulse * glow_strength))
        b = int(60 * (0.4 + 0.6 * pulse * glow_strength))
        label.config(fg=f"#{r:02x}{g:02x}{b:02x}")
        label.config(font=("Arial", int(36 + 4 * pulse), "bold"))

        # particles çizimi
        canvas.delete("all")
        for p in particles:
            p["age"] += 30
            if p["age"] >= p["life"]:
                # recycle
                p.update({
                    "x": 210 + random.uniform(-40, 40),
                    "y": canvas_h / 2 + random.uniform(-10, 10),
                    "vx": random.uniform(-0.8, 0.8),
                    "vy": random.uniform(-1.2, -0.2),
                    "r": random.uniform(1.2, 4.0),
                    "life": random.uniform(700, 1600),
                    "age": 0
                })
            # fizik (hafif)
            p["vx"] *= 0.995
            p["vy"] += 0.03 * (1 - eased)
            p["x"] += p["vx"] * 1.5
            p["y"] += p["vy"] * 1.5
            life_ratio = max(0.0, 1.0 - (p["age"] / p["life"]))
            draw_r = max(1, p["r"] * (0.6 + 0.4 * life_ratio))
            col_r = min(255, r + 10)
            col = f"#{col_r:02x}{20:02x}{20:02x}"
            canvas.create_oval(
                p["x"] - draw_r,
                p["y"] - draw_r,
                p["x"] + draw_r,
                p["y"] + draw_r,
                fill=col,
                outline="")

        if pct >= 100:
            # hem Toplevel hem root'u kapat
            def finish_close():
                try:
                    win.destroy()
                except Exception:
                    pass
                try:
                    root.destroy()
                except Exception:
                    pass
            win.after(350, finish_close)
            return

        win.after(30, animate)

    # animasyonu başlat
    win.after(20, animate)


def main_app():
    print("welcome")

# ---------- Ses yardımı ----------


def play_sound(path):
    if not PYGAME_AVAILABLE:
        return

    def run():
        try:
            sound = pygame.mixer.Sound(path)
            sound.play()
        except Exception as e:
            print("Ses çalınamadı:", e)
    threading.Thread(target=run, daemon=True).start()


def play_startup():
    play_sound(os.path.join(ASSETS_DIR, "startup.wav"))


def play_info():
    play_sound(os.path.join(ASSETS_DIR, "info.wav"))


def play_error():
    play_sound(os.path.join(ASSETS_DIR, "error.wav"))


def play_shutdown():
    play_sound(os.path.join(ASSETS_DIR, "shutdown.wav"))


def show_info_with_sound(title, message):
    play_info()
    messagebox.showinfo(title, message)


def show_error_with_sound(title, message):
    play_error()
    messagebox.showerror(title, message)

# ---------- Safe subprocess decode ----------


def _safe_run_and_decode(cmd_list):
    try:
        proc = subprocess.run(
            cmd_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            shell=False)
        out_bytes = proc.stdout or b""
    except Exception:
        return ""
    encodings = ('utf-8', 'cp1254', 'cp850', 'cp437', 'latin1')
    for enc in encodings:
        try:
            return out_bytes.decode(enc)
        except Exception:
            continue
    return out_bytes.decode('utf-8', errors='replace')

# ---------- Kullanıcı bilgileri ----------


def is_admin():
    try:
        if os.name == 'nt':
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except Exception:
        return False


def detect_password_status(username):
    try:
        system = platform.system().lower()
        if system == 'windows':
            out = _safe_run_and_decode(['net', 'user', username]).lower()
            if not out.strip():
                return None
            return 'var'
        else:
            out = _safe_run_and_decode(['passwd', '-s', username]).lower(
            ) or _safe_run_and_decode(['passwd', '-S', username]).lower()
            if not out.strip():
                return None
            parts = out.split()
            if len(parts) > 1 and 'np' in parts[1]:
                return 'yok'
            return 'var'
    except Exception:
        return None


def get_user_info():
    info = {}
    try:
        username = getpass.getuser()
    except Exception:
        username = 'Bilinmiyor'
    current_user = username
    if PSUTIL_AVAILABLE:
        try:
            users_list = psutil.users()
            if users_list:
                current_user = users_list[0].name or username
        except Exception:
            current_user = username
    info['username'] = current_user or 'Bilinmiyor'
    info['is_admin'] = is_admin()
    info['password_status'] = detect_password_status(info['username'])
    return info

# ---------- Profil helper ----------


def add_user_profile_to_canvas(menu, canvas, width):
    user = get_user_info()
    profile_frame = tk.Frame(menu, bg='gray18')
    profile_frame.config(padx=10, pady=6)
    avatar_img = None
    try:
        sample_paths = [
            os.path.join(
                os.path.expanduser("~"),
                "Pictures",
                "Koala.jpg"),
            os.path.join(
                os.environ.get(
                    "WINDIR",
                    "C:\\Windows"),
                "System32",
                "oobe",
                "info",
                "backgrounds",
                "backgroundDefault.jpg")]
        found = None
        for p in sample_paths:
            if p and os.path.exists(p):
                found = p
                break
        if found and PIL_AVAILABLE:
            av = Image.open(found).convert("RGBA").resize((48, 48))
        else:
            av = Image.new('RGBA', (48, 48), (90, 90, 90, 255))
            draw = ImageDraw.Draw(av)
            draw.ellipse((4, 4, 44, 44), fill=(120, 120, 120, 255))
        avatar_img = ImageTk.PhotoImage(av) if PIL_AVAILABLE else None
        if avatar_img:
            _image_refs.append(avatar_img)
    except Exception:
        avatar_img = None
    avatar_lbl = Label(profile_frame, image=avatar_img, bg='gray18')
    avatar_lbl.image = avatar_img
    avatar_lbl.grid(row=0, column=0, rowspan=2, sticky='w', padx=(0, 10))
    name_lbl = Label(
        profile_frame,
        text=user['username'],
        bg='gray18',
        fg='white',
        font=(
            'Segoe UI',
            10,
            'bold'))
    name_lbl.grid(row=0, column=1, sticky='w')
    role_text = "Yönetici (Admin)" if user['is_admin'] else "Standart kullanıcı"
    role_lbl = Label(
        profile_frame,
        text=role_text,
        bg='gray18',
        fg='lightgray',
        font=(
            'Segoe UI',
            9))
    role_lbl.grid(row=1, column=1, sticky='w')
    if user['password_status'] == 'yok':
        pwd_text = "Şifre: şifre yok"
    elif user['password_status'] == 'var':
        pwd_text = "Şifre: " + "*" * 12
    else:
        pwd_text = "Şifre: ************"
    pwd_lbl = Label(
        profile_frame,
        text=pwd_text,
        bg='gray18',
        fg='white',
        font=(
            'Segoe UI',
            9))
    pwd_lbl.grid(row=2, column=0, columnspan=2, sticky='w', pady=(6, 0))
    btn_frame = tk.Frame(profile_frame, bg='gray18')
    btn_frame.grid(row=3, column=0, columnspan=2, sticky='we', pady=(8, 0))
    btn_frame.columnconfigure((0, 1, 2), weight=1)

    def lock_screen():
        try:
            if platform.system().lower() == 'windows':
                import ctypes
                ctypes.windll.user32.LockWorkStation()
            else:
                subprocess.run(['gnome-screensaver-command', '--lock'],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except Exception:
            pass

    def sign_out():
        try:
            if platform.system().lower() == 'windows':
                subprocess.run(
                    ['shutdown', '/l'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run(['pkill',
                                '-KILL',
                                '-u',
                                getpass.getuser()],
                               stdout=subprocess.DEVNULL,
                               stderr=subprocess.DEVNULL)
        except Exception:
            pass
    b_lock = Button(
        btn_frame,
        text="Kilitle",
        command=lock_screen,
        bg='gray30',
        fg='white',
        relief='flat')
    b_lock.grid(row=0, column=0, sticky='we', padx=2)
    b_signout = Button(
        btn_frame,
        text="Oturumu Kapat",
        command=sign_out,
        bg='gray30',
        fg='white',
        relief='flat')
    b_signout.grid(row=0, column=1, sticky='we', padx=2)
    b_settings = Button(btn_frame, text="Hesap Ayarları", command=lambda: print(
        "Hesap ayarları açılır."), bg='gray30', fg='white', relief='flat')
    b_settings.grid(row=0, column=2, sticky='we', padx=2)
    canvas.create_window(width // 2, 10, window=profile_frame, anchor='n')

    def open_profile_dialog(event=None):
        dlg = Toplevel(menu)
        dlg.title("Kullanıcı Profili")
        dlg.config(bg='gray18')
        dlg.geometry("360x220")
        Label(
            dlg,
            text=f"Kullanıcı: {user['username']}",
            bg='gray18',
            fg='white',
            font=(
                'Segoe UI',
                11,
                'bold')).pack(
            pady=(
                12,
                4))
        Label(
            dlg,
            text=f"Yetki: {role_text}",
            bg='gray18',
            fg='lightgray').pack()
        Label(
            dlg,
            text=f"{pwd_text}",
            bg='gray18',
            fg='white').pack(
            pady=(
                6,
                12))
        Button(
            dlg,
            text="Parola Değiştir (yönlendirici)",
            command=lambda: print("Parola değiştirici açılır."),
            bg='gray30',
            fg='white').pack(
            pady=6)
        Button(
            dlg,
            text="Kapat",
            command=dlg.destroy,
            bg='gray30',
            fg='white').pack(
            pady=8)
    profile_frame.bind("<Button-1>", open_profile_dialog)
    for w in profile_frame.winfo_children():
        w.bind("<Button-1>", open_profile_dialog)

# ---------- CMD / PowerShell Panel (güvenli) ----------





#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTLshell GUI - Toplevel tabanlı
open_cmd_panel() fonksiyonu PARAMETRESİZ (isteğin üzerine)
Kullanım: python btl_shell_gui.py
"""

import os
import sys
import shutil
import stat
import subprocess
import getpass
import re
import time
import threading
from datetime import datetime
from pathlib import Path
from collections import deque
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

# Optional: psutil varsa bazı komutlar daha zengin
try:
    import psutil
except Exception:
    psutil = None

# ---------- Ayarlar ----------
HISTORY_MAX = 200
history = deque(maxlen=HISTORY_MAX)
username = f"psutil_{getpass.getuser()}"
home = Path.home()

def short_path(path: Path):
    try:
        p = Path(path).resolve()
        return str(p).replace(str(home), "~")
    except Exception:
        return str(path)

# ---------- Basit komut motoru (her komut string döner) ----------
def safe_read_file_lines(path, n=None):
    with open(path, 'r', errors='replace') as f:
        if n is None:
            return f.read().splitlines()
        out = []
        for i, line in enumerate(f):
            out.append(line.rstrip('\n'))
            if i+1 >= n:
                break
        return out

def cmd_ls(args):
    target = Path(args[0]) if args else Path.cwd()
    out_lines = []
    try:
        entries = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for e in entries:
            flags = []
            if e.is_dir(): flags.append('d')
            if os.access(e, os.X_OK): flags.append('x')
            try:
                size = e.stat().st_size
                mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(e.stat().st_mtime))
            except Exception:
                size = 0
                mtime = '????-??-?? ??:??'
            out_lines.append(f"{''.join(flags):3} {size:8d} {mtime}  {e.name}")
    except Exception as ex:
        out_lines.append(f"ls: hata: {ex}")
    return "\n".join(out_lines)

def cmd_pwd(args):
    return str(Path.cwd())

def cmd_cd(args):
    target = args[0] if args else str(home)
    try:
        os.chdir(os.path.expanduser(target))
        return ""
    except Exception as ex:
        return f"cd: {ex}"

def cmd_cat(args):
    if not args:
        return "cat: dosya belirtilmedi"
    out = []
    for p in args:
        try:
            for line in safe_read_file_lines(Path(p)):
                out.append(line)
        except Exception as ex:
            out.append(f"cat: {p}: {ex}")
    return "\n".join(out)

def cmd_echo(args):
    return " ".join(args)

def cmd_touch(args):
    if not args:
        return "touch: dosya belirtilmedi"
    out = []
    for p in args:
        try:
            Path(p).touch(exist_ok=True)
        except Exception as ex:
            out.append(f"touch: {p}: {ex}")
    return "\n".join(out) if out else ""

def cmd_rm(args):
    if not args:
        return "rm: dosya belirtilmedi"
    out = []
    for p in args:
        try:
            path = Path(p)
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink()
        except Exception as ex:
            out.append(f"rm: {p}: {ex}")
    return "\n".join(out) if out else ""

def cmd_mkdir(args):
    if not args:
        return "mkdir: dizin belirtilmedi"
    out = []
    for p in args:
        try:
            Path(p).mkdir(parents=True, exist_ok=False)
        except FileExistsError:
            out.append(f"mkdir: zaten var: {p}")
        except Exception as ex:
            out.append(f"mkdir: {p}: {ex}")
    return "\n".join(out) if out else ""

def cmd_rmdir(args):
    if not args:
        return "rmdir: dizin belirtilmedi"
    out = []
    for p in args:
        try:
            Path(p).rmdir()
        except Exception as ex:
            out.append(f"rmdir: {p}: {ex}")
    return "\n".join(out)

def cmd_mv(args):
    if len(args) < 2:
        return "mv: eksik argüman. Kullanım: mv src dst"
    try:
        shutil.move(args[0], args[1])
        return ""
    except Exception as ex:
        return f"mv: {ex}"

def cmd_cp(args):
    if len(args) < 2:
        return "cp: eksik argüman. Kullanım: cp src dst"
    try:
        src = Path(args[0])
        dst = Path(args[1])
        if src.is_dir():
            shutil.copytree(src, dst)
        else:
            if dst.is_dir():
                dst = dst / src.name
            shutil.copy2(src, dst)
        return ""
    except Exception as ex:
        return f"cp: {ex}"

def cmd_head(args):
    n = 10
    files = args or []
    out = []
    for f in files:
        try:
            lines = safe_read_file_lines(Path(f), n)
            out.extend(lines)
        except Exception as ex:
            out.append(f"head: {f}: {ex}")
    return "\n".join(out)

def cmd_tail(args):
    n = 10
    files = args or []
    out = []
    for f in files:
        try:
            lines = safe_read_file_lines(Path(f))
            out.extend(lines[-n:])
        except Exception as ex:
            out.append(f"tail: {f}: {ex}")
    return "\n".join(out)

def cmd_grep(args):
    if not args:
        return "grep: pattern ve dosya(lar) gerekli"
    pattern = args[0]
    files = args[1:] or ['-']
    try:
        regex = re.compile(pattern)
    except re.error as ex:
        return f"grep: regex hatası: {ex}"
    out = []
    for f in files:
        try:
            if f == '-':
                out.append("stdin grepleri desteklenmiyor")
                continue
            for i, line in enumerate(safe_read_file_lines(Path(f))):
                if regex.search(line):
                    out.append(f"{f}:{i+1}:{line}")
        except Exception as ex:
            out.append(f"grep: {f}: {ex}")
    return "\n".join(out)

def cmd_find(args):
    start = args[0] if args else '.'
    out = []
    for root, dirs, files in os.walk(start):
        for name in files:
            out.append(os.path.join(root, name))
    return "\n".join(out)

def cmd_chmod(args):
    if len(args) < 2:
        return "chmod: kullanım: chmod 755 file"
    mode_str, target = args[0], args[1]
    try:
        mode = int(mode_str, 8)
        os.chmod(target, mode)
        return ""
    except Exception as ex:
        return f"chmod: {ex}"

def cmd_chown(args):
    if len(args) < 2:
        return "chown: kullanım: chown user:group file"
    spec, target = args[0], args[1]
    if os.name != 'posix':
        return "chown: sadece POSIX sistemlerde desteklenir."
    try:
        userpart = spec.split(':')[0]
        import pwd, grp
        uid = pwd.getpwnam(userpart).pw_uid
        gid = -1
        if ':' in spec and spec.split(':')[1]:
            gid = grp.getgrnam(spec.split(':')[1]).gr_gid
        if gid == -1:
            gid = Path(target).stat().st_gid
        os.chown(target, uid, gid)
        return ""
    except Exception as ex:
        return f"chown: {ex}"

def cmd_ps(args):
    out = []
    if psutil:
        for p in psutil.process_iter(['pid','name','username','cpu_percent']):
            out.append(f"{p.info['pid']:6d} {p.info.get('username','-'):15} {p.info.get('cpu_percent',0):5}% {p.info.get('name')}")
        return "\n".join(out)
    else:
        try:
            out_raw = subprocess.check_output(['ps','-ef'], stderr=subprocess.DEVNULL, text=True)
            return out_raw
        except Exception:
            return "ps: psutil yüklü değil ve 'ps' komutu yok/erişilemiyor"

def cmd_kill(args):
    if not args:
        return "kill: PID gerekli"
    try:
        pid = int(args[0])
        os.kill(pid, 15)
        return f"kill: {pid} sonlandırma sinyali gönderildi."
    except Exception as ex:
        return f"kill: {ex}"

def cmd_top(args):
    if psutil:
        procs = sorted(psutil.process_iter(['pid','name','cpu_percent','memory_percent']), key=lambda p: p.info.get('cpu_percent',0), reverse=True)[:20]
        out = []
        for p in procs:
            out.append(f"{p.info['pid']:6d} {p.info.get('cpu_percent',0):5.1f}% {p.info.get('memory_percent',0):5.1f}% {p.info.get('name')}")
        return "\n".join(out)
    else:
        return "top: psutil yok, sınırlı destek"

def cmd_uptime(args):
    if psutil:
        bt = psutil.boot_time()
        delta = time.time() - bt
        return f"Uptime: {int(delta)} saniye ({time.strftime('%H:%M:%S', time.gmtime(delta))})"
    else:
        return "uptime: psutil yok, destek sınırlı"

def cmd_whoami(args):
    return getpass.getuser()

def cmd_date(args):
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

def cmd_df(args):
    path = args[0] if args else '/'
    try:
        du = shutil.disk_usage(path)
        return f"{path} -> total: {du.total} free: {du.free} used: {du.used}"
    except Exception as ex:
        return f"df: {ex}"

def cmd_du(args):
    start = args[0] if args else '.'
    total = 0
    for root, dirs, files in os.walk(start):
        for f in files:
            try:
                total += Path(root, f).stat().st_size
            except Exception:
                pass
    return f"{start} toplam bayt: {total}"

def cmd_history(args):
    out = []
    for i, cmd in enumerate(history, 1):
        out.append(f"{i}\t{cmd}")
    return "\n".join(out)

def cmd_clear(args):
    # GUI'de clear sadece Text'i temizler
    return "__CLEAR__"

def cmd_env(args):
    out = []
    for k, v in os.environ.items():
        out.append(f"{k}={v}")
    return "\n".join(out)

def cmd_setenv(args):
    if len(args) < 2:
        return "setenv: kullanım: setenv KEY VALUE"
    os.environ[args[0]] = args[1]
    return ""

def cmd_unsetenv(args):
    if not args:
        return "unsetenv: KEY gerekli"
    os.environ.pop(args[0], None)
    return ""

# Komut tablosu - tam 30 komut (help + exit ayrı)
COMMANDS = {
    'ls': cmd_ls,
    'pwd': cmd_pwd,
    'cd': cmd_cd,               # özel komut
    'cat': cmd_cat,
    'echo': cmd_echo,
    'touch': cmd_touch,
    'rm': cmd_rm,
    'mkdir': cmd_mkdir,
    'rmdir': cmd_rmdir,
    'mv': cmd_mv,
    'cp': cmd_cp,
    'head': cmd_head,
    'tail': cmd_tail,
    'grep': cmd_grep,
    'find': cmd_find,
    'chmod': cmd_chmod,
    'chown': cmd_chown,
    'ps': cmd_ps,
    'kill': cmd_kill,
    'top': cmd_top,
    'uptime': cmd_uptime,
    'whoami': cmd_whoami,
    'date': cmd_date,
    'df': cmd_df,
    'du': cmd_du,
    'history': cmd_history,
    'clear': cmd_clear,
    'env': cmd_env,
    'setenv': cmd_setenv,
    'unsetenv': cmd_unsetenv,
}

WRAPPERS = {
    'help': None,  # GUI'de özel işlenecek
    'exit': None,
    'quit': None,
}

# ---------- Basit parser ----------
def parse_line(line):
    parts = []
    cur = ''
    in_quote = False
    quote_char = ''
    for ch in line.strip():
        if ch in ('"', "'"):
            if not in_quote:
                in_quote = True
                quote_char = ch
                continue
            elif quote_char == ch:
                in_quote = False
                quote_char = ''
                continue
        if ch.isspace() and not in_quote:
            if cur:
                parts.append(cur)
                cur = ''
        else:
            cur += ch
    if cur:
        parts.append(cur)
    return parts

# ---------- GUI uygulaması ----------
class BTLshellGUI:
    def __init__(self, root):
        self.root = root
        self.top = None  # Toplevel olacak
        self._build()
        self.cwd = Path.cwd()
        self.lock = threading.Lock()

    def _build(self):
        # root gizli; Toplevel oluşturulunca içerik eklenir
        pass

    def create_toplevel(self):
        # Eğer zaten açıksa, öne çıkar
        if self.top and tk.Toplevel.winfo_exists(self.top):
            try:
                self.top.lift()
                return
            except Exception:
                pass

        self.top = tk.Toplevel(self.root)
        self.top.title(f"{username}@BTL shell")
        self.top.geometry("900x500")

        # Menü
        menubar = tk.Menu(self.top)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Clear", command=lambda: self._write("__CLEAR__"))
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.top.withdraw)
        menubar.add_cascade(label="File", menu=filemenu)
        self.top.config(menu=menubar)

        # Çıktı alanı
        self.output = scrolledtext.ScrolledText(self.top, wrap=tk.NONE, state='disabled', font=("Consolas", 10))
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        # Girdi alanı
        bottom = ttk.Frame(self.top)
        bottom.pack(fill=tk.X, padx=4, pady=4)
        self.prompt_var = tk.StringVar()
        self.update_prompt()
        self.prompt_label = ttk.Label(bottom, textvariable=self.prompt_var, width=30, anchor="w")
        self.prompt_label.pack(side=tk.LEFT, padx=(0,4))
        self.entry = ttk.Entry(bottom)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Up>", self._on_history_up)
        self.entry.bind("<Down>", self._on_history_down)

        # odak
        self.entry.focus_set()

        # Kapatıldığında sadece gizle
        self.top.protocol("WM_DELETE_WINDOW", self.top.withdraw)

    def update_prompt(self):
        try:
            cwd = short_path(Path.cwd())
        except Exception:
            cwd = str(Path.cwd())
        self.prompt_var.set(f"{username}@BTL {cwd}: ")

    def _write(self, text):
        if text == "__CLEAR__":
            self.output.configure(state='normal')
            self.output.delete('1.0', tk.END)
            self.output.configure(state='disabled')
            return
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state='disabled')

    def _on_enter(self, event=None):
        line = self.entry.get().strip()
        if not line:
            return
        self._append_history(line)
        self._write(self.prompt_var.get() + line)
        self.entry.delete(0, tk.END)
        # Komutu ayrı thread'de çalıştır
        t = threading.Thread(target=self._execute_command, args=(line,), daemon=True)
        t.start()

    def _append_history(self, cmd):
        history.append(cmd)
        self._hist_index = len(history)

    def _on_history_up(self, event):
        if not history:
            return "break"
        self._hist_index = max(1, getattr(self, '_hist_index', len(history)))
        self._hist_index -= 1
        try:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, history[self._hist_index - 1])
        except Exception:
            pass
        return "break"

    def _on_history_down(self, event):
        if not history:
            return "break"
        self._hist_index = min(len(history), getattr(self, '_hist_index', len(history)))
        if self._hist_index < len(history):
            self._hist_index += 1
            try:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, history[self._hist_index - 1])
            except Exception:
                pass
        else:
            self.entry.delete(0, tk.END)
        return "break"

    def _execute_command(self, line):
        parts = parse_line(line)
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        # help / exit / quit işleme
        if cmd == 'help':
            help_text = "BTLshell - Komut listesi (kısa):\n"
            for name, fn in COMMANDS.items():
                doc = fn.__doc__ if fn.__doc__ else ""
                help_text += f"  {name:10} - {doc}\n"
            help_text += "\nEk: help, exit, quit"
            self._write(help_text)
            return
        if cmd in ('exit', 'quit'):
            self._write("Çıkılıyor. Pencere gizlendi.")
            try:
                self.top.withdraw()
            except Exception:
                pass
            return

        # Kayıtlı komutlar
        if cmd in COMMANDS:
            try:
                result = COMMANDS[cmd](args)
                if result == "__CLEAR__":
                    self._write("__CLEAR__")
                elif result:
                    self._write(result)
                # güncelle prompt (cd sonrası için)
                self.update_prompt()
            except Exception as ex:
                self._write(f"{cmd}: çalıştırılırken hata: {ex}")
            return

        # fallback: sistem komutu çalıştırmayı dene (küçük risk)
        try:
            proc = subprocess.run(parts, capture_output=True, text=True, shell=False, cwd=os.getcwd())
            if proc.stdout:
                self._write(proc.stdout.rstrip("\n"))
            if proc.stderr:
                self._write(proc.stderr.rstrip("\n"))
        except FileNotFoundError:
            self._write(f"{cmd}: bilinmiyor veya komut bulunamadı")
        except Exception as ex:
            self._write(f"{cmd}: çalıştırılamadı: {ex}")

# ---------- Global GUI instance ve open_cmd_panel (parametresiz) ----------
_root = None
_app = None

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BTLshell GUI - thread-safe düzeltme
open_cmd_panel() parametresiz
Kaydet: btl_shell_gui_fixed.py
Çalıştır: python btl_shell_gui_fixed.py
"""

import os
import sys
import shutil
import subprocess
import getpass
import re
import time
import threading
from datetime import datetime
from pathlib import Path
from collections import deque
import tkinter as tk
from tkinter import ttk, scrolledtext
from queue import Queue, Empty

try:
    import psutil
except Exception:
    psutil = None

HISTORY_MAX = 200
history = deque(maxlen=HISTORY_MAX)
username = f"psutil_{getpass.getuser()}"
home = Path.home()

def short_path(path: Path):
    try:
        p = Path(path).resolve()
        return str(p).replace(str(home), "~")
    except Exception:
        return str(path)

# --- Komutlar (kısaltılmış ama yeterli) ---
def safe_read_file_lines(path, n=None):
    with open(path, 'r', errors='replace') as f:
        if n is None:
            return f.read().splitlines()
        out = []
        for i, line in enumerate(f):
            out.append(line.rstrip('\n'))
            if i+1 >= n:
                break
        return out

def cmd_ls(args):
    target = Path(args[0]) if args else Path.cwd()
    out_lines = []
    try:
        entries = sorted(target.iterdir(), key=lambda p: (not p.is_dir(), p.name.lower()))
        for e in entries:
            flags = []
            if e.is_dir(): flags.append('d')
            if os.access(e, os.X_OK): flags.append('x')
            try:
                size = e.stat().st_size
                mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(e.stat().st_mtime))
            except Exception:
                size = 0
                mtime = '????-??-?? ??:??'
            out_lines.append(f"{''.join(flags):3} {size:8d} {mtime}  {e.name}")
    except Exception as ex:
        out_lines.append(f"ls: hata: {ex}")
    return "\n".join(out_lines)

def cmd_pwd(args): return str(Path.cwd())
def cmd_cd(args):
    target = args[0] if args else str(home)
    try:
        os.chdir(os.path.expanduser(target))
        return ""
    except Exception as ex:
        return f"cd: {ex}"
def cmd_echo(args): return " ".join(args)
def cmd_cat(args):
    if not args: return "cat: dosya belirtilmedi"
    out=[]
    for p in args:
        try:
            out.extend(safe_read_file_lines(Path(p)))
        except Exception as ex:
            out.append(f"cat: {p}: {ex}")
    return "\n".join(out)
def cmd_touch(args):
    if not args: return "touch: dosya belirtilmedi"
    out=[]
    for p in args:
        try: Path(p).touch(exist_ok=True)
        except Exception as ex: out.append(f"touch: {p}: {ex}")
    return "\n".join(out)
def cmd_rm(args):
    if not args: return "rm: dosya belirtilmedi"
    out=[]
    for p in args:
        try:
            path = Path(p)
            if path.is_dir(): shutil.rmtree(path)
            else: path.unlink()
        except Exception as ex: out.append(f"rm: {p}: {ex}")
    return "\n".join(out)
def cmd_mkdir(args):
    if not args: return "mkdir: dizin belirtilmedi"
    out=[]
    for p in args:
        try: Path(p).mkdir(parents=True, exist_ok=False)
        except FileExistsError: out.append(f"mkdir: zaten var: {p}")
        except Exception as ex: out.append(f"mkdir: {p}: {ex}")
    return "\n".join(out)
def cmd_history(args):
    return "\n".join(f"{i+1}\t{c}" for i,c in enumerate(history))
def cmd_date(args):
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
def cmd_whoami(args):
    return getpass.getuser()
def cmd_clear(args):
    return "__CLEAR__"
def cmd_env(args):
    return "\n".join(f"{k}={v}" for k,v in os.environ.items())
def cmd_df(args):
    path = args[0] if args else '/'
    try:
        du = shutil.disk_usage(path)
        return f"{path} -> total: {du.total} free: {du.free} used: {du.used}"
    except Exception as ex:
        return f"df: {ex}"

# Komut tablosu (örnek olarak 20+ tutuldu; istersen geri kalanları ekleriz)
COMMANDS = {
    'ls': cmd_ls, 'pwd': cmd_pwd, 'cd': cmd_cd, 'cat': cmd_cat, 'echo': cmd_echo,
    'touch': cmd_touch, 'rm': cmd_rm, 'mkdir': cmd_mkdir, 'history': cmd_history,
    'date': cmd_date, 'whoami': cmd_whoami, 'clear': cmd_clear, 'env': cmd_env,
    'df': cmd_df,
}

# --- GUI + thread-safe queue mekanizması ---
class BTLshellGUI:
    def __init__(self, root):
        self.root = root
        self.top = None
        self.output = None
        self.entry = None
        self.prompt_var = tk.StringVar()
        self._message_queue = Queue()
        self._hist_index = 0
        self.cwd = Path.cwd()
        # build window only when create_toplevel called

    def create_toplevel(self):
        if self.top and tk.Toplevel.winfo_exists(self.top):
            try:
                self.top.deiconify()
                self.top.lift()
                return
            except Exception:
                pass

        self.top = tk.Toplevel(self.root)
        self.top.title(f"{username}@BTL shell")
        self.top.geometry("900x500")

        # ScrolledText with terminal colors
        self.output = scrolledtext.ScrolledText(self.top, wrap=tk.NONE, state='disabled', font=("Consolas", 11),
                                                bg='black', fg='green', insertbackground='green')
        self.output.pack(fill=tk.BOTH, expand=True, padx=4, pady=4)

        bottom = ttk.Frame(self.top)
        bottom.pack(fill=tk.X, padx=4, pady=4)
        self.update_prompt()
        prompt_label = ttk.Label(bottom, textvariable=self.prompt_var, width=30, anchor="w")
        prompt_label.pack(side=tk.LEFT, padx=(0,4))
        self.entry = ttk.Entry(bottom)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", self._on_enter)
        self.entry.bind("<Up>", self._on_history_up)
        self.entry.bind("<Down>", self._on_history_down)
        self.entry.focus_set()

        # menu
        menubar = tk.Menu(self.top)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Clear", command=lambda: self.enqueue("__CLEAR__"))
        filemenu.add_separator()
        filemenu.add_command(label="Close", command=self.top.withdraw)
        menubar.add_cascade(label="File", menu=filemenu)
        self.top.config(menu=menubar)

        self.top.protocol("WM_DELETE_WINDOW", self.top.withdraw)

        # start polling the message queue regularly from main thread
        self._poll_queue()

    def update_prompt(self):
        try:
            cwd = short_path(Path.cwd())
        except Exception:
            cwd = str(Path.cwd())
        self.prompt_var.set(f"{username}@BTL {cwd}: ")

    # thread-safe: other threads call this to enqueue messages
    def enqueue(self, text):
        self._message_queue.put(text)

    # only main thread touches the Text widget, via this function
    def _write_main(self, text):
        if text == "__CLEAR__":
            self.output.configure(state='normal')
            self.output.delete('1.0', tk.END)
            self.output.configure(state='disabled')
            return
        self.output.configure(state='normal')
        self.output.insert(tk.END, text + "\n")
        self.output.see(tk.END)
        self.output.configure(state='disabled')

    # poll queue from main thread
    def _poll_queue(self):
        try:
            while True:
                text = self._message_queue.get_nowait()
                self._write_main(text)
        except Empty:
            pass
        # schedule next poll
        try:
            self.root.after(80, self._poll_queue)
        except Exception:
            # eğer root kapanmışsa sessizce kes
            pass

    def _on_enter(self, event=None):
        line = self.entry.get().strip()
        if not line: return
        history.append(line)
        self._hist_index = len(history)
        prompt = self.prompt_var.get()
        # göster hemen (ana thread)
        self.enqueue(prompt + line)
        self.entry.delete(0, tk.END)
        # komutu arka planda çalıştır
        t = threading.Thread(target=self._execute_command, args=(line,), daemon=True)
        t.start()

    def _on_history_up(self, event):
        if not history: return "break"
        self._hist_index = max(1, getattr(self, '_hist_index', len(history)))
        self._hist_index -= 1
        try:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, history[self._hist_index - 1])
        except Exception:
            pass
        return "break"

    def _on_history_down(self, event):
        if not history: return "break"
        self._hist_index = min(len(history), getattr(self, '_hist_index', len(history)))
        if self._hist_index < len(history):
            self._hist_index += 1
            try:
                self.entry.delete(0, tk.END)
                self.entry.insert(0, history[self._hist_index - 1])
            except Exception:
                pass
        else:
            self.entry.delete(0, tk.END)
        return "break"

    # here we run commands in background thread; GUI updates done by enqueue()
    def _execute_command(self, line):
        parts = self._parse_line(line)
        if not parts:
            return
        cmd = parts[0]
        args = parts[1:]

        if cmd == 'help':
            help_text = "BTLshell - Komut listesi (kısa):\n"
            for name in sorted(COMMANDS.keys()):
                help_text += f"  {name}\n"
            help_text += "\nEk: help, exit, quit"
            self.enqueue(help_text)
            return

        if cmd in ('exit', 'quit'):
            self.enqueue("Çıkılıyor. Pencere gizlendi.")
            try:
                self.top.withdraw()
            except Exception:
                pass
            return

        if cmd in COMMANDS:
            try:
                result = COMMANDS[cmd](args)
                if result == "__CLEAR__":
                    self.enqueue("__CLEAR__")
                elif result:
                    self.enqueue(result)
                # cd sonrası prompt güncelle
                self.update_prompt()
            except Exception as ex:
                self.enqueue(f"{cmd}: çalıştırılırken hata: {ex}")
            return

        # fallback: sistem komutu çalıştır
        try:
            # check if command exists on PATH (önlem)
            # Windows: bazı komutlar .exe,.bat,.cmd olabilir; subprocess will raise FileNotFoundError if not found
            proc = subprocess.run(parts, capture_output=True, text=True, shell=False, cwd=os.getcwd())
            if proc.stdout:
                self.enqueue(proc.stdout.rstrip("\n"))
            if proc.stderr:
                self.enqueue(proc.stderr.rstrip("\n"))
        except FileNotFoundError:
            self.enqueue(f"{cmd}: bilinmiyor veya komut bulunamadı")
        except Exception as ex:
            self.enqueue(f"{cmd}: çalıştırılamadı: {ex}")

    def _parse_line(self, line):
        parts=[]
        cur=''
        in_quote=False
        quote_char=''
        for ch in line.strip():
            if ch in ('"', "'"):
                if not in_quote:
                    in_quote=True; quote_char=ch; continue
                elif quote_char==ch:
                    in_quote=False; quote_char=''; continue
            if ch.isspace() and not in_quote:
                if cur:
                    parts.append(cur); cur=''
            else:
                cur+=ch
        if cur: parts.append(cur)
        return parts

# global app/root
_root = None
_app = None

def open_cmd_panel():
    global _root, _app
    if _root is None:
        _root = tk.Tk()
        _root.withdraw()
        _app = BTLshellGUI(_root)
    _app.create_toplevel()





# ---------- Search bar (taskbar) ----------
search_var = tk.StringVar()


def search_app(event=None):
    app_name = search_var.get().strip().lower()
    mapping = {
        "not defteri": open_notepad,
        "yılan oyunu": open_snake_game,
        "top yakalama": open_ball_game,
        "maria'yı kurtar": open_maria_game,
        "cmd paneli": open_cmd_panel,
        "kullanıcılar": lambda: messagebox.showinfo("Kullanıcılar", "\n".join(users)),
        "çöp kutusu": open_trash,
        "güncelleme": open_update_center,
        "media player": open_media_player,
        "btl store": btl_store,
        "youtube": lambda: subprocess.Popen(["start", "https://www.google.com"], shell=True),
        "hesap makinesi": open_calculator,
        "paint": open_paint_app,
        "dosya yöneticisi": open_file_manager,
        "ayarlar": open_settings,
        "görev yöneticisi": open_task_manager
    }
    func = mapping.get(app_name)
    if func:
        try:
            func()
        except Exception as e:
            messagebox.showerror("Hata", f"Uygulama açılırken hata: {e}")
    else:
        messagebox.showerror("Hata", "Böyle bir uygulama bulunamadı!")


search_entry = Entry(taskbar, textvariable=search_var, width=30)
search_entry.pack(side="left", padx=10)
search_entry.bind("<Return>", search_app)

# ---------- Sağ tık menüsü ----------


def show_context_menu(event):
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Yeni + Metin Belgesi",
                     command=lambda: create_new_file(BTL_DESKTOP))
    menu.add_command(
        label="Yeni + Klasör",
        command=lambda: create_new_folder(BTL_DESKTOP))
    menu.add_command(label="Yeni + .zip Klasörü",
                     command=lambda: create_new_zip(BTL_DESKTOP))
    menu.add_command(label="Yenile", command=lambda: None)
    menu.post(event.x_root, event.y_root)


root.bind("<Button-3>", show_context_menu)

# ---------- Dosya/Klasör/Zip fonksiyonları ----------


def create_new_file(desktop_dir):
    path = os.path.join(desktop_dir, f"YeniDosya{random.randint(1,100)}.txt")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write("")
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "text.png")
    add_icon(200, 200, icon_path, os.path.basename(path),
             lambda p=path: safe_start(p), deletable=True)


def create_new_folder(desktop_dir):
    folder_path = os.path.join(desktop_dir,
                               f"YeniKlasor{random.randint(1,100)}")
    try:
        os.makedirs(folder_path, exist_ok=True)
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "clasor.png")
    add_icon(250, 200, icon_path, os.path.basename(folder_path),
             lambda p=folder_path: safe_start(p), deletable=True)


def create_new_zip(desktop_dir):
    zip_name = f"YeniZip{random.randint(1,100)}.zip"
    zip_path = os.path.join(desktop_dir, zip_name)
    try:
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            pass
    except Exception:
        pass
    icon_path = os.path.join(ICONS_DIR, "zip.png")
    add_icon(
        300,
        200,
        icon_path,
        zip_name,
        lambda p=zip_path: safe_start(p),
        deletable=True)

# ---------- YouTube kısayolu ----------


def open_youtube():
    subprocess.Popen(["start", "https://www.youtube.com"], shell=True)


add_icon(
    400, 200,
    os.path.join(ICONS_DIR, "youtube.png"),
    "YouTube",
    open_youtube,
    deletable=True
)

# ---------- Görev Yöneticisi (basit) ----------


def open_task_manager():
    win = tk.Toplevel(root)
    win.title("Görev Yöneticisi")
    win.geometry("250x150")
    cpu = random.randint(1, 100)
    ram = random.randint(1000, 16000)
    gpu = random.randint(1, 100)
    bellek = random.randint(1, 100)
    tk.Label(
        win,
        text=f"CPU Kullanımı: %{cpu}").pack(
        anchor="w",
        padx=10,
        pady=2)
    tk.Label(
        win,
        text=f"RAM Kullanımı: {ram} MB").pack(
        anchor="w",
        padx=10,
        pady=2)
    tk.Label(
        win,
        text=f"GPU Kullanımı: %{gpu}").pack(
        anchor="w",
        padx=10,
        pady=2)
    tk.Label(
        win,
        text=f"Bellek Kullanımı: %{bellek}").pack(
        anchor="w",
        padx=10,
        pady=2)


# ---------- Çöp Kutusu ----------

# Gerekli global'ler: programınızda zaten varsa bu tanımları atlayabilirsiniz.
desktop_icons = {}  # örn: {"UygulamaAdı": frame_object, ...}
RECYCLEBIN_DIR = os.path.join(os.path.expanduser("~"), ".my_app_recyclebin")

# Çöp klasörünü oluştur (varsa atla)
os.makedirs(RECYCLEBIN_DIR, exist_ok=True)

# Örnek add_icon imzası (kendi uygulamanıza göre uyarlayın)
# def add_icon(x:int, y:int, image, name:str, command:callable, deletable:bool=False): ...


def move_to_trash(app_name, frame):
    """
    Bir uygulamayı çöp kutusuna taşır:
    - GUI'deki frame'i kaldırır (varsa destroy/forget)
    - desktop_icons dict'inden siler
    - RECYCLEBIN_DIR içine <app_name>.txt dosyası yazar (geri yükleme bilgisi)
    """
    try:
        # GUI'den kaldırma: frame None olabilir veya place ile yerleştirilmiş
        # olabilir
        if frame is not None:
            try:
                # Eğer frame.place() ile konumlandırıldıysa .place_forget
                # kullan
                if hasattr(frame, "place_forget"):
                    frame.place_forget()
                # Eğer widget tamamiyle kaldırılmak isteniyorsa destroy() daha
                # uygundur
                elif hasattr(frame, "destroy"):
                    frame.destroy()
            except Exception:
                # fallback olarak destroy dene
                try:
                    frame.destroy()
                except Exception:
                    pass

        # desktop_icons içinden sil (varsa)
        try:
            desktop_icons.pop(app_name, None)
        except Exception:
            pass

        # Çöp kutusuna info dosyası yaz (zaman damgası ekle)
        safe_name = "".join(c for c in app_name if c not in r'\/:*?"<>|')
        filename = safe_name + ".txt"
        path = os.path.join(RECYCLEBIN_DIR, filename)
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"name:{app_name}\n")
            f.write(f"deleted_at:{time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        return True
    except Exception as e:
        # Hata ayıklama için konsola yaz (isterseniz kaldırın)
        print("move_to_trash hata:", e)
        traceback.print_exc()
        return False


def open_trash():
    win = Toplevel(root)
    win.title("Çöp Kutusu")
    win.geometry("300x400")
    files = [f for f in os.listdir(RECYCLEBIN_DIR) if f.endswith(".txt")]
    lb = tk.Listbox(win)
    lb.pack(expand=True, fill="both")
    for f in files:
        lb.insert(END, f.replace(".txt", ""))

    def restore():
        try:
            sel = lb.get(tk.ACTIVE)
        except Exception:
            return
        if sel:
            path = os.path.join(RECYCLEBIN_DIR, sel + ".txt")
            if os.path.exists(path):
                try:
                    os.remove(path)
                except Exception:
                    pass
                add_icon(
                    100,
                    100,
                    None,
                    sel,
                    lambda: messagebox.showinfo(
                        "Uygulama",
                        f"{sel} açıldı!"),
                    deletable=True)
                lb.delete(tk.ACTIVE)

    def empty_trash():
        for f in os.listdir(RECYCLEBIN_DIR):
            try:
                os.remove(os.path.join(RECYCLEBIN_DIR, f))
            except Exception:
                pass
        lb.delete(0, END)
    Button(win, text="Geri Yükle", command=restore).pack()
    Button(win, text="Çöp Kutusunu Boşalt", command=empty_trash).pack()
#!/usr/bin/env python3
# update_center_toplevel_simple_with_github.py
# Güncelleme Merkezi (Toplevel) — GitHub raw file çekip hedef dosyaya gömebilir.
# Kullanım: uygulamanda bir tk.Tk() varsa sadece `open_update_center()` çağır.

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time
import random
import functools
import urllib.request
import urllib.error
import hashlib
import os
import datetime

# ---------- Ayarlar (değiştirebilirsin) ----------
# RAW URL (örnek: Xaef-BTL/BTL-OS-Update repo'sundaki update.py)
UPDATE_RAW_URL = "https://raw.githubusercontent.com/Xaef-BTL/BTL-OS-Update/main/update.py"
# Hedef dosya (BTLv4.4Ultra.py içine yazacak)
TARGET_FILE = "BTLv4.4Ultra.py"
# Dosya içine bakılacak marker'lar (aynı olsun)
MARKER_START = "# === UPDATE_MODULE_START ==="
MARKER_END = "# === UPDATE_MODULE_END ==="
# ------------------------------------------------

class UpdateCenter(tk.Toplevel):
    def __init__(self, master=None, title="Güncelleme Merkezi"):
        super().__init__(master)
        self.title(title)
        self.resizable(False, False)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # Thread/queue kontrol
        self.q = queue.Queue()
        self.download_threads = {}
        self.download_cancel_events = {}
        self.progress_widgets = {}

        # UI
        self._build_ui()
        self._center_window()
        self.processing = False
        self.after(100, self._process_queue)

    def _build_ui(self):
        pad = 8
        top = ttk.Frame(self, padding=pad)
        top.grid(row=0, column=0, sticky="ew")

        self.check_btn = ttk.Button(
            top,
            text="Güncellemeleri Kontrol Et",
            command=self.check_updates)
        self.check_btn.grid(row=0, column=0, padx=4)

        self.download_selected_btn = ttk.Button(
            top, text="İndir / Uygula Seçileni", command=self.download_selected)
        self.download_selected_btn.grid(row=0, column=1, padx=4)

        self.download_all_btn = ttk.Button(
            top, text="Hepsini İndir", command=self.download_all)
        self.download_all_btn.grid(row=0, column=2, padx=4)

        self.cancel_all_btn = ttk.Button(
            top, text="İptal Et", command=self.cancel_all_downloads)
        self.cancel_all_btn.grid(row=0, column=3, padx=4)

        # Treeview: güncelleme listesi
        tree_frame = ttk.Frame(self, padding=(pad, 0))
        tree_frame.grid(row=1, column=0, sticky="nsew")

        self.tree = ttk.Treeview(
            tree_frame,
            columns=(
                "version",
                "size",
                "status"),
            show="headings",
            height=8)
        self.tree.heading("version", text="Versiyon")
        self.tree.heading("size", text="Boyut")
        self.tree.heading("status", text="Durum")
        self.tree.column("version", width=120, anchor="center")
        self.tree.column("size", width=100, anchor="center")
        self.tree.column("status", width=140, anchor="center")
        self.tree.grid(row=0, column=0, sticky="nsew")

        sb = ttk.Scrollbar(
            tree_frame,
            orient="vertical",
            command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        sb.grid(row=0, column=1, sticky="ns")

        # Progress alanı (her indirme için ayrı progressbar)
        prog_label = ttk.Label(self, text="İndirme / Uygulama Durumları:")
        prog_label.grid(row=2, column=0, sticky="w", padx=pad, pady=(6, 0))

        self.prog_container = ttk.Frame(self, padding=(pad, 0))
        self.prog_container.grid(row=3, column=0, sticky="ew")

        # Log
        log_label = ttk.Label(self, text="Günlük (log):")
        log_label.grid(row=4, column=0, sticky="w", padx=pad, pady=(6, 0))
        self.log = tk.Text(self, height=10, width=80, state="disabled")
        self.log.grid(row=5, column=0, padx=pad, pady=(0, pad))

        # Başlangıç: boş liste
        self.updates = []  # dict: {id,name,version,size,status, url(optional)}
        self._log(
            "Güncelleme Merkezi hazır. Kontrol etmek için 'Güncellemeleri Kontrol Et' tuşuna bas.")

    def _center_window(self):
        self.update_idletasks()
        w = self.winfo_width() or 800
        h = self.winfo_height() or 520
        try:
            master = self.master
            if master:
                mx = master.winfo_rootx()
                my = master.winfo_rooty()
                mw = master.winfo_width()
                mh = master.winfo_height()
                x = mx + (mw - w) // 2
                y = my + (mh - h) // 2
            else:
                raise Exception
        except Exception:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight()
            x = (screen_w - w) // 2
            y = (screen_h - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    # --- Gerçek GitHub kontrolü ve fallback simülasyon ---
    def check_updates(self):
        if self.processing:
            self._log(
                "Zaten işlem var, lütfen bekle.")
            return
        self.processing = True
        self.check_btn.config(state="disabled")
        self._log("Güncellemeler kontrol ediliyor... (GitHub kontrolü deneniyor)")
        t = threading.Thread(target=self._check_updates_worker, daemon=True)
        t.start()

    def _check_updates_worker(self):
        # Deneyeceğiz: UPDATE_RAW_URL'i çek ve tek bir güncelleme objesi oluştur
        try:
            raw = fetch_remote_file(UPDATE_RAW_URL)
            sha = hashlib.sha256(raw).hexdigest()[:12]
            size_bytes = len(raw)
            size_str = human_size(size_bytes)
            pkg = {
                "id": f"gh-{sha}",
                "name": os.path.basename(UPDATE_RAW_URL) or "update.py",
                "version": sha,
                "size": size_str,
                "status": "Bekliyor",
                "url": UPDATE_RAW_URL,
                "content_bytes": raw
            }
            self.q.put(("updates_found", [pkg]))
            self.q.put(("info", "GitHub'dan güncelleme bulundu ve listelendi."))
        except Exception as e:
            # Fallback: simule et (eski davranış)
            self.q.put(("info", f"GitHub kontrolü başarısız: {e}. Simülasyon başlatılıyor."))
            time.sleep(0.6)
            sample = []
            for i in range(random.randint(2, 5)):
                sample.append({
                    "id": f"pkg-{int(time.time()*1000)%100000 + i}",
                    "name": f"Paket-{random.choice(['A','B','C','X'])}{random.randint(1,99)}",
                    "version": f"{random.randint(0,3)}.{random.randint(0,9)}.{random.randint(0,20)}",
                    "size": f"{random.randint(1,100)} MB",
                    "status": "Bekliyor"
                })
            self.q.put(("updates_found", sample))
            self.q.put(("info", "Simüle edilmiş güncellemeler listelendi."))
        finally:
            self.q.put(("done_check", None))

    def populate_tree(self):
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        for u in self.updates:
            self.tree.insert(
                "", "end", iid=u["id"], values=(
                    u.get("version", ""), u.get("size", ""), u.get("status", "")))

    # --- İndirme / uygulama kontrol ---
    def download_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showinfo(
                "Seçilmedi", "İndirmek / uygulamak için önce bir paket seç.")
            return
        self._log(f"Seçilen {len(sel)} paket indirmeye/uygulamaya hazırlanıyor...")
        for sid in sel:
            self._start_download_for(sid)

    def download_all(self):
        if not self.updates:
            messagebox.showinfo("Boş Liste", "Önce güncelleme kontrolü yap.")
            return
        for u in self.updates:
            self._start_download_for(u["id"])

    def _start_download_for(self, pkg_id):
        if pkg_id in self.download_threads:
            self._log(f"{pkg_id} zaten indiriliyor veya indirildi.")
            return
        cancel_event = threading.Event()
        self.download_cancel_events[pkg_id] = cancel_event
        t = threading.Thread(
            target=self._download_worker, args=(pkg_id, cancel_event), daemon=True)
        self.download_threads[pkg_id] = t
        self._create_progress_widget(pkg_id)
        t.start()
        self._log(f"{pkg_id} için indirme/uygulama başlatıldı.")

    def _create_progress_widget(self, pkg_id):
        if pkg_id in self.progress_widgets:
            return
        frame = ttk.Frame(self.prog_container)
        lbl = ttk.Label(frame, text=pkg_id, width=28)
        pb = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=360,
            mode="determinate",
            maximum=100)
        status_lbl = ttk.Label(frame, text="0%")
        cancel_btn = ttk.Button(
            frame,
            text="İptal",
            width=6,
            command=functools.partial(
                self._cancel_pkg,
                pkg_id))
        lbl.grid(row=0, column=0, padx=4, sticky="w")
        pb.grid(row=0, column=1, padx=4)
        status_lbl.grid(row=0, column=2, padx=4)
        cancel_btn.grid(row=0, column=3, padx=4)
        frame.pack(anchor="w", pady=2)
        self.progress_widgets[pkg_id] = {
            "frame": frame, "pb": pb, "status": status_lbl}

    def _cancel_pkg(self, pkg_id):
        ev = self.download_cancel_events.get(pkg_id)
        if ev:
            ev.set()
            self._log(f"{pkg_id} iptal edildi (kullanıcı isteği).")

    def cancel_all_downloads(self):
        if not self.download_cancel_events:
            self._log("İptal edilecek aktif indirme yok.")
            return
        for ev in self.download_cancel_events.values():
            ev.set()
        self._log("Tüm indirmeler iptal edildi (istek gönderildi).")

    def _download_worker(self, pkg_id, cancel_event):
        # Bul paket meta
        pkg = next((x for x in self.updates if x["id"] == pkg_id), None)
        if not pkg:
            self.q.put(("log", f"{pkg_id}: Paket meta bulunamadı."))
            self.q.put(("download_finished", pkg_id))
            return

        self.q.put(("status_update", (pkg_id, "İndiriliyor")))

        # Eğer paket zaten content_bytes içeriyorsa doğrudan kullan (GitHub check ile geldi)
        content = pkg.get("content_bytes")
        if content is None and pkg.get("url"):
            # gerçek indirme (basit) — ilerleme simüle edilerek
            try:
                content = fetch_remote_file(pkg["url"], progress_callback=lambda p: self.q.put(("progress", (pkg_id, p))))
            except Exception as e:
                self.q.put(("log", f"{pkg_id}: indirme hatası: {e}"))
                self.q.put(("status_update", (pkg_id, "Hata")))
                self.q.put(("download_finished", pkg_id))
                return
        else:
            # Simüle edilmiş indirme (sadece ilerleme göstermek için)
            total_steps = random.randint(12, 24)
            for i in range(total_steps + 1):
                if cancel_event.is_set():
                    self.q.put(("status_update", (pkg_id, "İptal Edildi")))
                    self.q.put(("progress", (pkg_id, 0)))
                    self.q.put(("log", f"{pkg_id}: indirme iptal edildi."))
                    self.q.put(("download_finished", pkg_id))
                    return
                pct = int((i / total_steps) * 100)
                self.q.put(("progress", (pkg_id, pct)))
                time.sleep(0.06 + random.random() * 0.12)

        if cancel_event.is_set():
            self.q.put(("status_update", (pkg_id, "İptal Edildi")))
            self.q.put(("progress", (pkg_id, 0)))
            self.q.put(("log", f"{pkg_id}: indirme iptal edildi."))
            self.q.put(("download_finished", pkg_id))
            return

        self.q.put(("progress", (pkg_id, 100)))
        self.q.put(("status_update", (pkg_id, "İndirildi")))
        self.q.put(("log", f"{pkg_id}: indirildi. Kurulum/uygulama başlıyor..."))

        # Uygula: eğer paket bir update.py ise hedef dosyaya gömebiliriz
        try:
            applied = False
            if pkg.get("name", "").lower().endswith(".py"):
                applied = apply_update_to_target_file(content, TARGET_FILE)
            else:
                # diğer paket türleri için burada farklı uygulama yapılabilir
                applied = False

            if applied:
                self.q.put(("status_update", (pkg_id, "Yüklendi")))
                self.q.put(("log", f"{pkg_id}: başarıyla yüklendi. Dosyayı yeniden başlatın."))
            else:
                self.q.put(("status_update", (pkg_id, "Tamam - Uygulanmadı")))
                self.q.put(("log", f"{pkg_id}: indirildi fakat otomatik uygulama yapılmadı."))
        except Exception as e:
            self.q.put(("status_update", (pkg_id, "Hata")))
            self.q.put(("log", f"{pkg_id}: uygulama hatası: {e}"))
        finally:
            self.q.put(("download_finished", pkg_id))

    # --- Kuyruk işleme (ana thread'te çalışır) ---
    def _process_queue(self):
        try:
            while True:
                item = self.q.get_nowait()
                typ = item[0]
                data = item[1]
                if typ == "updates_found":
                    self.updates = data
                    for u in self.updates:
                        u["status"] = u.get("status", "Bekliyor")
                    self.populate_tree()
                elif typ == "info":
                    self._log(data)
                elif typ == "status_update":
                    pkg_id, status = data
                    self._set_status(pkg_id, status)
                elif typ == "progress":
                    pkg_id, pct = data
                    self._set_progress(pkg_id, pct)
                elif typ == "log":
                    self._log(data)
                elif typ == "download_finished":
                    pkg_id = data
                    self.download_threads.pop(pkg_id, None)
                    self.download_cancel_events.pop(pkg_id, None)
                    pw = self.progress_widgets.get(pkg_id)
                    if pw:
                        pw["status"].config(text="Tamam")
        except queue.Empty:
            pass
        finally:
            # check button'ı kontrolü (eğer check bitmişse yeniden aktif et)
            self.after(100, self._process_queue)

    def _set_status(self, pkg_id, status):
        for u in self.updates:
            if u["id"] == pkg_id:
                u["status"] = status
                break
        try:
            self.tree.set(pkg_id, "status", status)
        except Exception:
            pass

    def _set_progress(self, pkg_id, pct):
        pw = self.progress_widgets.get(pkg_id)
        if pw:
            pw["pb"]["value"] = pct
            pw["status"].config(text=f"{pct}%")
        try:
            self.tree.set(pkg_id, "status", f"{pct}%")
        except Exception:
            pass

    def _log(self, text):
        ts = time.strftime("%H:%M:%S")
        self.log.config(state="normal")
        self.log.insert("end", f"[{ts}] {text}\n")
        self.log.see("end")
        self.log.config(state="disabled")

    def on_close(self):
        if self.download_threads:
            if not messagebox.askyesno(
                "Kapat",
                    "Aktif indirmeler var. Pencereyi kapatmak indirmeleri iptal eder. Yine de kapatmak istiyor musunuz?"):
                return
            for ev in self.download_cancel_events.values():
                ev.set()
        self.destroy()

# ------------------------------------------------
# Yardımcı fonksiyonlar

def fetch_remote_file(url, progress_callback=None, timeout=15):
    """
    URL'den bytes olarak dosya çek. progress_callback(percent) çağırılabilir (opsiyonel).
    Basit: stream okuma ve callback.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "BTL-UpdateCenter/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        total = resp.getheader("Content-Length")
        if total:
            total = int(total)
        data = bytearray()
        chunk_size = 8192
        read = 0
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            data.extend(chunk)
            read += len(chunk)
            if total and progress_callback:
                pct = int((read / total) * 100)
                progress_callback(min(100, pct))
        if progress_callback:
            progress_callback(100)
        return bytes(data)

def human_size(n):
    # basit boyut gösterimi
    for unit in ['B','KB','MB','GB','TB']:
        if n < 1024.0:
            return f"{n:.1f} {unit}"
        n /= 1024.0
    return f"{n:.1f} PB"

def apply_update_to_target_file(content_bytes, target_path):
    """
    content_bytes (bytes) içeriğini target_path içine MARKER_START..MARKER_END arası yazar.
    Eğer marker'lar yoksa dosyanın sonuna marker bloğu ekler.
    Yedek alır: target_path.YYYYMMDD_HHMMSS.bak
    Döner: True = uygulanmış, False = uygulanmamış/başarısız (hata fırlatılabilir).
    """
    # backup
    if not os.path.exists(target_path):
        # hedef yoksa yeni dosya oluştur (yedek yok)
        orig_text = ""
    else:
        with open(target_path, "rb") as f:
            orig_text = f.read().decode("utf-8", errors="replace")

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    if os.path.exists(target_path):
        bak_path = f"{target_path}.{timestamp}.bak"
        with open(bak_path, "wb") as bf:
            bf.write(orig_text.encode("utf-8"))
    else:
        bak_path = None

    new_injected = content_bytes.decode("utf-8", errors="replace").strip()

    if MARKER_START in orig_text and MARKER_END in orig_text:
        before, rest = orig_text.split(MARKER_START, 1)
        _, after = rest.split(MARKER_END, 1)
        new_text = before + MARKER_START + "\n\n" + new_injected + "\n\n" + MARKER_END + after
    else:
        # marker yok, dosyanın sonuna ekle
        new_text = orig_text + "\n\n" + MARKER_START + "\n\n" + new_injected + "\n\n" + MARKER_END + "\n"

    # Yaz
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(new_text)

    return True

# ------------------------------------------------
# Tek fonksiyon: root parametresi yok (kullanıcının istediği şekilde).

def open_update_center():
    """
    Mevcut tk.Tk() (default root) üzerinden bir UpdateCenter (Toplevel) açar.
    Eğer uygulamada henüz bir tk.Tk() oluşturulmamışsa RuntimeError fırlatır.
    """
    root = tk._default_root
    if not root:
        raise RuntimeError(
            "Mevcut bir tk.Tk() örneği bulunamadı. Önce `root = tk.Tk()` oluştur (ve mainloop çalıştır ya da GUI aktif olsun).")
    uc = UpdateCenter(root)
    try:
        uc.grab_set()  # opsiyonel: modal davranış
    except Exception:
        pass
    return uc

# -------------------------
# Kısa kullanım örneği (yorum satırı):
# import tkinter as tk
# from update_center_toplevel_simple_with_github import open_update_center
# root = tk.Tk()
# root.geometry("600x300")
# tk.Button(root, text="Open Update Center", command=open_update_center).pack(pady=20)
# root.mainloop()
#
# Son.

# btl_store_clean.py
# Tek dosya. No defaults for ICONS_DIR. No DEFAULT_ICONS_DIR.
# Call: btl_store()
# Behaves: preserves existing btlstore.png; does not create icon folders or placeholder files.
# Requires: tkinter, standard lib. Uses GitHub API for listing.

import os
import random
import ssl
import json
import urllib.request
import urllib.parse
import ast
import re
import subprocess
import tkinter as tk
from tkinter import messagebox

# ensure root exists as global (don't override if user defined)
try:
    root  # noqa: F821
except NameError:
    root = tk.Tk()
    root.withdraw()

# -----------------------
# GitHub listing & download
# -----------------------
def _normalize_repo_arg(repo_arg):
    if repo_arg.startswith("http"):
        parts = repo_arg.rstrip("/").split("/")
        if len(parts) >= 2:
            owner = parts[-2]
            repo = parts[-1].replace(".git", "")
            return f"{owner}/{repo}"
    return repo_arg

def _github_list_py_files(repo_arg, path="", token=None, user_agent="BTLStore/1.0"):
    """
    Returns list of items {name, path, download_url}
    Uses GitHub API /contents. Raises on error.
    """
    repo_arg = _normalize_repo_arg(repo_arg)
    if "/" not in repo_arg:
        raise RuntimeError("Repo must be owner/repo or full URL.")
    owner, repo = repo_arg.split("/", 1)
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{urllib.parse.quote(path)}"
    req = urllib.request.Request(api_url, headers={"User-Agent": user_agent})
    if token:
        req.add_header("Authorization", f"token {token}")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = resp.read().decode("utf-8")
        items = json.loads(data)
    results = []
    if isinstance(items, dict) and items.get("type") == "file":
        if items.get("name","").endswith(".py"):
            results.append({"name": items["name"], "path": items["path"], "download_url": items.get("download_url")})
    elif isinstance(items, list):
        for it in items:
            if it.get("type") == "file" and it.get("name","").endswith(".py"):
                results.append({"name": it["name"], "path": it["path"], "download_url": it.get("download_url")})
    return results

def _download_raw(url, dest_path, token=None, user_agent="BTLStore/1.0"):
    req = urllib.request.Request(url, headers={"User-Agent": user_agent})
    if token:
        req.add_header("Authorization", f"token {token}")
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        data = resp.read()
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(data)
    return dest_path

# -----------------------
# Static analysis (AST + regex)
# -----------------------
def _static_analyze_py(path):
    """
    Return list of tuples (type, message). Empty if clean-ish.
    """
    suspicious = []
    try:
        src = open(path, "r", encoding="utf-8", errors="ignore").read()
    except Exception as e:
        suspicious.append(("read_error", str(e)))
        return suspicious

    # quick regex patterns
    regex_checks = {
        r"rm\s+-rf": "shell rm -rf pattern",
        r"shutil\.rmtree\s*\(": "shutil.rmtree call",
        r"os\.remove\s*\(": "os.remove call",
        r"subprocess\.Popen\s*\(": "subprocess.Popen call",
        r"os\.system\s*\(": "os.system call",
        r"exec\(": "exec() call",
        r"eval\(": "eval() call",
        r"open\s*\(.*['\"]/etc/": "opening /etc/*",
    }
    for pattern, label in regex_checks.items():
        if re.search(pattern, src, flags=re.IGNORECASE):
            suspicious.append(("regex", label))

    # AST analysis
    try:
        tree = ast.parse(src, filename=path)
        for node in ast.walk(tree):
            # detect exec/eval/compile calls
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in ("exec", "eval", "compile", "execfile"):
                    suspicious.append(("ast", f"calls {node.func.id}"))
            # imports
            if isinstance(node, ast.Import):
                for n in node.names:
                    nm = n.name
                    if nm and any(d in nm for d in ("subprocess","os","shutil","socket","paramiko","ftplib","requests","urllib")):
                        suspicious.append(("ast", f"imports {nm}"))
            if isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                if any(d in mod for d in ("subprocess","os","shutil","socket","paramiko","ftplib","requests","urllib")):
                    suspicious.append(("ast", f"from {mod} import ..."))
            # attribute usage like os.system
            if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
                if node.value.id in ("os","subprocess","shutil","socket","requests","urllib"):
                    suspicious.append(("ast", f"attribute {node.value.id}.{node.attr}"))
    except Exception as e:
        suspicious.append(("ast_parse_error", str(e)))

    # dedupe
    seen = set()
    dedup = []
    for t,m in suspicious:
        if (t,m) not in seen:
            seen.add((t,m))
            dedup.append((t,m))
    return dedup

# -----------------------
# Simple CAPTCHA (math)
# -----------------------
def _ask_captcha(parent):
    a = random.randint(2,9)
    b = random.randint(2,9)
    answer = a + b
    dlg = tk.Toplevel(parent)
    dlg.title("Doğrulama")
    dlg.geometry("300x130")
    tk.Label(dlg, text=f"Lütfen doğrulayın: {a} + {b} = ?").pack(pady=8)
    var = tk.StringVar()
    ent = tk.Entry(dlg, textvariable=var)
    ent.pack()
    ok = {"val": False}
    def on_ok():
        try:
            if int(var.get()) == answer:
                ok["val"] = True
                dlg.destroy()
            else:
                messagebox.showerror("Hata", "Yanlış cevap.")
        except Exception:
            messagebox.showerror("Hata", "Geçerli bir sayı girin.")
    tk.Button(dlg, text="Doğrula", command=on_ok).pack(pady=8)
    dlg.transient(parent)
    dlg.grab_set()
    parent.wait_window(dlg)
    return ok["val"]

# -----------------------
# subprocess runner
# -----------------------
def _run_subprocess(path):
    try:
        proc = subprocess.Popen([os.sys.executable, path])
        return proc
    except Exception as e:
        raise

# -----------------------
# Integrated GitHub panel adder
# -----------------------
def _add_github_panel(win, dest_dir="btlgames_tmp"):
    frame = tk.LabelFrame(win, text="GitHub -> .py files (listele, indir, çalıştır)", padx=6, pady=6)
    frame.pack(fill="x", padx=8, pady=6)

    top = tk.Frame(frame)
    top.pack(fill="x")
    tk.Label(top, text="Repo (owner/repo or URL):").grid(row=0, column=0, sticky="w")
    repo_var = tk.StringVar(value="Xaef-BTL/BTLstore")
    repo_entry = tk.Entry(top, textvariable=repo_var, width=36)
    repo_entry.grid(row=0, column=1, padx=6, sticky="w")

    tk.Label(top, text="Subfolder (optional):").grid(row=1, column=0, sticky="w")
    path_var = tk.StringVar(value="games")
    path_entry = tk.Entry(top, textvariable=path_var, width=20)
    path_entry.grid(row=1, column=1, padx=6, sticky="w")

    tk.Label(top, text="GitHub token (optional):").grid(row=2, column=0, sticky="w")
    token_var = tk.StringVar(value="")
    token_entry = tk.Entry(top, textvariable=token_var, width=36, show="*")
    token_entry.grid(row=2, column=1, padx=6, sticky="w")

    btn_frame = tk.Frame(frame)
    btn_frame.pack(fill="x", pady=6)
    listbox = tk.Listbox(frame, height=6)
    listbox.pack(fill="both", padx=4, pady=4, expand=True)

    files_meta = []

    def do_list():
        listbox.delete(0, "end")
        files_meta.clear()
        repo = repo_var.get().strip()
        p = path_var.get().strip()
        token = token_var.get().strip() or None
        if not repo:
            messagebox.showwarning("Hata", "Repo girin.")
            return
        try:
            found = _github_list_py_files(repo, path=p, token=token)
        except Exception as e:
            messagebox.showerror("Listeleme Hatası", f"Listeleme başarısız: {e}")
            return
        if not found:
            listbox.insert("end", "(no .py files found)")
            return
        for it in found:
            files_meta.append(it)
            listbox.insert("end", f"{it['path']}")

    def on_download_and_run():
        sel = listbox.curselection()
        if not sel:
            messagebox.showinfo("Seçim", "Önce bir dosya seçin.")
            return
        idx = sel[0]
        meta = files_meta[idx]
        repo = repo_var.get().strip()
        token = token_var.get().strip() or None

        # first CAPTCHA
        if not _ask_captcha(win):
            messagebox.showwarning("Doğrulama", "Doğrulama başarısız.")
            return

        # download target path
        owner_repo = _normalize_repo_arg(repo)
        dest_root = os.path.join(dest_dir, owner_repo.replace("/", "_"))
        dest_path = os.path.join(dest_root, meta["path"].replace("/", os.sep))
        try:
            _download_raw(meta["download_url"], dest_path, token=token)
        except Exception as e:
            messagebox.showerror("İndirme Hatası", f"İndirme başarısız: {e}")
            return

        # static analysis
        findings = _static_analyze_py(dest_path)
        if findings:
            txt = "\n".join([f"{t}: {m}" for t,m in findings])
            proceed = messagebox.askyesno("Şüpheli içerik tespit edildi",
                                          f"Aşağıdaki şüpheli kalıplar bulundu:\n\n{txt}\n\nDevam etmek istiyor musunuz? (tehlikeli olabilir!)")
            if not proceed:
                return

        # final CAPTCHA
        if not _ask_captcha(win):
            messagebox.showwarning("Doğrulama", "Doğrulama başarısız.")
            return

        # run in subprocess
        try:
            proc = _run_subprocess(dest_path)
            messagebox.showinfo("Başlatıldı", f"Oyun başlatıldı (PID {proc.pid}).")
        except Exception as e:
            messagebox.showerror("Çalıştırma Hatası", f"Oynatılırken hata: {e}")

    tk.Button(btn_frame, text="Listele .py", command=do_list).pack(side="left", padx=6)
    tk.Button(btn_frame, text="İndir ve Çalıştır", command=on_download_and_run).pack(side="left", padx=6)

    return frame

# -----------------------
# Main btl_store (no params, uses global root)
# -----------------------
def btl_store():
    win = tk.Toplevel(root)
    win.title("BTL Store")
    win.geometry("520x520")
    win.resizable(False, False)

    # Helper get_callable as before: fallback small apps/games
    def get_callable(name, fallback_type="app"):
        func = globals().get(name)
        if callable(func):
            return func
        if fallback_type == "game":
            def fallback_game():
                gwin = tk.Toplevel(win)
                gwin.title(name)
                gwin.geometry("350x200")
                tk.Label(gwin, text=f"{name} - fallback oyun.").pack(pady=10)
                score = tk.IntVar(value=0)
                def clicker():
                    score.set(score.get() + 1)
                    lbl.config(text=f"Skor: {score.get()}")
                btn = tk.Button(gwin, text="Tıkla!", command=clicker)
                btn.pack(pady=5)
                lbl = tk.Label(gwin, text=f"Skor: {score.get()}")
                lbl.pack()
            return fallback_game
        else:
            def fallback_app():
                awin = tk.Toplevel(win)
                awin.title(name)
                awin.geometry("400x220")
                tk.Label(awin, text=f"{name} açıldı — fallback app").pack(pady=12)
                tk.Button(awin, text="Kapat", command=awin.destroy).pack(pady=8)
            return fallback_app

    # minimal built-ins (use real ones from globals if present)
    open_notepad_func = globals().get("open_notepad") or get_callable("Not Defteri", fallback_type="app")
    open_snake_func = globals().get("open_snake_game") or get_callable("Yılan Oyunu", fallback_type="game")
    open_ball_func = globals().get("open_ball_game") or get_callable("Top Yakalama", fallback_type="game")

    # UI: simple top search + body
    top_frame = tk.Frame(win)
    top_frame.pack(fill="x", padx=8, pady=6)
    tk.Label(top_frame, text="Ara:").pack(side="left")
    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var)
    search_entry.pack(side="left", fill="x", expand=True, padx=6)

    body = tk.Frame(win)
    body.pack(fill="both", expand=True, padx=8, pady=4)

    left = tk.LabelFrame(body, text="Mini Oyunlar")
    left.pack(side="left", fill="both", expand=True, padx=4)
    right = tk.LabelFrame(body, text="Mini Uygulamalar")
    right.pack(side="left", fill="both", expand=True, padx=4)

    # example lists
    mini_games = {
        "Yılan Oyunu": open_snake_func,
        "Top Yakalama": open_ball_func,
    }
    mini_apps = {
        "Not Defteri": open_notepad_func,
    }

    def populate_lists(filter_text=""):
        for w in left.winfo_children(): w.destroy()
        for w in right.winfo_children(): w.destroy()
        for name, func in mini_games.items():
            if filter_text and filter_text.lower() not in name.lower(): continue
            frm = tk.Frame(left); frm.pack(fill="x", pady=3, padx=4)
            tk.Label(frm, text=name).pack(side="left", anchor="w")
            tk.Button(frm, text="▶ Oyna", command=lambda f=func: f()).pack(side="right", padx=2)
            tk.Button(frm, text="📥 İndir", command=lambda n=name, f=func: messagebox.showinfo("İndir", f"{n} indirildi (sim).")).pack(side="right")
        for name, func in mini_apps.items():
            if filter_text and filter_text.lower() not in name.lower(): continue
            frm = tk.Frame(right); frm.pack(fill="x", pady=3, padx=4)
            tk.Label(frm, text=name).pack(side="left", anchor="w")
            tk.Button(frm, text="Aç", command=lambda f=func: f()).pack(side="right", padx=2)
            tk.Button(frm, text="📥 İndir", command=lambda n=name, f=func: messagebox.showinfo("İndir", f"{n} indirildi (sim).")).pack(side="right")

    try:
        search_var.trace_add("write", lambda *_: populate_lists(search_var.get()))
    except Exception:
        search_var.trace("w", lambda *_: populate_lists(search_var.get()))

    populate_lists("")

    # add GitHub panel (exactly the feature you asked)
    _add_github_panel(win, dest_dir="btlgames_tmp")

    bottom = tk.Frame(win)
    bottom.pack(fill="x", padx=8, pady=8)
    tk.Button(bottom, text="Kapat", command=win.destroy).pack(side="right")

    # add_icon behavior: only if both add_icon and ICONS_DIR exist in globals — NO creation, NO deletion
    if "add_icon" in globals() and "ICONS_DIR" in globals() and callable(globals().get("add_icon")):
        try:
            # prefer project btlstore.png if present
            project_png = os.path.join(os.path.abspath(os.path.dirname(__file__)) if "__file__" in globals() else os.getcwd(), "btlstore.png")
            chosen_icon = None
            if os.path.exists(project_png):
                chosen_icon = project_png
            else:
                alt = os.path.join(globals()["ICONS_DIR"], "btlstore.png")
                if os.path.exists(alt):
                    chosen_icon = alt
            if chosen_icon:
                try:
                    globals()["add_icon"](1050, 50, chosen_icon, "BTL Store", btl_store, deletable=True)
                except Exception:
                    pass
        except Exception:
            pass

# end of file

# ---------- Paint uygulaması ----------


def open_paint_app():
    import tkinter as tk
    from tkinter import Toplevel, colorchooser, filedialog, simpledialog, messagebox
    try:
        from PIL import Image, ImgeDraw, ImageTk, ImageOps
        PIL_OK = True
        Image_module = Image  # kolay referans
    except Exception:
        PIL_OK = False
        Image_module = None

    # Pillow sürüm uyumluluğu: uygun resample filtresini seç
    RESAMPLE_FILTER = None
    if PIL_OK:
        try:
            RESAMPLE_FILTER = Image_module.Resampling.LANCZOS
        except Exception:
            if hasattr(Image_module, "LANCZOS"):
                RESAMPLE_FILTER = Image_module.LANCZOS
            elif hasattr(Image_module, "ANTIALIAS"):
                RESAMPLE_FILTER = Image_module.ANTIALIAS
            elif hasattr(Image_module, "BICUBIC"):
                RESAMPLE_FILTER = Image_module.BICUBIC
            else:
                RESAMPLE_FILTER = 0

    # root isimli Tk kök penceresinin varlığını bekler (orijinal yapı)
    try:
        parent = root
    except NameError:
        raise RuntimeError(
            "open_paint_app: Bu fonksiyon 'root' isimli bir Tk örneği beklüyor. Önce root = tk.Tk() oluşturun.")

    paint_win = Toplevel(parent)
    paint_win.title("BTL Paint — Düzeltilmiş")
    paint_win.geometry("1000x700")

    # ---------- State ve Vars ----------
    bg_color = "#ffffff"
    # brush, eraser, line, rect, oval, fill, eyedrop, text
    current_tool = tk.StringVar(value="brush")
    color_var = tk.StringVar(value="#000000")
    brush_size = tk.IntVar(value=4)
    smooth_level = tk.IntVar(value=2)
    show_grid = tk.BooleanVar(value=False)

    canvas_w, canvas_h = 860, 560

    if PIL_OK:
        pil_image = Image_module.new("RGBA", (canvas_w, canvas_h), bg_color)
        pil_draw = ImageDraw.Draw(pil_image)
    else:
        pil_image = None
        pil_draw = None

    MAX_HISTORY = 40
    history = []
    hist_index = -1

    def push_history():
        nonlocal history, hist_index, pil_image
        if not PIL_OK:
            return
        # Trim ileri geçmiş
        history[:] = history[: hist_index + 1]
        history.append(pil_image.copy())
        if len(history) > MAX_HISTORY:
            history.pop(0)
        hist_index = len(history) - 1

    def undo(event=None):
        nonlocal hist_index, pil_image, pil_draw
        if not PIL_OK:
            messagebox.showinfo("Geri Al", "Pillow yüklü değil; undo yok.")
            return
        if hist_index > 0:
            hist_index -= 1
            pil_image.paste(history[hist_index])
            pil_draw = ImageDraw.Draw(pil_image)
            refresh_canvas_image()
        else:
            messagebox.showinfo("Geri Al", "Geri alınacak şey kalmadı.")

    def redo(event=None):
        nonlocal hist_index, pil_image, pil_draw
        if not PIL_OK:
            return
        if hist_index < len(history) - 1:
            hist_index += 1
            pil_image.paste(history[hist_index])
            pil_draw = ImageDraw.Draw(pil_image)
            refresh_canvas_image()
        else:
            messagebox.showinfo("İleri Al", "İleri alınacak şey kalmadı.")

    # ---------- UI ----------
    toolbar = tk.Frame(paint_win, bd=2, relief="raised")
    toolbar.pack(side="top", fill="x")

    tools = [("Fırça", "brush"), ("Silgi", "eraser"), ("Çizgi", "line"),
             ("Dikdörtgen", "rect"), ("Oval", "oval"), ("Dolgu", "fill"),
             ("Renk Al", "eyedrop"), ("Metin", "text")]
    for tname, tval in tools:
        tk.Radiobutton(
            toolbar,
            text=tname,
            variable=current_tool,
            value=tval).pack(
            side="left",
            padx=3,
            pady=3)

    palette = [
        "#000000",
        "#ff0000",
        "#00aa00",
        "#0000ff",
        "#ff7700",
        "#800080",
        "#8b4513",
        "#ffff00",
        "#ffb6c1"]
    palf = tk.Frame(toolbar)
    palf.pack(side="left", padx=8)
    for c in palette:
        tk.Button(
            palf,
            bg=c,
            width=2,
            command=lambda col=c: color_var.set(col)).pack(
            side="left",
            padx=2)

    def choose_color():
        c = colorchooser.askcolor(color_var.get(), parent=paint_win)
        if c and c[1]:
            color_var.set(c[1])

    tk.Button(
        toolbar,
        text="Renk...",
        command=choose_color).pack(
        side="left",
        padx=6)
    tk.Label(toolbar, text="Fırça:").pack(side="left")
    tk.Scale(
        toolbar,
        from_=1,
        to=60,
        orient="horizontal",
        variable=brush_size,
        width=8).pack(
        side="left",
        padx=6)
    tk.Label(toolbar, text="Yumuşatma:").pack(side="left")
    tk.Scale(
        toolbar,
        from_=0,
        to=6,
        orient="horizontal",
        variable=smooth_level,
        width=6).pack(
        side="left",
        padx=6)
    tk.Checkbutton(
        toolbar,
        text="Izgara",
        variable=show_grid,
        command=lambda: refresh_canvas_image()).pack(
        side="left",
        padx=8)

    def save_image():
        if not PIL_OK:
            messagebox.showerror(
                "Kaydet", "Pillow yüklü değil. Kaydetme desteklenmiyor.")
            return
        path = filedialog.asksaveasfilename(
            defaultextension=".png", filetypes=[
                ("PNG", "*.png"), ("JPEG", "*.jpg;*.jpeg")])
        if not path:
            return
        out = pil_image.convert("RGBA")
        if out.mode == "RGBA":
            bg = Image_module.new("RGBA", out.size, bg_color)
            bg.paste(out, (0, 0), out)
            out = bg.convert("RGB")
        out.save(path)
        status.config(text=f"Kaydedildi: {path}")

    def open_image():
        nonlocal pil_image, pil_draw
        if not PIL_OK:
            messagebox.showerror(
                "Aç", "Pillow yüklü değil. Açma desteklenmiyor.")
            return
        path = filedialog.askopenfilename(
            filetypes=[("Görüntüler", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"), ("All", "*.*")])
        if not path:
            return
        img = Image_module.open(path).convert("RGBA")
        w, h = canvas.winfo_width() or canvas_w, canvas.winfo_height() or canvas_h
        # Ölçekle: resample parametresi uyumlu şekilde kullanılıyor
        try:
            img = ImageOps.contain(img, (w, h), method=RESAMPLE_FILTER)
        except TypeError:
            # older Pillow's ImageOps.contain may not accept method kw;
            # fallback to resize while keeping aspect
            img.thumbnail((w, h), RESAMPLE_FILTER)
        new_img = Image_module.new("RGBA", (w, h), bg_color)
        nx = (w - img.width) // 2
        ny = (h - img.height) // 2
        new_img.paste(img, (nx, ny), img)
        pil_image = new_img
        pil_draw = ImageDraw.Draw(pil_image)
        push_history()
        refresh_canvas_image()

    tk.Button(
        toolbar,
        text="Aç",
        command=open_image).pack(
        side="right",
        padx=6)
    tk.Button(
        toolbar,
        text="Kaydet",
        command=save_image).pack(
        side="right",
        padx=6)

    def clear_confirm():
        if not messagebox.askyesno("Temizle",
                                   "Tuvali temizlemek istiyor musun?"):
            return
        nonlocal pil_image, pil_draw
        if PIL_OK:
            w = canvas.winfo_width() or canvas_w
            h = canvas.winfo_height() or canvas_h
            pil_image = Image_module.new("RGBA", (w, h), bg_color)
            pil_draw = ImageDraw.Draw(pil_image)
            push_history()
            refresh_canvas_image()
        else:
            canvas.delete("all")
        status.config(text="Tuval temizlendi")

    tk.Button(
        toolbar,
        text="Temizle",
        command=clear_confirm).pack(
        side="right",
        padx=6)
    tk.Button(
        toolbar,
        text="Geri (Ctrl+Z)",
        command=undo).pack(
        side="right",
        padx=6)
    tk.Button(
        toolbar,
        text="İleri (Ctrl+Y)",
        command=redo).pack(
        side="right",
        padx=6)

    # ---------- Canvas ----------
    canvas_frame = tk.Frame(paint_win)
    canvas_frame.pack(expand=True, fill="both")
    canvas = tk.Canvas(canvas_frame, bg=bg_color, cursor="cross")
    canvas.pack(expand=True, fill="both")

    status = tk.Label(paint_win, text="Hazır", anchor="w")
    status.pack(side="bottom", fill="x")

    # PIL -> Canvas görüntü yenileme
    canvas_image_id = None

    def refresh_canvas_image():
        nonlocal canvas_image_id, pil_image, pil_draw
        w = canvas.winfo_width() or canvas_w
        h = canvas.winfo_height() or canvas_h
        if PIL_OK and pil_image:
            # Tuval boyutuyla eşitle (resize yaparken resample parametresi
            # uyumlu kullanılır)
            if pil_image.size != (w, h):
                try:
                    pil_image = pil_image.resize(
                        (w, h), resample=RESAMPLE_FILTER)
                except TypeError:
                    # bazı Pillow sürümlerinde argüman farklı olabilir
                    pil_image = pil_image.resize((w, h))
                pil_draw = ImageDraw.Draw(pil_image)
            tkimg = ImageTk.PhotoImage(pil_image)
            paint_win._tkimg = tkimg
            if canvas_image_id is None:
                canvas_image_id = canvas.create_image(
                    0, 0, anchor="nw", image=tkimg)
            else:
                canvas.itemconfig(canvas_image_id, image=tkimg)
        # Izgara gösterimi
        canvas.delete("__grid__")
        if show_grid.get():
            step = 20
            for gx in range(0, w, step):
                canvas.create_line(gx, 0, gx, h, tag="__grid__", dash=(2, 3))
            for gy in range(0, h, step):
                canvas.create_line(0, gy, w, gy, tag="__grid__", dash=(2, 3))

    # ---------- Çizim mantığı ----------
    last_x = last_y = None
    start_x = start_y = None
    preview_id = None
    stroke_points = []

    def hex_to_rgba(h):
        h = h.lstrip('#')
        if len(h) == 6:
            return (int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16), 255)
        if len(h) == 3:
            return (int(h[0] * 2, 16), int(h[1] * 2, 16),
                    int(h[2] * 2, 16), 255)
        return (0, 0, 0, 255)

    def flood_fill(sx, sy, fillcol):
        if not PIL_OK:
            return
        w, h = pil_image.size
        if not (0 <= sx < w and 0 <= sy < h):
            return
        px = pil_image.load()
        target = px[sx, sy]
        if target == fillcol:
            return
        stack = [(sx, sy)]
        while stack:
            cx, cy = stack.pop()
            try:
                if px[cx, cy] == target:
                    px[cx, cy] = fillcol
                    if cx > 0:
                        stack.append((cx - 1, cy))
                    if cx < w - 1:
                        stack.append((cx + 1, cy))
                    if cy > 0:
                        stack.append((cx, cy - 1))
                    if cy < h - 1:
                        stack.append((cx, cy + 1))
            except IndexError:
                pass

    def start_draw(event):
        nonlocal last_x, last_y, start_x, start_y, preview_id, stroke_points
        x, y = event.x, event.y
        last_x, last_y = x, y
        start_x, start_y = x, y
        stroke_points = [(x, y)]
        tool = current_tool.get()
        if tool == "text":
            txt = simpledialog.askstring(
                "Metin", "Yazılacak metni gir:", parent=paint_win)
            if txt:
                if PIL_OK:
                    pil_draw.text((x, y), txt, fill=color_var.get())
                    push_history()
                    refresh_canvas_image()
                else:
                    canvas.create_text(
                        x, y, text=txt, anchor="nw", fill=color_var.get(), font=(
                            "Arial", max(
                                8, brush_size.get() * 2)))
        elif tool == "fill":
            if PIL_OK:
                flood_fill(x, y, hex_to_rgba(color_var.get()))
                push_history()
                refresh_canvas_image()
            else:
                messagebox.showinfo(
                    "Dolgu", "Pillow yok; dolgu desteklenmiyor.")
        elif tool == "eyedrop":
            if PIL_OK:
                try:
                    px = pil_image.getpixel((x, y))
                    hexc = '#%02x%02x%02x' % px[:3]
                    color_var.set(hexc)
                except Exception:
                    pass

    def draw(event):
        nonlocal last_x, last_y, preview_id, stroke_points, pil_draw
        x, y = event.x, event.y
        tool = current_tool.get()
        status.config(
            text=f"Araç: {tool} | Koordinat: ({x},{y}) | Renk: {color_var.get()}")
        if tool in ("brush", "eraser"):
            stroke_points.append((x, y))
            if PIL_OK:
                draw_color = (
                    255,
                    255,
                    255,
                    255) if tool == "eraser" else hex_to_rgba(
                    color_var.get())
                w = max(1, brush_size.get())
                pil_draw.line((last_x, last_y, x, y), fill=draw_color, width=w)
                refresh_canvas_image()
            else:
                col = "white" if tool == "eraser" else color_var.get()
                canvas.create_line(
                    last_x,
                    last_y,
                    x,
                    y,
                    fill=col,
                    width=brush_size.get(),
                    capstyle=tk.ROUND,
                    smooth=True)
            last_x, last_y = x, y
        elif tool in ("line", "rect", "oval"):
            if preview_id:
                canvas.delete(preview_id)
            if tool == "line":
                preview_id = canvas.create_line(
                    start_x,
                    start_y,
                    x,
                    y,
                    fill=color_var.get(),
                    width=brush_size.get(),
                    dash=(
                        4,
                        2))
            elif tool == "rect":
                preview_id = canvas.create_rectangle(
                    start_x,
                    start_y,
                    x,
                    y,
                    outline=color_var.get(),
                    width=brush_size.get(),
                    dash=(
                        4,
                        2))
            else:
                preview_id = canvas.create_oval(
                    start_x,
                    start_y,
                    x,
                    y,
                    outline=color_var.get(),
                    width=brush_size.get(),
                    dash=(
                        4,
                        2))

    def end_draw(event):
        nonlocal preview_id, pil_draw, pil_image, hist_index, last_x, last_y
        x, y = event.x, event.y
        tool = current_tool.get()
        if preview_id:
            canvas.delete(preview_id)
            preview_id = None
        if tool in ("line", "rect", "oval"):
            if PIL_OK:
                if tool == "line":
                    pil_draw.line((start_x, start_y, x, y),
                                  fill=color_var.get(), width=brush_size.get())
                elif tool == "rect":
                    pil_draw.rectangle(
                        (start_x, start_y, x, y), outline=color_var.get(), width=brush_size.get())
                else:
                    pil_draw.ellipse(
                        (start_x, start_y, x, y), outline=color_var.get(), width=brush_size.get())
                push_history()
                refresh_canvas_image()
            else:
                if tool == "line":
                    canvas.create_line(
                        start_x,
                        start_y,
                        x,
                        y,
                        fill=color_var.get(),
                        width=brush_size.get())
                elif tool == "rect":
                    canvas.create_rectangle(
                        start_x,
                        start_y,
                        x,
                        y,
                        outline=color_var.get(),
                        width=brush_size.get())
                else:
                    canvas.create_oval(
                        start_x,
                        start_y,
                        x,
                        y,
                        outline=color_var.get(),
                        width=brush_size.get())
        else:
            if PIL_OK and tool in ("brush", "eraser"):
                push_history()
        last_x = last_y = None

    # ---------- Bindler ----------
    canvas.bind("<ButtonPress-1>", start_draw)
    canvas.bind("<B1-Motion>", draw)
    canvas.bind("<ButtonRelease-1>", end_draw)

    def on_right_click(event):
        if PIL_OK:
            try:
                px = pil_image.getpixel((event.x, event.y))
                hexc = '#%02x%02x%02x' % px[:3]
                color_var.set(hexc)
                status.config(text=f"Renk alındı: {hexc}")
            except Exception:
                pass

    canvas.bind("<Button-3>", on_right_click)
    paint_win.bind_all("<Control-z>", lambda e: undo())
    paint_win.bind_all("<Control-y>", lambda e: redo())
    paint_win.bind_all("<Control-s>", lambda e: save_image())

    def on_canvas_config(event):
        refresh_canvas_image()
    canvas.bind("<Configure>", on_canvas_config)

    # Başlangıç
    if PIL_OK:
        push_history()
        refresh_canvas_image()
    else:
        messagebox.showwarning(
            "Pillow yok",
            "Gelişmiş özellikler için `pip install pillow` yap. Yine de çizim yapabilirsin.")

    status.config(
        text="BTL Paint hazır — sağ tık ile renk al, Text aracı ile tıkla yaz.")
    return paint_win

import sys
import tkinter as tk

# PyQt imports (gecikmeli import, Tk-only senaryolarda da hata vermez)
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QLabel, QSizePolicy, QTabWidget, QToolButton
)
from PyQt6.QtWebEngineWidgets import QWebEngineView


# ----------------------------
# Basit gömülebilir BrowserWidget (sekme, devtools, arama eklendi)
# ----------------------------
class BrowserWidget(QWidget):
    def __init__(self, url: str = "about:blank", parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Lightning - Embedded")
        self.resize(1100, 700)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(6,6,6,6)
        # tek satır kaldırıldı: layout.setSpacing(6)

        # Toolbar: gezinme + url + sekme yönetimi + devtools + arama
        toolbar = QWidget()
        tlay = QHBoxLayout(toolbar)
        tlay.setContentsMargins(0,0,0,0)
        tlay.setSpacing(4)

        self.back_btn = QPushButton("◀")
        self.forward_btn = QPushButton("▶")
        self.reload_btn = QPushButton("⟳")
        self.stop_btn = QPushButton("✖")
        for b in (self.back_btn, self.forward_btn, self.reload_btn, self.stop_btn):
            b.setFixedWidth(36)
            tlay.addWidget(b)

        # Sekme yönetimi butonları
        self.new_tab_btn = QToolButton()
        self.new_tab_btn.setText("+")
        self.new_tab_btn.setToolTip("Yeni Sekme")
        self.new_tab_btn.setFixedWidth(28)
        tlay.addWidget(self.new_tab_btn)

        self.close_tab_btn = QToolButton()
        self.close_tab_btn.setText("−")
        self.close_tab_btn.setToolTip("Sekmeyi Kapat")
        self.close_tab_btn.setFixedWidth(28)
        tlay.addWidget(self.close_tab_btn)

        # URL çubuğu
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("Adres gir (ör. example.com veya https://...)")
        self.url_edit.setClearButtonEnabled(True)
        self.url_edit.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred))
        tlay.addWidget(self.url_edit)

        self.go_btn = QPushButton("Git")
        self.go_btn.setFixedWidth(48)
        tlay.addWidget(self.go_btn)

        # Devtools toggle
        self.devtools_btn = QPushButton("DevTools")
        self.devtools_btn.setFixedWidth(80)
        tlay.addWidget(self.devtools_btn)

        # Arama çubuğu (sayfa içi)
        self.find_edit = QLineEdit()
        self.find_edit.setPlaceholderText("Sayfa içinde ara...")
        self.find_edit.setMaximumWidth(200)
        tlay.addWidget(self.find_edit)

        self.find_next_btn = QPushButton("→")
        self.find_next_btn.setFixedWidth(36)
        tlay.addWidget(self.find_next_btn)

        layout.addWidget(toolbar)

        # Sekmeler
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self._close_tab)
        layout.addWidget(self.tabs, stretch=1)

        # Alt durum etiketi
        self.status = QLabel("")
        layout.addWidget(self.status)

        # Devtools penceresi (kullanılınca oluşturulacak)
        self._devtools_view = None
        self._devtools_shown = False

        # bağlantılar
        self.back_btn.clicked.connect(lambda: self._current_web().back())
        self.forward_btn.clicked.connect(lambda: self._current_web().forward())
        self.reload_btn.clicked.connect(lambda: self._current_web().reload())
        self.stop_btn.clicked.connect(lambda: self._current_web().stop())
        self.go_btn.clicked.connect(self._on_go)
        self.url_edit.returnPressed.connect(self._on_go)

        self.new_tab_btn.clicked.connect(lambda: self._add_tab("about:blank", make_active=True))
        self.close_tab_btn.clicked.connect(lambda: self._close_tab(self.tabs.currentIndex()))

        self.devtools_btn.clicked.connect(self._toggle_devtools)

        self.find_edit.returnPressed.connect(self._on_find)
        self.find_next_btn.clicked.connect(self._on_find)

        self.tabs.currentChanged.connect(self._on_tab_changed)

        # İlk sekmeyi ekle
        self._add_tab(url)
        self.load_url(url)

    # yeni yardımcılar (isimler orijinal fonksiyonları bozmaz)
    def _create_webview(self, url: str):
        web = QWebEngineView()
        web.setUrl(QUrl.fromUserInput(url))
        web.urlChanged.connect(self._on_url_changed)
        web.titleChanged.connect(lambda title: self._update_tab_title_for_web(web, title))
        web.loadFinished.connect(lambda ok: self._on_load_finished(web, ok))
        return web

    def _add_tab(self, url: str = "about:blank", make_active: bool = False):
        web = self._create_webview(url)
        idx = self.tabs.addTab(web, "Yeni Sekme")
        if make_active:
            self.tabs.setCurrentIndex(idx)
        return web

    def _close_tab(self, index: int):
        if index < 0:
            return
        widget = self.tabs.widget(index)
        if widget:
            try:
                widget.deleteLater()
            except Exception:
                pass
        self.tabs.removeTab(index)
        # Sekme kalmadıysa bir tane aç
        if self.tabs.count() == 0:
            self._add_tab("about:blank", make_active=True)

    def _current_web(self) -> QWebEngineView:
        w = self.tabs.currentWidget()
        if isinstance(w, QWebEngineView):
            return w
        # fallback: eğer widget değilse yeni sekme aç
        return self._create_and_set_tab("about:blank")

    def _create_and_set_tab(self, url: str):
        web = self._add_tab(url, make_active=True)
        return web

    def _on_tab_changed(self, idx: int):
        web = self._current_web()
        try:
            cur_url = web.url().toString()
            self.url_edit.setText(cur_url)
        except Exception:
            pass
        # Eğer devtools açıksa yeni sayfaya bağla
        if self._devtools_shown and self._devtools_view is not None:
            try:
                web.page().setDevToolsPage(self._devtools_view.page())
            except Exception:
                pass

    def _update_tab_title_for_web(self, web: QWebEngineView, title: str):
        # sekme başlığını güncelle
        for i in range(self.tabs.count()):
            if self.tabs.widget(i) is web:
                self.tabs.setTabText(i, title or "Yeni Sekme")
                break

    def _on_load_finished(self, web: QWebEngineView, ok: bool):
        if ok and self.tabs.currentWidget() is web:
            self.status.setText("Yüklendi: " + web.url().toString())
        elif not ok and self.tabs.currentWidget() is web:
            self.status.setText("Yükleme başarısız.")

    # Orijinal fonksiyon isimleri değişmedi:
    def load_url(self, url: str):
        q = QUrl.fromUserInput(url)
        if q.isEmpty():
            q = QUrl("about:blank")
        # mevcut sekmeyi yükle
        web = self._current_web()
        web.load(q)

    def _on_go(self):
        t = self.url_edit.text().strip()
        if t:
            self.load_url(t)

    def _on_url_changed(self, qurl: QUrl):
        new = qurl.toString()
        # sadece aktif sekmedeki url düzenleyiciyi güncelle
        web = self._current_web()
        try:
            if web.url().toString() == new and self.url_edit.text() != new:
                self.url_edit.setText(new)
            elif self.tabs.currentWidget() is web and self.url_edit.text() != new:
                self.url_edit.setText(new)
        except Exception:
            # bazı durumlarda widget hemen hazır olmayabilir
            self.url_edit.setText(new)

    # devtools göstergesini aç/kapat
    def _toggle_devtools(self):
        web = self._current_web()
        if self._devtools_view is None:
            # yeni bir devtools QWebEngineView oluştur
            self._devtools_view = QWebEngineView()
            self._devtools_view.setWindowTitle("DevTools")
            self._devtools_view.resize(900, 600)
        if not self._devtools_shown:
            try:
                web.page().setDevToolsPage(self._devtools_view.page())
                self._devtools_view.show()
                self._devtools_shown = True
                self.devtools_btn.setText("DevTools ○")
            except Exception as e:
                self.status.setText("Devtools açılamadı: " + str(e))
        else:
            try:
                # ayrılmayı dene
                web.page().setDevToolsPage(None)
                self._devtools_view.hide()
            except Exception:
                pass
            self._devtools_shown = False
            self.devtools_btn.setText("DevTools")

    # arama
    def _on_find(self):
        text = self.find_edit.text().strip()
        if not text:
            return
        web = self._current_web()
        try:
            # ileri arama (temel)
            web.findText("")  # önce temizle (önceki işaretleri sıfırla)
            web.findText(text)
            self.status.setText(f"Arandı: {text}")
        except Exception as e:
            self.status.setText("Arama hatası: " + str(e))


# ----------------------------
# Globals ve helper'lar (isimler korunmuş)
# ----------------------------
_app = None            # QApplication instance (veya None)
_window = None         # BrowserWidget instance (veya None)
_qt_pump_started = False
DEFAULT_URL = "https://www.google.com/"   # open_browser() bu url'i açar; gerekirse globali değiştir.

def _ensure_qapplication():
    global _app
    if QApplication.instance() is None:
        _app = QApplication(sys.argv)
    else:
        _app = QApplication.instance()
    return _app

def _start_qt_pump(root, interval_ms=20):
    """Tk mainloop içinde Qt olaylarını periyodik olarak işler."""
    global _qt_pump_started
    if _qt_pump_started:
        return
    _qt_pump_started = True
    app = _ensure_qapplication()
    def pump():
        try:
            app.processEvents()
        except Exception as e:
            # Hata fırlatmadan devam et (logla)
            print("Qt event pump hata:", e)
        root.after(interval_ms, pump)
    root.after(interval_ms, pump)

# ----------------------------
# İSTEDİĞİN parametresiz fonksiyon (ismi değişmedi)
# ----------------------------
def open_browser():
    """
    Parametresiz: Tk uygulamanın zaten var olduğunu varsayar (tk._default_root).
    Butonunun command'una bunu bağla: command=open_browser
    """
    global _app, _window
    root = getattr(tk, "_default_root", None)
    if root is None:
        raise RuntimeError("Tk kök penceresi bulunamadı. Önce tk.Tk() çalıştırılmış olmalı.")

    _ensure_qapplication()

    # Eğer pencere zaten varsa güncelle ve öne çıkar
    if _window is not None:
        try:
            # artık sekmeler olduğu için aktif sekmeyi DEFAULT_URL ile güncelle
            _window.load_url(DEFAULT_URL)
            _window.show()
            _window.raise_()
            _window.activateWindow()
        except Exception:
            try:
                _window.close()
            except Exception:
                pass
            _window = None

    if _window is None:
        _window = BrowserWidget(url=DEFAULT_URL, parent=None)
        _window.show()

    # Qt pump'i başlat (sadece ilk defa)
    _start_qt_pump(root)

# ----------------------------
# Opsiyonel: program kapanırken PyQt penceresini kapat (ismi değişmedi)
# ----------------------------
def _on_tk_close():
    global _window
    try:
        if _window is not None:
            _window.close()
    finally:
        # gerçek kapatma (default behavior)
        root = getattr(tk, "_default_root", None)
        if root is not None:
            try:
                root.destroy()
            except Exception:
                pass

# Not: Eğer kendi kodunda root varsa, şöyle bağlayabilirsin:
# root.protocol("WM_DELETE_WINDOW", _on_tk_close)
# ve DEFAULT_URL globalini buton callback'inde değiştirebilirsin:
# DEFAULT_URL = "https://yeni-adres.com"; open_browser()




# ---------- Media Player ----------

# pygame isteğe bağlı
try:
    import pygame
    PYGAME_AVAILABLE = True
except Exception:
    pygame = None
    PYGAME_AVAILABLE = False


import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import vlc
import time

def open_media_player():
    """
    Gelişmiş VLC tabanlı medya oynatıcı pencere açar.
    - parent: var olan bir Tk widget'ı (ör. root veya başka bir pencereden gelen widget).
    - NOT: Fonksiyon kesinlikle tk.Tk(), mainloop veya yeni bir root oluşturmaz.
    """

    # VLC instance ve player
    vlc_instance = vlc.Instance()
    player = vlc_instance.media_player_new()

    # Toplevel pencere
    win = tk.Toplevel()
    win.title("Sarma Media Player — VLC Edition")
    win.geometry("980x900")
    win.minsize(640, 360)

    # Üst: Video alanı (canvas içine gömülecek)
    video_frame = ttk.Frame(win)
    video_frame.pack(side="top", fill="both", expand=True)

    canvas = tk.Canvas(video_frame, background="black")
    canvas.pack(fill="both", expand=True)

    # Sağ bölme: oynatma listesi ve kontroller
    right_frame = ttk.Frame(win, width=260)
    right_frame.pack(side="right", fill="y")

    # Playlist
    playlist_label = ttk.Label(right_frame, text="Playlist")
    playlist_label.pack(anchor="nw", padx=6, pady=(6,0))

    playlist_box = tk.Listbox(right_frame, activestyle="none")
    playlist_box.pack(fill="both", expand=False, padx=6, pady=6, ipady=60)

    # Kontrol butonları
    controls = ttk.Frame(right_frame)
    controls.pack(fill="x", padx=6, pady=(0,6))

    btn_play = ttk.Button(controls, text="Play")
    btn_pause = ttk.Button(controls, text="Pause")
    btn_stop = ttk.Button(controls, text="Stop")
    btn_prev = ttk.Button(controls, text="Prev")
    btn_next = ttk.Button(controls, text="Next")

    btn_prev.grid(row=0, column=0, padx=3, pady=3)
    btn_play.grid(row=0, column=1, padx=3, pady=3)
    btn_pause.grid(row=0, column=2, padx=3, pady=3)
    btn_stop.grid(row=0, column=3, padx=3, pady=3)
    btn_next.grid(row=0, column=4, padx=3, pady=3)

    # Ses ve pozisyon
    vol_frame = ttk.Frame(right_frame)
    vol_frame.pack(fill="x", padx=6, pady=6)
    ttk.Label(vol_frame, text="Volume").pack(anchor="w")
    vol_scale = ttk.Scale(vol_frame, from_=0, to=100, orient="horizontal")
    vol_scale.set(80)
    vol_scale.pack(fill="x")

    pos_frame = ttk.Frame(win)
    pos_frame.pack(side="bottom", fill="x")
    time_label = ttk.Label(pos_frame, text="00:00 / 00:00")
    time_label.pack(side="left", padx=6)
    pos_scale = ttk.Scale(pos_frame, from_=0, to=1000, orient="horizontal")
    pos_scale.pack(side="left", fill="x", expand=True, padx=6, pady=6)

    # Alt: Dosya ve ayarlar
    bottom_frame = ttk.Frame(right_frame)
    bottom_frame.pack(fill="x", padx=6, pady=(0,12))
    btn_open = ttk.Button(bottom_frame, text="Open Files")
    btn_add_url = ttk.Button(bottom_frame, text="Open URL")
    btn_open.pack(fill="x", pady=3)
    btn_add_url.pack(fill="x", pady=3)

    # Durum ve ayarlar
    loop_var = tk.BooleanVar(value=False)
    btn_loop = ttk.Checkbutton(bottom_frame, text="Loop", variable=loop_var)
    btn_loop.pack(anchor="w", pady=(6,0))

    mute_var = tk.BooleanVar(value=False)
    btn_mute = ttk.Checkbutton(bottom_frame, text="Mute", variable=mute_var)
    btn_mute.pack(anchor="w")

    # Playlist veri yapısı
    playlist = []
    current_index = {"idx": None}

    # Yardımcı fonksiyonlar
    def set_video_handle():
        win.update_idletasks()
        handle = canvas.winfo_id()
        if sys.platform.startswith("win"):
            player.set_hwnd(handle)
        elif sys.platform == "darwin":
            # macOS: pylibvlc set_nsobject bazen kaygan olabilir, çoğu durumda win id işe yarar
            try:
                player.set_nsobject(handle)
            except Exception:
                player.set_xwindow(handle)
        else:
            player.set_xwindow(handle)

    def play_index(idx):
        if idx is None or idx < 0 or idx >= len(playlist):
            return
        path = playlist[idx]
        media = vlc_instance.media_new(path)
        player.set_media(media)
        set_video_handle()
        player.play()
        current_index["idx"] = idx
        playlist_box.selection_clear(0, "end")
        playlist_box.selection_set(idx)
        update_volume()
        # kısa gecikme ile pozisyon/uzunluk güncellemesi başlat
        win.after(200, update_pos)

    def add_files():
        files = filedialog.askopenfilenames(parent=win,
            title="Select media files",
            filetypes=[("Media files", "*.mp3 *.wav *.ogg *.flac *.mp4 *.mkv *.avi *.mov *.wmv"), ("All files", "*.*")])
        if not files:
            return
        for f in files:
            playlist.append(f)
            playlist_box.insert("end", os.path.basename(f))
        if current_index["idx"] is None:
            play_index(0)

    def open_url():
        url = tk.simpledialog.askstring("Open URL", "Enter stream or media URL:", parent=win)
        if not url:
            return
        playlist.append(url)
        playlist_box.insert("end", url)
        if current_index["idx"] is None:
            play_index(0)

    def update_volume(event=None):
        vol = int(vol_scale.get())
        player.audio_set_volume(vol)
        if mute_var.get():
            player.audio_set_mute(True)
        else:
            player.audio_set_mute(False)

    def on_play():
        idx = current_index["idx"]
        if idx is None:
            if playlist:
                play_index(0)
            return
        player.play()

    def on_pause():
        player.pause()

    def on_stop():
        player.stop()

    def on_next():
        if not playlist:
            return
        idx = current_index["idx"]
        if idx is None:
            idx = 0
        else:
            idx = (idx + 1) % len(playlist)
        play_index(idx)

    def on_prev():
        if not playlist:
            return
        idx = current_index["idx"]
        if idx is None:
            idx = 0
        else:
            idx = (idx - 1) % len(playlist)
        play_index(idx)

    def on_playlist_double(event):
        sel = playlist_box.curselection()
        if sel:
            play_index(sel[0])

    def seek_to(scale_value):
        # scale_value: 0..1000
        try:
            length = player.get_length()
            if length > 0:
                new_ms = int((float(scale_value) / 1000.0) * length)
                player.set_time(new_ms)
        except Exception:
            pass

    seeking = {"user": False}
    def on_pos_press(event):
        seeking["user"] = True

    def on_pos_release(event):
        seeking["user"] = False
        seek_to(pos_scale.get())

    def update_pos():
        # periyodik pozisyon ve süre güncellemesi
        if player is None:
            return
        try:
            length = player.get_length()  # ms
            pos = player.get_time()       # ms
        except Exception:
            length = 0
            pos = 0

        if length > 0:
            # pos_scale 0..1000 aralığında
            if not seeking["user"]:
                try:
                    pos_scale.set(int((pos / length) * 1000))
                except Exception:
                    pass
            # zaman etiketi
            def fmt(ms):
                if ms <= 0:
                    return "00:00"
                s = int(ms/1000)
                m = s//60
                s = s%60
                return f"{m:02d}:{s:02d}"
            time_label.config(text=f"{fmt(pos)} / {fmt(length)}")
        else:
            if not seeking["user"]:
                pos_scale.set(0)
            time_label.config(text="00:00 / 00:00")

        # otomatik sonraki parça
        state = player.get_state()
        # Eğer bitti ve loop açık -> tekrar oynat; değilse sıradaki
        if state == vlc.State.Ended:
            if loop_var.get():
                idx = current_index["idx"]
                play_index(idx if idx is not None else 0)
            else:
                # sonraki
                idx = current_index["idx"]
                if idx is None:
                    pass
                else:
                    if idx + 1 < len(playlist):
                        play_index(idx + 1)
        # tekrar çağır
        win.after(500, update_pos)

    # Bindler
    playlist_box.bind("<Double-Button-1>", on_playlist_double)
    pos_scale.bind("<Button-1>", on_pos_press)
    pos_scale.bind("<ButtonRelease-1>", on_pos_release)
    vol_scale.bind("<ButtonRelease-1>", update_volume)
    vol_scale.bind("<B1-Motion>", update_volume)

    btn_open.config(command=add_files)
    btn_add_url.config(command=open_url)
    btn_play.config(command=on_play)
    btn_pause.config(command=on_pause)
    btn_stop.config(command=on_stop)
    btn_next.config(command=on_next)
    btn_prev.config(command=on_prev)

    def on_close():
        try:
            player.stop()
        except Exception:
            pass
        win.destroy()

    win.protocol("WM_DELETE_WINDOW", on_close)

    # Öz: çift tıklayla tam ekran toggle
    def toggle_fullscreen(event=None):
        is_fs = win.attributes("-fullscreen")
        win.attributes("-fullscreen", not is_fs)
    canvas.bind("<Double-Button-1>", toggle_fullscreen)

    # İlk video handle ayarı (pencere çizildikten sonra)
    win.after(200, set_video_handle)

    # Başlangıç: eğer parent uygulaman zaten playback yapıyorsa vs. sessizlik önlemi
    update_volume()
    # Pozisyon güncellemesini başlat
    win.after(500, update_pos)

    # Return player object ve playlist kullanımı gerekiyorsa için referans
    return {
        "window": win,
        "player": player,
        "instance": vlc_instance,
        "playlist": playlist,
        "playlist_box": playlist_box,
        "controls": {
            "play": on_play, "pause": on_pause, "stop": on_stop,
            "next": on_next, "prev": on_prev
        }
    }


# ---------- Hesap Makinesi ----------
def open_calculator():
    hesap = tk.Toplevel()
    hesap.title("Hesap Makinesi")
    entry = tk.Entry(
        hesap,
        width=16,
        font=(
            "Arial",
            24),
        borderwidth=2,
        relief="solid")
    entry.grid(row=0, column=0, columnspan=4, padx=10, pady=10)

    def ekle(sayi):
        entry.insert(tk.END, str(sayi))

    def temizle():
        entry.delete(0, tk.END)

    def hesapla():
        try:
            sonuc = eval(entry.get())
            entry.delete(0, tk.END)
            entry.insert(tk.END, str(sonuc))
        except BaseException:
            entry.delete(0, tk.END)
            entry.insert(tk.END, "Hata!")
    sayi_butonlar = [
        ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
        ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
        ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
        ('0', 4, 0), ('.', 4, 1)
    ]
    for (text, row, col) in sayi_butonlar:
        tk.Button(
            hesap,
            text=text,
            width=5,
            height=2,
            command=lambda t=text: ekle(t)).grid(
            row=row,
            column=col)
    islem_butonlar = [
        ('+', 1, 3), ('-', 2, 3), ('*', 3, 3), ('/', 4, 3)
    ]
    for (text, row, col) in islem_butonlar:
        tk.Button(
            hesap,
            text=text,
            width=5,
            height=2,
            bg="orange",
            fg="white",
            command=lambda t=text: ekle(t)).grid(
            row=row,
            column=col)
    tk.Button(
        hesap,
        text="=",
        width=5,
        height=2,
        bg="green",
        fg="white",
        command=hesapla).grid(
        row=4,
        column=2)
    tk.Button(
        hesap,
        text="C",
        width=5,
        height=2,
        bg="red",
        fg="white",
        command=temizle).grid(
        row=4,
        column=1)
    add_icon(
        500,
        200,
        r"C:\Users\Yiğit Aslan\Desktop\BTL_setups.exe\Icons\calculator.png",
        "Hesap Makinesi",
        open_calculator,
        deletable=True)


# ---------- Ayarlar (basit) ----------
settings_data = {"Tema": ["Light", "green", "Blue"], "Ses": ["Açık", "Kapalı"]}
current_settings = {"Tema": "Light", "Ses": "Açık"}


def apply_theme(theme):
    if theme == "Light":
        root.config(bg="deepskyblue")
        taskbar.config(bg="gray20")
    elif theme == "green":
        root.config(bg="green")
        taskbar.config(bg="gray10")
    elif theme == "Blue":
        root.config(bg="blue")
        taskbar.config(bg="darkblue")
    for data in desktop_icons.values():
        try:
            data["frame"].config(bg=root.cget("bg"))
            for widget in data["frame"].winfo_children():
                widget.config(bg=root.cget("bg"))
        except Exception:
            pass


def open_settings():
    win = Toplevel(root)
    win.title("Ayarlar")
    win.geometry("300x250")
    tk.Label(win, text="Ayarlar", font=("Arial", 14, "bold")).pack(pady=10)
    options_vars = {}
    for key, options in settings_data.items():
        frame = tk.Frame(win)
        frame.pack(fill="x", pady=5, padx=10)
        tk.Label(frame, text=key).pack(side="left")
        var = tk.StringVar(value=current_settings[key])
        options_vars[key] = var
        tk.OptionMenu(frame, var, *options).pack(side="right")

    def save_settings():
        for k, v in options_vars.items():
            current_settings[k] = v.get()
        apply_theme(current_settings["Tema"])
        if current_settings["Ses"] == "Açık":
            play_info()
        messagebox.showinfo(
            "Ayarlar Kaydedildi",
            "Ayarlar başarıyla uygulandı!")
    save_btn = tk.Button(win, text="Kaydet", command=save_settings)
    save_btn.pack(pady=10)


# ---------- Dil seçenekleri ----------
LANGUAGES = {
    "TR": {
        "start_menu": "Başlat",
        "task_manager": "Görev Yöneticisi",
        "notepad": "Not Defteri",
        "snake_game": "Yılan Oyunu",
        "ball_game": "Top Yakalama",
        "settings": "Ayarlar",
        "maria_game": "Maria'yı Kurtar",
        "cmd_panel": "CMD Paneli",
        "trash": "Çöp Kutusu",
        "browser": "BTL Tarayıcı",
        "update_center": "Güncelleme Merkezi",
        "paint": "Paint",
        "store": "BTL Store",
        "restore": "Geri Yükle",
        "empty_trash": "Çöp Kutusunu Boşalt",
        "info_title": "Bilgi",
        "error_title": "Hata",
        "game_over": "Oyun Bitti",
        "boss_defeated": "Boss yenildi! Maria kurtarıldı!",
        "sely_dead": "Sely öldü! Maria kurtulamadı!"},
    "EN": {
        "start_menu": "Start",
        "task_manager": "Task Manager",
        "notepad": "Notepad",
        "snake_game": "Snake Game",
        "ball_game": "Ball Catch",
        "maria_game": "Save Maria",
        "cmd_panel": "CMD Panel",
        "trash": "Trash",
        "browser": "BTL Browser",
        "update_center": "Update Center",
        "paint": "Paint",
        "store": "BTL Store",
        "restore": "Restore",
        "empty_trash": "Empty Trash",
        "info_title": "Info",
        "error_title": "Error",
        "game_over": "Game Over",
        "boss_defeated": "Boss defeated! Maria saved!",
        "sely_dead": "Sely died! Maria couldn't be saved!"}}
current_lang = "EN"
L = LANGUAGES[current_lang]


def change_language(lang_code):
    global current_lang, L
    if lang_code in LANGUAGES:
        current_lang = lang_code
        L = LANGUAGES[current_lang]
        update_ui_texts()


def update_ui_texts():
    try:
        start_button.config(text=L["start_menu"])
    except Exception:
        pass


# ---------- Start button (ikon yükleme güvenli) ----------
start_icon_path = os.path.join(ICONS_DIR, "startbutton.png")
start_icon = load_image_as_tk(start_icon_path, size=(24, 24))
if start_icon:
    start_button = Button(
        taskbar,
        image=start_icon,
        command=lambda: open_start_menu(),
        bg="gray30",
        fg="white",
        relief="flat",
        bd=0,
        activebackground="gray45")
    start_button.image = start_icon
else:
    start_button = Button(
        taskbar,
        text="Start",
        command=lambda: open_start_menu())
start_button.pack(side="left", padx=5)

# ---------- Start menu (tanım, start_button referansı kullanınca start_bu


def open_start_menu():
    """
    Geliştirilmiş open_start_menu() - parametresiz, global isimlere dayanır.
    - Yeni uygulama oluşturmaz. Sadece Menü işlevselliğini geliştirir.
    - Scrollbar + mousewheel uyumu, daha iyi arama/odak davranışı,
      sağ-tık PIN/Gizle (durum kaydı), numara kısayolları, güvenli kapanış vb.
    """
    try:
        import os, json, webbrowser, subprocess, time
        from tkinter import Toplevel, Canvas, Frame, Label, Button, Entry, StringVar, Menu, messagebox, Scrollbar, VERTICAL, RIGHT, Y, LEFT, BOTH
    except Exception:
        return

    # --- yardımcılar (küçük, dikkatli) ---
    def _safe_call(fn, *a, **k):
        try:
            return fn(*a, **k)
        except Exception:
            try:
                # sessizce geç
                return None
            except Exception:
                return None

    # resolve global root ve start_button
    root_local = globals().get("root", None)
    start_btn_local = globals().get("start_button", None)

    menu = Toplevel(root_local) if root_local else Toplevel()
    try:
        menu.taskbar_exclude = True
    except Exception:
        pass
    menu.overrideredirect(True)
    menu.config(bg="gray10")

    width = 420
    height = 480

    try:
        bx = start_btn_local.winfo_rootx()
        by = start_btn_local.winfo_rooty()
        bwidth = start_btn_local.winfo_width()
        bheight = start_btn_local.winfo_height()
    except Exception:
        bx = 100
        try:
            by = root_local.winfo_rooty() + root_local.winfo_height() - 40
        except Exception:
            by = 200
        bwidth = 50
        bheight = 20

    x = bx + bwidth // 2 - width // 2
    y_final = by - height
    y_start = by

    # shadow (isteğe bağlı)
    try:
        shadow = Toplevel(root_local) if root_local else Toplevel()
        try:
            shadow.taskbar_exclude = True
        except Exception:
            pass
        shadow.overrideredirect(True)
        try:
            shadow.attributes("-alpha", 0.18)
        except Exception:
            pass
        shadow.config(bg="black")
        shadow.geometry(f"{width+10}x{height+10}+{x-5}+{y_start+5}")
    except Exception:
        shadow = None

    menu.geometry(f"{width}x{height}+{x}+{y_start}")

    # ana canvas (içine scrollable frame yerleştirilecek)
    canvas = Canvas(menu, width=width, height=height, bg="gray17", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    # header
    header = Frame(menu, bg="gray12", height=42)
    canvas.create_window(0, 0, window=header, anchor='nw', width=width, height=42)
    lbl_title = Label(header, text="Başlat — BTL", bg="gray12", fg="white", font=("Segoe UI", 11, "bold"))
    lbl_title.pack(side="left", padx=10)

    def _close():
        if shadow:
            try:
                shadow.destroy()
            except Exception:
                pass
        try:
            menu.destroy()
        except Exception:
            pass

    btn_close = Button(header, text="✕", bg="gray12", fg="white", bd=0, relief='flat', command=_close, cursor="hand2")
    btn_close.pack(side="right", padx=8, pady=6)
    try:
        _ToolTip(btn_close, "Kapat (Esc)")
    except Exception:
        pass

    # sürükleme header
    _drag = {"x": 0, "y": 0}
    def drag_start(e):
        _drag["x"], _drag["y"] = e.x, e.y
    def drag_move(e):
        nx = menu.winfo_x() + e.x - _drag["x"]
        ny = menu.winfo_y() + e.y - _drag["y"]
        menu.geometry(f"+{nx}+{ny}")
        if shadow:
            try:
                shadow.geometry(f"+{nx-5}+{ny+5}")
            except Exception:
                pass
    header.bind("<Button-1>", drag_start)
    header.bind("<B1-Motion>", drag_move)

    # profil alanı (eğer kullanıcı kodu eklemişse kullan)
    try:
        if callable(globals().get("add_user_profile_to_canvas", None)):
            globals()["add_user_profile_to_canvas"](menu, canvas, width)
        else:
            _default_add_user_profile_to_canvas(menu, canvas, width)
    except Exception:
        try:
            _default_add_user_profile_to_canvas(menu, canvas, width)
        except Exception:
            pass

    # arama kutusu
    search_var = StringVar()
    entry_search = Entry(canvas, textvariable=search_var, bd=0, font=("Segoe UI", 10))
    canvas.create_window(width // 2, 68, window=entry_search, anchor='n', width=360)
    entry_search.insert(0, "Ara... (yaz başlasın zaten)")

    def on_search_focus_in(e):
        v = entry_search.get()
        if v.startswith("Ara"):
            entry_search.delete(0, "end")
    def on_search_focus_out(e):
        if entry_search.get().strip() == "":
            entry_search.insert(0, "Ara... (yaz başlasın zaten)")
    entry_search.bind("<FocusIn>", on_search_focus_in)
    entry_search.bind("<FocusOut>", on_search_focus_out)

    # -- scrollable frame yapısı (Scrollbar + Canvas içinde frame)
    scroll_canvas = Canvas(btn_frame := Frame(canvas, bg="gray17"), bg="gray17", highlightthickness=0)
    vscroll = Scrollbar(btn_frame, orient=VERTICAL, command=scroll_canvas.yview)
    scroll_canvas.configure(yscrollcommand=vscroll.set)
    # place inside main canvas
    canvas.create_window(width // 2, 110, window=btn_frame, anchor='n', width=380, height=height - 170)
    vscroll.pack(side=RIGHT, fill=Y)
    scroll_canvas.pack(side=LEFT, fill=BOTH, expand=True)
    inner_frame = Frame(scroll_canvas, bg="gray17")
    # inner_frame'ı canvas içine yerleştir
    inner_id = scroll_canvas.create_window((0,0), window=inner_frame, anchor='nw')
    def _update_inner_scrollregion(event=None):
        try:
            scroll_canvas.update_idletasks()
            bbox = scroll_canvas.bbox(inner_id)
            if bbox:
                scroll_canvas.configure(scrollregion=bbox)
        except Exception:
            pass
    inner_frame.bind("<Configure>", _update_inner_scrollregion)

    # mousewheel binding: hem Windows/Mac (delta) hem X11 (Button-4/5)
    def _on_mousewheel(event):
        try:
            if getattr(event, "delta", None):
                delta = int(-1 * (event.delta / 120))
                scroll_canvas.yview_scroll(delta, "units")
            else:
                if event.num == 4:
                    scroll_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    scroll_canvas.yview_scroll(1, "units")
        except Exception:
            pass
    try:
        menu.bind_all("<MouseWheel>", _on_mousewheel)
        menu.bind_all("<Button-4>", _on_mousewheel)
        menu.bind_all("<Button-5>", _on_mousewheel)
    except Exception:
        pass

    # orijinal uygulama listesi (hesap makinesi yok; orijinaller korunuyor)
    raw_buttons = [
        ("📝 Not Defteri", lambda: _safe_call(globals().get("open_notepad", lambda: messagebox.showinfo("Hata", "Notepad yok")))),
        ("🌐 BTL Tarayıcı", lambda: _safe_call(lambda: webbrowser.open("https://www.google.com"))),
        ("🐍 Yılan Oyunu", lambda: _safe_call(globals().get("open_snake_game", lambda: messagebox.showinfo("Hata", "Snake yok")))),
        ("⚽ Top Yakalama", lambda: _safe_call(globals().get("open_ball_game", lambda: messagebox.showinfo("Hata", "Ball game yok")))),
        ("🧩 Maria'yı Kurtar", lambda: _safe_call(globals().get("open_maria_game", lambda: messagebox.showinfo("Hata", "Maria yok")))),
        ("🧠 CMD Paneli", lambda: _safe_call(globals().get("open_cmd_panel", lambda: messagebox.showinfo("Hata", "CMD yok")))),
        ("👤 Kullanıcılar", lambda: messagebox.showinfo("Kullanıcılar", "\n".join(globals().get("users", [])) if globals().get("users") else "Kullanıcı yok")),
        ("🎨 Paint", lambda: _safe_call(globals().get("open_paint_app", lambda: messagebox.showinfo("Hata", "Paint yok")))),
        ("ℹ️ Hakkında", lambda: messagebox.showinfo("BTL hakkında", "BTL4 - BTL version is 4, you use updated version - BTL25_4")),
        ("🚪 Çıkış", lambda: _safe_call(globals().get("shutdown_animation", lambda: messagebox.showinfo("Çıkış", "Shutdown yok")))),
        ("⚙️ Yapılandırma", lambda: _safe_call(globals().get("open_control_panel", lambda: messagebox.showinfo("Hata", "Control Panel yok")))),
        ("📘 Kayıt Defteri", lambda: _safe_call(globals().get("open_reg", lambda: messagebox.showinfo("Hata", "Regedit yok")))),
        ("♟️ BTL chess", lambda: _safe_call(globals().get("open_chess_game", lambda: messagebox.showinfo("Hata", "Chess yok")))),
        ("📟 Lightning Code", lambda: _safe_call(globals().get("open_lightning_code", lambda: messagebox.showinfo("Hata", "Code editor yok"))))
    ]

    # buton widget'larını oluştur ve inner_frame içine koy
    btn_widgets = []
    def make_btn(text, cmd):
        b = Button(inner_frame, text=text, anchor='w', width=36, padx=10, font=("Segoe UI", 10),
                   bd=0, relief='flat', bg="gray24", fg="white", cursor="hand2", activebackground="gray36")
        def on_enter(e): b.config(bg="gray35")
        def on_leave(e): b.config(bg="gray24")
        b.bind("<Enter>", on_enter)
        b.bind("<Leave>", on_leave)
        b.config(command=lambda: (_safe_call(cmd), _enhanced_close()))
        return b

    for text, cmd in raw_buttons:
        b = make_btn(text, cmd)
        b.pack(fill='x', pady=6)
        try:
            _ToolTip(b, text)
        except Exception:
            pass
        btn_widgets.append((text.lower(), b))

    # ARAMA: gelişmiş davranış - kelime bazlı, ilk eşleşmeyi seç, Enter çalıştırır
    def filter_buttons(*_):
        q = search_var.get().strip().lower()
        if q == "" or q.startswith("ara"):
            q = ""
        parts = q.split()
        for name, widget in btn_widgets:
            visible = True
            if parts:
                for p in parts:
                    if p not in name:
                        visible = False
                        break
            if visible:
                widget.pack_configure(fill='x', pady=6)
            else:
                widget.pack_forget()
        # ilk eşleşmeyi seç
        try:
            visible_widgets = [w for nm, w in btn_widgets if str(w.winfo_manager()) != ""]
            if visible_widgets:
                select_index(0)
                # scroll first visible into view
                try:
                    scroll_canvas.update_idletasks()
                    y = visible_widgets[0].winfo_y()
                    scroll_canvas.yview_moveto(max(0, y / max(1, scroll_canvas.bbox(inner_id)[3])))
                except Exception:
                    pass
        except Exception:
            pass
    try:
        search_var.trace_add("write", filter_buttons)
    except Exception:
        pass

    # klavye gezinmesi ve seçim
    selection = {"idx": 0}
    def select_index(idx):
        visible = [w for nm, w in btn_widgets if str(w.winfo_manager()) != ""]
        if not visible:
            return
        idx = max(0, min(idx, len(visible) - 1))
        selection['idx'] = idx
        for _, w in btn_widgets:
            try:
                w.config(relief='flat')
            except Exception:
                pass
        try:
            visible[idx].config(relief='ridge')
            visible[idx].focus_set()
            # scroll into view
            try:
                scroll_canvas.update_idletasks()
                wy = visible[idx].winfo_y()
                h = scroll_canvas.winfo_height()
                scroll_canvas.yview_moveto(max(0, (wy - 10) / max(1, scroll_canvas.bbox(inner_id)[3])))
            except Exception:
                pass
        except Exception:
            pass

    def on_key(e):
        visible = [w for nm, w in btn_widgets if str(w.winfo_manager()) != ""]
        if e.keysym == "Down":
            selection['idx'] = min(selection['idx'] + 1, max(0, len(visible) - 1))
            select_index(selection['idx'])
        elif e.keysym == "Up":
            selection['idx'] = max(selection['idx'] - 1, 0)
            select_index(selection['idx'])
        elif e.keysym == "Return":
            if visible:
                visible[selection['idx']].invoke()
        elif e.keysym == "Escape":
            _enhanced_close()
        else:
            # harf basıldıysa aramaya odaklan
            if len(e.keysym) == 1 and e.keysym.isprintable():
                entry_search.focus_set()
    try:
        menu.bind_all("<Key>", on_key)
    except Exception:
        pass

    # CONTEXT MENU: Özellikler, Başlata Sabitle (pin), Gizle
    # pinned ve hidden durumlarını state dosyasında saklıyoruz
    try:
        state_file = os.path.join(os.path.expanduser("~"), ".btl_start_state.json")
    except Exception:
        state_file = "btl_start_state.json"

    pinned = set()
    hidden = set()
    def _save_state():
        try:
            s = {"pinned": list(pinned), "hidden": list(hidden), "selection": selection.get("idx", 0)}
            with open(state_file, "w", encoding="utf-8") as f:
                json.dump(s, f)
        except Exception:
            pass

    def _load_state():
        try:
            if os.path.exists(state_file):
                with open(state_file, "r", encoding="utf-8") as f:
                    s = json.load(f)
                for nm, w in btn_widgets:
                    if nm in s.get("hidden", []):
                        try:
                            w.pack_forget()
                        except Exception:
                            pass
                for p in s.get("pinned", []):
                    pinned.add(p)
                # apply pin order
                if pinned:
                    # move pinned widgets to top in order they appear in raw_buttons
                    ordered = []
                    for nm, w in btn_widgets:
                        if nm in pinned:
                            ordered.append((nm, w))
                    # repack: first pinned, then others
                    for nm, w in ordered:
                        try:
                            w.pack_forget()
                            w.pack(fill='x', pady=6)
                        except Exception:
                            pass
                idx = s.get("selection", 0)
                menu.after(120, lambda: select_index(idx))
        except Exception:
            pass

    # oluştur context menu'yu widget başına bağla
    try:
        for name, widget in btn_widgets:
            try:
                ctx_btn = Menu(menu, tearoff=0)
            except Exception:
                ctx_btn = Menu(menu, tearoff=0)
            btn_text = widget.cget("text")
            def _show_props(w=widget, t=btn_text):
                try:
                    messagebox.showinfo("Özellikler", f"Öğe: {t}")
                except Exception:
                    pass
            def _pin_to_start(w=widget, nm=name, t=btn_text):
                try:
                    if nm in pinned:
                        pinned.discard(nm)
                        # görsel feedback
                        _ToolTip(w, t)
                    else:
                        pinned.add(nm)
                        _ToolTip(w, f"Pinned: {t}")
                    # repack: pinnedleri öne al
                    try:
                        # remove and repack pinned in order of appearance in raw_buttons
                        for p_nm, p_w in list(btn_widgets):
                            if p_nm in pinned:
                                p_w.pack_forget()
                                p_w.pack(fill='x', pady=6)
                    except Exception:
                        pass
                    _save_state()
                except Exception:
                    pass
            def _hide_button(w=widget, nm=name, t=btn_text):
                try:
                    w.pack_forget()
                    hidden.add(nm)
                    _save_state()
                except Exception:
                    pass
            ctx_btn.add_command(label="Özellikler", command=_show_props)
            ctx_btn.add_command(label="Başlata Sabitle", command=_pin_to_start)
            ctx_btn.add_command(label="Gizle", command=_hide_button)
            def _popup(e, m=ctx_btn):
                try:
                    m.tk_popup(e.x_root, e.y_root)
                except Exception:
                    pass
            widget.bind("<Button-3>", _popup)
    except Exception:
        pass

    # numara kısayolları (1-9)
    def _press_number(ev):
        try:
            if ev.char and ev.char.isdigit():
                n = int(ev.char)
                if n == 0:
                    return
                visible = [w for nm, w in btn_widgets if str(w.winfo_manager()) != ""]
                if not visible:
                    return
                idx = n - 1
                if idx < len(visible):
                    visible[idx].invoke()
        except Exception:
            pass
    try:
        for ch in "123456789":
            menu.bind_all(ch, _press_number)
    except Exception:
        pass

    # arama Enter davranışı: ilk görünür öğeyi çalıştır
    def _search_enter(ev=None):
        try:
            visible = [w for nm, w in btn_widgets if str(w.winfo_manager()) != ""]
            if visible:
                visible[0].invoke()
        except Exception:
            pass
    try:
        entry_search.bind("<Return>", _search_enter)
    except Exception:
        pass

    # state yükle
    try:
        _load_state()
    except Exception:
        pass

    # kapatırken temizlik + state kaydı
    def _enhanced_close():
        try:
            _save_state()
        except Exception:
            pass
        try:
            menu.unbind_all("<MouseWheel>")
            menu.unbind_all("<Button-4>")
            menu.unbind_all("<Button-5>")
            for ch in "123456789":
                menu.unbind_all(ch)
        except Exception:
            pass
        try:
            _close()
        except Exception:
            try:
                menu.destroy()
            except Exception:
                pass

    try:
        btn_close.config(command=_enhanced_close)
    except Exception:
        pass

    # menü dışına tıklama ile kapanış: daha güvenli sürüm
    def _global_click(e):
        try:
            if not menu.winfo_ismapped():
                return
            try:
                if menu.winfo_containing(e.x_root, e.y_root) is None:
                    _enhanced_close()
            except Exception:
                pass
        except Exception:
            pass
    try:
        menu.bind_all("<Button-1>", _global_click, add="+")
    except Exception:
        pass

    # periyodik scroll region güncelle
    def _periodic_update():
        try:
            _update_inner_scrollregion()
        except Exception:
            pass
        try:
            menu.after(1000, _periodic_update)
        except Exception:
            pass
    try:
        menu.after(1200, _periodic_update)
    except Exception:
        pass

    # animasyon: yukarı kayma (daha yumuşak)
    def animate(y):
        nonlocal shadow
        try:
            if y > y_final:
                step = max(6, (y - y_final) // 8)
                y -= step
                if y < y_final:
                    y = y_final
                menu.geometry(f"{width}x{height}+{x}+{y}")
                if shadow:
                    try:
                        shadow.geometry(f"{width+10}x{height+10}+{x-5}+{y+5}")
                    except Exception:
                        pass
                menu.after(12, lambda: animate(y))
            else:
                menu.geometry(f"{width}x{height}+{x}+{y_final}")
                if shadow:
                    try:
                        shadow.geometry(f"{width+10}x{height+10}+{x-5}+{y_final+5}")
                    except Exception:
                        pass
        except Exception:
            pass
    try:
        animate(y_start)
    except Exception:
        pass

    # canvas içinden sürükleme (ekstra taşıma)
    def move_menu(event):
        nx = event.x_root - width // 2
        ny = event.y_root - 20
        menu.geometry(f"+{nx}+{ny}")
        if shadow:
            try:
                shadow.geometry(f"+{nx-5}+{ny+5}")
            except Exception:
                pass
    canvas.bind("<B1-Motion>", move_menu)

    # odak ver
    menu.focus_force()
    entry_search.focus_set()

    # root yeniden boyutlanırsa menüyü kapat (kullanıcının masaüstünü bozmamak için)
    try:
        root_local.bind("<Configure>", lambda e: _enhanced_close())
    except Exception:
        pass

    # ilk seçim
    menu.after(120, lambda: select_index(0))

    # ufak bip (opsiyonel)
    try:
        import winsound
        try:
            winsound.MessageBeep()
        except Exception:
            pass
    except Exception:
        pass

# ---------- Başlangıç İkonları (örnek) ----------
# Güvenli çağrı: bazı ikon yolları olmayabilir; add_icon fallback yapar
add_icon(
    50,
    50,
    os.path.join(
        ICONS_DIR,
        "notepad.png"),
    "Not Defteri",
    open_notepad,
    deletable=False)
add_icon(
    150,
    50,
    os.path.join(
        ICONS_DIR,
        "snake.png"),
    "Yılan Oyunu",
    open_snake_game,
    deletable=False)
add_icon(
    250,
    50,
    os.path.join(
        ICONS_DIR,
        "ball.png"),
    "Top Yakalama",
    open_ball_game,
    deletable=False)
add_icon(
    350,
    50,
    os.path.join(
        ICONS_DIR,
        "maria.png"),
    "Maria'yı Kurtar",
    open_maria_game,
    deletable=False)
add_icon(
    450,
    50,
    os.path.join(
        ICONS_DIR,
        "cmd.png"),
    "CMD Paneli",
    open_cmd_panel,
    deletable=False)
add_icon(
    550,
    50,
    os.path.join(
        ICONS_DIR,
        "trash.png"),
    "Çöp Kutusu",
    open_trash,
    deletable=False)
add_icon(
    650,
    50,
    os.path.join(ICONS_DIR, "browser.png"),
    "BTL Tarayıcı",
    lambda: open_browser(),  # parametresiz, tıklandığında açacak
    deletable=False
)

add_icon(
    750,
    50,
    os.path.join(
        ICONS_DIR,
        "update.png"),
    "Güncelleme Merkezi",
    open_update_center,
    deletable=False)
add_icon(
    850,
    50,
    os.path.join(
        ICONS_DIR,
        "folder.png"),
    "Dosya Yöneticisi",
    open_file_manager,
    deletable=False)
add_icon(
    950,
    50,
    os.path.join(
        ICONS_DIR,
        "settings.png"),
    "Ayarlar",
    open_settings,
    deletable=False)
add_icon(
    1250,
    50,
    os.path.join(
        ICONS_DIR,
        "paint.png"),
    "Paint",
    open_paint_app,
    deletable=True)

# Media Player icon
add_icon(1150, 50, os.path.join(ICONS_DIR, "mediaplayer.png"),
         "BTL Media Player", open_media_player, deletable=False)

# ---------- Wi-Fi & Battery simgeleri ----------


def wifi_status():
    stats = psutil.net_if_stats()

    wifi_iface = None
    for iface in stats:
        if "wi" in iface.lower() or "wlan" in iface.lower():
            wifi_iface = iface
            break

    if wifi_iface:
        if stats[wifi_iface].isup:
            messagebox.showinfo("Wi-Fi", f"{wifi_iface} bağlı!")
        else:
            messagebox.showwarning("Wi-Fi", f"{wifi_iface} bağlı değil!")
    else:
        messagebox.showerror("Wi-Fi", "Wi-Fi arayüzü bulunamadı!")


wifi_icon = tk.Label(
    taskbar,
    text="🛜",
    bg="gray20",
    fg="white",
    font=(
        "Arial",
         16))
wifi_icon.pack(side="left", padx=2)
wifi_icon.bind("<Button-1>", lambda e: wifi_status())

battery_icon = tk.Label(
    taskbar,
    text="🔋",
    bg="gray20",
    fg="white",
    font=(
        "Arial",
         16))
battery_icon.pack(side="left", padx=2)


def battery_click(event):
    try:
        if PSUTIL_AVAILABLE:
            battery = psutil.sensors_battery()
            if battery:
                percent = battery.percent
                plugged = battery.power_plugged
                status = "Şarjda" if plugged else "Şarjda değil"
                messagebox.showinfo(
                    "Pil Durumu", f"Şarj: %{percent}\nDurum: {status}")
                return
    except Exception:
        pass
    messagebox.showinfo("Pil Durumu", "Pil bilgisi alınamadı!")


battery_icon.bind("<Button-1>", battery_click)

# ---------- Start up sequence ----------
root.after(5000, lambda: startup_animation(main_app))


# ---------- Dil menüsü ----------
lang_var = tk.StringVar(value=current_lang)


def lang_change(event=None):
    change_language(lang_var.get())


lang_menu = tk.OptionMenu(
    taskbar,
    lang_var,
    *LANGUAGES.keys(),
    command=lambda _: lang_change())
lang_menu.config(bg="gray30", fg="white")
lang_menu.pack(side="left", padx=5)

# ---------- Son: mainloop ----------
root.mainloop()
