"""
=============================================================================
PRAKTIKUM PENGOLAHAN CITRA DAN VISI KOMPUTER (PCV)
TUGAS 1: INTRO TO IMAGE & VIDEO PROCESSING
File: 1-Intro.py
Deskripsi:
  1. Membaca gambar (Read Image)
  2. Menampilkan gambar (Show Image)
  3. Memfilter warna pada gambar diam (Filter Color Image)
  4. Memfilter warna pada video / webcam secara real-time (Filter Color Video)
=============================================================================
"""

import os
import cv2
import numpy as np

# Direktori dasar tempat berkas ini berada
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def buat_gambar_sampel(filename=None):
    """
    Membuat gambar sampel sintetis dengan berbagai bentuk dan warna
    (merah, hijau, biru, kuning) jika file gambar belum tersedia.
    """
    if filename is None:
        filename = os.path.join(BASE_DIR, "sample.jpg")
    if os.path.exists(filename):
        return filename

    print(f"[INFO] Membuat gambar sampel otomatis: '{filename}'...")
    # Kanvas latar belakang abu-abu muda (400 x 500 x 3)
    img = np.ones((400, 500, 3), dtype=np.uint8) * 230

    # Gambar lingkaran merah (BGR: [0, 0, 255])
    cv2.circle(img, (120, 130), 70, (0, 0, 255), -1)
    cv2.putText(img, "Merah", (85, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Gambar persegi panjang biru (BGR: [255, 0, 0])
    cv2.rectangle(img, (260, 60), (420, 200), (255, 0, 0), -1)
    cv2.putText(img, "Biru", (315, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Gambar lingkaran hijau (BGR: [0, 255, 0])
    cv2.circle(img, (150, 290), 60, (0, 200, 0), -1)
    cv2.putText(img, "Hijau", (120, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Gambar kotak kuning (BGR: [0, 255, 255])
    cv2.rectangle(img, (280, 240), (400, 340), (0, 230, 230), -1)
    cv2.putText(img, "Kuning", (295, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.imwrite(filename, img)
    print(f"[INFO] Gambar sampel berhasil disimpan: '{filename}'")
    return filename


# =============================================================================
# 1 & 2. BACA DAN TAMPILKAN GAMBAR (READ & SHOW IMAGE)
# =============================================================================
def read_and_show_image(image_path):
    """
    Membaca citra dari file dan menampilkannya ke layar.
    """
    print(f"\n--- [1 & 2] READ & SHOW IMAGE ---")
    img = cv2.imread(image_path)

    if img is None:
        print(f"[ERROR] Gagal membaca gambar dari path: {image_path}")
        return None

    # Tampilkan informasi metadata gambar
    tinggi, lebar, kanal = img.shape
    print(f"[INFO] Path Gambar  : {image_path}")
    print(f"[INFO] Dimensi Citra: {lebar}x{tinggi} pixel")
    print(f"[INFO] Jumlah Kanal : {kanal} (Format BGR)")
    print(f"[INFO] Tipe Data    : {img.dtype}")

    # Menampilkan citra asli
    cv2.imshow("1. Citra Asli (Tekan sembarang tombol untuk lanjut)", img)
    print("[PETUNJUK] Tekan sembarang tombol pada jendela gambar untuk melanjutkan...")
    if not os.environ.get("NON_INTERACTIVE"):
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    return img


# =============================================================================
# 3. FILTER WARNA PADA GAMBAR (FILTER COLOR IMAGE)
# =============================================================================
def filter_color_image(img):
    """
    Memfilter warna tertentu pada citra diam menggunakan ruang warna HSV.
    Pada contoh ini dilakukan segmentasi warna BIRU dan MERAH.
    """
    print(f"\n--- [3] FILTER COLOR IMAGE ---")
    if img is None:
        print("[ERROR] Citra tidak valid untuk difilter.")
        return

    # Konversi dari BGR ke HSV (Hue, Saturation, Value)
    # HSV memisahkan informasi warna (Hue) dari intensitas cahaya (Value)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 1. Rentang warna Biru pada HSV
    # Hue: ~100 - 130
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([135, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    result_blue = cv2.bitwise_and(img, img, mask=mask_blue)

    # 2. Rentang warna Merah pada HSV (karena merah berada di batas rentang 0-10 & 170-180)
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    result_red = cv2.bitwise_and(img, img, mask=mask_red)

    # Simpan hasil komposit filter warna
    mask_blue_bgr = cv2.cvtColor(mask_blue, cv2.COLOR_GRAY2BGR)
    komposit = np.hstack([img, mask_blue_bgr, result_blue, result_red])
    out_path = os.path.join(BASE_DIR, "hasil_filter_warna_gambar.png")
    cv2.imwrite(out_path, komposit)
    print(f"[INFO] Gambar perbandingan filter disimpan ke '{out_path}'")

    print("[INFO] Menampilkan hasil filter warna Biru dan Merah.")
    cv2.imshow("Filter Citra - Asli", img)
    cv2.imshow("Filter Citra - Mask Biru", mask_blue)
    cv2.imshow("Filter Citra - Hasil Filter Biru", result_blue)
    cv2.imshow("Filter Citra - Hasil Filter Merah", result_red)

    print("[PETUNJUK] Tekan sembarang tombol pada jendela gambar untuk lanjut ke filter video...")
    if not os.environ.get("NON_INTERACTIVE"):
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)
    cv2.destroyAllWindows()


# =============================================================================
# 4. FILTER WARNA PADA VIDEO (FILTER COLOR VIDEO / LIVE WEBCAM)
# =============================================================================
def filter_color_video():
    """
    Membaca aliran video secara real-time dari kamera/webcam,
    lalu memfilter warna secara interaktif dengan trackbar HSV.
    """
    print(f"\n--- [4] FILTER COLOR VIDEO (REAL-TIME WEBCAM) ---")
    print("[INFO] Membuka webcam (index 0)...")
    cap = cv2.VideoCapture(0)

    # Jika webcam default tidak terbuka, coba index 1
    if not cap.isOpened():
        print("[WARNING] Webcam index 0 tidak dapat diakses, mencoba index 1...")
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("[PERINGATAN] Webcam fisik tidak terdeteksi atau tidak memiliki izin akses.")
        print("[INFO] Menjalankan simulasi video buatan untuk demonstrasi filter warna video...")
        _jalankan_simulasi_filter_video()
        return

    # Buat window interaktif untuk kontrol threshold warna
    window_name = "Live Color Filter (Tekan 'q' untuk keluar)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    def nothing(x):
        pass

    # Buat Trackbar untuk mengatur nilai threshold HSV secara interaktif
    # Default diset untuk mendeteksi warna Biru
    cv2.createTrackbar("H Min", window_name, 100, 179, nothing)
    cv2.createTrackbar("H Max", window_name, 135, 179, nothing)
    cv2.createTrackbar("S Min", window_name, 100, 255, nothing)
    cv2.createTrackbar("S Max", window_name, 255, 255, nothing)
    cv2.createTrackbar("V Min", window_name, 50, 255, nothing)
    cv2.createTrackbar("V Max", window_name, 255, 255, nothing)

    print("[INFO] Webcam berhasil terhubung!")
    print("[PETUNJUK] Geser trackbar untuk menyesuaikan warna target.")
    print("[PETUNJUK] Tekan 's' pada keyboard untuk menyimpan snapshot frame kapan saja.")
    print("[PETUNJUK] Tekan 'q' atau tombol ESC untuk keluar (frame saat tombol ditekan otomatis disimpan ke file).")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[WARNING] Gagal membaca frame dari webcam.")
            break

        # Resize frame agar performa lancar
        frame = cv2.resize(frame, (640, 480))

        # Konversi ke HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Ambil nilai dari trackbar
        h_min = cv2.getTrackbarPos("H Min", window_name)
        h_max = cv2.getTrackbarPos("H Max", window_name)
        s_min = cv2.getTrackbarPos("S Min", window_name)
        s_max = cv2.getTrackbarPos("S Max", window_name)
        v_min = cv2.getTrackbarPos("V Min", window_name)
        v_max = cv2.getTrackbarPos("V Max", window_name)

        lower_bound = np.array([h_min, s_min, v_min])
        upper_bound = np.array([h_max, s_max, v_max])

        # Buat mask biner
        mask = cv2.inRange(hsv, lower_bound, upper_bound)

        # Segmentasikan warna menggunakan bitwise AND
        result = cv2.bitwise_and(frame, frame, mask=mask)

        # Ubah mask 1-channel ke 3-channel agar dapat digabung horizontal
        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

        # Tampilkan teks pada frame
        cv2.putText(frame, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(mask_bgr, "Mask Biner", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(result, "Hasil Filter", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Gabungkan secara horizontal: Asli | Mask | Hasil
        display_combined = np.hstack([frame, mask_bgr, result])

        # Skala tampilan gabungan agar pas di layar
        display_combined = cv2.resize(display_combined, (960, 320))
        cv2.imshow(window_name, display_combined)
        last_display = display_combined.copy()

        # Simpan jika mode non-interaktif
        if os.environ.get("NON_INTERACTIVE"):
            out_vid_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_vid_path, last_display)
            break

        key = cv2.waitKey(1) & 0xFF
        # Tekan 's' untuk snapshot manual sewaktu-waktu
        if key == ord('s'):
            out_vid_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_vid_path, last_display)
            print(f"[INFO] Snapshot manual berhasil disimpan ke '{out_vid_path}'!")
        elif key == ord('q') or key == 27:
            # Simpan frame tepat saat tombol 'q' atau ESC ditekan
            out_vid_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_vid_path, last_display)
            print(f"[INFO] Frame saat tombol 'q' ditekan berhasil disimpan ke '{out_vid_path}'!")
            break

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Video filter selesai ditutup.")


def _jalankan_simulasi_filter_video():
    """
    Fallback jika tidak ada perangkat webcam terpasang:
    Membuat animasi objek berwarna bergerak untuk membuktikan logika filter video bekerja.
    """
    window_name = "Simulasi Live Video (Tekan 'q' untuk keluar)"
    cv2.namedWindow(window_name)

    # Objek bergerak
    x, y = 50, 50
    dx, dy = 5, 4
    radius = 35

    print("[INFO] Menjalankan simulasi frame bergerak selama webcam tidak tersedia.")
    print("[PETUNJUK] Tekan 'q' untuk keluar dari simulasi.")

    frame_count = 0
    while frame_count < 300:  # Berjalan beberapa ratus frame atau sampai user menekan 'q'
        frame = np.ones((360, 480, 3), dtype=np.uint8) * 220

        # Update posisi lingkaran biru yang bergerak
        x += dx
        y += dy
        if x - radius <= 0 or x + radius >= 480:
            dx = -dx
        if y - radius <= 0 or y + radius >= 360:
            dy = -dy

        # Bola biru bergerak
        cv2.circle(frame, (x, y), radius, (255, 0, 0), -1)
        # Objek statis merah di tengah
        cv2.rectangle(frame, (200, 140), (280, 220), (0, 0, 255), -1)

        # Filter warna biru
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array([100, 100, 50]), np.array([135, 255, 255]))
        result = cv2.bitwise_and(frame, frame, mask=mask)

        mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
        combined = np.hstack([frame, mask_bgr, result])

        last_sim_frame = combined.copy()
        cv2.imshow(window_name, combined)

        if os.environ.get("NON_INTERACTIVE"):
            out_sim_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_sim_path, last_sim_frame)
            break

        key = cv2.waitKey(30) & 0xFF
        if key == ord('s'):
            out_sim_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_sim_path, last_sim_frame)
            print(f"[INFO] Snapshot simulasi berhasil disimpan ke '{out_sim_path}'!")
        elif key == ord('q') or key == 27:
            out_sim_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")
            cv2.imwrite(out_sim_path, last_sim_frame)
            print(f"[INFO] Frame saat tombol 'q' ditekan berhasil disimpan ke '{out_sim_path}'!")
            break
        frame_count += 1

    cv2.destroyAllWindows()
    print("[INFO] Simulasi video selesai.")


# =============================================================================
# MAIN ENTRYPOINT
# =============================================================================
if __name__ == "__main__":
    print("=" * 65)
    print(" PRAKTIKUM CITRA VISI - LIVE CODE 1: INTRO")
    print("=" * 65)

    # 1. Siapkan file gambar
    img_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(img_path):
        buat_gambar_sampel(img_path)

    # 2. Read & Show Image
    citra = read_and_show_image(img_path)

    # 3. Filter Color Image
    filter_color_image(citra)

    # 4. Filter Color Video
    filter_color_video()

    print("\n[SELESAI] Seluruh modul 1-Intro.py telah berhasil dieksekusi!")
