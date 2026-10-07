"""Praktikum Pengolahan Citra dan Visi Komputer (PCV)
Tugas 2: Transformasi Intensitas dan Ekualisasi Histogram
Berkas: 2-ti-eq.py
Catatan: Algoritma diimplementasikan manual secara from-scratch tanpa
menggunakan fungsi bawaan paket pengolahan citra (cv2.equalizeHist, cv2.LUT, dll.).
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def manual_rgb_to_grayscale(img_bgr):
    """Konversi BGR ke Grayscale menggunakan formulasi bobot luminansi standar:
    Gray = 0.299*R + 0.587*G + 0.114*B
    """
    b = img_bgr[:, :, 0].astype(np.float32)
    g = img_bgr[:, :, 1].astype(np.float32)
    r = img_bgr[:, :, 2].astype(np.float32)
    gray = 0.114 * b + 0.587 * g + 0.299 * r
    return np.round(gray).astype(np.uint8)


def manual_image_negative(img_gray):
    """1. Citra Negatif: s = (L - 1) - r = 255 - r."""
    return (255 - img_gray).astype(np.uint8)


def manual_log_transform(img_gray):
    """2. Transformasi Logaritmik: s = c * log(1 + r)
    dengan c = 255 / log(1 + max(r)).
    """
    r_max = float(np.max(img_gray))
    if r_max == 0:
        return img_gray.copy()

    c = 255.0 / np.log(1.0 + r_max)
    log_val = c * np.log(1.0 + img_gray.astype(np.float32))
    return np.clip(np.round(log_val), 0, 255).astype(np.uint8)


def manual_gamma_transform(img_gray, gamma=1.0):
    """3. Transformasi Pangkat / Gamma: s = 255 * (r / 255) ^ gamma."""
    r_norm = img_gray.astype(np.float32) / 255.0
    s = 255.0 * (r_norm ** gamma)
    return np.clip(np.round(s), 0, 255).astype(np.uint8)


def manual_contrast_stretching(img_gray):
    """4. Peregangan Kontras: memetakan rentang [r_min, r_max] ke [0, 255]:
    s = ((r - r_min) / (r_max - r_min)) * 255
    """
    r_min = float(np.min(img_gray))
    r_max = float(np.max(img_gray))
    if r_max == r_min:
        return img_gray.copy()

    s = ((img_gray.astype(np.float32) - r_min) / (r_max - r_min)) * 255.0
    return np.clip(np.round(s), 0, 255).astype(np.uint8)


def manual_thresholding(img_gray, threshold=128):
    """5. Pengambangan Biner: s = 255 jika r >= T, selain itu 0."""
    return np.where(img_gray >= threshold, 255, 0).astype(np.uint8)


def manual_compute_histogram(img_gray):
    """Menghitung frekuensi kemunculan intensitas piksel 0..255 tanpa cv2.calcHist."""
    return np.bincount(img_gray.ravel(), minlength=256)


def manual_histogram_equalization(img_gray):
    """Ekualisasi histogram manual berbasis fungsi distribusi kumulatif (CDF):
    1. Frekuensi kemunculan n_k untuk k = 0..255.
    2. CDF: cdf(k) = sum(n_j) / (M * N).
    3. Pemetaan baru: s_k = round(cdf(k) * 255).
    4. Penggantian nilai piksel sesuai tabel pemetaan.
    """
    total_pixels = img_gray.size
    hist = manual_compute_histogram(img_gray)

    # Perhitungan CDF manual
    cdf = np.cumsum(hist).astype(np.float64) / total_pixels

    # Look-up table pemetaan intensitas
    mapping = np.clip(np.round(cdf * 255.0), 0, 255).astype(np.uint8)

    # Petakan setiap nilai piksel citra ke nilai baru
    img_equalized = mapping[img_gray]
    hist_equalized = manual_compute_histogram(img_equalized)

    return img_equalized, hist, hist_equalized, cdf


def buat_citra_kontras_rendah(filename=None):
    """Membuat citra sintetis berkontras sempit jika berkas uji belum ada."""
    if filename is None:
        filename = os.path.join(BASE_DIR, "low_contrast_sample.jpg")
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        return filename

    x = np.linspace(70, 140, 300, dtype=np.uint8)
    y = np.linspace(70, 140, 300, dtype=np.uint8)
    xx, yy = np.meshgrid(x, y)
    base = ((xx.astype(np.float32) + yy.astype(np.float32)) / 2.0).astype(np.uint8)

    cv2.circle(base, (150, 150), 70, 110, -1)
    cv2.rectangle(base, (60, 60), (120, 120), 85, -1)
    cv2.rectangle(base, (180, 180), (240, 240), 130, -1)

    cv2.imwrite(filename, base)
    return filename


def main():
    print("PRAKTIKUM PCV - TUGAS 2: TRANSFORMASI INTENSITAS & EKUALISASI HISTOGRAM")

    input_file = os.path.join(BASE_DIR, "low_contrast_sample.jpg")
    if not os.path.exists(input_file):
        buat_citra_kontras_rendah(input_file)

    bgr_img = cv2.imread(input_file)
    if bgr_img is None:
        bgr_img = np.full((250, 250, 3), 100, dtype=np.uint8)

    gray_img = manual_rgb_to_grayscale(bgr_img)
    print(f"[INFO] Resolusi citra: {gray_img.shape[1]}x{gray_img.shape[0]} piksel")
    print(f"[INFO] Rentang intensitas awal: Min={np.min(gray_img)}, Max={np.max(gray_img)}")

    # Eksekusi Transformasi Intensitas
    img_negative = manual_image_negative(gray_img)
    img_log = manual_log_transform(gray_img)
    img_gamma_dark = manual_gamma_transform(gray_img, gamma=0.5)
    img_gamma_bright = manual_gamma_transform(gray_img, gamma=2.0)
    img_stretched = manual_contrast_stretching(gray_img)

    # Eksekusi Ekualisasi Histogram
    img_eq, hist_orig, hist_eq, _ = manual_histogram_equalization(gray_img)
    print(f"[INFO] Rentang intensitas setelah ekualisasi: Min={np.min(img_eq)}, Max={np.max(img_eq)}")

    # Visualisasi Transformasi Intensitas
    plt.figure(figsize=(14, 8))
    plt.suptitle("Transformasi Intensitas Spasial (Implementasi Manual)", fontsize=13, fontweight='bold')

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
    print(f"[INFO] Hasil transformasi disimpan ke: '{output_ti_plot}'")

    # Visualisasi Ekualisasi Histogram
    plt.figure(figsize=(12, 8))
    plt.suptitle("Ekualisasi Histogram Manual (From Scratch)", fontsize=13, fontweight='bold')

    plt.subplot(2, 2, 1)
    plt.imshow(gray_img, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Sebelum Ekualisasi\n(Rentang: {np.min(gray_img)} - {np.max(gray_img)})")
    plt.axis('off')

    plt.subplot(2, 2, 2)
    plt.bar(range(256), hist_orig, color='gray', width=1.0)
    plt.title("Histogram Sebelum Ekualisasi")
    plt.xlabel("Intensitas Piksel (0-255)")
    plt.ylabel("Frekuensi")
    plt.xlim([0, 255])

    plt.subplot(2, 2, 3)
    plt.imshow(img_eq, cmap='gray', vmin=0, vmax=255)
    plt.title(f"Setelah Ekualisasi Manual\n(Rentang: {np.min(img_eq)} - {np.max(img_eq)})")
    plt.axis('off')

    plt.subplot(2, 2, 4)
    plt.bar(range(256), hist_eq, color='steelblue', width=1.0)
    plt.title("Histogram Setelah Ekualisasi")
    plt.xlabel("Intensitas Piksel (0-255)")
    plt.ylabel("Frekuensi")
    plt.xlim([0, 255])

    plt.tight_layout()
    output_eq_plot = os.path.join(BASE_DIR, "hasil_ekualisasi_histogram.png")
    plt.savefig(output_eq_plot, dpi=150)
    print(f"[INFO] Hasil ekualisasi disimpan ke: '{output_eq_plot}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("[SELESAI] Eksekusi 2-ti-eq.py selesai.")


if __name__ == "__main__":
    main()
