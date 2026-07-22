"""
Bajar la transcripción de un video de YouTube y quedarse solo con el texto,
sin las marcas de tiempo. Interfaz gráfica simple con tkinter.

Uso:
    python3 transcribir_youtube.py

Se abre una ventana donde pegás el link (o ID) del video, elegís los
idiomas preferidos y el archivo donde guardar el resultado.
"""

import re
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import (
    TranscriptsDisabled,
    NoTranscriptFound,
    VideoUnavailable,
)


def obtener_id_video(url_o_id: str) -> str:
    """Extrae el ID del video desde distintas formas de URL, o lo devuelve tal cual si ya es un ID."""
    url_o_id = url_o_id.strip()
    if re.fullmatch(r"[0-9A-Za-z_-]{11}", url_o_id):
        return url_o_id

    patrones = [
        r"(?:v=|\/)([0-9A-Za-z_-]{11}).*",
        r"youtu\.be\/([0-9A-Za-z_-]{11})",
    ]
    for patron in patrones:
        match = re.search(patron, url_o_id)
        if match:
            return match.group(1)

    raise ValueError(f"No se pudo extraer el ID del video de: {url_o_id!r}")


def obtener_transcripcion_texto(url_o_id: str, idiomas) -> str:
    """Devuelve la transcripción como un solo bloque de texto, sin timestamps."""
    video_id = obtener_id_video(url_o_id)

    api = YouTubeTranscriptApi()
    transcripcion = api.fetch(video_id, languages=list(idiomas))

    texto_completo = " ".join(snippet.text for snippet in transcripcion)

    return texto_completo


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Transcriptor de YouTube")
        self.geometry("560x520")
        self.resizable(False, False)

        # --- Link del video ---
        tk.Label(self, text="Link o ID del video de YouTube:", anchor="w").pack(fill="x", padx=12, pady=(12, 2))
        self.entry_url = tk.Entry(self, width=70)
        self.entry_url.pack(fill="x", padx=12)

        # --- Idiomas preferidos ---
        tk.Label(self, text="Idiomas preferidos, en orden (separados por coma. Ej: es, en):", anchor="w").pack(fill="x", padx=12, pady=(12, 2))
        self.entry_idiomas = tk.Entry(self, width=70)
        self.entry_idiomas.insert(0, "es, en")
        self.entry_idiomas.pack(fill="x", padx=12)

        # --- Archivo de salida ---
        tk.Label(self, text="Guardar como:", anchor="w").pack(fill="x", padx=12, pady=(12, 2))
        frame_salida = tk.Frame(self)
        frame_salida.pack(fill="x", padx=12)
        self.entry_salida = tk.Entry(frame_salida, width=56)
        self.entry_salida.insert(0, "transcripcion.txt")
        self.entry_salida.pack(side="left", fill="x", expand=True)
        tk.Button(frame_salida, text="Examinar...", command=self.elegir_archivo).pack(side="left", padx=(6, 0))

        # --- Botón procesar ---
        self.btn_procesar = tk.Button(self, text="Obtener transcripción", command=self.procesar, bg="#2563eb", fg="white")
        self.btn_procesar.pack(pady=14)

        # --- Vista previa / estado ---
        tk.Label(self, text="Resultado:", anchor="w").pack(fill="x", padx=12)
        self.texto_resultado = scrolledtext.ScrolledText(self, height=16, wrap="word")
        self.texto_resultado.pack(fill="both", expand=True, padx=12, pady=(2, 12))

    def elegir_archivo(self):
        ruta = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivo de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile="transcripcion.txt",
        )
        if ruta:
            self.entry_salida.delete(0, tk.END)
            self.entry_salida.insert(0, ruta)

    def procesar(self):
        url = self.entry_url.get().strip()
        idiomas_raw = self.entry_idiomas.get().strip()
        salida = self.entry_salida.get().strip()

        if not url:
            messagebox.showwarning("Falta el link", "Pegá el link o ID del video de YouTube.")
            return
        if not salida:
            messagebox.showwarning("Falta el archivo", "Indicá dónde guardar la transcripción.")
            return

        idiomas = [i.strip() for i in idiomas_raw.split(",") if i.strip()] or ["es", "en"]

        self.btn_procesar.config(state="disabled", text="Procesando...")
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, "Buscando transcripción...\n")

        # Ejecutar en un hilo aparte para no congelar la ventana
        hilo = threading.Thread(target=self._procesar_en_hilo, args=(url, idiomas, salida))
        hilo.start()

    def _procesar_en_hilo(self, url, idiomas, salida):
        try:
            texto = obtener_transcripcion_texto(url, idiomas)
            with open(salida, "w", encoding="utf-8") as f:
                f.write(texto)
            self.after(0, self._mostrar_resultado, texto, salida)
        except (TranscriptsDisabled, NoTranscriptFound):
            self.after(0, self._mostrar_error, "Este video no tiene transcripción/subtítulos disponibles en esos idiomas.")
        except VideoUnavailable:
            self.after(0, self._mostrar_error, "El video no está disponible (privado, eliminado o link incorrecto).")
        except ValueError as e:
            self.after(0, self._mostrar_error, str(e))
        except Exception as e:
            self.after(0, self._mostrar_error, f"Error inesperado: {e}")

    def _mostrar_resultado(self, texto, salida):
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, texto)
        self.btn_procesar.config(state="normal", text="Obtener transcripción")
        messagebox.showinfo("Listo", f"Transcripción guardada en:\n{salida}")

    def _mostrar_error(self, mensaje):
        self.texto_resultado.delete("1.0", tk.END)
        self.texto_resultado.insert(tk.END, f"⚠ {mensaje}")
        self.btn_procesar.config(state="normal", text="Obtener transcripción")
        messagebox.showerror("Error", mensaje)


if __name__ == "__main__":
    app = App()
    app.mainloop()
