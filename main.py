import base64
import csv
import hashlib
import io
import os
import tkinter as tk
from datetime import datetime
from tkinter import filedialog, messagebox

import customtkinter as ctk
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

# --- Constants ---

VERSAO_APP = "3.0"
GITHUB_USER = "MatPicolli"
FILES_DIR = "files"
PASSWORD_FILE = os.path.join(FILES_DIR, "senhas.enc")
MASTER_PASSWORD_FILE = os.path.join(FILES_DIR, "senha_mestre.key")
LEGACY_PASSWORD_FILE = os.path.join(FILES_DIR, "senhas.csv")
MAGIC_HEADER = b"PICO"
PBKDF2_ITERATIONS = 480_000

# --- Theme ---

C_BG = "#0d0d0d"
C_CARD = "#181818"
C_BORDER = "#2a2a2a"
C_TEXT = "#e0e0e0"
C_DIM = "#666666"
C_ACCENT = "#3b82f6"
C_ACCENT_HOVER = "#2563eb"
C_DANGER = "#dc2626"
C_DANGER_HOVER = "#b91c1c"
C_INPUT_BG = "#111111"
C_SELECT = "#1e3a5f"

FONT = ("Segoe UI", 12)
FONT_SMALL = ("Segoe UI", 10)
FONT_MONO = ("Consolas", 12)
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_LABEL = ("Segoe UI", 9)

# --- State ---

_passwords: list[list[str]] = []
_fernet: Fernet | None = None


def _ensure_dirs():
    os.makedirs(FILES_DIR, exist_ok=True)


# --- Crypto ---


def _derive_fernet_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def _hash_master(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        "sha256", password.encode(), salt + b"auth", PBKDF2_ITERATIONS
    )


def _init_fernet(password: str, salt: bytes):
    global _fernet
    _fernet = Fernet(_derive_fernet_key(password, salt))


def _save_master_password(password: str):
    _ensure_dirs()
    salt = os.urandom(16)
    pw_hash = _hash_master(password, salt)
    with open(MASTER_PASSWORD_FILE, "wb") as f:
        f.write(MAGIC_HEADER + salt + pw_hash)
    _init_fernet(password, salt)


def verify_master_password(password: str) -> bool:
    _ensure_dirs()
    if not os.path.exists(MASTER_PASSWORD_FILE):
        return False

    with open(MASTER_PASSWORD_FILE, "rb") as f:
        data = f.read()

    if data[:4] == MAGIC_HEADER:
        salt, stored_hash = data[4:20], data[20:52]
        if _hash_master(password, salt) == stored_hash:
            _init_fernet(password, salt)
            return True
        return False

    # Legacy format (ord * 3)
    try:
        text = data.decode("utf-8")
        stored = "".join(chr(ord(c) // 3) for c in text)
        if password == stored:
            _migrate_from_legacy(password)
            return True
    except (UnicodeDecodeError, ValueError, ZeroDivisionError):
        pass
    return False


# --- Storage ---


def _save_passwords():
    _ensure_dirs()
    buf = io.StringIO()
    csv.writer(buf).writerows(_passwords)
    encrypted = _fernet.encrypt(buf.getvalue().encode())
    with open(PASSWORD_FILE, "wb") as f:
        f.write(encrypted)


def _load_passwords():
    global _passwords
    _ensure_dirs()
    if not os.path.exists(PASSWORD_FILE):
        _passwords = []
        return
    with open(PASSWORD_FILE, "rb") as f:
        data = f.read()
    if not data:
        _passwords = []
        return
    decrypted = _fernet.decrypt(data).decode()
    _passwords = [row for row in csv.reader(io.StringIO(decrypted)) if row]


def _migrate_from_legacy(password: str):
    global _passwords
    legacy_data = []
    if os.path.exists(LEGACY_PASSWORD_FILE):
        with open(LEGACY_PASSWORD_FILE, "r", encoding="utf-8") as f:
            legacy_data = [row for row in csv.reader(f) if row]

    _save_master_password(password)
    _passwords = legacy_data
    _save_passwords()

    if os.path.exists(LEGACY_PASSWORD_FILE):
        os.replace(LEGACY_PASSWORD_FILE, LEGACY_PASSWORD_FILE + ".bak")


def _read_csv_file(path: str) -> list[list[str]]:
    for enc in ("utf-8", "latin-1"):
        try:
            with open(path, "r", encoding=enc) as f:
                return list(csv.reader(f))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"Nao foi possivel decodificar: {path}")


def _import_from_csv() -> int:
    global _passwords

    path = filedialog.askopenfilename(
        title="Selecione o arquivo CSV",
        filetypes=[("CSV", "*.csv")],
    )
    if not path:
        return 0

    try:
        rows = _read_csv_file(path)
    except (ValueError, OSError) as e:
        messagebox.showerror("Erro", str(e))
        return 0

    if not rows:
        messagebox.showinfo("Importar", "Arquivo vazio!")
        return 0

    # Normalize to 5 columns
    normalized = []
    for row in rows:
        if not row or not row[0].strip():
            continue
        padded = (row + ["", "", "", "", ""])[:5]
        normalized.append(padded)

    existing = {item[0] for item in _passwords}
    new = [r for r in normalized if r[0] not in existing]
    dupes = len(normalized) - len(new)

    if not new:
        messagebox.showinfo("Importar", "Todas as senhas ja existem!")
        return 0

    if dupes > 0:
        msg = f"{len(new)} novas, {dupes} duplicadas (ignoradas)."
        if not messagebox.askokcancel("Importar", msg):
            return 0

    _passwords.extend(new)
    _save_passwords()
    return len(new)


# --- UI helpers ---


def _make_entry(parent, **kwargs) -> ctk.CTkEntry:
    defaults = dict(
        font=FONT_MONO,
        height=34,
        fg_color=C_INPUT_BG,
        border_color=C_BORDER,
        border_width=1,
        corner_radius=4,
        text_color=C_TEXT,
    )
    defaults.update(kwargs)
    return ctk.CTkEntry(parent, **defaults)


def _flash_border(widget, color=C_DANGER, duration=1500):
    widget.configure(border_color=color)
    widget.after(duration, lambda: widget.configure(border_color=C_BORDER))


# --- Windows ---


class LoginWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        _ensure_dirs()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.configure(fg_color=C_BG)
        self.title("picoword")
        self.geometry("360x240")
        self.resizable(False, False)

        if os.path.exists(MASTER_PASSWORD_FILE):
            self._build_login()
        else:
            self._build_create()

        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.mainloop()

    def _on_close(self):
        self.quit()
        self.destroy()

    def _build_create(self):
        ctk.CTkLabel(self, text="picoword", font=FONT_TITLE, text_color=C_TEXT).pack(
            pady=(32, 4)
        )
        ctk.CTkLabel(
            self, text="crie sua senha mestre", font=FONT_SMALL, text_color=C_DIM
        ).pack(pady=(0, 16))

        self.p1 = _make_entry(self, font=FONT, width=240, height=36, corner_radius=6)
        self.p1.configure(placeholder_text="senha", show="*")
        self.p1.pack(pady=(0, 6))

        self.p2 = _make_entry(self, font=FONT, width=240, height=36, corner_radius=6)
        self.p2.configure(placeholder_text="confirmar", show="*")
        self.p2.pack(pady=(0, 14))
        self.p2.bind("<Return>", lambda _: self._on_create())

        ctk.CTkButton(
            self,
            text="confirmar",
            font=FONT,
            width=240,
            height=36,
            fg_color=C_ACCENT,
            hover_color=C_ACCENT_HOVER,
            corner_radius=6,
            command=self._on_create,
        ).pack()

    def _on_create(self):
        p1, p2 = self.p1.get(), self.p2.get()
        if not p1:
            _flash_border(self.p1)
            return
        if p1 != p2:
            _flash_border(self.p2)
            return
        _save_master_password(p1)
        self.destroy()
        MainWindow()

    def _build_login(self):
        ctk.CTkLabel(self, text="picoword", font=FONT_TITLE, text_color=C_TEXT).pack(
            pady=(48, 4)
        )
        ctk.CTkLabel(self, text="senha mestre", font=FONT_SMALL, text_color=C_DIM).pack(
            pady=(0, 16)
        )

        self.pw = _make_entry(self, font=FONT, width=240, height=36, corner_radius=6)
        self.pw.configure(placeholder_text="*****", show="*")
        self.pw.pack(pady=(0, 14))
        self.pw.bind("<Return>", lambda _: self._on_login())
        self.after(100, self.pw.focus_set)

        ctk.CTkButton(
            self,
            text="entrar",
            font=FONT,
            width=240,
            height=36,
            fg_color=C_ACCENT,
            hover_color=C_ACCENT_HOVER,
            corner_radius=6,
            command=self._on_login,
        ).pack()

    def _on_login(self):
        if verify_master_password(self.pw.get()):
            self.destroy()
            MainWindow()
        else:
            self.pw.delete(0, "end")
            _flash_border(self.pw)


class PasswordDialog(ctk.CTkToplevel):
    FIELDS = ["Index", "Usuario", "Senha", "E-mail"]

    def __init__(self, parent, title, data=None, readonly=False, allow_delete=False):
        super().__init__(parent)
        self.configure(fg_color=C_BG)
        self.title(title)
        self.geometry("380x460")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.result = None
        self.deleted = False
        self.entries: dict[str, ctk.CTkEntry] = {}

        for i, field in enumerate(self.FIELDS):
            ctk.CTkLabel(
                self,
                text=field.lower(),
                font=FONT_LABEL,
                text_color=C_DIM,
                anchor="w",
            ).pack(fill="x", padx=24, pady=(14 if i == 0 else 6, 0))

            entry = _make_entry(self)
            if data:
                entry.insert(0, data[i])
            if readonly or (field == "Index" and data):
                entry.configure(state="disabled")
            entry.pack(fill="x", padx=24)
            self.entries[field] = entry

        ctk.CTkLabel(
            self, text="adicional", font=FONT_LABEL, text_color=C_DIM, anchor="w"
        ).pack(fill="x", padx=24, pady=(6, 0))

        self.additional = ctk.CTkTextbox(
            self,
            font=FONT_MONO,
            height=70,
            fg_color=C_INPUT_BG,
            border_color=C_BORDER,
            border_width=1,
            corner_radius=4,
            text_color=C_TEXT,
        )
        if data and len(data) > 4:
            self.additional.insert("1.0", data[4])
        if readonly:
            self.additional.configure(state="disabled")
        self.additional.pack(fill="x", padx=24)

        if not readonly:
            btn_frame = ctk.CTkFrame(self, fg_color="transparent")
            btn_frame.pack(fill="x", padx=24, pady=(16, 20))

            ctk.CTkButton(
                btn_frame,
                text="salvar",
                font=FONT,
                height=34,
                fg_color=C_ACCENT,
                hover_color=C_ACCENT_HOVER,
                corner_radius=4,
                command=self._on_save,
            ).pack(side="left", expand=True, fill="x", padx=(0, 4))

            if allow_delete:
                ctk.CTkButton(
                    btn_frame,
                    text="deletar",
                    font=FONT,
                    height=34,
                    fg_color="transparent",
                    hover_color=C_DANGER_HOVER,
                    border_color=C_DANGER,
                    border_width=1,
                    text_color=C_DANGER,
                    corner_radius=4,
                    command=self._on_delete,
                ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        self.wait_window()

    def _on_save(self):
        if not self.entries["Index"].get():
            _flash_border(self.entries["Index"])
            return
        self.result = [self.entries[f].get() for f in self.FIELDS] + [
            self.additional.get("1.0", "end-1c")
        ]
        self.destroy()

    def _on_delete(self):
        if messagebox.askyesno("Confirmar", "Deletar esta senha?", parent=self):
            self.deleted = True
            self.destroy()


class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")
        self.configure(fg_color=C_BG)
        self.title("picoword")
        self.geometry("440x560")
        self.resizable(False, False)

        _ensure_dirs()
        if not os.path.exists(PASSWORD_FILE):
            _save_passwords()
        _load_passwords()

        self._build_ui()
        self._refresh_list()
        self.after(100, self.search_entry.focus_set)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.mainloop()

    def _on_close(self):
        self.quit()
        self.destroy()

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 0))

        ctk.CTkLabel(header, text="picoword", font=FONT_TITLE, text_color=C_TEXT).pack(
            side="left"
        )
        ctk.CTkLabel(
            header, text=f"v{VERSAO_APP}", font=FONT_LABEL, text_color=C_DIM
        ).pack(side="left", padx=(8, 0), pady=(8, 0))

        ctk.CTkButton(
            header,
            text="importar",
            font=FONT_SMALL,
            width=70,
            height=28,
            fg_color="transparent",
            hover_color=C_CARD,
            border_color=C_BORDER,
            border_width=1,
            corner_radius=4,
            text_color=C_DIM,
            command=self._on_import,
        ).pack(side="right")

        ctk.CTkFrame(self, height=1, fg_color=C_BORDER).pack(
            fill="x", padx=20, pady=(12, 0)
        )

        # Search
        self.search_var = ctk.StringVar()
        self.search_var.trace_add("write", lambda *_: self._on_search())

        self.search_entry = _make_entry(
            self,
            font=FONT,
            height=36,
            corner_radius=4,
            textvariable=self.search_var,
            placeholder_text="buscar...",
        )
        self.search_entry.pack(fill="x", padx=20, pady=(12, 8))

        # List
        list_frame = ctk.CTkFrame(
            self,
            fg_color=C_CARD,
            corner_radius=6,
            border_width=1,
            border_color=C_BORDER,
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))

        scrollbar = ctk.CTkScrollbar(list_frame, width=8)
        scrollbar.pack(side="right", fill="y", padx=(0, 2), pady=2)

        self.listbox = tk.Listbox(
            list_frame,
            font=FONT_MONO,
            selectmode=tk.SINGLE,
            borderwidth=0,
            highlightthickness=0,
            activestyle="none",
            bg=C_CARD,
            fg=C_TEXT,
            selectbackground=C_SELECT,
            selectforeground="white",
            relief="flat",
            yscrollcommand=scrollbar.set,
        )
        self.listbox.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=4)
        self.listbox.bind("<Double-Button-1>", lambda _: self._on_view())

        scrollbar.configure(command=self.listbox.yview)

        # Action buttons
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 6))

        ctk.CTkButton(
            btn_frame,
            text="+ adicionar",
            font=FONT,
            height=36,
            fg_color=C_ACCENT,
            hover_color=C_ACCENT_HOVER,
            corner_radius=4,
            command=self._on_add,
        ).pack(side="left", expand=True, fill="x", padx=(0, 4))

        ctk.CTkButton(
            btn_frame,
            text="editar",
            font=FONT,
            height=36,
            fg_color="transparent",
            hover_color=C_CARD,
            border_color=C_BORDER,
            border_width=1,
            text_color=C_TEXT,
            corner_radius=4,
            command=self._on_modify,
        ).pack(side="right", expand=True, fill="x", padx=(4, 0))

        # Footer
        ctk.CTkLabel(
            self,
            text=f"{GITHUB_USER}  ·  {datetime.now().year}",
            font=("Segoe UI", 9),
            text_color="#333333",
        ).pack(pady=(0, 10))

    def _refresh_list(self, items=None):
        display = items if items is not None else _passwords
        self.listbox.delete(0, tk.END)
        for item in display:
            self.listbox.insert(tk.END, f"  {item[0]}")

    def _selected(self) -> int | None:
        sel = self.listbox.curselection()
        if not sel:
            return None
        name = self.listbox.get(sel[0]).strip()
        return next((i for i, p in enumerate(_passwords) if p[0] == name), None)

    def _on_search(self):
        q = self.search_var.get().lower()
        if not q:
            self._refresh_list()
        else:
            self._refresh_list([p for p in _passwords if q in p[0].lower()])

    def _on_add(self):
        dialog = PasswordDialog(self, "adicionar")
        if dialog.result:
            if any(dialog.result[0] == p[0] for p in _passwords):
                messagebox.showwarning("Aviso", "Index ja existente!")
                return
            _passwords.append(dialog.result)
            _save_passwords()
            self._refresh_list()

    def _on_view(self):
        idx = self._selected()
        if idx is not None:
            PasswordDialog(self, "visualizar", data=_passwords[idx], readonly=True)

    def _on_modify(self):
        idx = self._selected()
        if idx is None:
            return
        dialog = PasswordDialog(self, "editar", data=_passwords[idx], allow_delete=True)
        if dialog.deleted:
            del _passwords[idx]
            _save_passwords()
            self._refresh_list()
        elif dialog.result:
            _passwords[idx] = dialog.result
            _save_passwords()
            self._refresh_list()

    def _on_import(self):
        count = _import_from_csv()
        if count > 0:
            self._refresh_list()
            messagebox.showinfo("Importar", f"{count} senhas importadas!")


if __name__ == "__main__":
    LoginWindow()
