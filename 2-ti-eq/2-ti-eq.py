"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 2: TRANSFORMASI INTENSITAS DAN EKUALISASI HISTOGRAM
File: 2-ti-eq.py
Aturan: DILARANG MENGGUNAKAN FUNGSI BAWAAN PACKAGE 
        (seperti cv2.equalizeHist, cv2.LUT, skimage.exposure, dll.)
        Semua algoritma diimplementasikan manual secara from-scratch.
=============================================================================
"""

import os
import math
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Direktori dasar tempat berkas ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# 1. IMPLEMENTASI MANUAL TRANSFORMASI INTENSITAS (INTENSITY TRANSFORMATIONS)
# =============================================================================

def manual_rgb_to_grayscale(img_bgr):
    """
    Konversi citra BGR ke Grayscale secara manual menggunakan rumus luminansi standar:
    Gray = 0.299*R + 0.587*G + 0.114*B
    (Format OpenCV adalah BGR: B=kanal 0, G=kanal 1, R=kanal 2)
    """
    h, w = img_bgr.shape[:2]
    gray = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            b = float(img_bgr[i, j, 0])
            g = float(img_bgr[i, j, 1])
            r = float(img_bgr[i, j, 2])
            val = 0.114 * b + 0.587 * g + 0.299 * r
            gray[i, j] = int(round(val))
    return gray


def manual_image_negative(img_gray):
    """
    1. Citra Negatif (Image Negative)
       Rumus: s = (L - 1) - r = 255 - r
    """
    h, w = img_gray.shape
    negatif = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            negatif[i, j] = 255 - img_gray[i, j]
    return negatif


def manual_log_transform(img_gray):
    """
    2. Transformasi Logaritmik (Log Transformation)
       Rumus: s = c * log(1 + r)
       Konstanta c = 255 / log(1 + max(r))
    """
    h, w = img_gray.shape
    r_max = int(np.max(img_gray))
    if r_max == 0:
        return img_gray.copy()

    c = 255.0 / math.log(1.0 + r_max)
    log_img = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            r = float(img_gray[i, j])
            s = c * math.log(1.0 + r)
            log_img[i, j] = int(round(s))
    return log_img


def manual_gamma_transform(img_gray, gamma=1.0):
    """
    3. Transformasi Pangkat / Gamma (Power-Law / Gamma Transformation)
       Rumus: s = c * r^gamma
       Dengan normalisasi input [0, 255] -> [0, 1]:
       s = 255 * (r / 255) ^ gamma
       - gamma < 1: menerangkan area gelap (mengurangi kontras di area terang)
       - gamma > 1: menggelapkan citra (meningkatkan kontras di area gelap)
    """
    h, w = img_gray.shape
    gamma_img = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            r_norm = float(img_gray[i, j]) / 255.0
            s = 255.0 * (r_norm ** gamma)
            # Batasi nilai rentang 0-255 (clamping)
            gamma_img[i, j] = int(round(min(255.0, max(0.0, s))))
    return gamma_img


def manual_contrast_stretching(img_gray):
    """
    4. Peregangan Kontras (Contrast Stretching / Piecewise-Linear Transformation)
       Memetakan rentang intensitas [r_min, r_max] ke skala penuh [0, 255]:
       Rumus: s = ((r - r_min) / (r_max - r_min)) * 255
    """
    h, w = img_gray.shape
    r_min = float(np.min(img_gray))
    r_max = float(np.max(img_gray))

    stretched = np.zeros((h, w), dtype=np.uint8)
    if r_max == r_min:
        return img_gray.copy()

    for i in range(h):
        for j in range(w):
            r = float(img_gray[i, j])
            s = ((r - r_min) / (r_max - r_min)) * 255.0
            stretched[i, j] = int(round(s))
    return stretched


def manual_thresholding(img_gray, T=128):
    """
    5. Pengambangan Biner (Binary Thresholding)
       Rumus: s = 255 jika r >= T, selain itu s = 0
    """
    h, w = img_gray.shape
    thresh = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            if img_gray[i, j] >= T:
                thresh[i, j] = 255
            else:
                thresh[i, j] = 0
    return thresh


# =============================================================================
# 2. IMPLEMENTASI MANUAL EKUALISASI HISTOGRAM (HISTOGRAM EQUALIZATION)
# =============================================================================

def manual_compute_histogram(img_gray):
    """
    Menghitung histogram (frekuensi kemunculan pixel 0-255) secara manual murni
    tanpa menggunakan cv2.calcHist ataupun np.histogram.
    """
    hist = [0] * 256
    h, w = img_gray.shape
    for i in range(h):
        for j in range(w):
            val = int(img_gray[i, j])
            hist[val] += 1
    return hist


def manual_histogram_equalization(img_gray):
    """
    Melakukan Ekualisasi Histogram secara manual murni:
    1. Hitung frekuensi kemunculan n_k untuk setiap tingkat keabuan k = 0..255
    2. Hitung fungsi probabilitas kemunculan (PDF): p(r_k) = n_k / (M * N)
    3. Hitung Cumulative Distribution Function (CDF): cdf(k) = sum_{j=0}^k p(r_j)
    4. Hitung nilai pemetaan baru: s_k = round(cdf(k) * 255)
    5. Petakan setiap pixel citra ke nilai baru s_k
    """
    h, w = img_gray.shape
    total_pixels = h * w

    # 1. Hitung histogram frekuensi
    hist = manual_compute_histogram(img_gray)

    # 2 & 3. Hitung CDF (Cumulative Distribution Function)
    cdf = [0.0] * 256
    cumulative_sum = 0
    for k in range(256):
        cumulative_sum += hist[k]
        cdf[k] = cumulative_sum / total_pixels

    # 4. Buat tabel pemetaan intensitas baru (Look-Up Table manual)
    mapping = [0] * 256
    for k in range(256):
        mapping[k] = int(round(cdf[k] * 255.0))

    # 5. Terapkan pemetaan ke setiap pixel citra
    img_equalized = np.zeros((h, w), dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            original_val = img_gray[i, j]
            img_equalized[i, j] = mapping[original_val]

    # Hitung juga histogram citra hasil ekualisasi
    hist_equalized = manual_compute_histogram(img_equalized)

    return img_equalized, hist, hist_equalized, cdf


# =============================================================================
# FUNGSI UNTUK MEMBUAT SAMPEL CITRA DENGAN KONTRAS RENDAH (LOW CONTRAST)
# =============================================================================
def buat_citra_kontras_rendah(filename=None):
    """
    Membuat citra dengan rentang kontras rendah/sempit agar efek
    ekualisasi histogram dan contrast stretching terlihat sangat dramatis dan jelas.
    """
    if filename is None:
        filename = os.path.join(BASE_DIR, "low_contrast_sample.jpg")
    if os.path.exists(filename):
        return filename

    # Buat gradien dengan rentang terbatas (misal hanya 70 sampai 140 dari 0-255)
    x = np.linspace(70, 140, 300, dtype=np.uint8)
    y = np.linspace(70, 140, 300, dtype=np.uint8)
    xx, yy = np.meshgrid(x, y)
    base = ((xx.astype(np.float32) + yy.astype(np.float32)) / 2.0).astype(np.uint8)

    # Tambahkan pola lingkaran dan persegi di dalamnya
    cv2.circle(base, (150, 150), 70, 110, -1)
    cv2.rectangle(base, (60, 60), (120, 120), 85, -1)
    cv2.rectangle(base, (180, 180), (240, 240), 130, -1)

    cv2.imwrite(filename, base)
    return filename


# =============================================================================
# MAIN RUNNER & VISUALISASI
# =============================================================================
def main():
    print("=" * 70)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 2: TI & EKUALISASI HISTOGRAM")
    print(" (Seluruh algoritma menggunakan implementasi manual tanpa fungsi bawaan)")
    print("=" * 70)

    # 1. Siapkan citra input
    input_file = os.path.join(BASE_DIR, "low_contrast_sample.jpg")
    buat_citra_kontras_rendah(input_file)

    # Baca citra menggunakan cv2.imread lalu ubah ke grayscale secara manual
    bgr_img = cv2.imread(input_file)
    if bgr_img is None:
        # Fallback jika file gagal dibaca
        bgr_img = np.full((250, 250, 3), 100, dtype=np.uint8)

    print("[INFO] Mengonversi citra BGR ke Grayscale dengan rumus manual...")
    gray_img = manual_rgb_to_grayscale(bgr_img)
    print(f"[INFO] Citra berhasil dimuat: Dimensi {gray_img.shape[1]}x{gray_img.shape[0]}")
    print(f"[INFO] Rentang intensitas awal: Min={np.min(gray_img)}, Max={np.max(gray_img)}")

    # 2. Eksekusi Transformasi Intensitas Manual
    print("\n--- [1] MENJALANKAN TRANSFORMASI INTENSITAS MANUAL ---")
    img_negative = manual_image_negative(gray_img)
    print("  -> Selesai: Image Negative")

    img_log = manual_log_transform(gray_img)
    print("  -> Selesai: Log Transformation")

    img_gamma_dark = manual_gamma_transform(gray_img, gamma=0.5)  # Menerangkan
    img_gamma_bright = manual_gamma_transform(gray_img, gamma=2.0) # Menggelapkan
    print("  -> Selesai: Gamma Transformation (gamma=0.5 dan gamma=2.0)")

    img_stretched = manual_contrast_stretching(gray_img)
    print("  -> Selesai: Contrast Stretching")

    img_thresh = manual_thresholding(gray_img, T=110)
    print("  -> Selesai: Thresholding (T=110)")

    # 3. Eksekusi Ekualisasi Histogram Manual
    print("\n--- [2] MENJALANKAN EKUALISASI HISTOGRAM MANUAL ---")
    img_eq, hist_orig, hist_eq, cdf = manual_histogram_equalization(gray_img)
    print("  -> Selesai: Perhitungan Histogram, CDF, dan Equalization Manual")
    print(f"[INFO] Rentang intensitas sesudah Equalization: Min={np.min(img_eq)}, Max={np.max(img_eq)}")

    # 4. Visualisasi Transformasi Intensitas
    print("\n[INFO] Menyiapkan visualisasi hasil Transformasi Intensitas...")
    plt.figure(figsize=(14, 8))
    plt.suptitle("Penerapan Transformasi Intensitas (Manual Implementation)", fontsize=14, fontweight='bold')

    titles_ti = [
        "1. Citra Grayscale Asli",
        "2. Image Negative",
        "3. Log Transformation",
        "4. Gamma (0.5 - Terang)",
        "5. Gamma (2.0 - Gelap)",
        "6. Contrast Stretching"
    ]
    images_ti = [gray_img, img_negative, img_log, img_gamma_dark, img_gamma_bright, img_stretched]

    for idx in range(6):
        plt.subplot(2, 3, idx + 1)
        plt.imshow(images_ti[idx], cmap='gray', vmin=0, vmax=255)
        plt.title(titles_ti[idx], fontsize=10)
        plt.axis('off')

    plt.tight_layout()
    output_ti_plot = os.path.join(BASE_DIR, "hasil_transformasi_intensitas.png")
    plt.savefig(output_ti_plot, dpi=150)
    print(f"[INFO] Grafik transformasi intensitas disimpan ke '{output_ti_plot}'")

    # 5. Visualisasi Ekualisasi Histogram (Perbandingan Citra & Histogram)
    print("[INFO] Menyiapkan visualisasi hasil Ekualisasi Histogram...")
    plt.figure(figsize=(12, 8))
    plt.suptitle("Penerapan Ekualisasi Histogram Manual (From Scratch)", fontsize=14, fontweight='bold')

    # Subplot 1: Citra Asli
    plt.subplot(2, 2, 1)
    plt.imshow(gray_img, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Citra Sebelum Ekualisasi\n(Rentang: {np.min(gray_img)} - {np.max(gray_img)})")
    plt.axis('off')

    # Subplot 2: Histogram Citra Asli
    plt.subplot(2, 2, 2)
    plt.bar(range(256), hist_orig, color='gray', width=1.0)
    plt.title("Histogram Citra Asli (Distribusi Menumpuk)")
    plt.xlabel("Tingkat Intensitas Pixel (0-255)")
    plt.ylabel("Frekuensi")
    plt.xlim([0, 255])

    # Subplot 3: Citra Setelah Ekualisasi
    plt.subplot(2, 2, 3)
    plt.imshow(img_eq, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Citra Setelah Ekualisasi Manual\n(Rentang: {np.min(img_eq)} - {np.max(img_eq)})")
    plt.axis('off')

    # Subplot 4: Histogram Citra Setelah Ekualisasi
    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_eq, color='steelblue', width=1.0)
    plt.title("Histogram Setelah Ekualisasi (Distribusi Merata)")
    plt.xlabel("Tingkat Intensitas Pixel (0-255)")
    plt.ylabel("Frekuensi")
    plt.xlim([0, 255])

    plt.tight_layout()
    output_eq_plot = os.path.join(BASE_DIR, "hasil_ekualisasi_histogram.png")
    plt.savefig(output_eq_plot, dpi=150)
    print(f"[INFO] Grafik ekualisasi histogram disimpan ke '{output_eq_plot}'")

    # Tampilkan jendela GUI jika tidak dalam mode non-interaktif
    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("\n[SELESAI] Eksekusi 2-ti-eq.py selesai dengan sempurna!")


if __name__ == "__main__":
    main()
