"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 3: PENERAPAN FILTER SPASIAL (SPATIAL FILTERING)
File: 3-filter-spasial.py
Deskripsi:
  Penerapan filter spasial pada ranah spasial menggunakan konsep konvolusi 2D:
  - Perhitungan filter dilakukan pada representasi intensitas hitam-putih (kanal V pada HSV).
  - Setelah kalkulasi selesai, nilai intensitas disatukan kembali dengan kanal warna asli (H dan S),
    sehingga citra keluaran tetap mempertahankan warna aslinya secara utuh (Full Color)!
  
  1. Filter Smoothing (Penghalusan / Low-Pass Filter):
     - Mean Filter (Rata-rata 3x3)
     - Gaussian Filter (Gaussian 3x3)
     - Median Filter (Non-linear filter pereduksi noise salt-and-pepper)
  2. Filter Sharpening & Deteksi Tepi (High-Pass Filter):
     - Laplacian Sharpening (Turunan kedua untuk penajaman detail)
     - Sobel Operator (Deteksi tepi arah X, Y, dan Magnitudo Gradien)
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

def konvolusi_2d(citra_hitam_putih, kernel):
    """
    Melakukan operasi konvolusi 2D antara citra 1-kanal (hitam putih) dan sebuah kernel filter.
    Menggunakan zero-padding pada tepian citra.
    """
    h_img, w_img = citra_hitam_putih.shape
    k_size = kernel.shape[0]
    pad = k_size // 2

    # Lakukan padding pada citra agar ukuran citra keluaran sama dengan masukan
    citra_pad = np.pad(citra_hitam_putih, pad, mode='constant', constant_values=0).astype(np.float32)
    output = np.zeros((h_img, w_img), dtype=np.float32)

    # Lakukan sliding window kernel secara efisien di seluruh piksel
    for u in range(k_size):
        for v in range(k_size):
            output += citra_pad[u:u + h_img, v:v + w_img] * kernel[u, v]

    return output


# =============================================================================
# 2. FILTER SMOOTHING (LOW-PASS FILTER) PADA CITRA HITAM PUTIH
# =============================================================================

def filter_mean_gray(citra_gray, size=3):
    """
    Mean / Box Filter: Mengambil rata-rata nilai intensitas tetangga.
    Kernel berukuran size x size dengan setiap bobot bernilai 1 / (size^2).
    """
    kernel = np.ones((size, size), dtype=np.float32) / (size * size)
    hasil = konvolusi_2d(citra_gray, kernel)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def filter_gaussian_gray(citra_gray):
    """
    Gaussian Filter 3x3: Menghaluskan citra dengan bobot distribusi normal.
    Piksel di pusat memiliki bobot tertinggi, menurun ke arah luar.
    """
    kernel_gaussian = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float32) / 16.0

    hasil = konvolusi_2d(citra_gray, kernel_gaussian)
    return np.clip(hasil, 0, 255).astype(np.uint8)


def filter_median_gray(citra_gray, size=3):
    """
    Median Filter: Filter non-linear yang mengurutkan semua nilai piksel
    di lingkungan sekitar dan mengambil nilai median (tengah).
    Sangat efektif dalam mereduksi noise Salt-and-Pepper tanpa mengaburkan tepi.
    """
    h, w = citra_gray.shape
    pad = size // 2
    citra_pad = np.pad(citra_gray, pad, mode='edge')
    neighbors = [citra_pad[u:u + h, v:v + w] for u in range(size) for v in range(size)]
    stack = np.stack(neighbors, axis=-1)
    return np.median(stack, axis=-1).astype(np.uint8)


# =============================================================================
# 3. FILTER SHARPENING & DETEKSI TEPI (HIGH-PASS FILTER)
# =============================================================================

def filter_laplacian_gray(citra_gray):
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


def filter_sobel_gray(citra_gray):
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
# 4. TEKNIK PEMISAHAN HITAM-PUTIH (LUMINANSI) & RESTORASI WARNA ASLI
# =============================================================================

def proses_filter_dan_kembalikan_warna(citra_bgr, func_filter, **kwargs):
    """
    Metode Ilmiah Pengolahan Citra:
    1. Konversi BGR -> HSV untuk memisahkan warna murni (Hue & Saturation)
       dari kecerahan/intensitas monokrom (Value).
    2. Ekstrak kanal V (Value), yang berwujud citra hitam-putih skalar.
    3. Lakukan kalkulasi filter spasial pada citra hitam-putih V tersebut.
    4. Gabungkan kanal V hasil kalkulasi dengan kanal warna asli (H dan S).
    5. Konversi kembali ke format BGR, sehingga hasil akhir tetap berwarna asli!
    """
    hsv = cv2.cvtColor(citra_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # Perhitungan dilakukan pada citra hitam putih (kanal V)
    v_hasil = func_filter(v, **kwargs)

    # Kembalikan ke warna aslinya
    hsv_restorasi = cv2.merge([h, s, v_hasil])
    bgr_restorasi = cv2.cvtColor(hsv_restorasi, cv2.COLOR_HSV2BGR)
    return bgr_restorasi


def tambah_salt_and_pepper_noise_warna(citra_bgr, probabilitas=0.04):
    """
    Menambahkan derau Salt-and-Pepper bintik putih dan hitam pada citra berwarna.
    """
    noisy = citra_bgr.copy()
    np.random.seed(42)
    h, w, c = citra_bgr.shape
    num_noise = int(probabilitas * h * w)

    # Titik Putih (Salt)
    y_salt = np.random.randint(0, h, num_noise // 2)
    x_salt = np.random.randint(0, w, num_noise // 2)
    noisy[y_salt, x_salt] = [255, 255, 255]

    # Titik Hitam (Pepper)
    y_pepper = np.random.randint(0, h, num_noise // 2)
    x_pepper = np.random.randint(0, w, num_noise // 2)
    noisy[y_pepper, x_pepper] = [0, 0, 0]

    return noisy


# =============================================================================
# MAIN RUNNER & VISUALISASI
# =============================================================================
def main():
    print("=" * 70)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 3: FILTER SPASIAL")
    print(" (Perhitungan pada intensitas hitam-putih, direstorasi ke warna asli)")
    print("=" * 70)

    # 1. Siapkan citra input
    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        # Buat sampel jika belum ada
        img = np.ones((300, 300, 3), dtype=np.uint8) * 200
        cv2.circle(img, (150, 150), 60, (0, 0, 255), -1)
        cv2.rectangle(img, (50, 50), (120, 120), (255, 0, 0), -1)
        cv2.imwrite(sample_path, img)

    img_bgr = cv2.imread(sample_path)
    if img_bgr is None:
        img_bgr = np.ones((250, 250, 3), dtype=np.uint8) * 180

    # Resize citra ke ukuran proporsional yang tajam dan responsif
    h_orig, w_orig = img_bgr.shape[:2]
    max_dim = 450
    if max(h_orig, w_orig) > max_dim:
        skala = max_dim / max(h_orig, w_orig)
        img_bgr = cv2.resize(img_bgr, (int(w_orig * skala), int(h_orig * skala)))

    print(f"[INFO] Citra uji: Ukuran {img_bgr.shape[1]}x{img_bgr.shape[0]} piksel (3 kanal warna)")

    # Tambahkan noise Salt & Pepper untuk pengujian filter median
    img_noisy = tambah_salt_and_pepper_noise_warna(img_bgr, probabilitas=0.05)

    # 2. Eksekusi Filter Smoothing pada Hitam-Putih lalu Kembalikan ke Warna Asli
    print("\n--- [1] MENJALANKAN FILTER SPASIAL SMOOTHING ---")
    mean_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_mean_gray, size=3)
    print("  -> Selesai: Mean Filter (Dihitung pada B&W, warna direstorasi)")

    gauss_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_gaussian_gray)
    print("  -> Selesai: Gaussian Filter (Dihitung pada B&W, warna direstorasi)")

    median_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_median_gray, size=3)
    print("  -> Selesai: Median Filter (Noise bersih total, warna asli pulih sempurna)")

    # 3. Eksekusi Filter Sharpening & Deteksi Tepi
    print("\n--- [2] MENJALANKAN FILTER SHARPENING & DETEKSI TEPI ---")
    laplacian_color = proses_filter_dan_kembalikan_warna(img_bgr, filter_laplacian_gray)
    print("  -> Selesai: Laplacian Sharpening (Detail dipertajam, warna asli terjaga)")

    # Sobel dihitung pada intensitas keabuan (V) untuk memetakan tepi objek
    hsv_sample = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    _, _, v_gray = cv2.split(hsv_sample)
    sobel_mag, sobel_x, sobel_y = filter_sobel_gray(v_gray)
    print("  -> Selesai: Sobel Edge Detection (Magnitude, Gx, Gy)")

    # 4. Visualisasi Komparatif Matplotlib (Konversi BGR -> RGB untuk warna yang akurat)
    print("\n[INFO] Menyiapkan visualisasi komparatif semua filter...")
    plt.figure(figsize=(14, 10))
    plt.suptitle("Penerapan Filter Spasial (Perhitungan pada B&W, Direstorasi ke Warna Asli)", fontsize=13, fontweight='bold')

    plots = [
        ("1. Citra Asli (Full Color)", cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB), False),
        ("2. Citra + Noise Salt & Pepper", cv2.cvtColor(img_noisy, cv2.COLOR_BGR2RGB), False),
        ("3. Mean Filter (Warna Pulih)", cv2.cvtColor(mean_color, cv2.COLOR_BGR2RGB), False),
        ("4. Gaussian Filter (Warna Pulih)", cv2.cvtColor(gauss_color, cv2.COLOR_BGR2RGB), False),
        ("5. Median Filter (Noise Bersih, Warna Pulih)", cv2.cvtColor(median_color, cv2.COLOR_BGR2RGB), False),
        ("6. Laplacian Sharpen (Warna Tajam)", cv2.cvtColor(laplacian_color, cv2.COLOR_BGR2RGB), False),
        ("7. Sobel Arah X (Gx)", sobel_x, True),
        ("8. Sobel Arah Y (Gy)", sobel_y, True),
        ("9. Sobel Magnitude (Peta Tepi)", sobel_mag, True)
    ]

    for idx, (title, pic, is_gray) in enumerate(plots):
        plt.subplot(3, 3, idx + 1)
        if is_gray:
            plt.imshow(pic, cmap='gray', vmin=0, vmax=255)
        else:
            plt.imshow(pic)
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
