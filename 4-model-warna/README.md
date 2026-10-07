# Laporan Tugas 4: Konversi Model Warna (RGB, CMYK, HSI, HSV)

Mata Kuliah: Praktikum Pengolahan Citra dan Visi Komputer (PCV)  
Berkas Program: [`4-model-warna.py`](4-model-warna.py)

---

## Ringkasan Tugas

Eksplorasi dan komparasi representasi citra pada empat model ruang warna utama:
1. **RGB (Red, Green, Blue)**: Model warna aditif untuk perangkat layar monitor.
2. **CMYK (Cyan, Magenta, Yellow, Key/Black)**: Model warna subtraktif standar proses percetakan fisik.
3. **HSI (Hue, Saturation, Intensity)**: Model yang memodelkan persepsi visual manusia dengan memisahkan rona dan saturasi dari intensitas kecerahan rata-rata.
4. **HSV (Hue, Saturation, Value)**: Model kerucut heksagonal yang merepresentasikan warna berdasarkan rona, kejenuhan, dan kecerahan maksimum.

---

## Dasar Teori dan Perumusan Matematis

### 1. Model Warna CMYK (Subtraktif)
Dari nilai RGB yang dinormalisasi ke rentang $[0, 1]$:
- **Kanal K (Black / Key):**
  $$K = 1 - \max(R, G, B)$$
- **Kanal Cyan ($C$), Magenta ($M$), dan Yellow ($Y$):**
  $$C = \frac{1 - R - K}{1 - K}, \quad M = \frac{1 - G - K}{1 - K}, \quad Y = \frac{1 - B - K}{1 - K}$$
  *(Jika $K = 1$, maka $C = M = Y = 0$)*
- **Rekonstruksi CMYK $\rightarrow$ RGB:**
  $$R = 255 \times (1 - C) \times (1 - K)$$
  $$G = 255 \times (1 - M) \times (1 - K)$$
  $$B = 255 \times (1 - Y) \times (1 - K)$$

---

### 2. Model Warna HSI (Human Perception)
Berdasarkan formulasi standar Digital Image Processing (Gonzalez & Woods):
- **Intensitas ($I$):**
  $$I = \frac{R + G + B}{3}$$
- **Saturasi ($S$):**
  $$S = 1 - \frac{3}{R + G + B} \min(R, G, B) \quad (\text{jika } R+G+B = 0 \Rightarrow S = 0)$$
- **Hue ($H$):**
  $$\theta = \arccos\left(\frac{\frac{1}{2}[(R - G) + (R - B)]}{\sqrt{(R - G)^2 + (R - B)(G - B)}}\right)$$
  $$H = \begin{cases} \theta, & \text{jika } B \le G \\ 360^\circ - \theta, & \text{jika } B > G \end{cases}$$

---

### 3. Model Warna HSV (Hexcone Model)
- **Value ($V$):** $V = \max(R, G, B)$
- **Saturation ($S$):** $S = \frac{V - \min(R, G, B)}{V}$ *(jika $V = 0 \Rightarrow S = 0$)*
- **Hue ($H$):** Menghitung sudut rotasi warna berdasarkan kanal dengan nilai maksimum.

---

## Hasil Eksperimen

### 1. Citra Masukan
Citra sampel spektrum warna yang digunakan dalam pengujian:

![Citra Input](sample.jpg)

---

### 2. Dekomposisi Kanal dan Rekonstruksi (16 Panel)
Grafik komparatif menampilkan dekomposisi setiap kanal warna beserta hasil rekonstruksi kembali ke RGB:

![Hasil Model Warna](hasil_model_warna.png)

Analisis visual dekomposisi kanal:
1. **RGB (Baris 1):** Daerah berwarna merah memiliki nilai intensitas tertinggi pada kanal R, daerah hijau pada kanal G, dan daerah biru pada kanal B.
2. **CMYK (Baris 2):** Bekerja berdasarkan prinsip penyerapan pigmen (subtraktif). Warna merah menyerap cahaya Cyan sehingga kanal C bernilai rendah (gelap), sedangkan pigmen Cyan menghasilkan nilai kanal C tinggi (terang).
3. **HSI (Baris 3):** Memisahkan kromatisitas ($H$ dan $S$) dari tingkat kecerahan rata-rata ($I$). Hasil rekonstruksi $HSI \rightarrow RGB$ memulihkan distribusi warna asli secara akurat.
4. **HSV (Baris 4):** Komponen Value menggunakan nilai intensitas maksimum dari ketiga kanal, menghasilkan distribusi intensitas yang berbeda dari rata-rata pada HSI.

---

## Panduan Menjalankan Program

Jalankan perintah berikut di terminal:
```bash
python 4-model-warna/4-model-warna.py
```
Seluruh proses dekomposisi dan rekonstruksi akan dieksekusi, lalu grafik 16 panel disimpan ke `hasil_model_warna.png`.
