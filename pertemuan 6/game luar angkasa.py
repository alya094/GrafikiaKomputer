import pygame, sys, math, random, numpy as np

SCREEN_W, SCREEN_H = 1280, 720
FPS = 60

TOP = (15, 0, 25)
BOTTOM = (110, 0, 20)
SIL = (240,240,240)
ENEMY = (255, 200, 200)
MOUNTAIN = (10,10,20)
MID_MTN = (20,20,35)
FRONT_MTN = (30,30,50)

def T(x,y):
    return np.array([[1,0,x],[0,1,y],[0,0,1]],float)

def R(a):
    r=math.radians(a)
    return np.array([[math.cos(r),-math.sin(r),0],
                     [math.sin(r), math.cos(r),0],
                     [0,0,1]],float)

def S(sx, sy):
    return np.array([[sx,0,0],[0,sy,0],[0,0,1]],float)

def apply(pts,M):
    homo=np.hstack([pts,np.ones((pts.shape[0],1))])
    return (M@homo.T).T[:,:2]


# BACKGROUND ---------------------------------------------------------
def draw_gradient(surf):
    for y in range(SCREEN_H):
        t=y/SCREEN_H
        r=TOP[0]*(1-t)+BOTTOM[0]*t
        g=TOP[1]*(1-t)+BOTTOM[1]*t
        b=TOP[2]*(1-t)+BOTTOM[2]*t
        pygame.draw.line(surf,(int(r),int(g),int(b)),(0,y),(SCREEN_W,y))

def draw_mountains(surf):
    pygame.draw.polygon(surf, MOUNTAIN,
        [(0,500),(300,380),(700,520),(1000,360),(1280,480),(1280,720),(0,720)])
    pygame.draw.polygon(surf, MID_MTN,
        [(0,580),(350,470),(700,600),(1100,500),(1280,580),(1280,720),(0,720)])
    pygame.draw.polygon(surf, FRONT_MTN,
        [(0,620),(350,550),(650,640),(900,560),(1280,650),(1280,720),(0,720)])

    wolf=[[-20,0],[0,-30],[25,-15],[15,0],[25,20],[10,25],[0,10],[-10,25],[-20,10]]
    wolf=np.array(wolf,float)
    pygame.draw.polygon(surf,SIL,apply(wolf,T(350,530)))

stars=[(random.randint(0,SCREEN_W),random.randint(0,SCREEN_H//2)) for _ in range(100)]
def draw_stars(surf):
    for (x,y) in stars:
        pygame.draw.circle(surf,(255,255,255),(x,y),1)

def draw_dead_tree(surf):
    pygame.draw.polygon(surf,SIL,
        [(100,600),(120,480),(110,420),(140,350),(120,330),(160,280),(150,240),(200,260),
         (170,310),(180,370),(160,450),(200,500),(180,600)])


# PARTICLE -----------------------------------------------------------
class Particle:
    def __init__(self,pos):
        self.pos=np.array(pos,float)
        ang=random.random()*6.28
        self.vel=np.array([math.cos(ang)*100,math.sin(ang)*100])
        self.life=0.6

    def update(self,dt):
        self.pos+=self.vel*dt
        self.life-=dt

    def draw(self,surf):
        if self.life>0:
            pygame.draw.circle(surf,(255,150,150),
                (int(self.pos[0]),int(self.pos[1])),3)


# NINJA ---------------------------------------------------------------
class Ninja:
    def __init__(self):
        self.pos=np.array([250,450],float)
        self.speed=260
        self.slashing=False
        self.slash_start=0
        self.arm_angle=0
        self.hp=5

        self.scale = 1.0
        self.mirror = 1     # 1 = normal, -1 = flipped

        self.body=np.array([[-25,-50],[25,-50],[25,50],[-25,50]],float)
        self.head=np.array([[-18,-70],[18,-70],[18,-50],[-18,-50]],float)
        self.hair=np.array([[-5,-70],[5,-70],[15,-90],[-15,-90]],float)
        self.katana=np.array([[20,-10],[120,-5]],float)

    def scale_up(self):
        self.scale = min(3.0, self.scale + 0.1)

    def scale_down(self):
        self.scale = max(0.4, self.scale - 0.1)

    def flip(self):
        self.mirror *= -1

    def slash(self,t):
        self.slashing=True
        self.slash_start=t

    def update(self,dt,t,keys):
        move=np.array([0.,0.])
        if keys[pygame.K_w]: move[1]-=1
        if keys[pygame.K_s]: move[1]+=1
        if keys[pygame.K_a]: move[0]-=1
        if keys[pygame.K_d]: move[0]+=1

        if np.linalg.norm(move)>0:
            move/=np.linalg.norm(move)
        self.pos+=move*self.speed*dt

        if self.slashing:
            if t-self.slash_start>0.25:
                self.slashing=False
                self.arm_angle=0
            else:
                self.arm_angle=170*math.sin((t-self.slash_start)*25)

    def get_sword_tip(self):
        M = T(self.pos[0],self.pos[1]) @ S(self.mirror*self.scale, self.scale) @ R(self.arm_angle)
        return apply(self.katana,M)[1]

    def draw(self,surf):

        # MATRIX UTAMA (Scale + Mirror + Translate)
        Base = T(self.pos[0],self.pos[1]) @ S(self.mirror*self.scale, self.scale)

        # Draw body
        pygame.draw.polygon(surf,SIL,apply(self.body,Base))
        pygame.draw.polygon(surf,SIL,apply(self.head,Base))
        pygame.draw.polygon(surf,SIL,apply(self.hair,Base))

        # ARM + KATANA rotation
        Arm = Base @ R(self.arm_angle)
        K=apply(self.katana,Arm)
        pygame.draw.line(surf,SIL,K[0],K[1],4)


# WITCH (Enemy) -------------------------------------------------------
class Witch:
    def __init__(self):
        self.pos=np.array([random.randint(900,1200),random.randint(200,500)],float)
        self.body=np.array([[-30,-40],[30,-40],[50,40],[-50,40]],float)
        self.hat=np.array([[-20,-60],[0,-90],[20,-60]],float)
        self.hp=70
        self.alive=True

    def update(self,dt,target):
        if not self.alive: return
        d=target-self.pos
        if np.linalg.norm(d)>3:
            d/=np.linalg.norm(d)
        self.pos+=d*70*dt

    def hit(self,damage):
        self.hp-=damage
        if self.hp<=0:
            self.alive=False

    def draw(self,surf):
        if not self.alive: return
        M=T(self.pos[0],self.pos[1])
        pygame.draw.polygon(surf,ENEMY,apply(self.body,M))
        pygame.draw.polygon(surf,ENEMY,apply(self.hat,M))
        for i in range(3):
            pygame.draw.ellipse(surf,(255,200,200),
                (self.pos[0]-40,self.pos[1]+20+i*10,80,10),1)


# RESET FUNCTION -----------------------------------------------------
def reset_game():
    return Ninja(), [], [], 0, False, False, 0


# MAIN GAME LOOP -----------------------------------------------------
def main():
    pygame.init()
    screen=pygame.display.set_mode((SCREEN_W,SCREEN_H))
    clock=pygame.time.Clock()
    font=pygame.font.SysFont("arial",28)
    bigfont=pygame.font.SysFont("arial",72)
    medfont=pygame.font.SysFont("arial",36)

    ninja, enemies, particles, kills, game_over, win, spawn_timer = reset_game()
    max_enemies=20

    while True:
        dt=clock.tick(FPS)/1000
        t=pygame.time.get_ticks()/1000

        for e in pygame.event.get():
            if e.type==pygame.QUIT: pygame.quit(); sys.exit()
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_ESCAPE: pygame.quit(); sys.exit()

                # Restart ketika game over atau menang
                if game_over or win:
                    if e.key==pygame.K_y:
                        ninja, enemies, particles, kills, game_over, win, spawn_timer = reset_game()
                    elif e.key==pygame.K_n:
                        pygame.quit(); sys.exit()

                # Slash attack (hanya saat game aktif)
                if not game_over and not win:
                    if e.key==pygame.K_j:
                        ninja.slash(t)

                    # SCALE
                    if e.key==pygame.K_e: ninja.scale_up()
                    if e.key==pygame.K_r: ninja.scale_down()

                    # MIRROR
                    if e.key==pygame.K_f: ninja.flip()

        keys=pygame.key.get_pressed()

        # Update
        if not game_over and not win:
            ninja.update(dt,t,keys)

            spawn_timer+=dt
            if spawn_timer>1.2 and len(enemies)<max_enemies:
                enemies.append(Witch())
                spawn_timer=0

            for w in enemies: w.update(dt,ninja.pos)

            # Sword hit
            tip=ninja.get_sword_tip()
            for w in enemies:
                if w.alive and np.linalg.norm(tip-w.pos)<80 and ninja.slashing:
                    w.hit(40)
                    particles += [Particle(w.pos) for _ in range(10)]
                    if not w.alive:
                        kills+=1

            # Enemy hits ninja
            for w in enemies:
                if w.alive and np.linalg.norm(w.pos-ninja.pos)<50:
                    ninja.hp-=1
                    w.alive=False
                    particles += [Particle(w.pos) for _ in range(10)]

            # Cek kondisi kalah
            if ninja.hp<=0:
                game_over=True
            
            # Cek kondisi menang
            if kills>=max_enemies:
                win=True

            for p in particles[:]:
                p.update(dt)
                if p.life<=0: particles.remove(p)

        # DRAW -----------------------------------------------------
        draw_gradient(screen)
        draw_stars(screen)
        draw_mountains(screen)
        draw_dead_tree(screen)

        for w in enemies: w.draw(screen)
        ninja.draw(screen)
        for p in particles: p.draw(screen)

        # UI normal saat bermain
        if not game_over and not win:
            screen.blit(font.render("W/A/S/D Gerak  |  J Serang  |  E/R Scale  |  F Mirror",True,(255,255,255)),(20,20))
            screen.blit(font.render(f"Musuh Mati: {kills}/{max_enemies}", True, (255,255,255)), (20,60))
            screen.blit(font.render(f"HP Ninja: {ninja.hp}", True, (255,120,120)), (20,100))

        # LAYAR MENANG
        if win:
            # Overlay gelap semi-transparan
            overlay = pygame.Surface((SCREEN_W, SCREEN_H))
            overlay.set_alpha(128)
            overlay.fill((0, 20, 0))
            screen.blit(overlay, (0, 0))
            
            # Pesan kemenangan
            title = bigfont.render("KAMU MENANG!", True, (100, 255, 100))
            screen.blit(title, (SCREEN_W//2 - title.get_width()//2, SCREEN_H//2 - 120))
            
            # Apresiasi
            appreciation = medfont.render("Hebat! Semua musuh berhasil dikalahkan!", True, (200, 255, 200))
            screen.blit(appreciation, (SCREEN_W//2 - appreciation.get_width()//2, SCREEN_H//2 - 40))
            
            stats = font.render(f"Total Musuh Dikalahkan: {kills}", True, (255, 255, 255))
            screen.blit(stats, (SCREEN_W//2 - stats.get_width()//2, SCREEN_H//2 + 10))
            
            # Pilihan restart
            prompt = medfont.render("Main Lagi? (Y) | Keluar? (N)", True, (255, 255, 255))
            screen.blit(prompt, (SCREEN_W//2 - prompt.get_width()//2, SCREEN_H//2 + 70))

        # LAYAR GAME OVER
        if game_over:
            # Overlay gelap semi-transparan
            overlay = pygame.Surface((SCREEN_W, SCREEN_H))
            overlay.set_alpha(128)
            overlay.fill((20, 0, 0))
            screen.blit(overlay, (0, 0))
            
            # Pesan game over
            title = bigfont.render("GAME OVER", True, (255, 80, 80))
            screen.blit(title, (SCREEN_W//2 - title.get_width()//2, SCREEN_H//2 - 100))
            
            # Info statistik
            stats = font.render(f"Musuh yang Dikalahkan: {kills}/{max_enemies}", True, (255, 200, 200))
            screen.blit(stats, (SCREEN_W//2 - stats.get_width()//2, SCREEN_H//2 - 20))
            
            # Pilihan restart
            prompt = medfont.render("Main Lagi? (Y) | Keluar? (N)", True, (255, 255, 255))
            screen.blit(prompt, (SCREEN_W//2 - prompt.get_width()//2, SCREEN_H//2 + 40))

        pygame.display.flip()


if __name__=="__main__":
    main()