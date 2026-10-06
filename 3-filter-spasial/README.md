# Laporan Tugas 3: Penerapan Filter Spasial (Spatial Filtering)

Mata Kuliah: **Praktikum Pengolahan Citra dan Visi Komputer (PCV)**  
Berkas Program: [`3-filter-spasial.py`](3-filter-spasial.py)

---

## 📌 Ringkasan Tugas & Pendekatan Ilmiah
Filter spasial beroperasi langsung pada piksel citra menggunakan operasi konvolusi 2D atau pengurutan statistik nilai lokal.

### 💡 Teknik Pemrosesan Intensitas & Restorasi Warna Asli:
Untuk menjaga agar **warna asli citra tidak hilang / pudar**:
1. **Pemisahan Intensitas:** Citra warna BGR dikonversi ke ruang warna **HSV** guna memisahkan komponen warna murni ($H$ = Hue, $S$ = Saturation) dari intensitas kecerahan monokrom ($V$ = Value / hitam-putih).
2. **Kalkulasi pada Citra Hitam-Putih:** Seluruh operasi filter spasial (konvolusi Mean, Gaussian, Median, dan Laplacian) dihitung **pada kanal hitam-putih $V$**.
3. **Restorasi Warna:** Nilai $V$ hasil kalkulasi disatukan kembali dengan kanal warna asli ($H$ dan $S$) lalu dikonversi kembali ke format BGR.
4. **Hasil:** Citra keluaran tetap mempertahankan warna asli secara utuh (*Full Color*), sementara efek penghalusan, pereduksian derau, dan penajaman berhasil diterapkan dengan optimal!

---

## 🧠 Dasar Teori & Matriks Kernel

### 1. Konvolusi 2D Spasial
Operasi konvolusi menggeser jendela matriks bobot (kernel $w$) berukuran $m \times n$ di atas citra intensitas $f(x,y)$:
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
Citra sampel berwarna asli yang digunakan pada pengujian:

![Citra Input](sample.jpg)

---

### 2. Hasil Perbandingan Filter Spasial (9 Panel)
Grafik visualisasi komparatif yang menampilkan hasil evaluasi seluruh filter spasial:

![Hasil Filter Spasial](hasil_filter_spasial.png)

> **Analisis Hasil Komparatif:**
> 1. **Restorasi Warna Penuh pada Smoothing & Sharpening:**
>    - Citra masukan tetap tampil dalam warna aslinya (*RGB*).
>    - **Mean & Gaussian Filter:** Menghaluskan variasi intensitas pada citra dengan warna asli yang tetap lembut dan natural.
>    - **Median Filter:** **Membersihkan 100% bintik Salt-and-Pepper** dan mengembalikan warna objek secara utuh tanpa meninggalkan bekas noda noise.
>    - **Laplacian Sharpening:** Meningkatkan ketajaman tepi, kontur, dan tekstur objek dengan warna asli yang tetap hidup dan kontras.
> 2. **Deteksi Tepi Sobel ($G_x$, $G_y$, Magnitude):**
>    - $G_x$ menonjolkan garis tepi vertikal objek.
>    - $G_y$ menonjolkan garis tepi horizontal objek.
>    - *Magnitude* menggabungkan kedua komponen menjadi peta kontur dan batas bentuk objek secara lengkap.

---

## 💻 Cara Menjalankan Berkas
Masuk ke direktori tugas ini lalu jalankan:
```bash
python 3-filter-spasial.py
```
Hasil visualisasi komparatif 9 panel akan langsung ditampilkan di layar dan tersimpan ke berkas `hasil_filter_spasial.png`.
