import turtle
import time

# -------------------------
# SETUP TURTLE CANVAS
# -------------------------
turtle.title("Praktikum Garis, Lingkaran, dan Poligon")
turtle.speed(0)
turtle.bgcolor("white")
turtle.color("black")
turtle.penup()


# ============================================================
#            ALGORITMA GARIS (DDA)
# ============================================================
def DDA(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    steps = int(max(abs(dx), abs(dy)))

    x_inc = dx / steps
    y_inc = dy / steps

    x = x1
    y = y1

    for i in range(steps):
        turtle.goto(round(x), round(y))
        turtle.dot(3, "black")
        x += x_inc
        y += y_inc
        time.sleep(0.001)


# ============================================================
#        ALGORITMA MIDPOINT CIRCLE
# ============================================================
def draw_circle_midpoint(x_center, y_center, r):

    def plot_circle_points(xc, yc, x, y):
        points = [
            (xc + x, yc + y),
            (xc - x, yc + y),
            (xc + x, yc - y),
            (xc - x, yc - y),
            (xc + y, yc + x),
            (xc - y, yc + x),
            (xc + y, yc - x),
            (xc - y, yc - x),
        ]
        for p in points:
            turtle.goto(p[0], p[1])
            turtle.dot(3, "red")
            time.sleep(0.001)

    x = 0
    y = r
    d = 1 - r

    plot_circle_points(x_center, y_center, x, y)

    while x < y:
        x += 1
        if d < 0:
            d += 2 * x + 1
        else:
            y -= 1
            d += 2 * (x - y) + 1

        plot_circle_points(x_center, y_center, x, y)


# ============================================================
#              POLIGON (DDA)
# ============================================================
def draw_polygon(points):
    n = len(points)
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        DDA(x1, y1, x2, y2)


# ============================================================
#        GAMBAR + TULISAN DI ATAS GAMBAR
# ============================================================

# ------- GARIS (KIRI) -------
# Posisi gambar garis
gx1, gy1 = -350, -50
gx2, gy2 = -150, 100

# TULISAN
turtle.goto((gx1 + gx2) / 2, gy2 + 40)
turtle.write("Garis (DDA)", align="center", font=("Arial", 12, "bold"))

# Gambar garis
DDA(gx1, gy1, gx2, gy2)


# ------- LINGKARAN (TENGAH) -------
cx, cy, r = 0, -20, 120

# TULISAN
turtle.goto(cx, cy + r + 40)
turtle.write("Lingkaran (Midpoint)", align="center", font=("Arial", 12, "bold"))

# Gambar lingkaran
draw_circle_midpoint(cx, cy, r)


# ------- POLIGON (KANAN) -------
persegi = [(200, -50), (350, -50), (350, 100), (200, 100)]

# Cari titik atas poligon (untuk tulisannya)
max_y = max(y for (_, y) in persegi)

# TULISAN
turtle.goto(275, max_y + 40)
turtle.write("Poligon (Persegi)", align="center", font=("Arial", 12, "bold"))

# Gambar poligon
draw_polygon(persegi)


turtle.hideturtle()
turtle.done()
