import math

# Input titik
x1 = float(input("Masukkan x1: "))
y1 = float(input("Masukkan y1: "))
x2 = float(input("Masukkan x2: "))
y2 = float(input("Masukkan y2: "))

# Hitung jarak Euclidean
jarak = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Menentukan kuadran titik pertama
if x1 > 0 and y1 > 0:
    kuadran = "Kuadran I"
elif x1 < 0 and y1 > 0:
    kuadran = "Kuadran II"
elif x1 < 0 and y1 < 0:
    kuadran = "Kuadran III"
elif x1 > 0 and y1 < 0:
    kuadran = "Kuadran IV"
elif x1 == 0 and y1 == 0:
    kuadran = "Titik pusat (0,0)"
elif x1 == 0:
    kuadran = "Berada pada sumbu Y"
else:
    kuadran = "Berada pada sumbu X"

# Output
print("\n=== HASIL ===")
print(f"Titik pertama: ({x1}, {y1})")
print(f"Titik kedua  : ({x2}, {y2})")
print(f"Jarak antar titik: {round(jarak, 2)}")
print(f"Titik pertama berada di: {kuadran}")