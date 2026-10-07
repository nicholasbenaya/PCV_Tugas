"""Praktikum Pengolahan Citra dan Visi Komputer (PCV)
Tugas 4: Konversi Model Warna (RGB, CMYK, HSI, HSV)
Berkas: 4-model-warna.py
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def buat_citra_sampel_warna(filepath):
    """Membuat citra sintetis beraneka ragam warna spektrum untuk uji model warna."""
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        return filepath

    print(f"[INFO] Membuat citra sampel berwarna: '{filepath}'")
    h, w = 360, 480
    img = np.ones((h, w, 3), dtype=np.uint8) * 240

    cv2.rectangle(img, (30, 30), (130, 150), (0, 0, 255), -1)
    cv2.putText(img, "Red", (55, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.rectangle(img, (150, 30), (250, 150), (0, 255, 0), -1)
    cv2.putText(img, "Green", (165, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (270, 30), (370, 150), (255, 0, 0), -1)
    cv2.putText(img, "Blue", (295, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.rectangle(img, (30, 180), (130, 300), (255, 255, 0), -1)
    cv2.putText(img, "Cyan", (50, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.rectangle(img, (150, 180), (250, 300), (0, 255, 255), -1)
    cv2.putText(img, "Magenta", (155, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    cv2.rectangle(img, (270, 180), (370, 300), (0, 255, 255), -1)
    cv2.putText(img, "Yellow", (280, 250), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    for i in range(h):
        val = int((i / float(h)) * 255)
        img[i, 400:460] = [val, val, val]
    cv2.putText(img, "Gray", (405, 330), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1)

    cv2.imwrite(filepath, img)
    return filepath


def rgb_to_cmyk(img_rgb):
    """Konversi RGB [0, 255] ke CMYK [0, 1]:
    K = 1 - max(R', G', B')
    C = (1 - R' - K) / (1 - K)
    M = (1 - G' - K) / (1 - K)
    Y = (1 - B' - K) / (1 - K)
    """
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    k = 1.0 - np.maximum(np.maximum(r, g), b)

    denom = 1.0 - k
    denom[denom <= 1e-6] = 1e-6

    c = (1.0 - r - k) / denom
    m = (1.0 - g - k) / denom
    y = (1.0 - b - k) / denom

    is_black = k >= (1.0 - 1e-6)
    c[is_black] = 0.0
    m[is_black] = 0.0
    y[is_black] = 0.0

    return np.clip(c, 0, 1), np.clip(m, 0, 1), np.clip(y, 0, 1), np.clip(k, 0, 1)


def cmyk_to_rgb(c, m, y, k):
    """Rekonstruksi CMYK [0, 1] ke RGB [0, 255]:
    R = 255 * (1 - C) * (1 - K)
    G = 255 * (1 - M) * (1 - K)
    B = 255 * (1 - Y) * (1 - K)
    """
    r = 255.0 * (1.0 - c) * (1.0 - k)
    g = 255.0 * (1.0 - m) * (1.0 - k)
    b = 255.0 * (1.0 - y) * (1.0 - k)
    rgb = np.stack([r, g, b], axis=-1)
    return np.clip(np.round(rgb), 0, 255).astype(np.uint8)


def rgb_to_hsi(img_rgb):
    """Konversi RGB ke HSI berbasis perumusan Gonzalez & Woods:
    I = (R + G + B) / 3
    S = 1 - 3*min(R,G,B) / (R+G+B)
    theta = arccos( 0.5*((R-G)+(R-B)) / sqrt((R-G)^2 + (R-B)*(G-B)) )
    """
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    # Intensitas (I)
    i = (r + g + b) / 3.0

    # Saturasi (S)
    min_rgb = np.minimum(np.minimum(r, g), b)
    sum_rgb = r + g + b
    sum_safe = np.where(sum_rgb == 0, 1e-7, sum_rgb)

    s = 1.0 - (3.0 / sum_safe) * min_rgb
    s[sum_rgb == 0] = 0.0
    s = np.clip(s, 0, 1)

    # Hue (H)
    num = 0.5 * ((r - g) + (r - b))
    den = np.sqrt((r - g) ** 2 + (r - b) * (g - b))
    den_safe = np.where(den == 0, 1e-7, den)

    arg = np.clip(num / den_safe, -1.0, 1.0)
    theta = np.arccos(arg) * (180.0 / np.pi)

    h = theta.copy()
    h[b > g] = 360.0 - theta[b > g]
    h[s == 0] = 0.0

    return h, s, i


def hsi_to_rgb(h, s, i):
    """Rekonstruksi model HSI ke RGB berdasarkan tiga sektor sudut (RG, GB, BR)."""
    h_rad = h * (np.pi / 180.0)
    r = np.zeros_like(h, dtype=np.float32)
    g = np.zeros_like(h, dtype=np.float32)
    b = np.zeros_like(h, dtype=np.float32)

    # Sektor RG: 0 <= H < 120
    mask1 = (h >= 0) & (h < 120)
    b[mask1] = i[mask1] * (1.0 - s[mask1])
    denom1 = np.cos((60.0 * np.pi / 180.0) - h_rad[mask1])
    denom1 = np.where(denom1 == 0, 1e-7, denom1)
    r[mask1] = i[mask1] * (1.0 + (s[mask1] * np.cos(h_rad[mask1])) / denom1)
    g[mask1] = 3.0 * i[mask1] - (r[mask1] + b[mask1])

    # Sektor GB: 120 <= H < 240
    mask2 = (h >= 120) & (h < 240)
    h_rad2 = h_rad[mask2] - (120.0 * np.pi / 180.0)
    r[mask2] = i[mask2] * (1.0 - s[mask2])
    denom2 = np.cos((60.0 * np.pi / 180.0) - h_rad2)
    denom2 = np.where(denom2 == 0, 1e-7, denom2)
    g[mask2] = i[mask2] * (1.0 + (s[mask2] * np.cos(h_rad2)) / denom2)
    b[mask2] = 3.0 * i[mask2] - (r[mask2] + g[mask2])

    # Sektor BR: 240 <= H <= 360
    mask3 = (h >= 240) & (h <= 360)
    h_rad3 = h_rad[mask3] - (240.0 * np.pi / 180.0)
    g[mask3] = i[mask3] * (1.0 - s[mask3])
    denom3 = np.cos((60.0 * np.pi / 180.0) - h_rad3)
    denom3 = np.where(denom3 == 0, 1e-7, denom3)
    b[mask3] = i[mask3] * (1.0 + (s[mask3] * np.cos(h_rad3)) / denom3)
    r[mask3] = 3.0 * i[mask3] - (g[mask3] + b[mask3])

    rgb = np.stack([r, g, b], axis=-1) * 255.0
    return np.clip(np.round(rgb), 0, 255).astype(np.uint8)


def rgb_to_hsv_manual(img_rgb):
    """Konversi RGB ke HSV (model kerucut heksagonal Smith)."""
    rgb_norm = img_rgb.astype(np.float32) / 255.0
    r = rgb_norm[:, :, 0]
    g = rgb_norm[:, :, 1]
    b = rgb_norm[:, :, 2]

    c_max = np.maximum(np.maximum(r, g), b)
    c_min = np.minimum(np.minimum(r, g), b)
    delta = c_max - c_min

    v = c_max

    s = np.zeros_like(v)
    mask_v = v > 0
    s[mask_v] = delta[mask_v] / v[mask_v]

    h = np.zeros_like(v)
    delta_safe = np.where(delta == 0, 1e-7, delta)

    mask_r = (c_max == r) & (delta != 0)
    mask_g = (c_max == g) & (c_max != r) & (delta != 0)
    mask_b = (c_max == b) & (c_max != r) & (c_max != g) & (delta != 0)

    h[mask_r] = 60.0 * (((g[mask_r] - b[mask_r]) / delta_safe[mask_r]) % 6.0)
    h[mask_g] = 60.0 * (((b[mask_g] - r[mask_g]) / delta_safe[mask_g]) + 2.0)
    h[mask_b] = 60.0 * (((r[mask_b] - g[mask_b]) / delta_safe[mask_b]) + 4.0)

    h[h < 0] += 360.0
    return h, s, v


def main():
    print("PRAKTIKUM PCV - TUGAS 4: MODEL WARNA")

    sample_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(sample_path):
        buat_citra_sampel_warna(sample_path)

    img_bgr = cv2.imread(sample_path)
    if img_bgr is None:
        buat_citra_sampel_warna(sample_path)
        img_bgr = cv2.imread(sample_path)

    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    print(f"[INFO] Citra uji: {img_rgb.shape[1]}x{img_rgb.shape[0]} piksel")

    # Dekomposisi RGB
    r_chan = img_rgb[:, :, 0]
    g_chan = img_rgb[:, :, 1]
    b_chan = img_rgb[:, :, 2]

    # Konversi CMYK
    c_chan, m_chan, y_chan, k_chan = rgb_to_cmyk(img_rgb)
    reconstructed_rgb_cmyk = cmyk_to_rgb(c_chan, m_chan, y_chan, k_chan)

    # Konversi HSI
    h_hsi, s_hsi, i_hsi = rgb_to_hsi(img_rgb)
    reconstructed_rgb_hsi = hsi_to_rgb(h_hsi, s_hsi, i_hsi)

    # Konversi HSV
    h_hsv, s_hsv, v_hsv = rgb_to_hsv_manual(img_rgb)

    # Visualisasi 16 panel
    fig, axes = plt.subplots(4, 4, figsize=(16, 14))
    fig.suptitle("Perbandingan Dekomposisi Model Warna (RGB, CMYK, HSI, HSV)", fontsize=15, fontweight='bold')

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
    axes[1, 0].imshow(c_chan, cmap='Blues')
    axes[1, 0].set_title("Kanal C (Cyan)", fontsize=11)
    axes[1, 1].imshow(m_chan, cmap='Purples')
    axes[1, 1].set_title("Kanal M (Magenta)", fontsize=11)
    axes[1, 2].imshow(y_chan, cmap='YlOrBr')
    axes[1, 2].set_title("Kanal Y (Yellow)", fontsize=11)
    axes[1, 3].imshow(k_chan, cmap='gray')
    axes[1, 3].set_title("Kanal K (Black / Key)", fontsize=11)

    # Baris 3: HSI
    axes[2, 0].imshow(h_hsi, cmap='hsv')
    axes[2, 0].set_title("HSI: Hue (Rona)", fontsize=11)
    axes[2, 1].imshow(s_hsi, cmap='gray')
    axes[2, 1].set_title("HSI: Saturation (Kejenuhan)", fontsize=11)
    axes[2, 2].imshow(i_hsi, cmap='gray')
    axes[2, 2].set_title("HSI: Intensity (Luminansi)", fontsize=11)
    axes[2, 3].imshow(reconstructed_rgb_hsi)
    axes[2, 3].set_title("Rekonstruksi HSI -> RGB", fontsize=11, fontweight='bold')

    # Baris 4: HSV
    axes[3, 0].imshow(h_hsv, cmap='hsv')
    axes[3, 0].set_title("HSV: Hue (Rona)", fontsize=11)
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
    print(f"[INFO] Hasil visualisasi disimpan ke: '{output_plot_path}'")

    try:
        if not os.environ.get("NON_INTERACTIVE"):
            plt.show()
        else:
            plt.close('all')
    except Exception:
        pass

    print("[SELESAI] Eksekusi 4-model-warna.py selesai.")


if __name__ == "__main__":
    main()
