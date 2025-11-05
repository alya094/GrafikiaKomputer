#soal 1
# Ukuran grid
rows, cols = 10, 10

# Membuat grid awal dengan "."
grid = [["." for _ in range(cols)] for _ in range(rows)]

# Mengganti piksel di posisi (4,6) menjadi "X"
grid[4][6] = "X"  # indeks mulai dari 0

# Menampilkan grid
for row in grid:
    print(" ".join(row))

#soal 2
# Titik awal dan akhir
x0, y0 = 0, 0
x1, y1 = 5, 3

# Hitung jumlah langkah (jarak terbesar di x atau y)
steps = max(abs(x1 - x0), abs(y1 - y0))

# Hitung titik-titik garis
for i in range(steps + 1):
    x = x0 + i * (x1 - x0) / steps
    y = y0 + i * (y1 - y0) / steps
    print(f"({round(x)}, {round(y)})")
