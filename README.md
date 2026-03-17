# 🫁 OncoScan AI — Lung Cancer Detection with VGG16

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/kilarisasikumar682-prog/Deep-Learning-project/blob/main/Lung_cancer.ipynb)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.19-orange?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-3.1-lightgrey?logo=flask)
![License](https://img.shields.io/badge/License-MIT-green)

> **A deep learning system for automated lung cancer classification from CT/pathology images, featuring Grad-CAM visualisations and AI-generated diagnostic PDF reports.**

---

## 📋 Table of Contents
- [Overview](#overview)
- [Demo](#demo)
- [Classes](#classes)
- [Model Architecture](#model-architecture)
- [Training Strategy](#training-strategy)
- [Results](#results)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Dataset](#dataset)
- [Tech Stack](#tech-stack)
- [Disclaimer](#disclaimer)

---

## Overview

**OncoScan AI** is a two-stage transfer-learning pipeline built on **VGG16** that classifies lung tissue images into four categories — three cancer subtypes and normal tissue. The system is wrapped in a **Flask** web application (tunnelled via ngrok on Colab) that accepts image uploads, returns predictions with confidence scores, overlays Grad-CAM heatmaps, and generates professional **PDF diagnostic reports**.

---

## Demo

| Upload CT Image | Grad-CAM Heatmap | PDF Report |
|:-:|:-:|:-:|
| Drag & drop via browser | Highlights tumour regions | Auto-generated per scan |

---

## Classes

| Label | Description |
|---|---|
| `adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib` | Adenocarcinoma — left lower lobe, Stage Ib |
| `large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa` | Large Cell Carcinoma — Stage IIIa |
| `normal` | Healthy lung tissue |
| `squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa` | Squamous Cell Carcinoma — Stage IIIa |

---

## Model Architecture

```
Model: "OncoScan_VGG16"
─────────────────────────────────────────────────────────
 Layer                        Output Shape    Params
─────────────────────────────────────────────────────────
 vgg16 (Functional)           (None, 512)     14,714,688
 BatchNormalization           (None, 512)      2,048
 Dense (512, ReLU)            (None, 512)    262,656
 Dropout                      (None, 512)          0
 BatchNormalization           (None, 512)      2,048
 Dense (256, ReLU)            (None, 256)    131,328
 Dropout                      (None, 256)          0
 Dense (4, Softmax)           (None, 4)        1,028
─────────────────────────────────────────────────────────
 Total params:  15,113,796 (57.65 MB)
 Trainable:        397,060  (1.51 MB)
 Non-trainable: 14,716,736 (56.14 MB)
─────────────────────────────────────────────────────────
```

---

## Training Strategy

Training is split into **two phases** for stable convergence:

### Phase 1 — Frozen Backbone (60 epochs)
- VGG16 backbone fully frozen; only the custom head is trained
- Optimizer: **Adam**, lr = `1e-3`
- Callbacks: `ModelCheckpoint`, `EarlyStopping`, `ReduceLROnPlateau`
- Mixed precision: `float16` compute / `float32` variables

### Phase 2 — Fine-tuning (40 epochs)
- **block4** and **block5** of VGG16 unfrozen
- Optimizer: **RMSprop**, lr = `1e-5`
- Same callbacks as Phase 1

**Class imbalance** is handled via computed class weights applied during both phases.

---

## Results

| Split | Images | Steps/Epoch |
|---|---|---|
| Train | 622 | 39 |
| Validation | 72 | 5 |
| Test | 315 | 20 |

The model is evaluated on the held-out test set; best checkpoint (Phase 2, by `val_loss`) is restored before evaluation.

---

## Features

- ✅ **2-phase transfer learning** with VGG16 backbone
- ✅ **Grad-CAM heatmap overlay** highlighting discriminative regions
- ✅ **Flask REST API** with file upload endpoint
- ✅ **ngrok tunnelling** for Colab-hosted public URLs
- ✅ **PDF diagnostic reports** (FPDF) with confidence bar charts
- ✅ **SQLite record store** for scan history
- ✅ **Temp-file auto-cleanup** to prevent disk bloat
- ✅ **Class-weighted training** to handle imbalanced data

---

## Project Structure

```
Deep-Learning-project/
│
├── Lung_cancer.ipynb          # Model training pipeline (Phase 1 & 2)
├── UserInterface__1_.ipynb    # Flask app + Grad-CAM + PDF reports
│
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files excluded from version control
├── LICENSE                    # MIT License
└── README.md                  # This file
```

> **Note:** Saved model files (`.keras`, `.h5`, `saved_model/`) and the dataset are stored in Google Drive and are **not** committed to this repository. See [Dataset](#dataset) for download instructions.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/kilarisasikumar682-prog/Deep-Learning-project.git
cd Deep-Learning-project
```

### 2. Create a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

### Training (Google Colab — GPU recommended)
1. Open `Lung_cancer.ipynb` in Google Colab.
2. Mount your Google Drive and set `DATA_DIR` to your dataset path.
3. Run all cells — Phase 1 then Phase 2 train automatically.
4. The best model is saved to `saved_models/vgg16_model.keras`.

### Web Interface (Google Colab)
1. Open `UserInterface__1_.ipynb` in Google Colab.
2. Set your ngrok auth token.
3. Run all cells — a public URL is printed in the output.
4. Open the URL in any browser, upload a CT image, and receive:
   - Predicted class with confidence scores
   - Grad-CAM heatmap overlay
   - Downloadable PDF diagnostic report

---

## Dataset

The dataset contains CT scan images organised into four class folders.

| Source | Link |
|---|---|
| Kaggle — Lung and Colon Cancer Histopathological Images | [kaggle.com/datasets/andrewmvd/lung-and-colon-cancer-histopathological-images](https://www.kaggle.com/datasets/andrewmvd/lung-and-colon-cancer-histopathological-images) |

After downloading, arrange as:
```
LungCancer/
  Data/
    train/
      adenocarcinoma_left.lower.lobe_T2_N0_M0_Ib/
      large.cell.carcinoma_left.hilum_T2_N2_M0_IIIa/
      normal/
      squamous.cell.carcinoma_left.hilum_T1_N2_M0_IIIa/
    valid/
    test/
```

---

## Tech Stack

| Library | Version | Purpose |
|---|---|---|
| TensorFlow / Keras | 2.19 | Model training & inference |
| Flask | 3.1 | REST API web server |
| pyngrok | 7.5 | Colab → public URL tunnel |
| OpenCV | 4.13 | Grad-CAM overlay rendering |
| Pillow | 11.3 | Image I/O |
| FPDF | 1.7 | PDF report generation |
| NumPy | 2.0 | Array operations |
| Matplotlib | — | Training curve plots |
| SQLite3 | built-in | Scan record storage |

---

## Disclaimer

> ⚠️ **This project is for educational and research purposes only.**
> The AI-generated diagnostic report is **NOT intended for clinical use**.
> Always confirm findings with a licensed pathologist or medical professional.

---

## License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.
