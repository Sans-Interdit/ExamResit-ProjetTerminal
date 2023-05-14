class ProjBoule(pg.sprite.Sprite):
    def __init__(self,x,y,type,taille):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        if type in ("faux1", "faux2", "faucille"):
            self.image = pg.image.load("faux.png").convert_alpha()
            self.t = 0
            self.x_first = x
            self.y_first = y
            self.r = sqrt((p1.rect.x - x) ** 2 + (p1.rect.y - y) ** 2)//2
            if self.r <= 50:
                self.r = 50
            if type == "faucille":
                dx = int(p1.rect.x - x)
                dy = int(p1.rect.y - y)
                if dx == 0:
                    self.speedx = 0
                    self.speedy = 0.2
                if dy == 0:
                    self.speedy = 0
                    self.speedx = 0.2
                elif dy < 0:
                    a = dx / dy
                    self.speedy = -0.2/sqrt(a**2 + 1)
                    self.speedx = a * self.speedy
                elif dy > 0:
                    a = dx / dy
                    self.speedy = 0.2/sqrt(a**2 + 1)
                    self.speedx = a* self.speedy
        else:
            self.image = pg.image.load("bouBoule.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = pg.Rect(x-25-(14*self.taille/30-30), y+10-(14*self.taille/30-30),self.taille+10,self.taille)
        self.type = type
        self.speed = 5
        self.x2 = 0
        self.y2 = self.rect.y
        self.tmp = pg.time.get_ticks()


    def update(self):
        if self.type=="simple":
            self.rect.x -=7
        elif self.type=="vacillant":
            self.x2 -= 4
            self.rect.x -= 4
            self.rect.y = sin(self.x2/50)*100+self.y2
        elif self.type=="suivant":
            self.autoguidage(p1,"lent")
        elif self.type == "faux1":
            self.rect.x = self.x_first + self.r * (cos(self.t*pi/120) - 1)
            self.rect.y = 50 + self.y_first - self.r * 0.8 * sin(self.t*pi/120)
            self.t += 1
            if self.t >= 230:
                self.kill()
                self = None
        elif self.type == "faux2":
            self.rect.x = self.x_first + self.r * (cos(self.t*pi/120) - 1)
            self.rect.y = 50 + self.y_first + self.r * 0.8 * sin(self.t*pi/120)
            self.t += 1
            if self.t >= 230:
                self.kill()
                self = None
        elif self.type == "faucille":
            self.rect.x += self.speedx * dt
            self.rect.y += self.speedy * dt
            if (self.rect.x < -50 or self.rect.x > 1050 or self.rect.y < -10 or self.rect.y > 750) and pg.time.get_ticks() - self.tmp > 1000:
                self.kill()
                self = None

        #elif self.type=="missile":
        #    self.autoguidage(p1,"vite")

    def autoguidage(self, joueur, vit):
        if vit=="lent":
            vect = pg.math.Vector2(joueur.rect.x+40 - self.rect.x, joueur.rect.y+30 - self.rect.y)
            if vect[0]!=0 or vect[1]!=0:
                if abs(vect[0])+abs(vect[1])<150:
                    self.speed = 3.5
                else:
                    self.speed = 4
                vect.scale_to_length(self.speed)
                self.rect.move_ip(vect)


class ProjFaux(pg.sprite.Sprite):
    def __init__(self,x,y,i,taille):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        self.image = pg.image.load("faux.png").convert_alpha()
        self.t = 0
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))
        self.mask = pg.mask.from_surface(self.image)
        self.rect = pg.Rect(x-25-(14*self.taille/30-30), y+10-(14*self.taille/30-30),self.taille+10,self.taille)
        self.i = i
        self.move = "turn"


    def update(self):
        if self.move == "turn":
            self.rect.x = p1.rect.x + 250 * cos(self.i*2*pi/5 + (self.t)*pi/150)
            self.rect.y = p1.rect.y + 250 * sin(self.i*2*pi/5 + (self.t)*pi/150)
            self.t += 1
        if self.t >= 150:
            self.move = "stop"
        if self.move == "stop":
            self.rect.x = p1.rect.x + (self.t+100) * cos(self.i*2*pi/5 + 150*pi/150)
            self.rect.y = p1.rect.y + (self.t+100) * sin(self.i*2*pi/5 + 150*pi/150)
            self.t += 1
        if self.t >= 230:
            ProjBoule(self.rect.x,self.rect.y,"faucille",self.taille)
            self.kill()
            self = None



class LostSoul(MobGeneral):
    def  __init__(self,x,y):
        MobGeneral.__init__(self,x,y,90,70,25,100,100,100,0,25,"lost_soul.png")
        self.move = "asc"
        self.speed = -0.3

    def action(self):
        global dt
        if self.move == "charge":
            self.rect.x -= self.speed * dt
            if self.rect.x <= -20:
                self.kill()
                self = None
        else:
            self.rect.y += self.speed * dt
            if self.rect.y <= 60:
                self.speed = 0.3
            if self.rect.y >= 650:
                self.speed = -0.3
            if p1.rect.y + 20 >= self.rect.y and p1.rect.y - 20 <= self.rect.y:
                self.move = "charge"
                self.speed = 0.7

class Tentacule(MobGeneral):
    def  __init__(self,x,nature="normal",place="bas"):
        self.act = "idle"
        if nature == "normal":
            self.time_delay = 100
        elif nature == "demon":
            self.time_delay = 70
        self.tmp = pg.time.get_ticks()
        if place == "haut":
            y = 60
        elif place == "bas":
            y = 660
        self.place = place
        self.i = 0
        MobGeneral.__init__(self,x,y,90,40,50,100,100,100,0,25,"tentacule1.png")
        self.images = []
        for i in range(6):
            if place == "bas":
                self.images.append(pg.image.load("tentacule"+str(i+1)+".png").convert_alpha())
            elif place == "haut":
                self.images.append(pg.transform.flip(pg.image.load("tentacule"+str(i+1)+".png").convert_alpha(), False, True))
        self.image = self.images[0]

    def action(self):
        if self.act == "idle" and p1.rect.x + 20 >= self.rect.x and p1.rect.x - 20 <= self.rect.x:
            self.act = "attack"
        elif self.act == "attack":
            if pg.time.get_ticks() - self.tmp > self.time_delay and self.i < 5:
                self.i += 1
                self.image = self.images[self.i]
                self.mask = pg.mask.from_surface(self.image)
                if self.place == "bas":
                    self.rect.y -= 22
                self.tmp = pg.time.get_ticks()
            elif self.i == 5:
                self.act = "wait"
        if self.act == "wait":
            if pg.time.get_ticks() - self.tmp >= 1000:
                self.act = "return"
                self.tmp = pg.time.get_ticks()
        if self.act == "return":
            if pg.time.get_ticks() - self.tmp > 60 and self.i > 0:
                self.i -= 1
                self.image = self.images[self.i]
                self.mask = pg.mask.from_surface(self.image)
                self.tmp = pg.time.get_ticks()
                if self.place == "bas":
                    self.rect.y += 22
            elif self.i == 0:
                self.act = "idle"

class Faucheur(MobGeneral):
    def  __init__(self,x,y):
        MobGeneral.__init__(self,x,y,60,95,100,80,90,95,3,150,"faucheur.png")
        self.tmp = pg.time.get_ticks()
        self.speedy = 0.2

    def action(self):
        if pg.time.get_ticks() - self.tmp > 2500:
            ProjBoule(self.rect.x,self.rect.y,"faux1",50)
            ProjBoule(self.rect.x,self.rect.y,"faux2",50)
            self.tmp = pg.time.get_ticks()
        self.rect.y += self.speedy * dt
        if self.rect.y <= 90:
                self.speedy = 0.2
        elif self.rect.y >= 450:
                self.speedy = -0.2


class BossFaucheur(MobGeneral):
    def __init__(self):
        MobGeneral.__init__(self,600,300,342,270,1200,0,40,60,0,3000,"grand_faucheur1.png")
        self.phase = 1
        self.counter = 0
        self.n_cercle = 5
        self.tmp = pg.time.get_ticks()
        self.speedy = -0.15



    def action(self):
        if pg.time.get_ticks() - self.tmp > 2000:
            nouvx = randint(80, 920)
            nouvy = randint(60, 620)
            if p1.rect.x - 150 <= nouvx <= p1.rect.x + 150 and p1.rect.y - 150 <= nouvy <= p1.rect.y + 150:
                nouvx += 300
                nouvy += 300
            ProjBoule(nouvx,nouvy,"faucille",50)
            if randint(1,6) == 4:
                for i in range(5):
                    ProjFaux(-100,-100,i,40)
                self.tmp = pg.time.get_ticks() + 3000
            else:
                ProjBoule(self.rect.x,self.rect.y,"faux1",80)
                ProjBoule(self.rect.x,self.rect.y,"faux2",80)
                self.tmp = pg.time.get_ticks()
        self.rect.y += self.speedy * dt
        if self.rect.y <= 90:
                self.speedy = 0.15
        elif self.rect.y >= 450:
                self.speedy = -0.15
