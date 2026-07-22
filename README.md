# Transcribir Texto YouTube

Aplicación de escritorio simple (con interfaz gráfica en tkinter) para obtener la transcripción de un video de YouTube y guardarla como texto plano, sin marcas de tiempo.

## ¿Qué hace?

1. Pegás el link (o el ID) de un video de YouTube.
2. Elegís los idiomas preferidos para la transcripción, en orden de prioridad (por ejemplo: `es, en`).
3. Elegís dónde guardar el resultado.
4. La app descarga la transcripción disponible en YouTube (subtítulos/CC) y la guarda como un archivo `.txt` con el texto completo, sin timestamps.

No descarga audio ni video, ni genera la transcripción por sí misma: usa las transcripciones/subtítulos que YouTube ya tiene disponibles para ese video.

## Requisitos

- Python 3.8 o superior
- tkinter (viene incluido con Python en la mayoría de las instalaciones; en Linux puede requerir instalarlo aparte, ver más abajo)

## Instalación

1. Cloná el repositorio:
   ```bash
   git clone https://github.com/javialvaredo/transcribir_texto_youtube.git
   cd transcribir_texto_youtube
   ```

2. Creá y activá un entorno virtual:
   ```bash
   python3 -m venv venv

   # Linux/Mac
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

3. Instalá las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

4. (Solo Linux, si tkinter no está instalado) instalá el paquete del sistema:
   ```bash
   sudo apt install python3-tk
   ```

## Uso

Con el entorno virtual activado, ejecutá:

```bash
python3 transcribir_youtube.py
```

Se abre una ventana donde:
- Pegás el link o ID del video de YouTube.
- Escribís los idiomas preferidos, separados por coma (ej: `es, en`). El programa intenta cada idioma en ese orden hasta encontrar una transcripción disponible.
- Elegís el archivo de salida (por defecto `transcripcion.txt`), con el botón "Examinar..." si querés cambiar la ubicación.
- Hacés clic en "Obtener transcripción".

El resultado se muestra en la ventana y se guarda automáticamente en el archivo elegido.

## Errores posibles

- **"Este video no tiene transcripción/subtítulos disponibles en esos idiomas"**: el video no tiene subtítulos en ninguno de los idiomas indicados. Probá agregando más idiomas a la lista.
- **"El video no está disponible"**: el link es incorrecto, o el video es privado o fue eliminado.

## Dependencias principales

- [`youtube-transcript-api`](https://pypi.org/project/youtube-transcript-api/): para obtener las transcripciones de YouTube.
- `tkinter`: interfaz gráfica (incluida en la biblioteca estándar de Python).
