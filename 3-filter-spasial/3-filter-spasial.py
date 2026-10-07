"""Praktikum Pengolahan Citra dan Visi Komputer (PCV)
Tugas 3: Penerapan Filter Spasial (Spatial Filtering)
Berkas: 3-filter-spasial.py
Deskripsi:
  Penerapan konvolusi 2D pada ranah spasial. Operasi filter diterapkan pada
  kanal intensitas luminansi (V pada ruang warna HSV), kemudian digabungkan
  kembali dengan kanal rona (H) dan saturasi (S) asli untuk mempertahankan
  warna citra secara utuh.
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def konvolusi_2d(citra_gray, kernel):
    """Operasi konvolusi 2D spasial diskret dengan zero-padding pada batas tepi.
    Kernel dibalik 180 derajat sesuai definisi matematis konvolusi.
    """
    h_img, w_img = citra_gray.shape
    k_size = kernel.shape[0]
    pad = k_size // 2

    # Balik kernel 180 derajat (rotasi spasial untuk konvolusi sejati)
    k_rot = kernel[::-1, ::-1]

    citra_pad = np.pad(citra_gray, pad, mode='constant', constant_values=0).astype(np.float32)
    output = np.zeros((h_img, w_img), dtype=np.float32)

    for u in range(k_size):
        for v in range(k_size):
            output += citra_pad[u:u + h_img, v:v + w_img] * k_rot[u, v]

    return output


def filter_mean_gray(citra_gray, size=3):
    """Mean / Box Filter: perataan seragam dengan kernel size x size berbobot 1/(size^2)."""
    kernel = np.ones((size, size), dtype=np.float32) / float(size * size)
    hasil = konvolusi_2d(citra_gray, kernel)
    return np.clip(np.round(hasil), 0, 255).astype(np.uint8)


def filter_gaussian_gray(citra_gray):
    """Gaussian Filter 3x3: aproksimasi distribusi normal diskret."""
    kernel_gaussian = np.array([
        [1, 2, 1],
        [2, 4, 2],
        [1, 2, 1]
    ], dtype=np.float32) / 16.0

    hasil = konvolusi_2d(citra_gray, kernel_gaussian)
    return np.clip(np.round(hasil), 0, 255).astype(np.uint8)


def filter_median_gray(citra_gray, size=3):
    """Median Filter: filter non-linear pengambil nilai tengah lingkungan piksel.
    Ukuran jendela harus ganjil (size % 2 == 1).
    """
    if size % 2 == 0:
        size += 1

    h, w = citra_gray.shape
    pad = size // 2
    citra_pad = np.pad(citra_gray, pad, mode='edge')
    neighbors = [citra_pad[u:u + h, v:v + w] for u in range(size) for v in range(size)]
    stack = np.stack(neighbors, axis=-1)
    return np.median(stack, axis=-1).astype(np.uint8)


def filter_laplacian_gray(citra_gray):
    """Laplacian Sharpening: mempertegas transisi intensitas tepi dengan kernel turunan kedua."""
    kernel_sharpen = np.array([
        [ 0, -1,  0],
        [-1,  5, -1],
        [ 0, -1,  0]
    ], dtype=np.float32)

    hasil = konvolusi_2d(citra_gray, kernel_sharpen)
    return np.clip(np.round(hasil), 0, 255).astype(np.uint8)


def filter_sobel_gray(citra_gray):
    """Sobel Edge Detection: gradien arah horizontal (Gx), vertikal (Gy), dan magnitudo."""
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

    magnitude = np.sqrt(gx**2 + gy**2)
    max_val = float(np.max(magnitude))
    magnitude_norm = (magnitude / max_val) * 255.0 if max_val > 0 else magnitude

    mag_u8 = np.clip(np.round(magnitude_norm), 0, 255).astype(np.uint8)
    gx_u8 = np.clip(np.round(np.abs(gx)), 0, 255).astype(np.uint8)
    gy_u8 = np.clip(np.round(np.abs(gy)), 0, 255).astype(np.uint8)

    return mag_u8, gx_u8, gy_u8


def proses_filter_dan_kembalikan_warna(citra_bgr, func_filter, **kwargs):
    """Menerapkan filter spasial pada kanal intensitas V (HSV) lalu menyatukannya
    kembali dengan kanal rona (H) dan saturasi (S) asli untuk mempertahankan warna.
    """
    hsv = cv2.cvtColor(citra_bgr, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    v_hasil = func_filter(v, **kwargs)
    v_hasil_u8 = np.clip(v_hasil, 0, 255).astype(np.uint8)

    hsv_restorasi = cv2.merge([h, s, v_hasil_u8])
    return cv2.cvtColor(hsv_restorasi, cv2.COLOR_HSV2BGR)


def tambah_salt_and_pepper_noise_warna(citra_bgr, probabilitas=0.04):
    """Menambahkan derau impulsif bintik putih (salt) dan hitam (pepper)."""
    noisy = citra_bgr.copy()
    np.random.seed(42)
    h, w = citra_bgr.shape[:2]
    num_noise = int(probabilitas * h * w)

    y_salt = np.random.randint(0, h, num_noise // 2)
    x_salt = np.random.randint(0, w, num_noise // 2)
    noisy[y_salt, x_salt] = [255, 255, 255]

    y_pepper = np.random.randint(0, h, num_noise // 2)
    x_pepper = np.random.randint(0, w, num_noise // 2)
    noisy[y_pepper, x_pepper] = [0, 0, 0]

    return noisy


def main():
    print("PRAKTIKUM PCV - TUGAS 3: FILTER SPASIAL")

    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        img = np.ones((300, 300, 3), dtype=np.uint8) * 200
        cv2.circle(img, (150, 150), 60, (0, 0, 255), -1)
        cv2.rectangle(img, (50, 50), (120, 120), (255, 0, 0), -1)
        cv2.imwrite(sample_path, img)

    img_bgr = cv2.imread(sample_path)
    if img_bgr is None:
        img_bgr = np.ones((250, 250, 3), dtype=np.uint8) * 180

    h_orig, w_orig = img_bgr.shape[:2]
    max_dim = 450
    if max(h_orig, w_orig) > max_dim:
        skala = max_dim / float(max(h_orig, w_orig))
        img_bgr = cv2.resize(img_bgr, (int(w_orig * skala), int(h_orig * skala)))

    print(f"[INFO] Resolusi citra uji: {img_bgr.shape[1]}x{img_bgr.shape[0]} piksel")

    img_noisy = tambah_salt_and_pepper_noise_warna(img_bgr, probabilitas=0.05)

    # Eksekusi filter spasial dengan restorasi warna
    mean_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_mean_gray, size=3)
    gauss_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_gaussian_gray)
    median_color = proses_filter_dan_kembalikan_warna(img_noisy, filter_median_gray, size=3)
    laplacian_color = proses_filter_dan_kembalikan_warna(img_bgr, filter_laplacian_gray)

    # Eksekusi deteksi tepi Sobel pada kanal luminansi
    hsv_sample = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    _, _, v_gray = cv2.split(hsv_sample)
    sobel_mag, sobel_x, sobel_y = filter_sobel_gray(v_gray)

    # Visualisasi 9 panel
    plt.figure(figsize=(14, 10))
    plt.suptitle("Penerapan Filter Spasial dengan Restorasi Warna Asli", fontsize=13, fontweight='bold')

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
    print(f"[INFO] Hasil filter spasial disimpan ke: '{output_filename}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("[SELESAI] Eksekusi 3-filter-spasial.py selesai.")


if __name__ == "__main__":
    main()
