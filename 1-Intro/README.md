# Laporan Tugas 1: Pengenalan Citra dan Video (Intro)

Mata Kuliah: Praktikum Pengolahan Citra dan Visi Komputer (PCV)  
Berkas Program: [`1-Intro.py`](1-Intro.py)

---

## Ringkasan Tugas

Implementasi dasar pemrosesan citra digital dan streaming video menggunakan OpenCV dan Python:
1. **Read Image**: Membaca citra dari berkas lokal dan memeriksa metadatanya (resolusi, kanal warna, tipe data).
2. **Show Image**: Menampilkan citra asli ke jendela grafis.
3. **Filter Color Image**: Melakukan segmentasi warna (biru dan merah) pada citra diam dalam ruang warna HSV.
4. **Filter Color Video**: Membaca aliran video webcam secara real-time, menyediakan trackbar HSV interaktif untuk penyesuaian ambang batas warna, serta menyimpan frame aktif saat tombol `'q'` atau `'s'` ditekan.

---

## Dasar Teori

### Segmentasi Ruang Warna HSV dibanding RGB/BGR
Pada ruang warna standar BGR/RGB, informasi kromatisitas (warna) dan luminansi (kecerahan) terdistribusi bersama di ketiga kanal ($B, G, R$). Kondisi ini menyebabkan segmentasi warna rentan terhadap fluktuasi pencahayaan dan bayangan.

Ruang warna HSV memisahkan komponen warna dari intensitas cahaya:
- **Hue ($H$)**: Sudut representasi warna murni (pada OpenCV bernilai $0 - 179$).
- **Saturation ($S$)**: Kemurnian atau kepekatan warna ($0 - 255$).
- **Value ($V$)**: Kecerahan atau intensitas cahaya ($0 - 255$).

Pemisahan ini memungkinkan penentuan ambang batas (*threshold*) warna pada rentang Hue dan Saturasi yang konsisten meskipun intensitas pencahayaan ruangan bervariasi.

---

## Hasil Eksperimen

### 1. Citra Masukan
Citra sampel yang digunakan pada pengujian:

![Citra Input](sample.jpg)

---

### 2. Segmentasi Warna pada Citra Diam
Segmentasi warna biru dan merah dilakukan dengan `cv2.inRange()` dan operasi logika `cv2.bitwise_and()`.

![Hasil Filter Warna Gambar](hasil_filter_warna_gambar.png)

Keterangan panel:
- Panel 1: Citra asli (BGR).
- Panel 2: Mask biner target warna biru (putih menunjukkan piksel yang memenuhi rentang ambang batas).
- Panel 3: Hasil isolasi piksel warna biru.
- Panel 4: Hasil isolasi piksel warna merah.

---

### 3. Cuplikan Segmentasi Warna Video (Webcam)
Tangkapan layar saat pengujian webcam dengan penyesuaian trackbar HSV:

![Hasil Filter Video Webcam](hasil_filter_warna_video.png)

Keterangan tampilan:
- Sisi kiri: Frame asli webcam.
- Sisi tengah: Mask biner hasil ambang batas HSV.
- Sisi kanan: Citra hasil segmentasi objek berwarna.

---

## Video Demonstrasi Real-Time

<!-- ================================================================= -->
<!-- PETUNJUK CARA MELAMPIRKAN VIDEO PADA MARKDOWN GITHUB:             -->
<!--                                                                   -->
<!-- Opsi 1 (Disarankan untuk GitHub):                                  -->
<!-- 1. Buka repositori GitHub Anda di browser web.                    -->
<!-- 2. Buka tab "Issues" -> Buat "New Issue" (hanya untuk draft).     -->
<!-- 3. Drag & drop file rekaman video (.mp4) Anda ke kotak teks issue -->
<!-- 4. GitHub otomatis mengunggah video dan memberikan link URL CDN   -->
<!--    seperti: https://github.com/user-attachments/assets/xxxx       -->
<!-- 5. Copy link tersebut dan gantikan URL pada placeholder di bawah! -->
<!--                                                                   -->
<!-- Opsi 2 (File Lokal di Folder):                                    -->
<!-- 1. Simpan rekaman video Anda ke folder ini (misal: demo.mp4).     -->
<!-- 2. Gunakan tag video HTML di bawah ini:                           -->
<!--    <video src="demo.mp4" controls width="100%"></video>          -->
<!-- ================================================================= -->

### Rekaman Pengujian Video Webcam

> [!NOTE]
> Gantikan tautan atau berkas pada placeholder video di bawah ini dengan rekaman pengujian webcam Anda sesuai petunjuk di atas.

<!-- >>> PLACEHOLDER VIDEO START <<< -->

<div align="center">
  <video src="demo_video.mp4" controls="controls" width="80%">
    Browser Anda tidak mendukung tag video. Unduh berkas video secara langsung untuk memutar.
  </video>
  <p><em>Video 1.1: Demonstrasi Segmentasi Warna Real-Time dengan Trackbar HSV</em></p>
</div>

<!-- >>> PLACEHOLDER VIDEO END <<< -->

---

## Panduan Menjalankan Program

Jalankan perintah berikut di terminal:
```bash
python 1-Intro/1-Intro.py
```

Kendali interaktif pada jendela webcam:
- Geser slider trackbar untuk mengubah rentang warna target ($H_{min}, S_{min}, V_{min}$ dan $H_{max}, S_{max}, V_{max}$).
- Tekan **`s`** untuk menyimpan snapshot frame aktif.
- Tekan **`q`** atau **`ESC`** untuk keluar sekaligus menyimpan frame aktif ke `hasil_filter_warna_video.png`.
