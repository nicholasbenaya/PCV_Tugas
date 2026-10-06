# Laporan Tugas 5: Operasi Morfologi Citra (Erosi, Dilasi, Opening, Closing)

Mata Kuliah: **Praktikum Pengolahan Citra dan Visi Komputer (PCV)**  
Berkas Program: [`5-morphology.py`](5-morphology.py)

---

## 📌 Ringkasan Tugas
Morfologi matematika adalah teknik pengolahan citra berbasis bentuk geometris objek biner menggunakan suatu matriks kecil yang disebut **Structuring Element (SE)** atau elemen penstruktur:
1. **Erosi (Erosion):** Mengikis batas objek, mengecilkan ukuran objek putih, dan membuang tonjolan/noise kecil di luar.
2. **Dilasi (Dilation):** Memperluas batas objek, memperbesar area putih, dan menutup celah sempit atau lubang kecil.
3. **Opening (Pembukaan):** Operasi Erosi diikuti Dilasi. Berfungsi membersihkan derau bintik putih luar tanpa mengubah dimensi utama objek.
4. **Closing (Penutupan):** Operasi Dilasi diikuti Erosi. Berfungsi menutup lubang/rongga hitam di dalam objek dan menyambungkan garis putus-putus.
5. **Morphological Gradient:** Selisih antara citra hasil Dilasi dan Erosi, menghasilkan garis batas tepi (*outline*) morfologi.

---

## 🧠 Dasar Teori & Notasi Matematika

Jika $A$ adalah citra biner dan $B$ adalah *Structuring Element*:

* **Erosi ($A \ominus B$):**
  $$A \ominus B = \{z \mid (B)_z \subseteq A\}$$
  Piksel bernilai $1$ (putih) hanya jika seluruh titik pada kernel $B$ berada di dalam objek $A$.

* **Dilasi ($A \oplus B$):**
  $$A \oplus B = \{z \mid (\hat{B})_z \cap A \ne \emptyset\}$$
  Piksel bernilai $1$ jika minimal ada satu titik pada kernel $B$ yang bersentuhan dengan objek $A$.

* **Opening ($A \circ B$):**
  $$A \circ B = (A \ominus B) \oplus B$$

* **Closing ($A \bullet B$):**
  $$A \bullet B = (A \oplus B) \ominus B$$

* **Morphological Gradient ($G(A)$):**
  $$G(A) = (A \oplus B) - (A \ominus B)$$

---

## 🔬 Hasil Eksperimen

### 1. Citra Masukan Biner Ber-Noise (Input)
Citra sampel yang memiliki objek teks "PCV" & bentuk geometris, dengan derau bintik putih di luar (salt) dan rongga lubang hitam di dalam (pepper):

![Citra Input](sample.jpg)

---

### 2. Hasil Visualisasi Operasi Morfologi (9 Panel)
Grafik komparatif evaluasi operasi morfologi terhadap penghilangan derau dan pemulihan bentuk objek:

![Hasil Morfologi](hasil_morfologi.png)

> **Analisis Hasil Komparatif:**
> 1. **Erosi (Panel 2 & Panel 8-9):**
>    - Mengikis batas luar objek dan membuat garis teks menjadi lebih tipis.
>    - Berhasil menghapus bintik putih kecil di latar belakang, namun memperbesar lubang hitam di dalam objek.
> 2. **Dilasi (Panel 3):**
>    - Mempertebal objek dan menutup lubang-lubang hitam kecil di dalam objek, namun memperbesar ukuran bintik putih di latar belakang.
> 3. **Opening (Panel 4):**
>    - **Sangat efektif membersihkan bintik noise putih di luar objek** secara tuntas, sementara ukuran objek utama tetap terjaga normal.
> 4. **Closing (Panel 5):**
>    - **Sangat efektif menutup seluruh lubang hitam di dalam objek**, membuat permukaan objek solid dan menyambungkan celah sempit.
> 5. **Pembersihan Total (Panel 6 - Open lalu Close):**
>    - Menggabungkan keunggulan keduanya: bintik luar hilang total dan lubang dalam tertutup sempurna!
> 6. **Morphological Gradient (Panel 7):**
>    - Menampilkan kontur garis tepi luar dan dalam objek dengan ketebalan yang seragam.

---

## 💻 Cara Menjalankan Berkas
Masuk ke direktori tugas ini lalu jalankan:
```bash
python 5-morphology.py
```
Seluruh proses transformasi morfologi akan dieksekusi dan hasilnya tersimpan ke berkas `hasil_morfologi.png`.
