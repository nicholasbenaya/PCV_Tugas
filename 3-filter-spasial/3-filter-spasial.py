"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 3: PENERAPAN FILTER SPASIAL (SPATIAL FILTERING)
File: 3-filter-spasial.py
Deskripsi:
  Penerapan filter spasial pada ranah spasial menggunakan konsep konvolusi 2D:
  1. Filter Smoothing (Penghalusan / Low-Pass Filter):
     - Mean Filter (Rata-rata 3x3 dan 5x5)
     - Gaussian Filter (Gaussian 3x3)
     - Median Filter (Non-linear filter pereduksi noise salt-and-pepper)
  2. Filter Sharpening (Penajaman & Deteksi Tepi / High-Pass Filter):
     - Laplacian Filter (Turunan kedua untuk penajaman detail)
     - Sobel Filter (Deteksi tepi arah X, Y, dan Magnitude Gradien)
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
# 1. IMPLEMENTASI OPERASI KONVOLUSI 2D (2D SPATIAL CONVOLUTION)
# =============================================================================

def konvolusi_2d(citra_gray, kernel):
    """
    Melakukan operasi konvolusi 2D antara citra grayscale dan sebuah kernel filter.
    Menggunakan zero-padding pada tepian citra.
    """
    h_img, w_img = citra_gray.shape
    k_size = kernel.shape[0]
    pad = k_size // 2

    # Lakukan padding pada citra agar ukuran citra keluaran sama dengan masukan
    citra_pad = np.pad(citra_gray, pad, mode='constant', constant_values=0).astype(np.float32)
    output = np.zeros((h_img, w_img), dtype=np.float32)

    # Lakukan sliding window kernel di seluruh pixel citra
    for i in range(h_img):
        for j in range(w_img):
            # Ambil daerah lingkungan (neighborhood) berukuran k_size x k_size
            region = citra_pad[i:i + k_size, j:j + k_size]
            # Kalikan elemen demi elemen lalu jumlahkan
            val = np.sum(region * kernel)
            output[i, j] = val

    return output


# =============================================================================
# 2. FILTER SMOOTHING (LOW-PASS FILTER)
# =============================================================================

def filter_mean(citra_gray, size=3):
    """
    Mean / Box Filter: Mengambil rata-rata nilai intensitas tetangga.
    Kernel berukuran size x size dengan setiap bobot bernilai 1 / (size^2).
    """
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    hasil = konvolusi_2d(citra_gray, kernel)
    # Kliping nilai ke rentang [0, 255] dan konversi ke uint8
    return np.clip(hasil, 0, 255).astype(np.uint8)


def filter_gaussian(citra_gray):
    """
    Gaussian Filter 3x3: Menghaluskan citra dengan bobot distribusi normal.
    Pixel di pusat memiliki bobot tertinggi, menurun ke arah luar.
    """
    kernel_gaussian = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float32) / 16.0

    hasil = konvolusi_2d(citra_gray, kernel_gaussian)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def filter_median(citra_gray, size=3):
    """
    Median Filter: Filter non-linear yang mengurutkan semua nilai pixel
    di lingkungan sekitar dan mengambil nilai median (tengah).
    Sangat efektif dalam mereduksi noise Salt-and-Pepper tanpa mengaburkan tepi.
    """
    h, w = citra_gray.shape
    pad = size // 2
    citra_pad = np.pad(citra_gray, pad, mode='edge')
    output = np.zeros((h, w), dtype=np.uint8)

    for i in range(h):
        for j in range(w):
            window = citra_pad[i:i + size, j:j + size].flatten()
            window.sort()
            median_val = window[len(window) // 2]
            output[i, j] = median_val

    return output


# =============================================================================
# 3. FILTER SHARPENING & EDGE DETECTION (HIGH-PASS FILTER)
# =============================================================================

def filter_laplacian(citra_gray):
    """
    Laplacian Sharpening Filter:
    Menggunakan operator turunan kedua untuk menonjolkan transisi intensitas cepat (tepi/detail).
    Kernel penajaman:
      [ 0, -1,  0]
      [-1,  5, -1]
      [ 0, -1,  0]
    Kernel ini langsung menghasilkan citra yang telah dipertajam (Sharpened Image).
    """
    kernel_sharpen = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    hasil = konvolusi_2d(citra_gray, kernel_sharpen)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def filter_sobel(citra_gray):
    """
    Sobel Filter (Edge Detection):
    Menghitung gradien arah horizontal (Gx) dan vertikal (Gy),
    kemudian menghitung magnitudo gradien: G = sqrt(Gx^2 + Gy^2).
    """
    kernel_gx = np.array([
        [-1, 0, 1],
        [-2, 0, 2],
        [-1, 0, 1]
    ], dtype=np.float32)

    kernel_gy = np.array([
        [-1, -2, -1],
        [ 0,  0,  0],
        [ 1,  2,  1]
    ], dtype=np.float32)

    gx = konvolusi_2d(citra_gray, kernel_gx)
    gy = konvolusi_2d(citra_gray, kernel_gy)

    # Hitung Magnitudo gradien
    magnitude = np.sqrt(gx**2 + gy**2)

    # Normalisasi magnitudo ke skala [0, 255]
    max_val = np.max(magnitude)
    if max_val > 0:
        magnitude_norm = (magnitude / max_val) * 255.0
    else:
        magnitude_norm = magnitude

    return np.clip(magnitude_norm, 0, 255).astype(np.uint8), np.clip(np.abs(gx), 0, 255).astype(np.uint8), np.clip(np.abs(gy), 0, 255).astype(np.uint8)


# =============================================================================
# HELPER: MENAMBAHKAN NOISE SALT-AND-PEPPER PADA CITRA
# =============================================================================
def tambah_salt_and_pepper_noise(citra_gray, probabilitas=0.04):
    """
    Menambahkan noise bintik putih (salt = 255) dan hitam (pepper = 0)
    untuk menguji keunggulan filter median.
    """
    noisy = citra_gray.copy()
    np.random.seed(42)  # Seed konsisten
    num_noise = int(probabilitas * citra_gray.size)

    # Titik Salt (Putih)
    coords_salt = [np.random.randint(0, i, num_noise // 2) for i in citra_gray.shape]
    noisy[tuple(coords_salt)] = 255

    # Titik Pepper (Hitam)
    coords_pepper = [np.random.randint(0, i, num_noise // 2) for i in citra_gray.shape]
    noisy[tuple(coords_pepper)] = 0

    return noisy


# =============================================================================
# MAIN RUNNER & VISUALISASI
# =============================================================================
def main():
    print("=" * 65)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 3: FILTER SPASIAL")
    print("=" * 65)

    # 1. Siapkan citra input
    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        from importlib.machinery import SourceFileLoader
        # Buat sampel jika belum ada
        img = np.ones((300, 300, 3), dtype=np.uint8) * 200
        cv2.circle(img, (150, 150), 60, (0, 0, 255), -1)
        cv2.rectangle(img, (50, 50), (120, 120), (255, 0, 0), -1)
        cv2.imwrite(sample_path, img)

    img_bgr = cv2.imread(sample_path)
    if img_bgr is None:
        img_bgr = np.ones((250, 250, 3), dtype=np.uint8) * 180

    # Konversi ke Grayscale untuk pemrosesan filter spasial
    img_gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    # Resize ke dimensi wajar agar proses konvolusi cepat dan responsif
    img_gray = cv2.resize(img_gray, (250, 250))
    print(f"[INFO] Citra uji: Ukuran {img_gray.shape[1]}x{img_gray.shape[0]} pixel")

    # Tambahkan citra bernoise untuk pengujian filter median
    img_noisy = tambah_salt_and_pepper_noise(img_gray, probabilitas=0.05)

    # 2. Eksekusi Filter Spasial Smoothing
    print("\n--- [1] MENJALANKAN FILTER SPASIAL SMOOTHING ---")
    mean_3x3 = filter_mean(img_noisy, size=3)
    print("  -> Selesai: Mean Filter 3x3")

    gaussian_3x3 = filter_gaussian(img_noisy)
    print("  -> Selesai: Gaussian Filter 3x3")

    median_3x3 = filter_median(img_noisy, size=3)
    print("  -> Selesai: Median Filter 3x3 (Efektif hapus noise salt & pepper)")

    # 3. Eksekusi Filter Spasial Sharpening & Edge Detection
    print("\n--- [2] MENJALANKAN FILTER SPASIAL SHARPENING & EDGE ---")
    laplacian_sharp = filter_laplacian(img_gray)
    print("  -> Selesai: Laplacian Sharpening")

    sobel_mag, sobel_x, sobel_y = filter_sobel(img_gray)
    print("  -> Selesai: Sobel Edge Detection (Magnitude, Gx, Gy)")

    # 4. Visualisasi Komparatif Matplotlib
    print("\n[INFO] Menyiapkan visualisasi komparatif semua filter...")
    plt.figure(figsize=(14, 10))
    plt.suptitle("Penerapan Filter Spasial (Smoothing, Sharpening & Edge Detection)", fontsize=14, fontweight='bold')

    plots = [
        ("1. Citra Asli", img_gray),
        ("2. Citra + Salt & Pepper Noise", img_noisy),
        ("3. Hasil Filter Mean 3x3", mean_3x3),
        ("4. Hasil Filter Gaussian 3x3", gaussian_3x3),
        ("5. Hasil Filter Median 3x3 (Bersih)", median_3x3),
        ("6. Laplacian Sharpening", laplacian_sharp),
        ("7. Sobel Direction X (Gx)", sobel_x),
        ("8. Sobel Direction Y (Gy)", sobel_y),
        ("9. Sobel Magnitude (Tepi Lengkap)", sobel_mag)
    ]

    for idx, (title, pic) in enumerate(plots):
        plt.subplot(3, 3, idx + 1)
        plt.imshow(pic, cmap='gray', vmin=0, vmax=255)
        plt.title(title, fontsize=10)
        plt.axis('off')

    plt.tight_layout()
    output_filename = os.path.join(BASE_DIR, "hasil_filter_spasial.png")
    plt.savefig(output_filename, dpi=150)
    print(f"[INFO] Gambar perbandingan filter berhasil disimpan ke '{output_filename}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("\n[SELESAI] Eksekusi 3-filter-spasial.py selesai dengan sempurna!")


if __name__ == "__main__":
    main()
