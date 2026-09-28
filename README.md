# Praktikum Pengolahan Citra dan Visi Komputer (PCV) - Tugas Live Code

Repositori ini berisi kumpulan tugas pemrograman *Live Code* mata kuliah **Praktikum Pengolahan Citra dan Visi Komputer (PCV)**.
Setiap tugas telah diorganisasikan ke dalam direktori/folder mandiri (*self-contained*) lengkap dengan kode program, citra input uji, dan hasil visualisasinya.

---

## 📁 Struktur Direktori Repositori

```text
PCV_Tugas/
│
├── 1-Intro/                                # [Tugas 1: Pengenalan Citra & Video]
│   ├── 1-Intro.py                          # Kode: Read, Show, Filter Color Image & Video
│   ├── sample.jpg                          # Citra sampel berwarna sintetis
│   ├── hasil_filter_warna_gambar.png       # Hasil filter warna Biru & Merah pada citra diam
│   └── hasil_filter_warna_video.png        # Hasil cuplikan filter warna video real-time
│
├── 2-ti-eq/                                # [Tugas 2: Transformasi Intensitas & Ekualisasi]
│   ├── 2-ti-eq.py                          # Kode: TI & Ekualisasi Histogram (Manual from Scratch)
│   ├── low_contrast_sample.jpg             # Citra sampel kontras sempit (70-140)
│   ├── hasil_transformasi_intensitas.png   # Grafik 6 mode transformasi intensitas manual
│   └── hasil_ekualisasi_histogram.png      # Perbandingan citra & histogram sebelum vs sesudah
│
├── 3-filter-spasial/                       # [Tugas 3: Penerapan Filter Spasial]
│   ├── 3-filter-spasial.py                 # Kode: Konvolusi 2D, Smoothing, Sharpening & Edge
│   ├── sample.jpg                          # Citra sampel uji spasial
│   └── hasil_filter_spasial.png            # Grafik komparasi 9 panel seluruh filter spasial
│
├── .gitignore
└── README.md
```

---

## 🚀 Rincian Tugas & Panduan Menjalankan

### 1. Tugas 1: Intro (`1-Intro/`)
- **Fitur**:
  - `read_and_show_image()`: Membaca dan menampilkan gambar serta mencetak metadata resolusi, jumlah kanal warna BGR, dan tipe data.
  - `filter_color_image()`: Mengonversi BGR ke HSV, mendeteksi rentang warna Biru dan Merah via `cv2.inRange()`, dan melakukan masking dengan `cv2.bitwise_and()`.
  - `filter_color_video()`: Membuka webcam secara live (`cv2.VideoCapture(0)`), menyediakan Trackbar HSV dinamis untuk mengatur batas warna secara interaktif, dan menampilkan jendela Asli, Mask, dan Hasil Filter.
- **Cara Menjalankan**:
  ```bash
  # Masuk ke foldernya lalu jalankan
  cd 1-Intro
  python 1-Intro.py

  # Atau jalankan langsung dari root
  python 1-Intro/1-Intro.py
  ```

---

### 2. Tugas 2: TI & Ekualisasi Histogram (`2-ti-eq/`)
> ⚠️ **Aturan Ketat:** Dilarang menggunakan fungsi bawaan package (`cv2.equalizeHist`, `cv2.LUT`, dll.). Seluruh algoritma diimplementasikan **murni dari rumus matematika dasar**.

- **Fitur**:
  - `manual_rgb_to_grayscale()`: Konversi BGR ke Gray via luminansi ($0.299R + 0.587G + 0.114B$).
  - **Transformasi Intensitas Manual**:
    1. *Image Negative*: $s = 255 - r$
    2. *Log Transformation*: $s = c \cdot \log(1 + r)$
    3. *Power-Law / Gamma Transformation*: $s = 255 \cdot (r/255)^\gamma$ ($\gamma = 0.5$ terang, $\gamma = 2.0$ gelap)
    4. *Contrast Stretching*: $s = \frac{r - r_{min}}{r_{max} - r_{min}} \times 255$
    5. *Binary Thresholding*: $r \ge T$
  - **Ekualisasi Histogram Manual**: Perhitungan frekuensi kemunculan pixel secara manual, perhitungan fungsi distribusi kumulatif (CDF), dan perataan intensitas ke skala $[0, 255]$.
- **Cara Menjalankan**:
  ```bash
  cd 2-ti-eq
  python 2-ti-eq.py

  # Atau
  python 2-ti-eq/2-ti-eq.py
  ```

---

### 3. Tugas 3: Filter Spasial (`3-filter-spasial/`)
- **Fitur**:
  - `konvolusi_2d()`: Operasi konvolusi spasial manual (sliding window dengan zero padding).
  - **Smoothing Filters**:
    - *Mean Filter ($3\times3$)*: Mengurangi noise acak.
    - *Gaussian Filter ($3\times3$)*: Menghaluskan dengan pembobotan normal.
    - *Median Filter ($3\times3$)*: Non-linear filter pereduksi noise *Salt-and-Pepper*.
  - **Sharpening & Edge Detection**:
    - *Laplacian Filter*: Turunan kedua penajam detail dan tekstur citra.
    - *Sobel Filter*: Gradien horizontal ($G_x$), vertikal ($G_y$), dan magnitudo gradien $\sqrt{G_x^2 + G_y^2}$.
- **Cara Menjalankan**:
  ```bash
  cd 3-filter-spasial
  python 3-filter-spasial.py

  # Atau
  python 3-filter-spasial/3-filter-spasial.py
  ```

---

## 📦 Pustaka Pendukung
```bash
pip install opencv-python numpy matplotlib
```
