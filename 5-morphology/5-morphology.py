"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 5: OPERASI MORFOLOGI CITRA (EROSI, DILASI, OPENING, CLOSING)
File: 5-morphology.py
Deskripsi:
  Penerapan operasi morfologi matematika pada pengolahan citra biner:
  1. Erosi   (Erosion)  : Mengikis tepi objek & mengeliminasi bintik kecil
  2. Dilasi  (Dilation) : Memperbesar objek & mengisi celah/lubang
  3. Opening (Buka)     : Erosi lalu Dilasi (membersihkan noise luar)
  4. Closing (Tutup)    : Dilasi lalu Erosi (menutup rongga/lubang dalam)
  5. Morphological Gradient : Dilasi - Erosi (deteksi kontur/tepi morfologi)
  6. Evaluasi Structuring Elements (Rectangular, Cross, Ellipse)
=============================================================================
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Direktori dasar tempat berkas ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# =============================================================================
# HELPER: PEMBUATAN CITRA BINER SAMPEL BER-NOISE UNTUK UJI MORFOLOGI
# =============================================================================
def buat_citra_sampel_morfologi(filepath):
    """
    Membuat citra biner sintetis yang memiliki objek geometris, teks,
    serta diberi derau bintik putih di luar (salt) dan lubang hitam di dalam (pepper)
    agar efektivitas Erosi, Dilasi, Opening, dan Closing terlihat sangat jelas.
    """
    if os.path.exists(filepath):
        return filepath

    print(f"[INFO] Membuat citra sampel morfologi otomatis: '{filepath}'...")
    h, w = 360, 480
    img = np.zeros((h, w), dtype=np.uint8)

    # 1. Gambar objek utama putih (Foreground = 255)
    cv2.rectangle(img, (50, 60), (170, 180), 255, -1)     # Kotak
    cv2.circle(img, (340, 120), 65, 255, -1)              # Lingkaran
    cv2.putText(img, "PCV", (140, 290), cv2.FONT_HERSHEY_SIMPLEX, 3.2, 255, 12)  # Teks tebal

    # 2. Tambahkan noise bintik putih kecil di luar objek (Noise Luar)
    np.random.seed(42)
    num_salt = 400
    for _ in range(num_salt):
        y = np.random.randint(0, h)
        x = np.random.randint(0, w)
        if img[y, x] == 0:
            img[y, x] = 255

    # 3. Tambahkan lubang-lubang hitam kecil di dalam objek (Noise Dalam / Rongga)
    num_pepper = 250
    for _ in range(num_pepper):
        y = np.random.randint(0, h)
        x = np.random.randint(0, w)
        if img[y, x] == 255:
            # Buat titik lubang berukuran 1-2 piksel
            img[max(0, y - 1):min(h, y + 2), max(0, x - 1):min(w, x + 2)] = 0

    cv2.imwrite(filepath, img)
    return filepath


# =============================================================================
# 1. STRUCTURING ELEMENTS (KERNEL MORFOLOGI)
# =============================================================================

def buat_structuring_element(bentuk="rect", ksize=3):
    """
    Membuat elemen penstruktur (Structuring Element):
    - 'rect'  : Persegi penuh
    - 'cross' : Berbentuk tanda plus (+)
    - 'ellipse': Berbentuk elips / lingkaran
    """
    if bentuk == "rect":
        return cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    elif bentuk == "cross":
        return cv2.getStructuringElement(cv2.MORPH_CROSS, (ksize, ksize))
    elif bentuk == "ellipse":
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    else:
        return np.ones((ksize, ksize), dtype=np.uint8)


# =============================================================================
# 2. OPERASI MORFOLOGI DASAR
# =============================================================================

def operasi_erosi(citra_biner, kernel, iterasi=1):
    """
    Erosi (Erosion): Mengikis tepian objek putih.
    Formula: A (-) B
    Piksel bernilai 255 hanya jika seluruh elemen kernel mencakup area putih.
    """
    return cv2.erode(citra_biner, kernel, iterations=iterasi)


def operasi_dilasi(citra_biner, kernel, iterasi=1):
    """
    Dilasi (Dilation): Memperbesar objek putih dan mengisi celah sempit.
    Formula: A (+) B
    Piksel bernilai 255 jika ada minimal satu elemen kernel menyentuh area putih.
    """
    return cv2.dilate(citra_biner, kernel, iterations=iterasi)


def operasi_opening(citra_biner, kernel):
    """
    Opening (Pembukaan): Erosi diikuti oleh Dilasi.
    Formula: A o B = (A (-) B) (+) B
    Efek: Menghilangkan noise/bintik kecil di luar objek tanpa mengecilkan ukuran objek.
    """
    tererosi = operasi_erosi(citra_biner, kernel)
    terbuka = operasi_dilasi(tererosi, kernel)
    return terbuka


def operasi_closing(citra_biner, kernel):
    """
    Closing (Penutupan): Dilasi diikuti oleh Erosi.
    Formula: A * B = (A (+) B) (-) B
    Efek: Menutup lubang/rongga hitam di dalam objek dan menyambungkan celah tipis.
    """
    terdilasi = operasi_dilasi(citra_biner, kernel)
    tertutup = operasi_erosi(terdilasi, kernel)
    return tertutup


def operasi_gradient(citra_biner, kernel):
    """
    Morphological Gradient: Dilasi dikurangi Erosi.
    Formula: Gradient(A) = (A (+) B) - (A (-) B)
    Efek: Menghasilkan batas tepi luar dan dalam (outline) dari objek.
    """
    dilasi = operasi_dilasi(citra_biner, kernel)
    erosi = operasi_erosi(citra_biner, kernel)
    return cv2.subtract(dilasi, erosi)


# =============================================================================
# MAIN RUNNER & VISUALISASI LENGKAP
# =============================================================================

def main():
    print("=" * 70)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 5: MORFOLOGI CITRA")
    print(" (Erosi, Dilasi, Opening, Closing, dan Structuring Elements)")
    print("=" * 70)

    # 1. Siapkan citra input
    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        buat_citra_sampel_morfologi(sample_path)

    img_input = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
    if img_input is None:
        buat_citra_sampel_morfologi(sample_path)
        img_input = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)

    # Pastikan citra dalam format biner murni (0 atau 255)
    _, binary_img = cv2.threshold(img_input, 127, 255, cv2.THRESH_BINARY)
    print(f"[INFO] Citra biner berhasil dimuat: Resolusi {binary_img.shape[1]}x{binary_img.shape[0]} piksel")

    # 2. Siapkan berbagai kernel penstruktur
    kernel_rect_3x3 = buat_structuring_element("rect", 3)
    kernel_rect_5x5 = buat_structuring_element("rect", 5)
    kernel_cross_5x5 = buat_structuring_element("cross", 5)
    kernel_ellipse_5x5 = buat_structuring_element("ellipse", 5)

    # 3. Eksekusi Operasi Morfologi
    print("\n--- [1] MENJALANKAN OPERASI EROSI & DILASI ---")
    erosi_3x3 = operasi_erosi(binary_img, kernel_rect_3x3)
    erosi_5x5 = operasi_erosi(binary_img, kernel_rect_5x5)
    dilasi_3x3 = operasi_dilasi(binary_img, kernel_rect_3x3)
    dilasi_5x5 = operasi_dilasi(binary_img, kernel_rect_5x5)
    print("  -> Erosi 3x3, Erosi 5x5, Dilasi 3x3, Dilasi 5x5 selesai.")

    print("\n--- [2] MENJALANKAN OPERASI OPENING & CLOSING ---")
    opening_3x3 = operasi_opening(binary_img, kernel_rect_3x3)
    closing_3x3 = operasi_closing(binary_img, kernel_rect_3x3)
    # Kombinasi (Opening lalu Closing untuk pembersihan total luar-dalam)
    bersih_total = operasi_closing(opening_3x3, kernel_rect_3x3)
    print("  -> Opening (Hapus bintik luar) & Closing (Tutup rongga dalam) selesai.")

    print("\n--- [3] MENJALANKAN MORPHOLOGICAL GRADIENT ---")
    gradien_morfologi = operasi_gradient(binary_img, kernel_rect_3x3)
    print("  -> Morphological Gradient (Deteksi kontur tepi) selesai.")

    # 4. Evaluasi Variasi Structuring Element (Perbandingan Erosi pada SE berbeda)
    erosi_cross = operasi_erosi(binary_img, kernel_cross_5x5)
    erosi_ellipse = operasi_erosi(binary_img, kernel_ellipse_5x5)

    # 5. Visualisasi Komparatif 9 Panel
    print("\n[INFO] Menyiapkan kanvas visualisasi komparatif 9 panel...")
    plt.figure(figsize=(15, 12))
    plt.suptitle("Penerapan Operasi Morfologi Citra (Erosi, Dilasi, Opening, Closing)", fontsize=15, fontweight='bold')

    panels = [
        ("1. Citra Biner Asli (Noise Bintik & Lubang)", binary_img),
        ("2. Erosi Kernel Persegi 3x3", erosi_3x3),
        ("3. Dilasi Kernel Persegi 3x3", dilasi_3x3),
        ("4. Opening (Bintik Luar Bersih Total)", opening_3x3),
        ("5. Closing (Lubang Dalam Tertutup Rapat)", closing_3x3),
        ("6. Pembersihan Sempurna (Open + Close)", bersih_total),
        ("7. Morphological Gradient (Garis Kontur Tepi)", gradien_morfologi),
        ("8. Erosi Kernel Cross 5x5", erosi_cross),
        ("9. Erosi Kernel Ellipse 5x5", erosi_ellipse)
    ]

    for idx, (title, pic) in enumerate(panels):
        plt.subplot(3, 3, idx + 1)
        plt.imshow(pic, cmap='gray', vmin=0, vmax=255)
        plt.title(title, fontsize=10, fontweight='bold' if idx in [0, 3, 4, 5] else 'normal')
        plt.axis('off')

    plt.tight_layout()
    output_plot_path = os.path.join(BASE_DIR, "hasil_morfologi.png")
    plt.savefig(output_plot_path, dpi=150)
    print(f"[INFO] Visualisasi komparatif disimpan ke '{output_plot_path}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("\n[SELESAI] Seluruh modul 5-morphology.py berhasil dieksekusi!")


if __name__ == "__main__":
    main()
