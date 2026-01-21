import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Robot3D:
    def __init__(self):
        self.position = [0, 0, 0]
        self.rotation = [0, 0, 0]  # Rotasi dalam derajat untuk X, Y, Z
        self.scale = 1.0
        self.reflection = [1, 1, 1]  # 1 = normal, -1 = refleksi
        
    def create_cube(self, center, size):
        """Membuat kubus dengan center dan ukuran tertentu"""
        x, y, z = center
        s = size / 2
        
        vertices = np.array([
            [x-s, y-s, z-s], [x+s, y-s, z-s], [x+s, y+s, z-s], [x-s, y+s, z-s],
            [x-s, y-s, z+s], [x+s, y-s, z+s], [x+s, y+s, z+s], [x-s, y+s, z+s]
        ])
        
        faces = [
            [vertices[0], vertices[1], vertices[5], vertices[4]],
            [vertices[7], vertices[6], vertices[2], vertices[3]],
            [vertices[0], vertices[3], vertices[7], vertices[4]],
            [vertices[1], vertices[2], vertices[6], vertices[5]],
            [vertices[0], vertices[1], vertices[2], vertices[3]],
            [vertices[4], vertices[5], vertices[6], vertices[7]]
        ]
        
        return faces
    
    def create_cylinder(self, center, radius, height, segments=20):
        """Membuat silinder untuk lengan dan kaki"""
        x, y, z = center
        theta = np.linspace(0, 2*np.pi, segments)
        
        # Lingkaran atas dan bawah
        circle_x = radius * np.cos(theta) + x
        circle_y = radius * np.sin(theta) + y
        
        vertices_bottom = np.column_stack([circle_x, circle_y, np.full(segments, z - height/2)])
        vertices_top = np.column_stack([circle_x, circle_y, np.full(segments, z + height/2)])
        
        faces = []
        # Sisi silinder
        for i in range(segments - 1):
            face = [vertices_bottom[i], vertices_bottom[i+1], 
                   vertices_top[i+1], vertices_top[i]]
            faces.append(face)
        
        return faces
    
    def create_robot_parts(self):
        """Membuat semua bagian robot"""
        parts = {}
        
        # Kepala (kubus)
        parts['head'] = self.create_cube([0, 0, 2.5], 0.8)
        
        # Badan (kubus)
        parts['body'] = self.create_cube([0, 0, 1.2], 1.2)
        
        # Lengan kiri
        parts['left_arm'] = self.create_cylinder([-0.8, 0, 1.2], 0.15, 0.8)
        
        # Lengan kanan
        parts['right_arm'] = self.create_cylinder([0.8, 0, 1.2], 0.15, 0.8)
        
        # Kaki kiri
        parts['left_leg'] = self.create_cylinder([-0.3, 0, 0.1], 0.18, 1.0)
        
        # Kaki kanan
        parts['right_leg'] = self.create_cylinder([0.3, 0, 0.1], 0.18, 1.0)
        
        return parts
    
    def rotation_matrix_x(self, angle):
        """Matriks rotasi terhadap sumbu X"""
        rad = np.radians(angle)
        return np.array([
            [1, 0, 0],
            [0, np.cos(rad), -np.sin(rad)],
            [0, np.sin(rad), np.cos(rad)]
        ])
    
    def rotation_matrix_y(self, angle):
        """Matriks rotasi terhadap sumbu Y"""
        rad = np.radians(angle)
        return np.array([
            [np.cos(rad), 0, np.sin(rad)],
            [0, 1, 0],
            [-np.sin(rad), 0, np.cos(rad)]
        ])
    
    def rotation_matrix_z(self, angle):
        """Matriks rotasi terhadap sumbu Z"""
        rad = np.radians(angle)
        return np.array([
            [np.cos(rad), -np.sin(rad), 0],
            [np.sin(rad), np.cos(rad), 0],
            [0, 0, 1]
        ])
    
    def apply_transformations(self, vertices):
        """Menerapkan semua transformasi pada vertices"""
        transformed = []
        
        for vertex in vertices:
            v = np.array(vertex)
            
            # 1. SKALA
            v = v * self.scale
            
            # 2. ROTASI (X, Y, Z)
            rot_x = self.rotation_matrix_x(self.rotation[0])
            rot_y = self.rotation_matrix_y(self.rotation[1])
            rot_z = self.rotation_matrix_z(self.rotation[2])
            
            v = rot_x @ v
            v = rot_y @ v
            v = rot_z @ v
            
            # 3. REFLEKSI
            v = v * self.reflection
            
            # 4. TRANSLASI
            v = v + self.position
            
            transformed.append(v)
        
        return transformed
    
    def render(self, ax):
        """Menampilkan robot dengan transformasi"""
        ax.clear()
        
        parts = self.create_robot_parts()
        colors = {
            'head': 'lightblue',
            'body': 'blue',
            'left_arm': 'green',
            'right_arm': 'green',
            'left_leg': 'red',
            'right_leg': 'red'
        }
        
        for part_name, faces in parts.items():
            transformed_faces = []
            for face in faces:
                transformed_face = self.apply_transformations(face)
                transformed_faces.append(transformed_face)
            
            poly = Poly3DCollection(transformed_faces, alpha=0.7, 
                                   facecolor=colors[part_name], 
                                   edgecolor='black', linewidth=0.5)
            ax.add_collection3d(poly)
        
        # Setting tampilan
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([-5, 5])
        ax.set_ylim([-5, 5])
        ax.set_zlim([-2, 5])
        ax.set_title('Robot 3D - Transformasi Geometri')
        
        # Panel Panduan Kontrol (Kiri Atas)
        control_text = "═══ PANDUAN KONTROL ═══\n"
        control_text += "┌─ TRANSLASI 3D ─────┐\n"
        control_text += "│ W/S: Maju/Mundur   │\n"
        control_text += "│ A/D: Kiri/Kanan    │\n"
        control_text += "│ Q/E: Naik/Turun    │\n"
        control_text += "├─ ROTASI 3D ────────┤\n"
        control_text += "│ I/K: Putar X ↕     │\n"
        control_text += "│ J/L: Putar Y ↔     │\n"
        control_text += "│ U/O: Putar Z ⟲     │\n"
        control_text += "├─ SKALA 3D ─────────┤\n"
        control_text += "│ +/-: Besar/Kecil   │\n"
        control_text += "├─ REFLEKSI 3D ──────┤\n"
        control_text += "│ 1: Cermin X        │\n"
        control_text += "│ 2: Cermin Y        │\n"
        control_text += "│ 3: Cermin Z        │\n"
        control_text += "├─ LAINNYA ──────────┤\n"
        control_text += "│ R: Reset Semua     │\n"
        control_text += "└────────────────────┘"
        
        ax.text2D(0.02, 0.98, control_text, transform=ax.transAxes, 
                 verticalalignment='top', fontfamily='monospace', fontsize=8,
                 bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.9, edgecolor='navy'))
        
        # Informasi Status Transformasi (Kanan Atas)
        info_text = "═══ STATUS TRANSFORMASI ═══\n"
        info_text += f"📍 Posisi (Translasi):\n"
        info_text += f"   X: {self.position[0]:+.1f}  Y: {self.position[1]:+.1f}  Z: {self.position[2]:+.1f}\n\n"
        info_text += f"🔄 Rotasi (Derajat):\n"
        info_text += f"   X: {self.rotation[0]:+.0f}°  Y: {self.rotation[1]:+.0f}°  Z: {self.rotation[2]:+.0f}°\n\n"
        info_text += f"📏 Skala: {self.scale:.2f}x\n\n"
        info_text += f"🪞 Refleksi:\n"
        ref_status = []
        if self.reflection[0] == -1: ref_status.append("X")
        if self.reflection[1] == -1: ref_status.append("Y")
        if self.reflection[2] == -1: ref_status.append("Z")
        info_text += f"   {'Aktif: ' + ', '.join(ref_status) if ref_status else 'Tidak Aktif'}"
        
        ax.text2D(0.98, 0.98, info_text, transform=ax.transAxes, 
                 verticalalignment='top', horizontalalignment='right',
                 fontfamily='monospace', fontsize=8,
                 bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9, edgecolor='orange'))

# Fungsi kontrol keyboard
def on_key(event, robot, ax, fig):
    step = 0.5
    angle_step = 15
    
    # TRANSLASI
    if event.key == 'w':  # Maju (Y+)
        robot.position[1] += step
    elif event.key == 's':  # Mundur (Y-)
        robot.position[1] -= step
    elif event.key == 'a':  # Kiri (X-)
        robot.position[0] -= step
    elif event.key == 'd':  # Kanan (X+)
        robot.position[0] += step
    elif event.key == 'q':  # Naik (Z+)
        robot.position[2] += step
    elif event.key == 'e':  # Turun (Z-)
        robot.position[2] -= step
    
    # ROTASI
    elif event.key == 'i':  # Rotasi X+
        robot.rotation[0] += angle_step
    elif event.key == 'k':  # Rotasi X-
        robot.rotation[0] -= angle_step
    elif event.key == 'j':  # Rotasi Y+
        robot.rotation[1] += angle_step
    elif event.key == 'l':  # Rotasi Y-
        robot.rotation[1] -= angle_step
    elif event.key == 'u':  # Rotasi Z+
        robot.rotation[2] += angle_step
    elif event.key == 'o':  # Rotasi Z-
        robot.rotation[2] -= angle_step
    
    # SKALA
    elif event.key == '+' or event.key == '=':
        robot.scale += 0.1
    elif event.key == '-':
        robot.scale = max(0.1, robot.scale - 0.1)
    
    # REFLEKSI
    elif event.key == '1':  # Toggle refleksi X
        robot.reflection[0] *= -1
    elif event.key == '2':  # Toggle refleksi Y
        robot.reflection[1] *= -1
    elif event.key == '3':  # Toggle refleksi Z
        robot.reflection[2] *= -1
    
    # RESET
    elif event.key == 'r':
        robot.position = [0, 0, 0]
        robot.rotation = [0, 0, 0]
        robot.scale = 1.0
        robot.reflection = [1, 1, 1]
    
    robot.render(ax)
    fig.canvas.draw()

# Main program
def main():
    print("=" * 60)
    print("ROBOT 3D - TRANSFORMASI GEOMETRI")
    print("=" * 60)
    print("\nKONTROL KEYBOARD:")
    print("\nTRANSLASI (Menggeser Posisi):")
    print("  W/S  : Maju/Mundur (Y)")
    print("  A/D  : Kiri/Kanan (X)")
    print("  Q/E  : Naik/Turun (Z)")
    print("\nROTASI (Memutar):")
    print("  I/K  : Rotasi sumbu X")
    print("  J/L  : Rotasi sumbu Y")
    print("  U/O  : Rotasi sumbu Z")
    print("\nSKALA (Mengubah Ukuran):")
    print("  +/-  : Perbesar/Perkecil")
    print("\nREFLEKSI (Mencerminkan):")
    print("  1    : Toggle refleksi sumbu X")
    print("  2    : Toggle refleksi sumbu Y")
    print("  3    : Toggle refleksi sumbu Z")
    print("\nLAINNYA:")
    print("  R    : Reset semua transformasi")
    print("=" * 60)
    
    robot = Robot3D()
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    robot.render(ax)
    
    fig.canvas.mpl_connect('key_press_event', 
                           lambda event: on_key(event, robot, ax, fig))
    
    plt.show()

if __name__ == "__main__":
    main()