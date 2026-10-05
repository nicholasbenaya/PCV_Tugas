# Laporan Tugas 3: Penerapan Filter Spasial (Spatial Filtering)

Mata Kuliah: **Praktikum Pengolahan Citra dan Visi Komputer (PCV)**  
Berkas Program: [`3-filter-spasial.py`](3-filter-spasial.py)

---

## 📌 Ringkasan Tugas
Filter spasial beroperasi langsung pada lingkungan (*neighborhood*) piksel citra menggunakan operasi konvolusi 2D atau pengurutan statistik nilai lokal. Pada tugas ini diimplementasikan dua kategori filter spasial utama:
1. **Filter Smoothing (Penghalusan / *Low-Pass Filter*):**
   - *Mean Filter* (Rata-rata $3\times3$)
   - *Gaussian Filter* (Pembobotan normal $3\times3$)
   - *Median Filter* (Non-linear rank statistic filter $3\times3$)
2. **Filter Sharpening & Deteksi Tepi (*High-Pass Filter*):**
   - *Laplacian Sharpening* (Turunan kedua untuk penajaman detail)
   - *Sobel Operator* (Gradien arah horizontal $G_x$, vertikal $G_y$, dan magnitudo $\sqrt{G_x^2 + G_y^2}$)

---

## 🧠 Dasar Teori & Matriks Kernel

### 1. Konvolusi 2D Spasial
Operasi konvolusi menggeser jendela matriks bobot (kernel $w$) berukuran $m \times n$ di atas citra $f(x,y)$:
$$g(x,y) = \sum_{s=-a}^a \sum_{t=-b}^b w(s,t) \cdot f(x+s, y+t)$$
Pada tepian citra diterapkan teknik *padding* agar dimensi citra keluaran tetap sama dengan citra masukan.

---

### 2. Matriks Kernel yang Digunakan

* **Mean Filter ($3\times3$):**
  $$W_{mean} = \frac{1}{9}\begin{bmatrix} 1 & 1 & 1 \\ 1 & 1 & 1 \\ 1 & 1 & 1 \end{bmatrix}$$

* **Gaussian Filter ($3\times3$):**
  $$W_{gauss} = \frac{1}{16}\begin{bmatrix} 1 & 2 & 1 \\ 2 & 4 & 2 \\ 1 & 2 & 1 \end{bmatrix}$$

* **Median Filter ($3\times3$):**
  Mengambil semua 9 piksel di sekitar jendela lingkungan, mengurutkannya dari nilai terkecil ke terbesar, dan mengambil nilai tengahnya (elemen ke-5). Sangat efektif menghilangkan derau impulsif bintik putih dan hitam (*Salt-and-Pepper Noise*) tanpa mengaburkan tepi citra.

* **Laplacian Sharpening Kernel ($3\times3$):**
  $$W_{laplacian} = \begin{bmatrix} 0 & -1 & 0 \\ -1 & 5 & -1 \\ 0 & -1 & 0 \end{bmatrix}$$
  Matriks ini langsung menghasilkan citra yang telah dipertajam (*sharpened image*) dengan menambahkan turunan kedua tepi kembali ke citra asli.

* **Sobel Operator (Deteksi Tepi):**
  $$G_x = \begin{bmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{bmatrix}, \quad G_y = \begin{bmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{bmatrix}$$
  Magnitudo tepi dihitung dengan rumus:
  $$|G| = \sqrt{G_x^2 + G_y^2}$$

---

## 🔬 Hasil Eksperimen

### 1. Citra Masukan (Input)
Citra sampel bertekstur yang digunakan pada pengujian:

![Citra Input](sample.jpg)

---

### 2. Hasil Perbandingan Filter Spasial (9 Panel)
Grafik visualisasi komparatif yang menampilkan hasil evaluasi seluruh filter spasial:

![Hasil Filter Spasial](hasil_filter_spasial.png)

> **Analisis Hasil Komparatif:**
> 1. **Mean vs Gaussian vs Median pada Noise Salt-and-Pepper:**
>    - *Mean Filter:* Menghaluskan noise tetapi bintik hitam/putih tetap meninggalkan noda buram samar.
>    - *Gaussian Filter:* Serupa dengan mean, tepi sedikit lebih terjaga namun titik noise masih tersisa.
>    - *Median Filter:* **Membersihkan 100% bintik Salt-and-Pepper**, menghasilkan citra yang sangat jernih karena nilai ekstrem (0 atau 255) otomatis tersingkirkan saat proses pengurutan median.
> 2. **Laplacian Sharpening:**
>    - Menghasilkan detail tekstur, tepian kontur, dan garis objek yang jauh lebih tegas dan tajam dibanding citra asli.
> 3. **Sobel Edge Detection ($G_x$, $G_y$, Magnitude):**
>    - $G_x$ menonjolkan garis tepi vertikal.
>    - $G_y$ menonjolkan garis tepi horizontal.
>    - *Magnitude* menggabungkan kedua komponen, menampilkan garis tepi batas seluruh objek secara utuh.

---

## 💻 Cara Menjalankan Berkas
Masuk ke direktori tugas ini lalu jalankan:
```bash
python 3-filter-spasial.py
```
Hasil visualisasi komparatif 9 panel akan langsung ditampilkan di layar dan tersimpan ke berkas `hasil_filter_spasial.png`.
