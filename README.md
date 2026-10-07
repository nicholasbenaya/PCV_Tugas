# Praktikum Pengolahan Citra dan Visi Komputer (PCV) - Tugas Live Code

Repositori tugas pemrograman *Live Code* mata kuliah Praktikum Pengolahan Citra dan Visi Komputer (PCV). Setiap tugas tersusun dalam direktori mandiri yang memuat kode sumber Python, citra uji, visualisasi hasil keluaran, dan laporan teknis Markdown (`README.md`).

---

## Struktur Direktori Repositori

```text
PCV_Tugas/
│
├── 1-Intro/                                # [Tugas 1: Pengenalan Citra & Video]
│   ├── 1-Intro.py                          # Kode: Read, Show, Filter Color Image & Video
│   ├── sample.jpg                          # Citra sampel input
│   ├── hasil_filter_warna_gambar.png       # Hasil segmentasi warna Biru & Merah pada citra diam
│   ├── hasil_filter_warna_video.png        # Hasil cuplikan filter warna video webcam
│   └── README.md                           # Laporan analisis Tugas 1 & Placeholder Video
│
├── 2-ti-eq/                                # [Tugas 2: Transformasi Intensitas & Ekualisasi]
│   ├── 2-ti-eq.py                          # Kode: TI & Ekualisasi Histogram (Manual from Scratch)
│   ├── low_contrast_sample.jpg             # Citra sampel ruangan gelap / kontras rendah
│   ├── hasil_transformasi_intensitas.png   # Grafik 6 mode transformasi intensitas manual
│   ├── hasil_ekualisasi_histogram.png      # Perbandingan citra & histogram sebelum vs sesudah
│   └── README.md                           # Laporan analisis Tugas 2 (Formulasi & Evaluasi CDF)
│
├── 3-filter-spasial/                       # [Tugas 3: Penerapan Filter Spasial]
│   ├── 3-filter-spasial.py                 # Kode: Konvolusi 2D, Smoothing, Sharpening & Edge
│   ├── sample.jpg                          # Citra sampel berwarna
│   ├── hasil_filter_spasial.png            # Grafik komparasi 9 panel dengan restorasi warna asli
│   └── README.md                           # Laporan analisis Tugas 3 (Kernel Spasial & Restorasi)
│
├── 4-model-warna/                          # [Tugas 4: Konversi Model Warna]
│   ├── 4-model-warna.py                    # Kode: Konversi matematis RGB, CMYK, HSI, HSV
│   ├── sample.jpg                          # Citra sampel spektrum warna
│   ├── hasil_model_warna.png               # Grafik komparasi 16 panel dekomposisi antarkanal
│   └── README.md                           # Laporan analisis Tugas 4 (Formulasi Model Warna)
│
├── 5-morphology/                           # [Tugas 5: Operasi Morfologi Citra]
│   ├── 5-morphology.py                     # Kode: Erosi, Dilasi, Opening, Closing, Gradient
│   ├── sample.jpg                          # Citra sampel biner berderau dan berongga
│   ├── hasil_morfologi.png                 # Grafik komparasi 9 panel evaluasi morfologi
│   └── README.md                           # Laporan analisis Tugas 5 (Aljabar Himpunan Morfologi)
│
├── .gitignore
└── README.md
```

---

## Rincian Tugas dan Petunjuk Eksekusi

### 1. Tugas 1: Intro (`1-Intro/`)
* **Fokus**: Pembacaan citra, segmentasi warna BGR $\rightarrow$ HSV (biru dan merah), serta streaming video webcam real-time dengan kendali interaktif trackbar HSV.
* **Eksekusi**:
  ```bash
  python 1-Intro/1-Intro.py
  ```

---

### 2. Tugas 2: Transformasi Intensitas dan Ekualisasi Histogram (`2-ti-eq/`)
* **Fokus**: Transformasi intensitas (negatif, log, gamma $\gamma = 0.5$ dan $\gamma = 2.0$, contrast stretching, thresholding) dan ekualisasi histogram manual *from-scratch* tanpa fungsi bawaan pustaka.
* **Eksekusi**:
  ```bash
  python 2-ti-eq/2-ti-eq.py
  ```

---

### 3. Tugas 3: Filter Spasial (`3-filter-spasial/`)
* **Fokus**: Konvolusi 2D, filter penghalusan (mean, Gaussian, median), penajaman Laplacian, dan deteksi tepi Sobel. Perhitungan dilakukan pada kanal intensitas luminansi ($V$) dan direkonstruksi kembali ke ruang warna BGR asli (*full color*).
* **Eksekusi**:
  ```bash
  python 3-filter-spasial/3-filter-spasial.py
  ```

---

### 4. Tugas 4: Model Warna (`4-model-warna/`)
* **Fokus**: Konversi matematis dan dekomposisi kanal antarmodel warna: RGB, CMYK, HSI, dan HSV, serta rekonstruksi kembali ke RGB.
* **Eksekusi**:
  ```bash
  python 4-model-warna/4-model-warna.py
  ```

---

### 5. Tugas 5: Morfologi Citra (`5-morphology/`)
* **Fokus**: Operasi morfologi biner meliputi erosi, dilasi, opening, closing, dan gradien morfologi menggunakan variasi elemen penstruktur (*structuring elements*: persegi, silang, elips).
* **Eksekusi**:
  ```bash
  python 5-morphology/5-morphology.py
  ```

---

## Dependensi

```bash
pip install opencv-python numpy matplotlib
```
