# TP 1 IHM — Generador de Video Atencional

Trabajo Práctico 1 — Interfaz Hombre-Máquina  
Docentes: Mg. Díaz, Santiago R. | BioIng. Hadad, A.

---

## Descripción

Este repositorio implementa el **mínimo viable** para producir un video breve (8–15 s)
orientado a captar la atención de usuarios con alta distractibilidad (TDAH), partiendo
de un PDF conceptual como fuente de conocimiento.

El sistema se organiza en **8 fases** que replican la arquitectura de producción
propuesta en la consigna del TP. Cada fase genera una salida intermedia en `output/`
que sirve como registro trazable del proceso.

---

## Arquitectura del pipeline

```
input/documento.pdf
        │
        ▼
┌─────────────────────────────────────────────────────┐
│  Fase 1 — Ingesta y comprensión del PDF             │
│  Herramienta: PyMuPDF  (prod: Azure Doc Intelligence)│
│  Salida: fase1_extracted_text.txt                   │
│          fase1_document_analysis.json               │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 2 — Selección del mensaje de atención         │
│  Herramienta: síntesis manual  (prod: GPT-4o)       │
│  Salida: fase2_hooks.json                           │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 3 — Traducción psicológica del mensaje        │
│  Herramienta: razonamiento puro (código)            │
│  Salida: fase3_psychological_mapping.json           │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 4 — Storyboard mínimo                         │
│  Estructura: Pulsión de muerte → Neutro → Vida      │
│  Salida: fase4_storyboard.json                      │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 5 — Referencias visuales                      │
│  Herramienta: assets locales  (prod: gpt-image-1)   │
│  Salida: fase5_visual_references.json               │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 6 — Generación del video ★ (FFmpeg real)      │
│  Herramienta: FFmpeg  (prod: Runway Gen-4 / Veo 3)  │
│  Entrada: assets/0.mp4 … assets/6.mp4               │
│  Salida: output/video_final.mp4                     │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 7 — Voz y audio                               │
│  Herramienta: manifiesto  (prod: Azure Speech TTS HD)│
│  Salida: fase7_audio_manifest.json                  │
└────────────────────────┬────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────┐
│  Fase 8 — Control de calidad                        │
│  Herramienta: criterios explícitos  (prod: OAI Evals)│
│  Salida: fase8_qa_report.json                       │
└─────────────────────────────────────────────────────┘
```

---

## Fases y modelos de IA propuestos

| Fase | Descripción | Herramienta MVP | Modelo producción |
|------|-------------|-----------------|-------------------|
| 1 | Ingesta y comprensión del PDF | PyMuPDF | Azure Document Intelligence Read |
| 2 | Selección del mensaje / hooks | Síntesis manual | GPT-4o |
| 3 | Traducción psicológica | Código puro | — |
| 4 | Storyboard mínimo | Código puro | — |
| 5 | Referencias visuales | Assets locales | gpt-image-1 / DALL-E 3 |
| 6 | Generación del video | FFmpeg | Runway Gen-4 / Vertex AI Veo 3 |
| 7 | Voz y audio | Manifiesto JSON | Azure Speech TTS HD Voices |
| 8 | Control de calidad | Criterios explícitos | OpenAI Evals + Azure AI Content Safety |

---

## Estructura del repositorio

```
generador-video-ihm/
├── main.py               ← Pipeline completo (8 fases)
├── requirements.txt
├── README.md
├── input/
│   └── documento.pdf     ← PDF conceptual de entrada
├── assets/
│   ├── 0.mp4 … 6.mp4     ← Clips generados externamente
│   ├── muerte.png        ← Referencia visual escena 1
│   ├── neutro.png        ← Referencia visual escena 2
│   └── vida.png          ← Referencia visual escena 3
├── docs/
│   ├── TP 1 IHM - TDAH.pdf
│   └── NEXIA_GCP_Reel_Factory_Arquitectura.pdf
└── output/               ← Generado automáticamente
    ├── fase1_extracted_text.txt
    ├── fase1_document_analysis.json
    ├── fase2_hooks.json
    ├── fase3_psychological_mapping.json
    ├── fase4_storyboard.json
    ├── fase5_visual_references.json
    ├── video_final.mp4
    ├── fase7_audio_manifest.json
    └── fase8_qa_report.json
```

---

## Instalación

### 1. Instalar FFmpeg (Windows)

```powershell
winget install --id Gyan.FFmpeg -e
```

### 2. Crear y activar entorno virtual

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependencias Python

```powershell
pip install -r requirements.txt
```

---

## Ejecución

```powershell
python main.py
```

El pipeline corre las 8 fases en secuencia. Al finalizar, todos los archivos
de salida están disponibles en `output/`.

---

## Prompts utilizados para generar los assets visuales

Las siguientes instrucciones se usaron para generar las imágenes de referencia
con un modelo de imagen (DALL-E 3 / Midjourney / similar):

**Escena 1 — Pulsión de muerte:**
```
Hyper-realistic close-up of a massive wave of dark, murky ocean water crashing,
but instead of foam, it's filled with thousands of crushed plastic bottles,
colorful debris, and tattered nets. Cinematic lighting, dramatic shadows, 8K.
Vertical 9:16, 1080×1920.
```

**Escena 2 — Estado neutro:**
```
Cinematic wide shot of a clean, minimalist laboratory. In the center, a single
clear glass tank filled with pure transparent water. Soft neutral lighting from
above. A scientist's hand in a white lab coat holding a small glowing organic
seed. Serene atmosphere, 8K. Vertical 9:16, 1080×1920.
```

**Escena 3 — Pulsión de vida:**
```
Inspiring close-up of a person's hands holding a vibrant green plant sprout in
a biodegradable pot made of recycled ocean plastic. Clean sunny beach in the
background. Golden hour lighting, warm tones, 8K, bokeh. Vertical 9:16, 1080×1920.
```

---

## Conceptos psicológicos aplicados

| Concepto | Dónde se aplica |
|----------|-----------------|
| Atención selectiva | Escena 1: imagen de alto impacto visual |
| Saliencia visual | Escena 1: contraste y novedad extrema |
| Carga cognitiva | Escena 2: reducción intencional de estímulos |
| Memoria de trabajo | Escena 2: pausa perceptiva |
| Recompensa inmediata | Escena 3: imagen de resolución positiva |
| Motivación | Escena 3: esperanza y renovación |
| Reducción de fricción | Formato 9:16, duración ≤ 12 s, sin texto en primera capa |
| Jerarquía visual | Progresión de 3 momentos diferenciados |

---

## Bibliografía

- NIMH. *Attention-Deficit/Hyperactivity Disorder (ADHD)*. National Institute of Mental Health.
- OpenAI. *GPT-4o documentation and evaluation guides*.
- Microsoft Learn. *Azure Document Intelligence, Azure AI Search, Azure Speech TTS HD Voices*.
- Runway Research. *Gen-4 and Gen-4.5 model documentation*.
- Google Cloud. *Vertex AI Veo 3 — Generate videos from text and images*.
- Sweller, J. (1988). *Cognitive Load During Problem Solving*. Cognitive Science.