"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 4: KONVERSI MODEL WARNA (RGB, CMYK, HSI, HSV)
File: 4-model-warna.py
Deskripsi:
  Implementasi konversi matematis dan dekomposisi antarmodel warna:
  1. RGB  (Red, Green, Blue) - Model Warna Aditif
  2. CMYK (Cyan, Magenta, Yellow, Key/Black) - Model Warna Subtraktif
  3. HSI  (Hue, Saturation, Intensity) - Model Persepsi Penglihatan Manusia
  4. HSV  (Hue, Saturation, Value) - Model Ruang Warna Kerucut Heksagonal
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
# HELPER: PEMBUATAN CITRA SAMPEL BERWARNA JIKA BELUM ADA
# =============================================================================
def buat_citra_sampel_warna(filepath):
    """
    Membuat citra sintetis beraneka ragam warna dengan spektrum luas
    (merah, hijau, biru, kuning, cyan, magenta, gradasi) untuk uji model warna.
    """
    if os.path.exists(filepath):
        return filepath

    print(f"[INFO] Membuat citra sampel berwarna otomatis: '{filepath}'...")
    h, w = 360, 480
    img = np.ones((h, w, 3), dtype=np.uint8) * 240

    # Kotak Merah murni
    cv2.rectangle(img, (30, 30), (130, 150), (0, 0, 255), -1)
    cv2.putText(img, "Red", (55, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Kotak Hijau murni
    cv2.rectangle(img, (150, 30), (250, 150), (0, 255, 0), -1)
    cv2.putText(img, "Green", (165, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Kotak Biru murni
    cv2.rectangle(img, (270, 30), (370, 150), (255, 0, 0), -1)
    cv2.putText(img, "Blue", (295, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # Kotak Cyan (Hijau + Biru)
    cv2.rectangle(img, (30, 180), (130, 300), (255, 255, 0), -1)
    cv2.putText(img, "Cyan", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Kotak Magenta (Merah + Biru)
    cv2.rectangle(img, (150, 180), (250, 300), (255, 0, 255), -1)
    cv2.putText(img, "Magenta", (155, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    # Kotak Kuning (Merah + Hijau)
    cv2.rectangle(img, (270, 180), (370, 300), (0, 255, 255), -1)
    cv2.putText(img, "Yellow", (280, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    # Strip gradasi abu-abu di samping kanan
    for i in range(h):
        val = int((i / h) * 255)
        img[i, 400:460] = [val, val, val]
    cv2.putText(img, "Gray", (405, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

    cv2.imwrite(filepath, img)
    return filepath


# =============================================================================
# 1. KONVERSI MODEL WARNA: RGB <-> CMYK
# =============================================================================

def rgb_to_cmyk(img_rgb):
    """
    Konversi RGB [0, 255] ke CMYK [0, 1]:
    K = 1 - max(R', G', B')
    C = (1 - R' - K) / (1 - K)
    M = (1 - G' - K) / (1 - K)
    Y = (1 - B' - K) / (1 - K)
    """
    # Normalisasi ke [0, 1]
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    # Hitung kanal K (Black/Key)
    k = 1.0 - np.maximum(np.maximum(r, g), b)

    # Hindari pembagian dengan nol saat k == 1 (hitam pekat)
    denom = 1.0 - k
    denom[denom == 0] = 1e-7

    c = (1.0 - r - k) / denom
    m = (1.0 - g - k) / denom
    y = (1.0 - b - k) / denom

    # Bila k == 1, C = M = Y = 0
    c[k == 1.0] = 0
    m[k == 1.0] = 0
    y[k == 1.0] = 0

    return np.clip(c, 0, 1), np.clip(m, 0, 1), np.clip(y, 0, 1), np.clip(k, 0, 1)


def cmyk_to_rgb(c, m, y, k):
    """
    Rekonstruksi CMYK [0, 1] kembali ke RGB [0, 255]:
    R = 255 * (1 - C) * (1 - K)
    G = 255 * (1 - M) * (1 - K)
    B = 255 * (1 - Y) * (1 - K)
    """
    r = 255.0 * (1.0 - c) * (1.0 - k)
    g = 255.0 * (1.0 - m) * (1.0 - k)
    b = 255.0 * (1.0 - y) * (1.0 - k)
    rgb = np.stack([r, g, b], axis=-1)
    return np.clip(rgb, 0, 255).astype(np.uint8)


# =============================================================================
# 2. KONVERSI MODEL WARNA: RGB <-> HSI
# =============================================================================

def rgb_to_hsi(img_rgb):
    """
    Konversi matematis RGB ke HSI (Gonzalez & Woods - Digital Image Processing):
    - I = (R + G + B) / 3
    - S = 1 - (3 / (R + G + B)) * min(R, G, B)
    - theta = arccos( 0.5 * ((R - G) + (R - B)) / sqrt((R - G)^2 + (R - B)*(G - B)) )
      H = theta jika B <= G, selain itu H = 360 - theta
    Output:
      H dalam derajat [0, 360)
      S dalam [0, 1]
      I dalam [0, 1]
    """
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    # 1. Intensitas (I)
    i = (r + g + b) / 3.0

    # 2. Saturasi (S)
    min_rgb = np.minimum(np.minimum(r, g), b)
    sum_rgb = r + g + b
    sum_rgb_safe = sum_rgb.copy()
    sum_rgb_safe[sum_rgb_safe == 0] = 1e-7

    s = 1.0 - (3.0 / sum_rgb_safe) * min_rgb
    s[sum_rgb == 0] = 0
    s = np.clip(s, 0, 1)

    # 3. Hue (H)
    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
    den_safe = den.copy()
    den_safe[den_safe == 0] = 1e-7

    arg = np.clip(num / den_safe, -1.0, 1.0)
    theta = np.arccos(arg) * (180.0 / np.pi)  # Derajat

    h = theta.copy()
    h[b > g] = 360.0 - theta[b > g]
    h[s == 0] = 0  # Warna abu-abu (tidak jenuh)

    return h, s, i


def hsi_to_rgb(h, s, i):
    """
    Rekonstruksi model warna HSI kembali ke RGB berdasarkan 3 sektor sudut:
    - Sektor RG: 0 <= H < 120
    - Sektor GB: 120 <= H < 240
    - Sektor BR: 240 <= H < 360
    """
    h_rad = h * (np.pi / 180.0)
    r = np.zeros_like(h, dtype=np.float32)
    g = np.zeros_like(h, dtype=np.float32)
    b = np.zeros_like(h, dtype=np.float32)

    # Sektor 1: 0 <= H < 120
    mask1 = (h >= 0) & (h < 120)
    b[mask1] = i[mask1] * (1.0 - s[mask1])
    denom1 = np.cos((60.0 * np.pi / 180.0) - h_rad[mask1])
    denom1[denom1 == 0] = 1e-7
    r[mask1] = i[mask1] * (1.0 + (s[mask1] * np.cos(h_rad[mask1])) / denom1)
    g[mask1] = 3.0 * i[mask1] - (r[mask1] + b[mask1])

    # Sektor 2: 120 <= H < 240
    mask2 = (h >= 120) & (h < 240)
    h_rad2 = h_rad[mask2] - (120.0 * np.pi / 180.0)
    r[mask2] = i[mask2] * (1.0 - s[mask2])
    denom2 = np.cos((60.0 * np.pi / 180.0) - h_rad2)
    denom2[denom2 == 0] = 1e-7
    g[mask2] = i[mask2] * (1.0 + (s[mask2] * np.cos(h_rad2)) / denom2)
    b[mask2] = 3.0 * i[mask2] - (r[mask2] + g[mask2])

    # Sektor 3: 240 <= H <= 360
    mask3 = (h >= 240) & (h <= 360)
    h_rad3 = h_rad[mask3] - (240.0 * np.pi / 180.0)
    g[mask3] = i[mask3] * (1.0 - s[mask3])
    denom3 = np.cos((60.0 * np.pi / 180.0) - h_rad3)
    denom3[denom3 == 0] = 1e-7
    b[mask3] = i[mask3] * (1.0 + (s[mask3] * np.cos(h_rad3)) / denom3)
    r[mask3] = 3.0 * i[mask3] - (g[mask3] + b[mask3])

    rgb = np.stack([r, g, b], axis=-1) * 255.0
    return np.clip(rgb, 0, 255).astype(np.uint8)


# =============================================================================
# 3. KONVERSI MODEL WARNA: RGB <-> HSV
# =============================================================================

def rgb_to_hsv_manual(img_rgb):
    """
    Konversi matematis RGB ke HSV (Model Kerucut / Hexcone Smith):
    - V = max(R, G, B)
    - S = (V - min(R, G, B)) / V jika V != 0
    - H dihitung dari pergeseran selisih nilai kanal maksimum
    Output:
      H dalam derajat [0, 360)
      S dalam rentang [0, 1]
      V dalam rentang [0, 1]
    """
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    c_max = np.maximum(np.maximum(r, g), b)
    c_min = np.minimum(np.minimum(r, g), b)
    delta = c_max - c_min

    # 1. Value (V)
    v = c_max

    # 2. Saturation (S)
    s = np.zeros_like(v)
    mask_v = v != 0
    s[mask_v] = delta[mask_v] / v[mask_v]

    # 3. Hue (H)
    h = np.zeros_like(v)
    delta_safe = delta.copy()
    delta_safe[delta_safe == 0] = 1e-7

    mask_r = (c_max == r) & (delta != 0)
    mask_g = (c_max == g) & (delta != 0)
    mask_b = (c_max == b) & (delta != 0)

    h[mask_r] = 60.0 * (((g[mask_r] - b[mask_r]) / delta_safe[mask_r]) % 6.0)
    h[mask_g] = 60.0 * (((b[mask_g] - r[mask_g]) / delta_safe[mask_g]) + 2.0)
    h[mask_b] = 60.0 * (((r[mask_b] - g[mask_b]) / delta_safe[mask_b]) + 4.0)

    h[h < 0] += 360.0
    return h, s, v


# =============================================================================
# MAIN RUNNER & VISUALISASI LENGKAP
# =============================================================================

def main():
    print("=" * 70)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 4: MODEL WARNA")
    print(" (Konversi & Dekomposisi RGB, CMYK, HSI, dan HSV)")
    print("=" * 70)

    # 1. Siapkan citra input
    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        buat_citra_sampel_warna(sample_path)

    img_bgr = cv2.imread(sample_path)
    if img_bgr is None:
        buat_citra_sampel_warna(sample_path)
        img_bgr = cv2.imread(sample_path)

    # Konversi BGR OpenCV ke RGB standar
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    print(f"[INFO] Citra uji dimuat: Resolusi {img_rgb.shape[1]}x{img_rgb.shape[0]} piksel")

    # 2. Dekomposisi Kanal RGB
    print("\n--- [1] PROSES MODEL WARNA RGB ---")
    r_chan = img_rgb[:, :, 0]
    g_chan = img_rgb[:, :, 1]
    b_chan = img_rgb[:, :, 2]
    print("  -> Kanal Red, Green, Blue berhasil didekomposisi.")

    # 3. Konversi dan Dekomposisi CMYK
    print("\n--- [2] PROSES MODEL WARNA CMYK ---")
    c_chan, m_chan, y_chan, k_chan = rgb_to_cmyk(img_rgb)
    reconstructed_rgb_cmyk = cmyk_to_rgb(c_chan, m_chan, y_chan, k_chan)
    print("  -> Konversi RGB -> CMYK -> RGB berhasil dieksekusi.")

    # 4. Konversi dan Dekomposisi HSI
    print("\n--- [3] PROSES MODEL WARNA HSI ---")
    h_hsi, s_hsi, i_hsi = rgb_to_hsi(img_rgb)
    reconstructed_rgb_hsi = hsi_to_rgb(h_hsi, s_hsi, i_hsi)
    print("  -> Konversi RGB -> HSI -> RGB berhasil dieksekusi.")

    # 5. Konversi dan Dekomposisi HSV
    print("\n--- [4] PROSES MODEL WARNA HSV ---")
    h_hsv, s_hsv, v_hsv = rgb_to_hsv_manual(img_rgb)
    print("  -> Konversi RGB -> HSV berhasil dieksekusi.")

    # 6. Visualisasi Komparatif Seluruh Kanal
    print("\n[INFO] Menyiapkan kanvas visualisasi komparatif 16 panel...")
    fig, axes = plt.subplots(4, 4, figsize=(16, 14))
    fig.suptitle("Perbandingan Dekomposisi Model Warna (RGB, CMYK, HSI, HSV)", fontsize=16, fontweight='bold')

    # Baris 1: RGB
    axes[0, 0].imshow(img_rgb)
    axes[0, 0].set_title("Citra Asli (RGB)", fontsize=11, fontweight='bold')
    axes[0, 1].imshow(r_chan, cmap='Reds')
    axes[0, 1].set_title("Kanal R (Red)", fontsize=11)
    axes[0, 2].imshow(g_chan, cmap='Greens')
    axes[0, 2].set_title("Kanal G (Green)", fontsize=11)
    axes[0, 3].imshow(b_chan, cmap='Blues')
    axes[0, 3].set_title("Kanal B (Blue)", fontsize=11)

    # Baris 2: CMYK
    axes[1, 0].imshow(c_chan, cmap='cyan' if 'cyan' in plt.colormaps() else 'Blues')
    axes[1, 0].set_title("Kanal C (Cyan)", fontsize=11)
    axes[1, 1].imshow(m_chan, cmap='Purples')
    axes[1, 1].set_title("Kanal M (Magenta)", fontsize=11)
    axes[1, 2].imshow(y_chan, cmap='YlOrBr')
    axes[1, 2].set_title("Kanal Y (Yellow)", fontsize=11)
    axes[1, 3].imshow(k_chan, cmap='gray')
    axes[1, 3].set_title("Kanal K (Black / Key)", fontsize=11)

    # Baris 3: HSI
    axes[2, 0].imshow(h_hsi, cmap='hsv')
    axes[2, 0].set_title("HSI: Hue (Warna Murni)", fontsize=11)
    axes[2, 1].imshow(s_hsi, cmap='gray')
    axes[2, 1].set_title("HSI: Saturation (Kepekatan)", fontsize=11)
    axes[2, 2].imshow(i_hsi, cmap='gray')
    axes[2, 2].set_title("HSI: Intensity (Luminansi)", fontsize=11)
    axes[2, 3].imshow(reconstructed_rgb_hsi)
    axes[2, 3].set_title("Rekonstruksi HSI -> RGB", fontsize=11, fontweight='bold')

    # Baris 4: HSV
    axes[3, 0].imshow(h_hsv, cmap='hsv')
    axes[3, 0].set_title("HSV: Hue (Warna Murni)", fontsize=11)
    axes[3, 1].imshow(s_hsv, cmap='gray')
    axes[3, 1].set_title("HSV: Saturation (Kejenuhan)", fontsize=11)
    axes[3, 2].imshow(v_hsv, cmap='gray')
    axes[3, 2].set_title("HSV: Value (Kecerahan)", fontsize=11)
    axes[3, 3].imshow(reconstructed_rgb_cmyk)
    axes[3, 3].set_title("Rekonstruksi CMYK -> RGB", fontsize=11, fontweight='bold')

    for ax_row in axes:
        for ax in ax_row:
            ax.axis('off')

    plt.tight_layout()
    output_plot_path = os.path.join(BASE_DIR, "hasil_model_warna.png")
    plt.savefig(output_plot_path, dpi=150)
    print(f"[INFO] Visualisasi komparatif disimpan ke '{output_plot_path}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("\n[SELESAI] Seluruh modul 4-model-warna.py berhasil dieksekusi!")


if __name__ == "__main__":
    main()
