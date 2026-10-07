# Laporan Tugas 2: Transformasi Intensitas dan Ekualisasi Histogram

Mata Kuliah: Praktikum Pengolahan Citra dan Visi Komputer (PCV)  
Berkas Program: [`2-ti-eq.py`](2-ti-eq.py)

---

## Ketentuan Khusus

> [!IMPORTANT]
> Seluruh algoritma transformasi intensitas dan ekualisasi histogram pada tugas ini diimplementasikan secara mandiri (*from scratch* / manual) menggunakan perumusan matematika dasar, tanpa menggunakan fungsi bawaan pustaka seperti `cv2.equalizeHist`, `cv2.LUT`, maupun modul otomatis dari `scikit-image`.

---

## Dasar Teori dan Perumusan Matematis

### 1. Transformasi Intensitas Spasial
Transformasi intensitas beroperasi langsung pada nilai piksel tunggal $r \in [0, 255]$ untuk menghasilkan nilai intensitas baru $s \in [0, 255]$:

1. **Citra Negatif (*Image Negative*):**
   $$s = (L - 1) - r = 255 - r$$
   Membalik tingkat keabuan citra, memetakan intensitas rendah menjadi tinggi dan sebaliknya.

2. **Transformasi Logaritmik (*Log Transformation*):**
   $$s = c \cdot \log(1 + r) \quad \text{dengan} \quad c = \frac{255}{\log(1 + \max(r))}$$
   Memperlebar rentang dinamis piksel bernilai rendah (area gelap) dan memampatkan rentang piksel bernilai tinggi.

3. **Transformasi Pangkat / Gamma (*Power-Law / Gamma Transformation*):**
   $$s = 255 \cdot \left(\frac{r}{255}\right)^\gamma$$
   - $\gamma < 1$ (misalnya $\gamma = 0.5$): Menaikkan nilai kecerahan pada area berintensitas rendah.
   - $\gamma > 1$ (misalnya $\gamma = 2.0$): Menurunkan nilai kecerahan, mempertegas kontras area gelap dan bayangan.

4. **Peregangan Kontras (*Contrast Stretching*):**
   $$s = \left(\frac{r - r_{min}}{r_{max} - r_{min}}\right) \times 255$$
   Memetakan rentang intensitas citra yang sempit $[r_{min}, r_{max}]$ ke rentang penuh $[0, 255]$ secara linier.

5. **Pengambangan Biner (*Binary Thresholding*):**
   $$s = \begin{cases} 255, & \text{jika } r \ge T \\ 0, & \text{jika } r < T \end{cases}$$

---

### 2. Ekualisasi Histogram Manual (From Scratch)
Tahapan komputasi ekualisasi histogram manual:
1. **Perhitungan Frekuensi Piksel:** Menghitung jumlah kemunculan $n_k$ untuk setiap tingkat keabuan $k \in [0, 255]$ melalui iterasi larik piksel.
2. **Fungsi Distribusi Kumulatif (CDF):**
   $$CDF(k) = \sum_{j=0}^{k} \frac{n_j}{M \times N}$$
   dengan $M \times N$ merepresentasikan jumlah total piksel pada citra.
3. **Tabel Pemetaan Nilai Baru (*Look-Up Table*):**
   $$s_k = \text{round}(CDF(k) \times 255)$$
4. **Transformasi Piksel:** Setiap piksel $r$ pada citra masukan diganti dengan nilai $s_k$ berdasarkan indeks pemetaan yang telah dihitung.

---

## Hasil Eksperimen

### 1. Citra Masukan
Uji coba menggunakan citra ruangan dalam kondisi pencahayaan rendah (*underexposed*, resolusi $960 \times 1280$ piksel, rata-rata intensitas $\approx 12.6$ pada skala 255):

![Citra Ruangan Gelap](low_contrast_sample.jpg)

---

### 2. Visualisasi Transformasi Intensitas
Hasil perbandingan 6 metode transformasi intensitas manual:

![Hasil Transformasi Intensitas](hasil_transformasi_intensitas.png)

Analisis transformasi intensitas:
- **Log Transformation dan Gamma ($\gamma = 0.5$):** Menaikkan tingkat kecerahan pada daerah berpiksel rendah sehingga struktur dan perabotan yang semula gelap menjadi teramati.
- **Gamma ($\gamma = 2.0$):** Menekan nilai intensitas lebih rendah, mempergelap bayangan dan meningkatkan kontras pada bagian yang memiliki pencahayaan cukup.
- **Image Negative:** Membalik distribusi intensitas ($255 - r$), menonjolkan batas objek gelap di atas latar belakang yang kini menjadi terang.
- **Contrast Stretching:** Merentangkan batas intensitas minimum dan maksimum citra ke skala penuh $[0, 255]$.

---

### 3. Visualisasi Ekualisasi Histogram Manual
Perbandingan citra dan profil distribusi frekuensi histogram sebelum dan sesudah ekualisasi:

![Hasil Ekualisasi Histogram](hasil_ekualisasi_histogram.png)

Analisis distribusi histogram:
- **Sebelum Ekualisasi:** Distribusi frekuensi terkonsentrasi pada rentang sempit di dekat nilai nol ($0 - 30$). Minimnya sebaran intensitas menyebabkan kontras visual sangat rendah.
- **Setelah Ekualisasi Manual:** Melalui pemetaan CDF kumulatif, nilai keabuan didistribusikan merata ke seluruh rentang dinamis $[0, 255]$.
- **Dampak Visual:** Kontur dinding, tekstur lantai, dan batas fisik objek di dalam ruangan tampak jelas akibat rentang kontras lokal yang telah diperlebar secara global.

---

## Panduan Menjalankan Program

Jalankan perintah berikut di terminal:
```bash
python 2-ti-eq/2-ti-eq.py
```
Program akan memproses kalkulasi transformasi dan ekualisasi secara manual, lalu menyimpan grafik keluaran ke format PNG di dalam folder tugas ini.
