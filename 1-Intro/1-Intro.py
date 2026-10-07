"""Praktikum Pengolahan Citra dan Visi Komputer (PCV)
Tugas 1: Pengenalan Citra dan Video (Intro)
Berkas: 1-Intro.py
"""

import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def buat_gambar_sampel(filename=None):
    """Membuat citra sampel sintetis jika berkas input belum ada."""
    if filename is None:
        filename = os.path.join(BASE_DIR, "sample.jpg")
    if os.path.exists(filename) and os.path.getsize(filename) > 0:
        return filename

    print(f"[INFO] Membuat citra sampel: '{filename}'")
    img = np.ones((400, 500, 3), dtype=np.uint8) * 230

    cv2.circle(img, (120, 130), 70, (0, 0, 255), -1)
    cv2.putText(img, "Merah", (85, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.rectangle(img, (260, 60), (420, 200), (255, 0, 0), -1)
    cv2.putText(img, "Biru", (315, 135), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.circle(img, (150, 290), 60, (0, 200, 0), -1)
    cv2.putText(img, "Hijau", (120, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.rectangle(img, (280, 240), (400, 340), (0, 230, 230), -1)
    cv2.putText(img, "Kuning", (295, 295), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

    cv2.imwrite(filename, img)
    return filename


def read_and_show_image(image_path):
    """Membaca citra dari berkas dan menampilkannya."""
    print("\n--- [1 & 2] READ & SHOW IMAGE ---")
    img = cv2.imread(image_path)

    if img is None:
        print(f"[ERROR] Gagal membaca gambar: {image_path}")
        return None

    tinggi, lebar, kanal = img.shape
    print(f"[INFO] Path: {image_path}")
    print(f"[INFO] Resolusi: {lebar}x{tinggi} piksel, {kanal} kanal (BGR)")
    print(f"[INFO] Tipe data: {img.dtype}")

    cv2.imshow("1. Citra Asli (Tekan sembarang tombol untuk lanjut)", img)
    if not os.environ.get("NON_INTERACTIVE"):
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)
    cv2.destroyAllWindows()

    return img


def filter_color_image(img):
    """Segmentasi warna biru dan merah pada citra diam berbasis ruang warna HSV."""
    print("\n--- [3] FILTER COLOR IMAGE ---")
    if img is None:
        print("[ERROR] Citra tidak valid.")
        return

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Segmentasi warna biru
    lower_blue = np.array([100, 100, 50])
    upper_blue = np.array([135, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    result_blue = cv2.bitwise_and(img, img, mask=mask_blue)

    # Segmentasi warna merah (mencakup batas 0-10 dan 170-180 pada sumbu Hue)
    lower_red1 = np.array([0, 100, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 100, 50])
    upper_red2 = np.array([180, 255, 255])
    mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask_red = cv2.bitwise_or(mask_red1, mask_red2)
    result_red = cv2.bitwise_and(img, img, mask=mask_red)

    # Simpan panel komposit hasil segmentasi
    mask_blue_bgr = cv2.cvtColor(mask_blue, cv2.COLOR_GRAY2BGR)
    komposit = np.hstack([img, mask_blue_bgr, result_blue, result_red])
    out_path = os.path.join(BASE_DIR, "hasil_filter_warna_gambar.png")
    cv2.imwrite(out_path, komposit)
    print(f"[INFO] Hasil filter citra diam disimpan ke: '{out_path}'")

    # Sesuaikan ukuran jika citra masukan berukuran besar agar muat pada layar
    h_k, w_k = komposit.shape[:2]
    if w_k > 1400:
        skala = 1400.0 / w_k
        komposit_display = cv2.resize(komposit, (int(w_k * skala), int(h_k * skala)))
    else:
        komposit_display = komposit

    cv2.imshow("Filter Citra Diam: Asli | Mask Biru | Hasil Biru | Hasil Merah", komposit_display)
    if not os.environ.get("NON_INTERACTIVE"):
        cv2.waitKey(0)
    else:
        cv2.waitKey(1)
    cv2.destroyAllWindows()


def filter_color_video():
    """Streaming video webcam real-time dengan pengaturan interaktif trackbar HSV."""
    print("\n--- [4] FILTER COLOR VIDEO (WEBCAM) ---")

    # Di Windows, backend DirectShow (CAP_DSHOW) menginisialisasi kamera lebih cepat
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) if os.name == 'nt' else cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("[WARNING] Kamera webcam tidak ditemukan. Menjalankan fallback simulasi.")
        _jalankan_simulasi_filter_video()
        return

    window_name = "Live Color Filter (Tekan 'q' untuk keluar)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    def nothing(_):
        pass

    cv2.createTrackbar("H Min", window_name, 100, 179, nothing)
    cv2.createTrackbar("H Max", window_name, 135, 179, nothing)
    cv2.createTrackbar("S Min", window_name, 100, 255, nothing)
    cv2.createTrackbar("S Max", window_name, 255, 255, nothing)
    cv2.createTrackbar("V Min", window_name, 50, 255, nothing)
    cv2.createTrackbar("V Max", window_name, 255, 255, nothing)

    print("[INFO] Webcam aktif.")
    print("[PETUNJUK] Tekan 's' untuk snapshot, tekan 'q' atau ESC untuk keluar.")

    last_display = None
    out_vid_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")

    try:
        while True:
            ret, frame = cap.read()
            if not ret or frame is None:
                break

            frame = cv2.resize(frame, (640, 480))
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            h_min = cv2.getTrackbarPos("H Min", window_name)
            h_max = cv2.getTrackbarPos("H Max", window_name)
            s_min = cv2.getTrackbarPos("S Min", window_name)
            s_max = cv2.getTrackbarPos("S Max", window_name)
            v_min = cv2.getTrackbarPos("V Min", window_name)
            v_max = cv2.getTrackbarPos("V Max", window_name)

            lower_bound = np.array([h_min, s_min, v_min])
            upper_bound = np.array([h_max, s_max, v_max])

            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            result = cv2.bitwise_and(frame, frame, mask=mask)
            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)

            cv2.putText(frame, "Original", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(mask_bgr, "Mask Biner", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.putText(result, "Hasil Filter", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            display_combined = np.hstack([frame, mask_bgr, result])
            display_combined = cv2.resize(display_combined, (960, 320))
            cv2.imshow(window_name, display_combined)
            last_display = display_combined.copy()

            if os.environ.get("NON_INTERACTIVE"):
                cv2.imwrite(out_vid_path, last_display)
                break

            key = cv2.waitKey(1) & 0xFF
            if key == ord('s'):
                cv2.imwrite(out_vid_path, last_display)
                print(f"[INFO] Snapshot tersimpan: '{out_vid_path}'")
            elif key == ord('q') or key == 27:
                cv2.imwrite(out_vid_path, last_display)
                print(f"[INFO] Frame saat tombol ditekan tersimpan: '{out_vid_path}'")
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


def _jalankan_simulasi_filter_video():
    """Fallback simulasi animasi jika perangkat webcam tidak tersedia."""
    window_name = "Simulasi Live Video (Tekan 'q' untuk keluar)"
    cv2.namedWindow(window_name)

    x, y = 50, 50
    dx, dy = 5, 4
    radius = 35
    out_sim_path = os.path.join(BASE_DIR, "hasil_filter_warna_video.png")

    frame_count = 0
    try:
        while frame_count < 300:
            frame = np.ones((360, 480, 3), dtype=np.uint8) * 220

            x += dx
            y += dy
            if x - radius <= 0 or x + radius >= 480:
                dx = -dx
            if y - radius <= 0 or y + radius >= 360:
                dy = -dy

            cv2.circle(frame, (x, y), radius, (255, 0, 0), -1)
            cv2.rectangle(frame, (200, 140), (280, 220), (0, 0, 255), -1)

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array([100, 100, 50]), np.array([135, 255, 255]))
            result = cv2.bitwise_and(frame, frame, mask=mask)

            mask_bgr = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
            combined = np.hstack([frame, mask_bgr, result])
            cv2.imshow(window_name, combined)

            if os.environ.get("NON_INTERACTIVE"):
                cv2.imwrite(out_sim_path, combined)
                break

            key = cv2.waitKey(30) & 0xFF
            if key == ord('s'):
                cv2.imwrite(out_sim_path, combined)
                print(f"[INFO] Snapshot simulasi tersimpan: '{out_sim_path}'")
            elif key == ord('q') or key == 27:
                cv2.imwrite(out_sim_path, combined)
                break
            frame_count += 1
    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    print("PRAKTIKUM PCV - TUGAS 1: PENGENALAN CITRA & VIDEO")

    img_path = os.path.join(BASE_DIR, "sample.jpg")
    if not os.path.exists(img_path):
        buat_gambar_sampel(img_path)

    citra = read_and_show_image(img_path)
    filter_color_image(citra)
    filter_color_video()
    print("\n[SELESAI] Eksekusi 1-Intro.py selesai.")
