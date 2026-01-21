from ursina import *
import random
import math

# =====================
# INISIALISASI APLIKASI
# =====================
app = Ursina()

# =====================
# VARIABEL GAME
# =====================
score = 0
lives = 3
fall_count = 0  # Hitung jumlah jatuh dari platform kuning
game_over = False
was_on_gold_platform = False  # Tandai apakah baru saja meninggalkan platform kuning

# =====================
# UI (TEKS LAYAR)
# =====================
# TRANSLASI: Posisi teks di layar menggunakan koordinat 2D
# Semua teks UI disembunyikan (visible=False)
score_text = Text(text=f'Skor: {score}', position=(-0.85, 0.45), scale=2, visible=False)
lives_text = Text(text=f'Nyawa: {lives}', position=(-0.85, 0.40), scale=2, visible=False)
fall_text = Text(text=f'Jatuh: {fall_count}/3', position=(-0.85, 0.35), scale=2, visible=False)
message_text = Text(text='', position=(0,0), scale=3, origin=(0,0))

# =====================
# KARAKTER ROBLOX
# =====================
class RobloxCharacter(Entity):
    def __init__(self):
        super().__init__()

        # === PEMBUATAN BLOK KEPALA ===
        # SKALA: scale=0.8 membuat kubus lebih kecil (80% dari ukuran asli)
        # TRANSLASI: position=(0,1.4,0) memindahkan kepala ke atas (y=1.4)
        self.head = Entity(model='cube', color=color.rgb(255,220,100),
                           scale=0.8, position=(0,1.4,0), parent=self)

        # === PEMBUATAN WAJAH KARAKTER ===
        # MATA KIRI
        # SKALA: scale=0.12 membuat mata kecil
        # TRANSLASI: position=(-0.2, 1.5, -0.41) memindahkan ke kiri atas DEPAN kepala (z negatif = depan)
        self.left_eye = Entity(model='sphere', color=color.black,
                               scale=0.12, position=(-0.2, 1.5, -0.41), parent=self)
        
        # MATA KANAN
        # SKALA: scale=0.12 sama dengan mata kiri
        # TRANSLASI: position=(0.2, 1.5, -0.41) memindahkan ke kanan atas DEPAN kepala (z negatif = depan)
        # REFLEKSI: Posisi x berlawanan dengan mata kiri (simetri cermin)
        self.right_eye = Entity(model='sphere', color=color.black,
                                scale=0.12, position=(0.2, 1.5, -0.41), parent=self)
        
        # MULUT
        # SKALA: scale=(0.3, 0.08, 0.08) membuat mulut pipih dan memanjang horizontal
        # TRANSLASI: position=(0, 1.25, -0.41) di tengah bawah wajah DEPAN (z negatif = depan)
        self.mouth = Entity(model='cube', color=color.black,
                            scale=(0.3, 0.08, 0.08), position=(0, 1.25, -0.41), parent=self)

        # === PEMBUATAN BLOK BADAN ===
        # SKALA NON-UNIFORM: scale=(1,1,0.5) - lebar=1, tinggi=1, kedalaman=0.5
        # TRANSLASI: position=(0,0.5,0) menempatkan badan di tengah
        self.body = Entity(model='cube', color=color.red,
                           scale=(1,1,0.5), position=(0,0.5,0), parent=self)

        # === PEMBUATAN BLOK LENGAN KIRI ===
        # SKALA: scale=(0.3,0.8,0.3) membuat lengan tipis dan panjang
        # TRANSLASI: position=(-0.65,0.5,0) memindahkan ke KIRI (x negatif)
        self.left_arm = Entity(model='cube', color=color.rgb(255,220,100),
                               scale=(0.3,0.8,0.3), position=(-0.65,0.5,0), parent=self)

        # === PEMBUATAN BLOK LENGAN KANAN ===
        # SKALA: scale=(0.3,0.8,0.3) sama dengan lengan kiri
        # TRANSLASI: position=(0.65,0.5,0) memindahkan ke KANAN (x positif)
        # REFLEKSI: Posisi x berlawanan dengan lengan kiri (simetri cermin terhadap sumbu Y)
        self.right_arm = Entity(model='cube', color=color.rgb(255,220,100),
                                scale=(0.3,0.8,0.3), position=(0.65,0.5,0), parent=self)

        # === PEMBUATAN BLOK KAKI KIRI ===
        # SKALA: scale=(0.4,1,0.4) membuat kaki agak tebal
        # TRANSLASI: position=(-0.3,-0.5,0) memindahkan ke KIRI dan BAWAH
        self.left_leg = Entity(model='cube', color=color.blue,
                               scale=(0.4,1,0.4), position=(-0.3,-0.5,0), parent=self)

        # === PEMBUATAN BLOK KAKI KANAN ===
        # SKALA: scale=(0.4,1,0.4) sama dengan kaki kiri
        # TRANSLASI: position=(0.3,-0.5,0) memindahkan ke KANAN dan BAWAH
        # REFLEKSI: Posisi x berlawanan dengan kaki kiri (simetri cermin terhadap sumbu Y)
        self.right_leg = Entity(model='cube', color=color.blue,
                                scale=(0.4,1,0.4), position=(0.3,-0.5,0), parent=self)

        # TRANSLASI: Posisi awal karakter di dunia 3D
        self.position = (0,5,0)
        self.velocity_y = 0
        self.on_ground = False

character = RobloxCharacter()

# =====================
# KAMERA
# =====================
# TRANSLASI: Posisi kamera di koordinat dunia
# ROTASI: rotation_x=-10 memutar kamera sedikit ke bawah (melihat karakter dari atas)
camera.position = (0,10,20)
camera.rotation_x = -10

# =====================
# GROUND (PEMBUATAN BLOK TANAH)
# =====================
# SKALA: scale=(200,1,200) membuat bidang sangat lebar tapi tipis (y=1)
# TRANSLASI: Posisi default (0,0,0) menempatkan ground di pusat
ground = Entity(
    model='plane',
    scale=(200,1,200),
    texture='white_cube',
    texture_scale=(100,100),
    collider='box',
    color=color.rgb(34,139,34)
)

# =====================
# LIST OBJEK
# =====================
platforms = []
coins = []
obstacles = []
robots = []

# =====================
# PLATFORM (PEMBUATAN BLOK PLATFORM)
# =====================
def create_platform(pos, scale_size, col, ptype='normal'):
    # TRANSLASI: pos menentukan posisi platform di dunia
    # SKALA: scale_size menentukan ukuran platform (lebar, tinggi, panjang)
    p = Entity(
        model='cube',
        position=pos,
        scale=scale_size,
        color=col,
        collider='box'
    )
    p.platform_type = ptype

    if ptype == 'moving':
        p.direction = 1
        p.original_x = pos[0]
        p.move_speed = 3  # Kecepatan translasi horizontal
    elif ptype == 'rotating':
        p.rotation_speed = 50  # Kecepatan rotasi dalam derajat per detik
    elif ptype == 'scaling':
        p.original_scale = scale_size
        p.scale_phase = 0
        p.scale_speed = 1.5  # Kecepatan perubahan skala

    platforms.append(p)
    return p

# === PEMBUATAN PLATFORM AWAL ===
# TRANSLASI: (0,0,0) di pusat dunia
# SKALA: (12,1,12) platform lebar dan datar
create_platform((0,0,0),(12,1,12),color.green)

# === PEMBUATAN PLATFORM BERTINGKAT ===
# TRANSLASI: Loop membuat 5 platform dengan posisi y dan z berubah
# Pola: setiap platform naik 3 unit (y) dan mundur 10 unit (z)
for i in range(1,6):
    create_platform((0,i*3,-i*10),(6,1,6),color.orange)

# === PLATFORM BERGERAK (MOVING) ===
# TRANSLASI DINAMIS: Platform akan bergerak kiri-kanan (translasi x berubah)
# SKALA: (5,1,5) platform berukuran sedang
for i in range(3):
    create_platform((0,20+i,-70-i*12),(5,1,5),color.violet,'moving')

# === PLATFORM BERPUTAR (ROTATING) ===
# ROTASI DINAMIS: Platform akan berputar pada sumbu Y
# TRANSLASI: Posisi lebih tinggi (y=25+i) dan lebih jauh (z=-110-i*12)
for i in range(3):
    create_platform((0,25+i,-110-i*12),(6,1,6),color.pink,'rotating')

# === PLATFORM SCALING ===
# SKALA DINAMIS: Platform akan membesar dan mengecil secara periodik
# TRANSLASI: Posisi paling tinggi (y=30+i) dan paling jauh (z=-150-i*12)
for i in range(3):
    create_platform((0,30+i,-150-i*12),(5,1,5),color.cyan,'scaling')

# === PLATFORM FINISH (WARNA KUNING/GOLD) ===
# TRANSLASI: Posisi paling akhir di (0,40,-200)
# SKALA: (10,1,10) platform besar sebagai tujuan akhir
finish_platform = create_platform((0,40,-200),(10,1,10),color.gold,'finish')
finish_platform.is_gold = True  # Tandai sebagai platform kuning

# =====================
# KOIN (PEMBUATAN BLOK KOIN)
# =====================
# TRANSLASI: Loop membuat 12 koin dengan posisi y dan z yang berubah
# SKALA: scale=0.6 membuat koin kecil (60% dari ukuran asli)
for i in range(12):
    c = Entity(
        model='sphere',
        color=color.gold,
        scale=0.6,
        position=(0,i*3+4,-i*15-8),  # TRANSLASI: y naik, z mundur
        collider='sphere'
    )
    c.collected = False
    coins.append(c)

# =====================
# OBSTACLE (PEMBUATAN BLOK RINTANGAN)
# =====================
# TRANSLASI: Loop membuat 10 obstacle dengan posisi acak
# SKALA: scale=(1.2,2.5,1.2) membuat obstacle tinggi dan ramping
for i in range(10):
    o = Entity(
        model='cube',
        color=color.red,
        scale=(1.2,2.5,1.2),
        position=(random.choice([-4,0,4]), i*3+3, -i*20-30),  # TRANSLASI acak x
        collider='box'
    )
    obstacles.append(o)

# =====================
# ROBOT MUSUH (PEMBUATAN BLOK ROBOT + ROTASI + WAJAH)
# =====================
class EnemyRobot(Entity):
    def __init__(self, pos):
        # === PEMBUATAN BLOK BADAN ROBOT ===
        # TRANSLASI: pos menentukan posisi robot
        # SKALA: scale=(1.5,2.5,1.5) membuat robot besar dan tinggi
        super().__init__(
            model='cube',
            color=color.gray,
            scale=(1.5,2.5,1.5),
            position=pos,
            collider='box'
        )

        # === PEMBUATAN BLOK MATA KIRI ===
        # SKALA: scale=0.15 membuat mata kecil
        # TRANSLASI: position=(-0.35, 0.6, 0.8) memindahkan ke kiri atas depan
        Entity(
            model='sphere',
            color=color.black,
            scale=0.15,
            position=(-0.35, 0.6, 0.8),
            parent=self
        )

        # === PEMBUATAN BLOK MATA KANAN ===
        # SKALA: scale=0.15 sama dengan mata kiri
        # TRANSLASI: position=(0.35, 0.6, 0.8) memindahkan ke kanan atas depan
        # REFLEKSI: Posisi x berlawanan dengan mata kiri (simetri cermin)
        Entity(
            model='sphere',
            color=color.black,
            scale=0.15,
            position=(0.35, 0.6, 0.8),
            parent=self
        )

        # === PEMBUATAN BLOK MULUT ===
        # SKALA: scale=(0.4, 0.1, 0.1) membuat mulut pipih dan memanjang horizontal
        # TRANSLASI: position=(0, 0.35, 0.8) di tengah bawah wajah
        Entity(
            model='cube',
            color=color.black,
            scale=(0.4, 0.1, 0.1),
            position=(0, 0.35, 0.8),
            parent=self
        )

        # ROTASI DINAMIS: Robot akan berputar dengan kecepatan acak
        self.rotation_speed = random.choice([60,90,120])

# TRANSLASI: Loop membuat 5 robot dengan posisi acak
for i in range(5):
    r = EnemyRobot((random.choice([-5,0,5]), i*5+5, -i*30-50))
    robots.append(r)

# =====================
# UPDATE
# =====================
def update():
    global score, lives, game_over, fall_count, was_on_gold_platform
    if game_over:
        return

    speed = 10 * time.dt

    # === TRANSLASI KARAKTER (PERGERAKAN) ===
    # Tombol W/A/S/D mengubah posisi x dan z karakter
    if held_keys['w']: character.z -= speed  # TRANSLASI: Maju (z negatif)
    if held_keys['s']: character.z += speed  # TRANSLASI: Mundur (z positif)
    if held_keys['a']: character.x -= speed  # TRANSLASI: Kiri (x negatif)
    if held_keys['d']: character.x += speed  # TRANSLASI: Kanan (x positif)

    # === ROTASI KARAKTER ===
    # Memutar karakter sesuai arah gerakan
    target_rotation = None
    if held_keys['w']: target_rotation = 0      # ROTASI: Menghadap depan (0°)
    elif held_keys['s']: target_rotation = 180  # ROTASI: Menghadap belakang (180°)
    elif held_keys['a']: target_rotation = -90  # ROTASI: Menghadap kiri (-90°)
    elif held_keys['d']: target_rotation = 90   # ROTASI: Menghadap kanan (90°)

    if target_rotation is not None:
        # ROTASI SMOOTH: Interpolasi rotasi untuk gerakan halus
        character.rotation_y = lerp(character.rotation_y, target_rotation, 8*time.dt)

    # === TRANSLASI VERTIKAL (LOMPAT DAN GRAVITASI) ===
    if held_keys['space'] and character.on_ground:
        character.velocity_y = 12  # TRANSLASI: Lompat ke atas

    character.velocity_y -= 30 * time.dt  # Gravitasi (translasi ke bawah)
    character.y += character.velocity_y * time.dt  # TRANSLASI: Update posisi Y

    # Deteksi collision dengan ground/platform
    ray = raycast(
        origin=character.world_position + Vec3(0,2,0),
        direction=Vec3(0,-1,0),
        distance=3,
        ignore=[character]
    )

    if ray.hit:
        character.y = ray.world_point.y + 1  # TRANSLASI: Reset posisi ke atas platform
        character.velocity_y = 0
        character.on_ground = True
        
        # === CEK APAKAH DI PLATFORM KUNING ===
        # Tandai jika karakter sedang berada di platform kuning (gold)
        hit_entity = ray.entity
        if hasattr(hit_entity, 'is_gold') and hit_entity.is_gold:
            was_on_gold_platform = True  # Pernah di platform kuning
    else:
        character.on_ground = False

    # === TRANSLASI KAMERA ===
    # Kamera mengikuti karakter dengan offset
    camera.position = (character.x, character.y+10, character.z+20)
    camera.look_at(character)

    # === ANIMASI PLATFORM ===
    for p in platforms:
        if p.platform_type == 'moving':
            # TRANSLASI HORIZONTAL: Platform bergerak kiri-kanan
            p.x += p.direction * p.move_speed * time.dt
            if abs(p.x - p.original_x) > 10:
                p.direction *= -1  # Balik arah
        elif p.platform_type == 'rotating':
            # ROTASI: Platform berputar pada sumbu Y
            p.rotation_y += p.rotation_speed * time.dt
        elif p.platform_type == 'scaling':
            # SKALA DINAMIS: Platform membesar dan mengecil
            p.scale_phase += p.scale_speed * time.dt
            s = 1 + 0.5 * abs(math.sin(p.scale_phase))
            p.scale = (p.original_scale[0]*s, p.original_scale[1], p.original_scale[2]*s)

    # === ROTASI KOIN ===
    for c in coins:
        if not c.collected:
            c.rotation_y += 150 * time.dt  # ROTASI: Koin berputar
            if character.intersects(c).hit:
                c.collected = True
                c.visible = False
                score += 100
                score_text.text = f'Skor: {score}'

    # === ROTASI OBSTACLE ===
    for o in obstacles:
        o.rotation_y += 60 * time.dt  # ROTASI: Obstacle berputar
        if character.intersects(o).hit:
            lives -= 1
            lives_text.text = f'Nyawa: {lives}'
            character.position = (0,5,0)  # TRANSLASI: Reset posisi
            character.velocity_y = 0

    # === ROTASI ROBOT ===
    for r in robots:
        r.rotation_y += r.rotation_speed * time.dt  # ROTASI: Robot berputar
        if character.intersects(r).hit:
            lives -= 1
            lives_text.text = f'Nyawa: {lives}'
            character.position = (0,5,0)  # TRANSLASI: Reset posisi
            character.velocity_y = 0

    # === DETEKSI JATUH DARI PLATFORM KUNING ===
    # Jika karakter jatuh di bawah y = -20, berarti jatuh dari tumpuan
    if character.y < -20:
        # Hanya hitung jatuh jika pernah berada di platform kuning
        if was_on_gold_platform:
            fall_count += 1  # Tambah hitungan jatuh dari platform kuning
            fall_text.text = f'Jatuh: {fall_count}/3'
            was_on_gold_platform = False  # Reset status
        
        # TRANSLASI: Kembali ke START (platform hijau di posisi awal)
        character.position = (0, 5, 0)
        character.velocity_y = 0
        
        # Cek apakah sudah jatuh 3 kali atau lebih
        if fall_count >= 3:
            message_text.text = 'GAME OVER - Jatuh 3x dari platform kuning! Tekan R'
            game_over = True

    if lives <= 0:
        message_text.text = 'GAME OVER - R untuk Restart'
        game_over = True

# =====================
# INPUT
# =====================
def input(key):
    global game_over, lives, score
    if key == 'r' and game_over:
        game_over = False
        lives = 3
        score = 0
        score_text.text = f'Skor: {score}'
        lives_text.text = f'Nyawa: {lives}'
        message_text.text = ''
        character.position = (0,5,0)  # TRANSLASI: Reset posisi karakter
        for c in coins:
            c.collected = False
            c.visible = True

# =====================
# UI INFO (PEMBUATAN BLOK INFO PANEL)
# =====================
# SKALA: scale=(0.45,0.35) menentukan ukuran panel
# TRANSLASI: position=(0.65,0.22) menempatkan panel di kanan bawah layar
info_panel = Entity(
    model='quad',
    color=color.rgba(0,0,0,200),
    scale=(0.45,0.35),
    position=(0.65,0.22),
    parent=camera.ui
)

Text(
    parent=info_panel,
    text='''
KONTROL:
W A S D - Gerak
SPACE - Lompat

''',
    scale=2.1,
    origin=(0,0),
    position=(0,0.12)
)

# =====================
# LINGKUNGAN
# =====================
Sky(color=color.rgb(135,206,235))
DirectionalLight().look_at(Vec3(-1,-1,-1))
AmbientLight(color=color.rgba(100,100,100,0.5))

# =====================
# RUN
# =====================
app.run()