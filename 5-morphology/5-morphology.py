"""Praktikum Pengolahan Citra dan Visi Komputer (PCV)
Tugas 5: Operasi Morfologi Citra (Erosi, Dilasi, Opening, Closing)
Berkas: 5-morphology.py
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def buat_citra_sampel_morfologi(filepath):
    """Membuat citra biner sintetis dengan derau bintik luar dan rongga dalam."""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return filepath

    print(f"[INFO] Membuat citra sampel morfologi: '{filepath}'")
    h, w = 360, 480
    img = np.zeros((h, w), dtype=np.uint8)

    cv2.rectangle(img, (50, 60), (170, 180), 255, -1)
    cv2.circle(img, (340, 120), 65, 255, -1)
    cv2.putText(img, "PCV", (140, 290), cv2.FONT_HERSHEY_SIMPLEX, 3.2, 255, 12)

    # Derau bintik putih di latar belakang (salt)
    np.random.seed(42)
    num_salt = 400
    for _ in range(num_salt):
        y = np.random.randint(0, h)
        x = np.random.randint(0, w)
        if img[y, x] == 0:
            img[y, x] = 255

    # Rongga hitam di dalam objek (pepper)
    num_pepper = 250
    for _ in range(num_pepper):
        y = np.random.randint(0, h)
        x = np.random.randint(0, w)
        if img[y, x] == 255:
            img[max(0, y - 1):min(h, y + 2), max(0, x - 1):min(w, x + 2)] = 0

    cv2.imwrite(filepath, img)
    return filepath


def buat_structuring_element(bentuk="rect", ksize=3):
    """Membuat elemen penstruktur (Structuring Element):
    - 'rect': persegi penuh
    - 'cross': tanda tambah (+)
    - 'ellipse': elips / lingkaran
    """
    if bentuk == "rect":
        return cv2.getStructuringElement(cv2.MORPH_RECT, (ksize, ksize))
    elif bentuk == "cross":
        return cv2.getStructuringElement(cv2.MORPH_CROSS, (ksize, ksize))
    elif bentuk == "ellipse":
        return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ksize, ksize))
    return np.ones((ksize, ksize), dtype=np.uint8)


def operasi_erosi(citra_biner, kernel, iterasi=1):
    """Erosi: mengikis batas objek biner (A (-) B)."""
    return cv2.erode(citra_biner, kernel, iterations=iterasi)


def operasi_dilasi(citra_biner, kernel, iterasi=1):
    """Dilasi: memperluas batas objek biner (A (+) B)."""
    return cv2.dilate(citra_biner, kernel, iterations=iterasi)


def operasi_opening(citra_biner, kernel):
    """Opening: erosi diikuti dilasi (A o B = (A (-) B) (+) B)."""
    tererosi = operasi_erosi(citra_biner, kernel)
    return operasi_dilasi(tererosi, kernel)


def operasi_closing(citra_biner, kernel):
    """Closing: dilasi diikuti erosi (A * B = (A (+) B) (-) B)."""
    terdilasi = operasi_dilasi(citra_biner, kernel)
    return operasi_erosi(terdilasi, kernel)


def operasi_gradient(citra_biner, kernel):
    """Morphological Gradient: selisih hasil dilasi dan erosi."""
    dilasi = operasi_dilasi(citra_biner, kernel)
    erosi = operasi_erosi(citra_biner, kernel)
    return cv2.subtract(dilasi, erosi)


def main():
    print("PRAKTIKUM PCV - TUGAS 5: MORFOLOGI CITRA")

    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        buat_citra_sampel_morfologi(sample_path)

    img_input = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)
    if img_input is None:
        buat_citra_sampel_morfologi(sample_path)
        img_input = cv2.imread(sample_path, cv2.IMREAD_GRAYSCALE)

    _, binary_img = cv2.threshold(img_input, 127, 255, cv2.THRESH_BINARY)
    print(f"[INFO] Resolusi citra biner: {binary_img.shape[1]}x{binary_img.shape[0]} piksel")

    # Siapkan kernel penstruktur
    kernel_rect_3x3 = buat_structuring_element("rect", 3)
    kernel_rect_5x5 = buat_structuring_element("rect", 5)
    kernel_cross_5x5 = buat_structuring_element("cross", 5)
    kernel_ellipse_5x5 = buat_structuring_element("ellipse", 5)

    # Eksekusi operasi morfologi
    erosi_3x3 = operasi_erosi(binary_img, kernel_rect_3x3)
    dilasi_3x3 = operasi_dilasi(binary_img, kernel_rect_3x3)
    opening_3x3 = operasi_opening(binary_img, kernel_rect_3x3)
    closing_3x3 = operasi_closing(binary_img, kernel_rect_3x3)
    bersih_total = operasi_closing(opening_3x3, kernel_rect_3x3)
    gradien_morfologi = operasi_gradient(binary_img, kernel_rect_3x3)

    # Variasi elemen penstruktur
    erosi_cross = operasi_erosi(binary_img, kernel_cross_5x5)
    erosi_ellipse = operasi_erosi(binary_img, kernel_ellipse_5x5)

    # Visualisasi 9 panel
    plt.figure(figsize=(15, 12))
    plt.suptitle("Penerapan Operasi Morfologi Citra (Erosi, Dilasi, Opening, Closing)", fontsize=14, fontweight='bold')

    panels = [
        ("1. Citra Biner Masukan (Noise Luar & Rongga)", binary_img),
        ("2. Erosi Kernel Persegi 3x3", erosi_3x3),
        ("3. Dilasi Kernel Persegi 3x3", dilasi_3x3),
        ("4. Opening (Eliminasi Derau Luar)", opening_3x3),
        ("5. Closing (Penutupan Rongga Dalam)", closing_3x3),
        ("6. Rekonstruksi Utuh (Open + Close)", bersih_total),
        ("7. Morphological Gradient (Kontur Tepi)", gradien_morfologi),
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
    print(f"[INFO] Hasil visualisasi disimpan ke: '{output_plot_path}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("[SELESAI] Eksekusi 5-morphology.py selesai.")


if __name__ == "__main__":
    main()
