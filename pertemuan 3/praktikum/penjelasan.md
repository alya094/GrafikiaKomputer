TugasPraktikum.py
<img width="1101" height="860" alt="Screenshot 2025-11-05 120650" src="https://github.com/user-attachments/assets/88e98175-ce78-4222-ac47-e47470c5f2d5" />
Program di atas terdiri dari dua bagian.
Pada bagian pertama, program membuat kotak grid berukuran 10x10 yang diisi dengan tanda titik (“.”) sebagai piksel kosong. Lalu, pada posisi (4,6) diganti menjadi huruf “X”. Bagian ini menggambarkan cara kerja gambar raster, yaitu gambar yang tersusun dari kumpulan titik atau piksel di dalam sebuah kotak.
Sedangkan pada bagian kedua, program menghitung dan menampilkan titik-titik koordinat dari garis yang ditarik dari (0,0) ke (5,3). Setiap titik dihitung menggunakan rumus perbandingan jarak agar garis terbentuk secara bertahap. Bagian ini menunjukkan gambar vektor, yang digambar menggunakan koordinat dan rumus matematika, bukan dari kumpulan piksel seperti pada raster.
tabel perbandingan vektor dan raster:
<img width="639" height="617" alt="image" src="https://github.com/user-attachments/assets/bb355ddc-9fca-4b02-a8ea-ebd85465ac7d" />

KoordinatTitik.py
<img width="693" height="663" alt="Screenshot 2025-11-05 121823" src="https://github.com/user-attachments/assets/3ed31a4e-afb8-4231-b05d-e4b35c22ee20" />
Program di atas digunakan untuk menampilkan pola berbentuk kotak menggunakan tanda titik (“.”). Berikut penjelasannya:
1.	for y in range(0, 5):
Perulangan ini mengatur jumlah baris yang akan ditampilkan, yaitu dari 0 sampai 4 (total 5 baris).
2.	for x in range(0, 10):
Perulangan di dalamnya mengatur jumlah kolom pada setiap baris, yaitu dari 0 sampai 9 (total 10 kolom).
3.	print(".", end="")
Perintah ini mencetak tanda titik (“.”) tanpa membuat baris baru, sehingga titik-titik dicetak berdampingan secara horizontal dalam satu baris.
4.	print()
Baris ini membuat pindah ke baris baru setelah satu baris titik selesai dicetak, sehingga hasilnya terlihat seperti kotak berisi 5 baris dan 10 kolom titik.

praktikum1.py
<img width="975" height="866" alt="Screenshot 2025-11-05 123226" src="https://github.com/user-attachments/assets/718802e9-d4e7-425b-828a-be2bfe4146b5" />
Input :x1, y1, x2, y2 dibaca dari pengguna sebagai angka desimal (float).
Menghitung jarak
1.	Rumus yang dipakai: jarak = sqrt((x2 - x1)^2 + (y2 - y1)^2).
2.	Fungsi math.sqrt mengambil akar kuadrat dari jumlah kuadrat selisih koordinat.
3.	Hasil jarak kemudian dibulatkan saat ditampilkan (round(jarak, 2)), jadi tampil dengan 2 angka di belakang koma.
Menentukan kuadran untuk titik pertama (x1,y1)
1.	Jika x1 > 0 dan y1 > 0 → Kuadran I (kanan atas).
2.	Jika x1 < 0 dan y1 > 0 → Kuadran II (kiri atas).
3.	Jika x1 < 0 dan y1 < 0 → Kuadran III (kiri bawah).
4.	Jika x1 > 0 dan y1 < 0 → Kuadran IV (kanan bawah).
5.	Jika x1 == 0 dan y1 == 0 → Titik pusat (0,0).
6.	Jika x1 == 0 (tapi y1 ≠ 0) → Berada pada sumbu Y.
7.	Jika kondisi di atas tidak terpenuhi (sisa kasus) → Berada pada sumbu X.

praktikum2.py
<img width="983" height="810" alt="Screenshot 2025-11-05 124337" src="https://github.com/user-attachments/assets/4d4ab3be-323b-4206-b86c-c14e506c9cb5" />
Program ini membuat tampilan grid berukuran 10 kolom dan 5 baris menggunakan simbol titik (.). Nilai x = 3 dan y = 2 menunjukkan posisi yang akan diganti dengan huruf “X”. Dua perulangan digunakan: yang pertama untuk baris (row), dan yang kedua untuk kolom (col). Setiap kali posisi kolom dan baris sama dengan nilai x dan y, program mencetak “X”; jika tidak, mencetak “.”. Perintah print() tanpa argumen di akhir setiap baris digunakan untuk pindah ke baris berikutnya. Hasil akhirnya adalah grid dengan satu titik “X” di koordinat (3,2).

raster.py
<img width="964" height="793" alt="Screenshot 2025-11-05 130742" src="https://github.com/user-attachments/assets/8f3bc875-0a9d-4601-9119-c40b69470ae5" />
Program ini menampilkan grid berukuran 5x5 menggunakan simbol titik (.). Pada setiap posisi, program memeriksa apakah koordinatnya berada di (2,3). Jika ya, maka dicetak huruf "X"; jika tidak, dicetak ".". Perintah print() di akhir digunakan untuk pindah ke baris baru, sehingga terbentuk tampilan grid dengan satu titik “X” di baris keempat dan kolom ketiga.

vektor.py
<img width="893" height="638" alt="Screenshot 2025-11-05 131202" src="https://github.com/user-attachments/assets/7c611d9b-fb58-43b9-a1cd-bcd3d263ca93" />
Program ini menghitung dan menampilkan titik-titik di antara dua koordinat, yaitu dari (0,0) ke (5,3). Nilai n = 5 berarti garis dibagi menjadi lima bagian sama panjang. Dalam setiap iterasi, rumus interpolasi linier digunakan untuk menghitung posisi x dan y pada titik ke-i, lalu hasilnya dicetak dalam format desimal satu angka di belakang koma.
