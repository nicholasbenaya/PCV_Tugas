# Praktikum Pengolahan Citra dan Visi Komputer (PCV) - Tugas Live Code

Repositori ini berisi kumpulan tugas pemrograman *Live Code* mata kuliah **Praktikum Pengolahan Citra dan Visi Komputer (PCV)**.
Setiap tugas telah diorganisasikan ke dalam direktori/folder mandiri (*self-contained*) lengkap dengan kode program, citra input uji, visualisasi keluaran, dan laporan Markdown (`README.md`).

---

## 📁 Struktur Direktori Repositori

```text
PCV_Tugas/
│
├── 1-Intro/                                # [Tugas 1: Pengenalan Citra & Video]
│   ├── 1-Intro.py                          # Kode: Read, Show, Filter Color Image & Video
│   ├── sample.jpg                          # Citra sampel input
│   ├── hasil_filter_warna_gambar.png       # Hasil filter warna Biru & Merah pada citra diam
│   ├── hasil_filter_warna_video.png        # Hasil cuplikan filter warna video webcam
│   └── README.md                           # Laporan analisis Tugas 1 & Placeholder Video
│
├── 2-ti-eq/                                # [Tugas 2: Transformasi Intensitas & Ekualisasi]
│   ├── 2-ti-eq.py                          # Kode: TI & Ekualisasi Histogram (Manual from Scratch)
│   ├── low_contrast_sample.jpg             # Citra sampel ruangan gelap / kontras rendah
│   ├── hasil_transformasi_intensitas.png   # Grafik 6 mode transformasi intensitas manual
│   └── hasil_ekualisasi_histogram.png      # Perbandingan citra & histogram sebelum vs sesudah
│   └── README.md                           # Laporan analisis Tugas 2 (Rumus & Perataan Histogram)
│
├── 3-filter-spasial/                       # [Tugas 3: Penerapan Filter Spasial]
│   ├── 3-filter-spasial.py                 # Kode: Konvolusi 2D, Smoothing, Sharpening & Edge
│   ├── sample.jpg                          # Citra sampel berwarna
│   ├── hasil_filter_spasial.png            # Grafik komparasi 9 panel (Warna Asli Dipulihkan)
│   └── README.md                           # Laporan analisis Tugas 3 (Kernel Spasial & Restorasi)
│
├── 4-model-warna/                          # [Tugas 4: Konversi Model Warna]
│   ├── 4-model-warna.py                    # Kode: Konversi matematis RGB, CMYK, HSI, HSV
│   ├── sample.jpg                          # Citra sampel aneka warna spektrum
│   ├── hasil_model_warna.png               # Grafik komparasi 16 panel dekomposisi antarkanal
│   └── README.md                           # Laporan analisis Tugas 4 (Formulasi Matematis Model Warna)
│
├── 5-morphology/                           # [Tugas 5: Operasi Morfologi Citra]
│   ├── 5-morphology.py                     # Kode: Erosi, Dilasi, Opening, Closing, Gradient
│   ├── sample.jpg                          # Citra sampel biner ber-noise luar & lubang dalam
│   ├── hasil_morfologi.png                 # Grafik komparasi 9 panel evaluasi morfologi
│   └── README.md                           # Laporan analisis Tugas 5 (Aljabar Himpunan Morfologi)
│
├── .gitignore
└── README.md
```

---

## 🚀 Rincian Tugas & Panduan Menjalankan

### 1. Tugas 1: Intro (`1-Intro/`)
* **Fitur**: Membaca citra, segmentasi warna BGR $\rightarrow$ HSV (Biru & Merah), serta streaming video webcam real-time dengan interaktif HSV Trackbar.
* **Cara Menjalankan**:
  ```bash
  python 1-Intro/1-Intro.py
  ```

---

### 2. Tugas 2: TI & Ekualisasi Histogram (`2-ti-eq/`)
* **Fitur**: Transformasi intensitas (Negatif, Log, Gamma 0.5/2.0, Contrast Stretching, Thresholding) dan Ekualisasi Histogram manual *from-scratch* (tanpa fungsi bawaan package).
* **Cara Menjalankan**:
  ```bash
  python 2-ti-eq/2-ti-eq.py
  ```

---

### 3. Tugas 3: Filter Spasial (`3-filter-spasial/`)
* **Fitur**: Konvolusi 2D manual, filter smoothing (Mean, Gaussian, Median), penajaman Laplacian, dan deteksi tepi Sobel. Perhitungan dilakukan pada intensitas hitam-putih lalu direstorasi ke warna asli (*Full Color*).
* **Cara Menjalankan**:
  ```bash
  python 3-filter-spasial/3-filter-spasial.py
  ```

---

### 4. Tugas 4: Model Warna (`4-model-warna/`)
* **Fitur**: Konversi matematis dan dekomposisi kanal antarmodel warna: RGB (Aditif), CMYK (Subtraktif), HSI (Persepsi Manusia), dan HSV (Kerucut Heksagonal) beserta rekonstruksi warna aslinya.
* **Cara Menjalankan**:
  ```bash
  python 4-model-warna/4-model-warna.py
  ```

---

### 5. Tugas 5: Morfologi Citra (`5-morphology/`)
* **Fitur**: Penerapan operasi morfologi biner: Erosi, Dilasi, Opening (pembersihan bintik noise luar), Closing (penutupan lubang rongga dalam), serta Morphological Gradient (deteksi garis kontur tepi) dengan berbagai *Structuring Elements* (Rectangular, Cross, Ellipse).
* **Cara Menjalankan**:
  ```bash
  python 5-morphology/5-morphology.py
  ```

---

## 📦 Pustaka Pendukung
```bash
pip install opencv-python numpy matplotlib
```
