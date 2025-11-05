# Ukuran layar
width = 10
height = 5

# Titik yang akan ditampilkan
x = 3
y = 2

# Membuat layar menggunakan simbol '.'
for row in range(height):
    for col in range(width):
        if col == x and row == y:
            print("X", end=" ")
        else:
            print(".", end=" ")
    print()  # ganti baris
