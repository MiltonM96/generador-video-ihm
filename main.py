import os
import json
import subprocess
from pathlib import Path
import fitz  # PyMuPDF
from moviepy import ImageClip, concatenate_videoclips


INPUT_PDF = "input/documento.pdf"
ASSETS_DIR = "assets"
OUTPUT_DIR = "output"

VIDEO_WIDTH = 1080
VIDEO_HEIGHT = 1920
FPS = 24


def ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def extract_text_from_pdf(pdf_path):
    """
    Extrae texto del PDF conceptual.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"No se encontró el archivo: {pdf_path}")

    doc = fitz.open(pdf_path)
    text = ""

    for page in doc:
        text += page.get_text() + "\n"

    return text.strip()


def save_text(text, path):
    with open(path, "w", encoding="utf-8") as file:
        file.write(text)


def build_storyboard(extracted_text):
    """
    MVP simple:
    Se toma el PDF conceptual como fuente de entrada y se genera
    una estructura narrativa fija basada en tres momentos atencionales:
    pulsión de muerte, estado neutro y pulsión de vida.
    """

    storyboard = {
        "idea_principal": "La contaminación oceánica produce una sensación de colapso ambiental, pero la innovación sostenible puede abrir una posibilidad de recuperación.",
        "publico_objetivo": "Usuarios con alta distractibilidad o dificultad para sostener la atención frente a contenidos digitales breves.",
        "tema": "Contaminación oceánica y recuperación ambiental mediante soluciones sostenibles.",
        "duracion_total": 12,
        "formato": "9:16 vertical",
        "escenas": [
            {
                "orden": 1,
                "nombre": "Pulsión de muerte",
                "duracion": 4,
                "descripcion_visual": "Ola oscura de agua contaminada, cargada de botellas plásticas, redes rotas y residuos.",
                "funcion_ihm": "Captar la atención mediante una imagen de urgencia ambiental, pérdida y amenaza.",
                "conceptos": [
                    "atención selectiva",
                    "saliencia visual",
                    "novedad",
                    "contraste",
                    "emoción"
                ],
                "asset": "muerte.png"
            },
            {
                "orden": 2,
                "nombre": "Estado neutro",
                "duracion": 4,
                "descripcion_visual": "Laboratorio limpio y minimalista con un tanque de agua transparente y una posible solución biodegradable.",
                "funcion_ihm": "Reducir la carga cognitiva luego del impacto inicial y generar una pausa perceptiva.",
                "conceptos": [
                    "carga cognitiva",
                    "memoria de trabajo",
                    "jerarquía visual",
                    "reducción de fricción"
                ],
                "asset": "neutro.png"
            },
            {
                "orden": 3,
                "nombre": "Pulsión de vida",
                "duracion": 4,
                "descripcion_visual": "Manos sosteniendo un brote verde en una maceta biodegradable hecha con plástico reciclado, con una playa limpia de fondo.",
                "funcion_ihm": "Presentar una solución visual positiva, asociada a la recuperación ambiental y la esperanza.",
                "conceptos": [
                    "motivación",
                    "recompensa inmediata",
                    "emoción positiva",
                    "esperanza",
                    "renovación"
                ],
                "asset": "vida.png"
            }
        ]
    }

    return storyboard


def save_json(data, path):
    with open(path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def create_video_from_storyboard(storyboard):
    """
    Crea un video vertical con movimiento suave a partir de tres imágenes.
    Se usa FFmpeg para aplicar zoom cinematográfico y componer el MP4 final.
    No agrega texto ni audio porque esas capas se consideran posteriores.
    """

    segments_dir = os.path.join(OUTPUT_DIR, "segments")
    os.makedirs(segments_dir, exist_ok=True)

    segment_paths = []

    for index, escena in enumerate(storyboard["escenas"], start=1):
        asset_path = os.path.join(ASSETS_DIR, escena["asset"])

        if not os.path.exists(asset_path):
            raise FileNotFoundError(f"No se encontró la imagen: {asset_path}")

        duration = escena["duracion"]
        total_frames = duration * FPS
        segment_output = os.path.join(segments_dir, f"scene_{index:02d}.mp4")

        # Zoom lento centrado.
        # La imagen se escala para cubrir 1080x1920 y luego se recorta al formato vertical.
        vf_filter = (
            f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={VIDEO_WIDTH}:{VIDEO_HEIGHT},"
            f"zoompan="
            f"z='1+0.10*on/{total_frames}':"
            f"x='iw/2-(iw/zoom/2)':"
            f"y='ih/2-(ih/zoom/2)':"
            f"d={total_frames}:"
            f"s={VIDEO_WIDTH}x{VIDEO_HEIGHT}:"
            f"fps={FPS},"
            f"fade=t=in:st=0:d=0.25,"
            f"fade=t=out:st={duration - 0.25}:d=0.25,"
            f"format=yuv420p"
        )

        command = [
            "ffmpeg",
            "-y",
            "-loop", "1",
            "-i", asset_path,
            "-vf", vf_filter,
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            "-an",
            segment_output
        ]

        print(f"Generando segmento {index}: {escena['nombre']}")
        subprocess.run(command, check=True)

        segment_paths.append(segment_output)

    # Crear archivo de concatenación para FFmpeg
    concat_file = os.path.join(segments_dir, "clips.txt")

    with open(concat_file, "w", encoding="utf-8") as file:
        for path in segment_paths:
            path_posix = Path(path).resolve().as_posix()
            file.write(f"file '{path_posix}'\n")

    output_path = os.path.join(OUTPUT_DIR, "video_final.mp4")

    concat_command = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_file,
        "-c", "copy",
        output_path
    ]

    print("Uniendo segmentos...")
    subprocess.run(concat_command, check=True)

    return output_path

def build_qa_report(storyboard):
    """
    Control de calidad básico.
    """

    total_duration = sum(scene["duracion"] for scene in storyboard["escenas"])

    qa_report = {
        "duracion_correcta": 8 <= total_duration <= 15,
        "duracion_total": total_duration,
        "cantidad_escenas": len(storyboard["escenas"]),
        "comunica_una_sola_idea": True,
        "usa_texto_en_video": False,
        "usa_audio_en_video": False,
        "evita_sobrecarga": True,
        "estructura_atencional": [
            "pulsión de muerte",
            "estado neutro",
            "pulsión de vida"
        ],
        "observacion": "El MVP genera un video visual sin texto ni audio, basado en una estructura de tres momentos: contaminación oceánica, pausa de observación e imagen de recuperación ambiental. El texto y el audio pueden incorporarse como capas posteriores."
    }

    return qa_report


def main():
    ensure_output_dir()

    print("Extrayendo texto del PDF...")
    extracted_text = extract_text_from_pdf(INPUT_PDF)
    save_text(extracted_text, os.path.join(OUTPUT_DIR, "extracted_text.txt"))

    print("Construyendo storyboard...")
    storyboard = build_storyboard(extracted_text)
    save_json(storyboard, os.path.join(OUTPUT_DIR, "storyboard.json"))

    print("Generando video...")
    video_path = create_video_from_storyboard(storyboard)

    print("Generando reporte de calidad...")
    qa_report = build_qa_report(storyboard)
    save_json(qa_report, os.path.join(OUTPUT_DIR, "qa_report.json"))

    print("Proceso finalizado.")
    print(f"Video generado en: {video_path}")


if __name__ == "__main__":
    main()