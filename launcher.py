#!/usr/bin/env python3.12
"""
Lanzador de escritorio — Procesador de Licitaciones Hologic Iberia
Doble clic en el icono del escritorio para abrir esta ventana.
"""
import subprocess
import sys
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, scrolledtext

PROJECT_DIR = Path(__file__).parent
PYTHON = sys.executable  # python3.12 (el que tiene tkinter + deps)

# ── Colores corporativos Hologic ──────────────────────────────────────────────
BG = "#FFFFFF"
ACCENT = "#003087"      # azul Hologic
ACCENT_LIGHT = "#E8EFF8"
BTN_GREEN = "#00703C"
BTN_GREEN_HOVER = "#005C2F"
TEXT_DARK = "#1A1A1A"
TEXT_MUTED = "#666666"
RED = "#C00000"


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Licitaciones Hologic Iberia")
        self.configure(bg=BG)
        self.resizable(False, False)
        self.geometry("620x560")
        self._center()
        self._folder = tk.StringVar(value="")
        self._running = False
        self._build_ui()

    def _center(self):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw - 620) // 2
        y = (sh - 560) // 2
        self.geometry(f"620x560+{x}+{y}")

    # ── UI ────────────────────────────────────────────────────────────────────

    def _build_ui(self):
        # Header
        header = tk.Frame(self, bg=ACCENT, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="HOLOGIC IBERIA  ·  Procesador de Licitaciones",
                 bg=ACCENT, fg="white",
                 font=("Helvetica", 14, "bold")).pack(expand=True)

        # Body
        body = tk.Frame(self, bg=BG, padx=28, pady=18)
        body.pack(fill="both", expand=True)

        # Step 1 — select folder
        tk.Label(body, text="1. Selecciona la carpeta con los documentos del concurso",
                 bg=BG, fg=TEXT_DARK, font=("Helvetica", 11, "bold"),
                 anchor="w").pack(fill="x", pady=(0, 6))

        row1 = tk.Frame(body, bg=BG)
        row1.pack(fill="x")

        self._folder_entry = tk.Entry(row1, textvariable=self._folder, width=46,
                                       font=("Helvetica", 10), fg=TEXT_DARK,
                                       relief="solid", bd=1)
        self._folder_entry.pack(side="left", ipady=5, padx=(0, 8))

        tk.Button(row1, text="Examinar…", command=self._browse,
                  bg=ACCENT_LIGHT, fg=ACCENT, font=("Helvetica", 10, "bold"),
                  relief="flat", cursor="hand2", padx=10, pady=5
                  ).pack(side="left")

        # Step 2 — launch
        tk.Label(body, text="2. Inicia el análisis automático",
                 bg=BG, fg=TEXT_DARK, font=("Helvetica", 11, "bold"),
                 anchor="w").pack(fill="x", pady=(18, 6))

        self._btn = tk.Button(
            body,
            text="▶  INICIAR ANÁLISIS",
            command=self._start,
            bg=BTN_GREEN, fg="white",
            font=("Helvetica", 13, "bold"),
            relief="flat", cursor="hand2",
            padx=20, pady=12, width=30,
        )
        self._btn.pack()
        self._btn.bind("<Enter>", lambda e: self._btn.config(bg=BTN_GREEN_HOVER))
        self._btn.bind("<Leave>", lambda e: self._btn.config(bg=BTN_GREEN))

        self._status = tk.Label(body, text="Esperando carpeta…",
                                bg=BG, fg=TEXT_MUTED,
                                font=("Helvetica", 9, "italic"))
        self._status.pack(pady=(8, 0))

        # Log area
        tk.Label(body, text="Progreso:", bg=BG, fg=TEXT_DARK,
                 font=("Helvetica", 10, "bold"), anchor="w").pack(fill="x", pady=(16, 4))

        self._log = scrolledtext.ScrolledText(
            body, height=11, font=("Courier", 9),
            bg="#F5F5F5", fg=TEXT_DARK, relief="solid", bd=1,
            state="disabled", wrap="word",
        )
        self._log.pack(fill="both", expand=True)
        self._log.tag_config("ok", foreground=BTN_GREEN)
        self._log.tag_config("err", foreground=RED)
        self._log.tag_config("info", foreground=ACCENT)

        # Footer
        footer = tk.Frame(self, bg=ACCENT_LIGHT, height=28)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(footer, text="Los resultados se enviarán a pedro.moronta@hologic.com",
                 bg=ACCENT_LIGHT, fg=TEXT_MUTED,
                 font=("Helvetica", 8)).pack(expand=True)

    # ── Actions ───────────────────────────────────────────────────────────────

    def _browse(self):
        folder = filedialog.askdirectory(title="Selecciona la carpeta de la licitación")
        if folder:
            self._folder.set(folder)
            self._status.config(text=f"Carpeta: {folder}", fg=ACCENT)

    def _log_write(self, text: str, tag: str = "") -> None:
        self._log.config(state="normal")
        self._log.insert("end", text + "\n", tag)
        self._log.see("end")
        self._log.config(state="disabled")

    def _set_running(self, running: bool) -> None:
        self._running = running
        if running:
            self._btn.config(state="disabled", text="⏳  Procesando…", bg="#888888")
            self._status.config(text="Procesando documentos… esto puede tardar varios minutos.", fg=ACCENT)
        else:
            self._btn.config(state="normal", text="▶  INICIAR ANÁLISIS", bg=BTN_GREEN)

    def _start(self):
        folder = self._folder.get().strip()
        if not folder:
            messagebox.showwarning("Sin carpeta", "Selecciona primero la carpeta con los documentos.")
            return
        if self._running:
            return

        # Clear log
        self._log.config(state="normal")
        self._log.delete("1.0", "end")
        self._log.config(state="disabled")

        self._set_running(True)
        threading.Thread(target=self._run_process, args=(folder,), daemon=True).start()

    def _run_process(self, folder: str):
        self._log_write(f"▶ Iniciando análisis de: {folder}", "info")
        self._log_write("─" * 60)

        cmd = [PYTHON, str(PROJECT_DIR / "main.py"), "--carpeta", folder]
        try:
            proc = subprocess.Popen(
                cmd,
                cwd=str(PROJECT_DIR),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
            )
            for line in proc.stdout:
                line = line.rstrip()
                if not line:
                    continue
                tag = ""
                if "ERROR" in line or "FALLIDO" in line:
                    tag = "err"
                elif "OK" in line or "completado" in line.lower():
                    tag = "ok"
                elif "PASO" in line or "INFO" in line:
                    tag = "info"
                self._log_write(line, tag)

            proc.wait()
            self._log_write("─" * 60)
            if proc.returncode == 0:
                self._log_write("✔ Proceso completado. Revisa tu correo.", "ok")
                self.after(0, lambda: self._status.config(
                    text="✔ Completado — revisa pedro.moronta@hologic.com", fg=BTN_GREEN))
                self.after(0, lambda: messagebox.showinfo(
                    "Listo",
                    "Análisis completado.\nLos resultados han sido enviados a pedro.moronta@hologic.com"
                ))
            else:
                self._log_write(f"⚠ Proceso finalizado con errores (código {proc.returncode}).", "err")
                self.after(0, lambda: self._status.config(
                    text="⚠ Finalizado con errores — revisa el log", fg=RED))

        except Exception as e:
            self._log_write(f"ERROR crítico al lanzar el proceso: {e}", "err")
            self.after(0, lambda: self._status.config(text="Error al iniciar", fg=RED))
        finally:
            self.after(0, lambda: self._set_running(False))


if __name__ == "__main__":
    app = App()
    app.mainloop()
