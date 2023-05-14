import pygame as pg
from pygame.locals import *
import sys
from random import randint
from math import cos, sin, exp, pi, sqrt
from os.path import exists

pg.init()
clock=pg.time.Clock()
fenetre = pg.display.set_mode((1000, 700))
dialogues = {"intro" : [("steve.png", "Que... Comment... Je suis où ?"), ("chevreuil.png", "Tu es mort. Tu as une toge et du sang, mon gars. Désolé."), ("steve.png", "Mais... Pourquoi... Ah oui tiens. Le bus, hein ?"), ("chevreuil.png", "Si tu veux. Bon je te préviens, ici on est un peu short sur le personnel \n donc en guise de jugement dernier, faudrait que tu te rendes un peu utile."), ("steve.png", "...Un genre de stage donc ?"), ("chevreuil.png", "D'accord bonhomme... Un genre de stage. Nettoies-moi donc les âmes plus ou moins impures qui traînent. Tu devrais t'en débrouiller."), ("chevreuil.png", "Oh et... Si tu vois un cristal violet. Casse-le. Compris ? Bien ! On se revoit... Bientôt.")]}
flavor_texts = ["GAME OVER YEEEAAAAAHH", "get dunnnkeeeeed oooonnn", "YOU DIED", "Aïe, ça avait l'air douloureux !", "Attends, tu n'es pas déjà mort ?", "Tu t'es fait tuer par ça ?", "Bonne chance pour la suite !"]
pg.display.set_caption("Exam Resit")
pg.display.set_icon(pg.image.load("icone_fenetre.png"))
#la bande où on voit les infos commence à y = 45
pg.mixer.init()


class ProjBoule(pg.sprite.Sprite):
    def __init__(self,x,y,type,taille,traj=None):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        self.rect = pg.Rect(x, y-self.taille//4,self.taille+10,self.taille)
        self.type = type
        if traj==None:
            self.vect = pg.math.Vector2(p1.rect.x+40 - self.rect.x, p1.rect.y+30 - self.rect.y)
        else:
            self.vect = pg.math.Vector2(traj[0],traj[1])
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
        elif self.type=="rebond":
            self.rebond = 0
            self.image = pg.image.load("bouleJaune.png").convert_alpha()
        elif self.type=="vacillantSpe":
            self.x2 = pg.time.get_ticks()/4
            self.y2 = self.rect.y
            self.image = pg.image.load("bouleRouge.png").convert_alpha()
        elif self.type=="vacillantHaut":
            self.y2 = 0
            self.x2 = self.rect.x
            self.image = pg.image.load("bouleRouge.png").convert_alpha()
        elif self.type=="vacillant":
            self.x2 = 0
            self.y2 = self.rect.y
            self.image = pg.image.load("bouleRouge.png").convert_alpha()
        elif self.type=="tripleTir":    #taille doit etre 30
            self.image = pg.image.load("bouleBleu.png").convert_alpha()
            self.vect = pg.math.Vector2(-2,1)
            ProjBoule(self.rect.x+7,self.rect.y-25,"tripleTir1",self.taille)
        elif self.type=="tripleTir1":
            self.image = pg.image.load("bouleBleu.png").convert_alpha()
            self.vect = pg.math.Vector2(-2,0)
            ProjBoule(self.rect.x+7,self.rect.y-25,"tripleTir2",self.taille)
        elif self.type=="tripleTir2":
            self.image = pg.image.load("bouleBleu.png").convert_alpha()
            self.vect = pg.math.Vector2(-2,-1)
        elif self.type=="simple":
            self.image = pg.image.load("bouleNoir.png").convert_alpha()
        elif self.type=="simpleVise":
            self.image = pg.image.load("bouleVert.png").convert_alpha()
        elif self.type=="frag2":
            self.image = pg.image.load("bouleNoir.png").convert_alpha()
            self.delai = self.taille/1.6
        if self.type=="frag1":
            self.image = pg.image.load("bouleNoir.png").convert_alpha()
            self.delai = 140
            self.speed = 7-self.taille/20
            self.vect.scale_to_length(self.speed)
        else:
            self.vect.scale_to_length(7)
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))


    def update(self):
        if self.type=="simple":
            self.rect.x -=7
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
            if (self.rect.x < -50 or self.rect.x > 1050 or self.rect.y < -10 or self.rect.y > 750) and pg.time.get_ticks() - self.t > 1000:
                self.kill()
                self = None
        elif self.type=="frag1":
            self.rect.move_ip(self.vect)
            self.delai -= 1
            if self.delai<=0 and self.taille>60:
                self.kill()
                for i in range(-2, 3):
                    for j in range(-3, 4):
                        if i!=0 or j!=0:
                            ProjBoule(self.rect.x+self.taille//2, self.rect.y+self.taille//2, "frag1", 15, (i, j))
        elif self.type=="frag2":
            self.rect.move_ip(self.vect)
            self.delai -= 1
            if self.delai<=0 and self.taille>=60:
                self.kill()
                ProjBoule(self.rect.x, self.rect.y, "frag2", self.taille-20, (-1, 0))
                ProjBoule(self.rect.x, self.rect.y, "frag2", self.taille-20, (1, 0))
                ProjBoule(self.rect.x, self.rect.y, "frag2", self.taille-20, (0, 1))
                ProjBoule(self.rect.x, self.rect.y, "frag2", self.taille-20, (0, -1))
        elif self.type=="simpleVise" or self.type[:9]=="tripleTir":
            self.rect.move_ip([round(self.vect[0]),round(self.vect[1])])
        elif self.type[:9]=="vacillant":
            if len(self.type)==9:
                self.rect.y = sin(self.x2/75)*100+self.y2
                self.x2 -= 4
                self.rect.x -= 4
            elif self.type[-3:]=="Spe":
                self.rect.y = sin(self.x2/200)*150+self.y2
                self.x2 -= 4
                self.rect.x -= 4
            else:
                self.rect.x = sin(self.y2/75)*100+self.x2
                self.y2 -= 4
                self.rect.y -= 4
        elif self.type=="rebond":
            if (self.rect.y>=700-self.taille or self.rect.y<0) and self.rebond<3:
                self.vect = pg.math.Vector2(self.vect[0],-self.vect[1])
                self.vect.scale_to_length(7)
                self.rebond+=1
            if (self.rect.x<0 or self.rect.x>1000-self.taille) and self.rebond<3:
                self.vect = pg.math.Vector2(-self.vect[0],self.vect[1])
                self.vect.scale_to_length(7)
                self.rebond+=1
            self.rect.move_ip([round(self.vect[0]),round(self.vect[1])])
        if self!=None and self.type[:3]!="fau":
            if self.type[:9]=="vacillant":
                if self.rect.x<=-self.taille or self.rect.x>=1000:
                    self.kill()
            elif self.rect.y>=700 or self.rect.y<-self.taille or self.rect.x<=-self.taille or self.rect.x>=1000:
                self.kill()

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

class ProjCassable(pg.sprite.Sprite):
    def __init__(self,x,y,type,taille):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        self.type = type
        if self.type[:7]=="suivant":
            self.image = pg.image.load("bouleMauve.png").convert_alpha()
        elif self.type[:5]=="piege":
            self.image = pg.image.load("flamme.png").convert_alpha()
        else:
            self.image = pg.image.load("meteor.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))
        self.rect = pg.Rect(x, y-self.taille//4,self.taille,self.taille)
        if self.type=="piege":
            self.hp = 3
        else:
            self.hp = 1
        self.speed = 5
        if self.type[:5]=="piege":
            self.trajP = pg.math.Vector2(-5, randint(-5,5))
        elif self.type=="meteor":
            self.trajP = pg.math.Vector2(-1,2)

    def update(self):
        global collisions
        if self.type=="meteor":
            self.trajP.scale_to_length(self.speed)
            self.rect.move_ip(self.trajP)
        elif self.type[:5]=="piege":
            if self.speed>0:
                self.trajP.scale_to_length(self.speed)
                self.rect.move_ip(self.trajP)
                self.speed -= 0.1
        elif self.type=="suivant":
            self.trajP = pg.math.Vector2(p1.rect.x+self.taille - self.rect.x, p1.rect.y+30 - self.rect.y)
            if self.trajP[0]!=0 or self.trajP[1]!=0:
                if abs(self.trajP[0])+abs(self.trajP[1])<150:
                    self.speed = 3.5
                else:
                    self.speed = 4
                self.trajP.scale_to_length(self.speed)
                self.rect.move_ip(self.trajP)
        elif self.type=="suivantSpe":
            self.rect.x -= 7
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp -= 1
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                self.kill()
        if self.rect.y>=700 or self.rect.y<-30 or self.rect.x<=-30 or self.rect.x>=1000:
            self.kill()
        if self.hp <= 0:
            self.kill()

class PluieMeteors():
    def __init__(self,cooldown):
        self.cooldown = cooldown
        self.actif = False
        self.dernier = -10000

    def desActiver(self):
        """active ou desactive la pluie de meteorite"""
        self.actif = not self.actif

    def setCooldown(self,cooldown):
        self.cooldown = cooldown

    def update(self):
        tmp = pg.time.get_ticks()
        if self.actif and tmp-self.dernier>self.cooldown:
            self.dernier = tmp
            ProjCassable(randint(40,1300),-50,"meteor",30)

class Cristal(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("cristal.png").convert_alpha()
        self.rect = Rect(500, 350, 25, 25)
        self.traj = self.traj = pg.math.Vector2(randint(-50, 50), randint(-50, 50))
        self.delai = 0
        self.hp = 5

    def update(self):
        global cristauxDetruits
        self.delai+=1
        if self.delai==1000:
            self.kill()
        if self.rect.x>=900:
            self.traj = pg.math.Vector2(randint(-50, 0), randint(-50, 50))
        elif self.rect.x<=100:
            self.traj = pg.math.Vector2(randint(0, 50), randint(-50, 50))
        elif self.rect.y>=600:
            self.traj = pg.math.Vector2(randint(-50, 50), randint(-50, 0))
        elif self.rect.y<=100:
            self.traj = pg.math.Vector2(randint(-50, 50), randint(0, 50))
        if self.traj[0]!=0 and self.traj[1]!=0:
            self.traj.scale_to_length(4)
            self.rect.move_ip(self.traj)
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp -= 1
                i[0].kill()
        if self.hp<=0:
            cristauxDetruits += 1
            self.kill()

class File:
    def __init__(self,tailleMax):
        self.lst=[]
        self.tailleMax = tailleMax
    def est_pleine(self):
        return len(self.lst)==self.tailleMax
    def enfiler(self,e):
        if not self.est_pleine():
            self.lst.append(e)
    def defiler(self):
        if self.lst!=[]:
            return self.lst.pop(0)

class Cible(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        groupe.add(self)
        self.image = pg.image.load("Cible.png").convert_alpha()
        self.taille = 40
        self.pos = File(50)
        self.rect = pg.Rect(500,350,30,30)
        self.traj = pg.math.Vector2(0,0)
        self.cmpt = 10

    def update(self):
        global collisions
        tous.remove(self)
        if self.pos.est_pleine():
            x,y=self.pos.defiler()
            self.traj = pg.math.Vector2(x-self.rect.x-self.taille//2+50,y-self.rect.y-self.taille//2+35)
        self.pos.enfiler((p1.rect.x,p1.rect.y))
        if (self.traj[0]<=-5 or self.traj[0]>=5) or (self.traj[1]<=-5 or self.traj[1]>=5):
            self.traj.scale_to_length(10)
            self.rect.move_ip(self.traj)
            self.taille = 40
        else:
            self.cmpt-=1
            if self.cmpt==0:
                self.rect.x+=1
                self.rect.y+=1
                self.cmpt = 10
            self.taille-=0.2
            if self.taille<=20:
                tous.add(self)
                self.taille = 40
        self.image = pg.image.load("Cible.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(int(self.taille),int(self.taille)))

class MobGeneral(pg.sprite.Sprite):
    def __init__(self,x,y,x_size,y_size,hp,min_nbr,nbr_damage,nbr_hp,karma,score,img_name):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.score = score
        self.hp = hp
        self.const = -4
        self.min_nbr = min_nbr
        self.nbr_damage = nbr_damage
        self.nbr_hp = nbr_hp
        self.karma = karma
        self.image = pg.image.load(img_name).convert_alpha()
        self.image = pg.transform.scale(self.image,(x_size,y_size))
        self.rect = self.image.get_rect()
        self.x2 = self.rect.x
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        global karma
        global score
        global collisions
        self.action()
        for i in collisions.items():
            if type(i[0]) in (Bullet, Explosion) and self in i[1]:
                if type(i[0]) == Bullet:
                    self.hp += - i[0].damage
                    i[0].kill()
                elif not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()
            nbr = randint(0,100)
            karma += self.karma
            score += self.score
            if nbr>self.min_nbr:
                if nbr>=self.nbr_damage:
                    tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                if nbr<=self.nbr_hp:
                    tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                else:
                    tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
            self = None

class trashMob(pg.sprite.Sprite):
    def __init__(self,x,y,hp,move,pattern,tire):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.hp = hp
        self.dernierTir = pg.time.get_ticks()-randint(0,1800) #traque des safe spots
        self.const = -4
        self.pattern = pattern
        self.tire = tire
        self.move = move
        if self.move=="traverse" or self.move=="doubleTraverse" or self.move=="passage" or self.move=="simple" or self.move=="piegeuageu":
            if self.pattern=="asc":
                self.rect = pg.Rect((x, 720),self.taille)
            elif self.pattern=="dsc":
                self.rect = pg.Rect((x, -70),self.taille)
            elif self.pattern=="devant" or self.pattern=="rush":
                self.rect = pg.Rect((1000, y), self.taille)
            else:# self.pattern=="derriere"
                self.rect = pg.Rect((-50, y), self.taille)
        elif self.move=="devantDerriere":
            if self.pattern=="asc":
                self.rect = pg.Rect((1000, 700), self.taille)
            else: # self.pattern=="dsc"
                self.rect = pg.Rect((1000, -200), self.taille)
        else:
            self.rect = pg.Rect((x, y), self.taille)
        self.x2 = self.rect.x

    def tirer(self):
        x, y = self.rect.x,self.rect.y+self.rect.height//2-self.tailleTir//2
        if 0<y<670 and 0<x<970 and pg.time.get_ticks()-self.dernierTir>self.cooldown and self.tire!="rien":
            if self.tire=="suivant":
                ProjCassable(x , y, self.tire, self.tailleTir)
            else:
                ProjBoule(x , y, self.tire, self.tailleTir)
            self.dernierTir = pg.time.get_ticks()

    def update(self):
        global karma, score
        if self.move=="simple":
            simple(self)
        elif self.move=="traverse":
            traverse(self)
        elif self.move=="doubleTraverse":
            doubleTraverse(self)
        elif self.move=="piegeuageu":
            piegeuageu(self)
        elif self.move=="devantDerriere":
            devantDerriere(self)
        elif self.move=="passage":
            passage(self)
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp -= i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()
            score+=100
            nbr = randint(0,100)
            if type(self)==Ange:
                if nbr>79:
                    if nbr>=98:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    elif nbr>=95:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    elif nbr>=92:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
                    elif nbr>=89:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bomb"))
                    elif nbr>=86:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_regular"))
                    elif nbr>=83:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_burst"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_shield"))
                if karma>-95:
                    karma-=5
                else:
                    karma = -100
            elif type(self)==Demon:
                if nbr>93:
                    if nbr==100:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    elif nbr==99:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    elif nbr==98:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
                    elif nbr==97:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bomb"))
                    elif nbr==96:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_regular"))
                    elif nbr==95:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_burst"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_shield"))
                if karma<=95:
                    karma+=5
                else:
                    karma = 100
            elif type(self)==Fantome:
                if nbr>86:
                    if nbr>=99:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    elif nbr>=97:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    elif nbr>=95:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
                    elif nbr>=93:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bomb"))
                    elif nbr>=91:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_regular"))
                    elif nbr>=89:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_burst"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "make_shield"))
                if karma<-5:
                    karma+=3
                elif karma>5:
                    karma-=3
                else:
                    karma = 0

class Ange(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=2000,tailleTir=30):
        if cooldown=="tuto":
            self.taille = 100, 100
            if tire=="rien":
                self.image = pg.image.load("tutoMobBleu.png").convert_alpha()
                if move=="spe":
                    trashMob.__init__(self,x,y,hp,"passage",pattern,tire)
                else:
                    trashMob.__init__(self,x,y,hp,move,pattern,tire)
            else:
                self.image = pg.image.load("tutoMobNoir.png").convert_alpha()
                trashMob.__init__(self,x,y,hp,"passage",pattern,tire)
            self.image = pg.transform.scale(self.image,self.taille)
            self.tailleTir = tailleTir
            self.cooldown = 2000
        else:
            if move=="spe":
                if tire=="simple":
                    self.image = pg.image.load("angeNoir.png").convert_alpha()
                elif tire=="vacillant":
                    self.image = pg.image.load("angeRouge.png").convert_alpha()
                elif tire=="tripleTir":
                    self.image = pg.image.load("angeBleu.png").convert_alpha()
                elif tire=="suivant":
                    self.image = pg.image.load("angeMauve.png").convert_alpha()
                elif tire=="rebond":
                    self.image = pg.image.load("angeJaune.png").convert_alpha()
                elif tire=="simpleVise":
                    self.image = pg.image.load("angeVert.png").convert_alpha()
                self.taille = 70, 70
                trashMob.__init__(self,x,y,hp,"passage",pattern,tire)
            else:
                if tire=="simple":
                    self.image = pg.image.load("pixieNoir.png").convert_alpha()
                elif tire=="vacillant":
                    self.image = pg.image.load("pixieRouge.png").convert_alpha()
                elif tire=="tripleTir":
                    self.image = pg.image.load("pixieBleu.png").convert_alpha()
                elif tire=="suivant":
                    self.image = pg.image.load("pixieMauve.png").convert_alpha()
                elif tire=="rebond":
                    self.image = pg.image.load("pixieJaune.png").convert_alpha()
                elif tire=="simpleVise":
                    self.image = pg.image.load("pixieVert.png").convert_alpha()
                self.taille = 56, 40
                trashMob.__init__(self,x,y,hp,move,pattern,tire)
            self.image = pg.transform.scale(self.image,self.taille)
            self.tailleTir = tailleTir
            self.cooldown = cooldown

class Demon(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=2000,tailleTir=30):
        if move=="spe":
            if tire=="simple":
                self.image = pg.image.load("demonNoir.png").convert_alpha()
            elif tire=="vacillant":
                self.image = pg.image.load("demonRouge.png").convert_alpha()
            elif tire=="tripleTir":
                self.image = pg.image.load("demonBleu.png").convert_alpha()
            elif tire=="suivant":
                self.image = pg.image.load("demonMauve.png").convert_alpha()
            elif tire=="rebond":
                self.image = pg.image.load("demonJaune.png").convert_alpha()
            elif tire=="simpleVise":
                self.image = pg.image.load("demonVert.png").convert_alpha()
            self.taille = 70, 70
            trashMob.__init__(self,x,randint(0,650),hp,"piegeuageu","rush",tire)
        else:
            if tire=="simple":
                self.image = pg.image.load("craneNoir.png").convert_alpha()
            elif tire=="vacillant":
                self.image = pg.image.load("craneRouge.png").convert_alpha()
            elif tire=="tripleTir":
                self.image = pg.image.load("craneBleu.png").convert_alpha()
            elif tire=="suivant":
                self.image = pg.image.load("craneMauve.png").convert_alpha()
            elif tire=="rebond":
                self.image = pg.image.load("craneJaune.png").convert_alpha()
            elif tire=="simpleVise":
                self.image = pg.image.load("craneVert.png").convert_alpha()
            self.taille = 40, 40
            trashMob.__init__(self,x,y,hp,move,pattern,tire)
        self.image = pg.transform.scale(self.image,self.taille)
        self.tailleTir = tailleTir
        self.cooldown = cooldown



class Fantome(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=2000,tailleTir=30):
        if move=="spe":
            if pattern=="devant":
                pattern = "asc"
            else:
                pattern = "dsc"
            if tire=="simple":
                self.image = pg.image.load("sorciereNoir.png").convert_alpha()
            elif tire=="vacillant":
                self.image = pg.image.load("sorciereRouge.png").convert_alpha()
            elif tire=="tripleTir":
                self.image = pg.image.load("sorciereBleu.png").convert_alpha()
            elif tire=="suivant":
                self.image = pg.image.load("sorciereMauve.png").convert_alpha()
            elif tire=="rebond":
                self.image = pg.image.load("sorciereJaune.png").convert_alpha()
            elif tire=="simpleVise":
                self.image = pg.image.load("sorciereVert.png").convert_alpha()
            self.taille = 70, 70
            trashMob.__init__(self,x,y,hp,"devantDerriere",pattern,tire)
        else:
            if tire=="simple":
                self.image = pg.image.load("fantomeNoir.png").convert_alpha()
            elif tire=="vacillant":
                self.image = pg.image.load("fantomeRouge.png").convert_alpha()
            elif tire=="tripleTir":
                self.image = pg.image.load("fantomeBleu.png").convert_alpha()
            elif tire=="suivant":
                self.image = pg.image.load("fantomeMauve.png").convert_alpha()
            elif tire=="rebond":
                self.image = pg.image.load("fantomeJaune.png").convert_alpha()
            elif tire=="simpleVise":
                self.image = pg.image.load("fantomeVert.png").convert_alpha()
            self.taille = 40, 56
            trashMob.__init__(self,x,y,hp,move,pattern,tire)
        self.image = pg.transform.scale(self.image,self.taille)
        self.tailleTir = tailleTir
        self.cooldown = cooldown

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

class MiniBossFantome(pg.sprite.Sprite): #ATTENTION PERTE DE FPS
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.rect = Rect(700,325,50,50)
        self.image = pg.image.load("miniBossFantome.png").convert_alpha()
        self.taille = 50
        self.hp = 250
        self.pattern = "gonflage"
        self.tmp = pg.time.get_ticks()
        self.enTir = False
        self.cible = (-1,0)
        HealthBar(self)


    def tirer(self):
        if pg.time.get_ticks()-self.tmp>3000 and not self.enTir:
            self.enTir = True
            self.tmp = pg.time.get_ticks()
            self.cible = p1.rect.x-self.rect.x+self.taille//2+40,p1.rect.y-self.rect.y-self.taille//2+20
        elif pg.time.get_ticks()-self.tmp>300 and pg.time.get_ticks()-self.tmp<500 and self.enTir:
            self.enTir = False
        if self.enTir:
            ProjBoule(self.rect.x,self.rect.y+0.4*self.taille,"rebond",self.taille//5,self.cible)
            if self.taille>=54:
                self.taille-=4
                self.rect.x+=2
                self.rect.y+=2
            elif self.taille>50:
                nbr = self.taille-4
                self.taille-=nbr
                self.rect.x+=nbr//2
                self.rect.y+=nbr//2
        elif pg.time.get_ticks()-self.tmp>150 and self.pattern=="degonflage":
            self.taille-=10
            self.rect.x+=5
            self.rect.y+=5
            ProjBoule(self.rect.x,self.rect.y+self.taille//2-15,"simpleVise",30,(-10,randint(-10,10)))
            self.tmp = pg.time.get_ticks()
            if self.taille<=50:
                self.pattern = "gonflage"

    def update(self):
        global collisions
        self.tirer()
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                if self.pattern=="gonflage":
                    self.taille+=8
                    self.rect.x -= 4
                    self.rect.y -= 4
                else:
                    self.hp-=i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted and self.pattern=="degonflage":
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.taille >= 500:
            self.pattern = "degonflage"
        if self.hp<=0:
            self.kill()
        self.image = pg.image.load("miniBossFantome.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))

class MiniBossAnge(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("miniBossAnge.png").convert_alpha()
        self.rect = pg.Rect(900, 300,100,100)
        self.tmp=pg.time.get_ticks()
        self.tmp2=pg.time.get_ticks()
        self.hp = 500
        self.move = "asc"
        HealthBar(self)

    def update(self):
        global collisions
        if pg.time.get_ticks()-self.tmp>2000:
            ProjBoule(self.rect.x,self.rect.y,"simple",50)
            self.tmp = pg.time.get_ticks()
        if pg.time.get_ticks()-self.tmp2>150:
            ProjBoule(850,150,"vacillantSpe",5)
            ProjBoule(850,495,"vacillantSpe",5)
            self.tmp2 = pg.time.get_ticks()
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()
        if self.move=="asc":
            self.rect.y-=3
        elif self.move=="dsc":
            self.rect.y+=3
        if self.rect.y>570:
            self.move = "asc"
        elif self.rect.y<30:
            self.move = "dsc"


class MiniBossDemon(pg.sprite.Sprite): #Il est plus trop "mini" mais bon...
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("miniBossDemon.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(300,300))
        self.rect = Rect(1000,200,300,300)
        self.triggerx = 500
        self.hp = 750
        self.passage = 0
        self.tmp = pg.time.get_ticks()
        HealthBar(self)

    def tirer(self):
        if pg.time.get_ticks()-self.tmp>2000:
            ProjBoule(self.rect.x+25,self.rect.y+100,"simpleVise",50,(p1.rect.x-self.rect.x-25,p1.rect.y-self.rect.y-85))
            self.tmp = pg.time.get_ticks()

    def update(self):
        if self.passage==0:
            if self.rect.x>700:
                self.rect.x-=3
            else:
                self.tirer()
        elif self.passage>0:
            self.rect.x-=8
            if self.rect.x<-300:
                self.rect.x = 1000
                self.passage -= 1
                if self.passage==0:
                    self.rect.y = 200
                else:
                    self.triggerx = randint(250,900)
                    self.rect.y = randint(0,400)
            if self.rect.x>self.triggerx-4 and self.rect.x<=self.triggerx+4:
                for i in range(10):
                    ProjCassable(self.rect.x+20, self.rect.y+80, "piegeSpe", 70)
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                hpAv = self.hp
                self.hp += - i[0].damage
                hpAp = self.hp
                i[0].kill()
                if hpAv>=500 and hpAp<=500:
                    self.passage += 4
                    self.enTir = False
                elif hpAv>=250 and hpAp<=250:
                    self.passage += 5
                    self.enTir = False
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    hpAv = self.hp
                    self.hp -= i[0].damage
                    hpAp = self.hp
                    i[0].mobsHitted.append(self)
                    if hpAv>=500 and hpAp<=500:
                        self.passage += 3
                        self.enTir = False
                    elif hpAv>=250 and hpAp<=250:
                        self.passage += 3
                        self.enTir = False
        if self.hp <= 0:
            self.kill()

class UFOBoss(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("ufoBoss.png")
        self.rect = Rect(700, 300, 200, 100)
        self.hp = 400
        self.delai = 100
        self.pattern = "base"
        self.cmpt = 0
        self.x2 = 500
        HealthBar(self)

    def update(self):
        global collisions
        if self.pattern=="derriere":
            if self.rect.x<1010:
                self.rect.x += 3
            elif self.delai<=0 and self.cmpt>0:
                for i in range(randint(0, 100), 700, 145):
                    ProjBoule(-49, i, "simpleVise", 50, (1, 0))
                self.delai = 40
                self.cmpt -= 1
            elif self.cmpt==0:
                self.pattern = "base"
                self.rect.x = 1010
                self.rect.y = 300
                self.delai = 300
        elif self.pattern=="dessous":
            if self.rect.y<710:
                self.rect.y += 4
            elif self.delai<=0 and self.cmpt>0:
                for i in range(randint(0, 100), 1000, 250):
                    ProjBoule(i, 710, "vacillantHaut", 50)
                self.delai = 40
                self.cmpt -= 1
            elif self.cmpt==0:
                self.pattern = "base"
                self.rect.x = 1010
                self.rect.y = 300
                self.delai = 300
        elif self.pattern=="dessus":
            if self.rect.y>-210:
                self.rect.y -= 4
            elif self.delai<=0 and self.cmpt>0:
                ProjBoule(500-self.x2, 0, "simpleVise", 50, (0, 1))
                ProjBoule(500+self.x2, 0, "simpleVise", 50, (0, 1))
                self.x2 -= 50
                self.delai = 10
                self.cmpt -= 1
            elif self.cmpt==0:
                self.pattern = "base"
                self.rect.x = 1010
                self.rect.y = 300
                self.delai = 300
        elif self.pattern=="base":
            if self.delai<=0:
                if self.rect.x>700:
                    self.rect.x -= 3
                elif self.rect.x<700:
                    self.delai = 100
                    self.rect.x += 1
                else:
                    self.pattern = ["dessus", "derriere", "dessous"][randint(0,2)]
                    if self.pattern=="dessus":
                        self.cmpt = 9
                        self.x2 = 500
                    else:
                        self.cmpt = 3
        self.delai -= 1
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()

class BossNuage(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("bossNuage.png")
        self.rect = Rect(750, 320, 50, 50)
        self.hp = 400
        self.cd = 100
        HealthBar(self)

    def update(self):
        global collisions
        if self.cd<=0:
            ProjBoule(self.rect.x, self.rect.y, "frag1", 80, (-2, randint(-1, 1)))
            self.cd += 150
        self.cd -= 1
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()

class TheNest(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("mur_visage.png").convert_alpha()
        self.rect = Rect(670, 260, 210, 230)
        self.mask = pg.mask.from_surface(self.image)
        self.hp = 8000
        self.cd = 100
        self.cdSpawn = 200
        self.cible = Cible()
        HealthBar(self)

    def update(self):
        global collisions
        fenetre.blit(pg.image.load("mur_chair.png").convert_alpha(),(620,55))
        if self.cdSpawn<=0:
            if randint(1,3) == 1:
                Oeil(randint(90, 620))
            else:
                LostSoul(700, randint(90, 620))
            self.cdSpawn = 100
        self.cdSpawn -= 1
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp <= 0:
            self.kill()
            self.cible.kill()

class Dieu(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("dieu.png")
        self.rect = Rect(880, 175, 50, 50)
        self.hp =  500
        self.delai = 150
        self.cd = 280
        self.d = MirorSheild()
        self.g = MirorSheild()
        self.descente = True
        self.instruct = ""
        self.code = pg.image.load("codeSource.png")
        self.pluieM = PluieMeteors(2000)
        self.pluieM.desActiver()
        self.HB = HealthBar(self)

    def update(self):
        global collisions
        if self.hp >= 30:
            self.g.rect.y = self.rect.y+70
            self.d.rect.y = self.rect.y-150
            self.pluieM.update()
            if self.delai<=0:
                self.descente = not self.descente
                self.delai = 150
            if self.descente:
                self.rect.y += 2
            else:
                self.rect.y -= 2
            if self.cd<=0:
                ProjBoule(self.rect.x, self.rect.y, "frag2", 80, (-1, 0))
                self.cd = 280
            for i in collisions.items():
                if type(i[0]) == Bullet and self in i[1]:
                    self.hp += - i[0].damage
                    i[0].kill()
                    self.pluieM.setCooldown(250+self.hp*3)
                if type(i[0]) == Explosion and self in i[1]:
                    if not self in i[0].mobsHitted:
                        self.hp -= i[0].damage
                        i[0].mobsHitted.append(self)
                        self.pluieM.setCooldown(250+self.hp*1.5)
        else:
            if self.rect.y>323:
                self.rect.y -= 3
                self.delai = 600
                self.cd = 0
            elif self.rect.y<320:
                self.rect.y += 3
                self.delai = 600
                self.cd = 0
            else:
                if self.delai>0:
                    self.megaMeteor = pg.image.load("meteor.png")
                    self.megaMeteor = pg.transform.scale(self.megaMeteor, (30-self.cd//2, 30-self.cd//2))
                    fenetre.blit(self.megaMeteor, (550+self.cd//3+randint(-2, 2), 30-self.cd))
                elif -100<self.delai<=0:
                    fenetre.fill((255,255,255))
                else:
                    self.HB.kill()
                    while self.alive():
                        for event in pg.event.get():
                            if event.type == QUIT:
                                pg.quit()
                                lancer = False
                                sys.exit()
                            elif event.type == 2:
                                if event.scancode == 14 and len(self.instruct) >= 1:
                                    self.instruct = self.instruct[:-1]
                                    self.code.blit(pg.font.SysFont('arialblack', 13).render(self.instruct, True,(255, 255, 255),(200 ,0, 0)), (0, 100))
                                elif event.scancode == 28:
                                    if self.instruct=="Dieu.kill()":
                                        self.kill()
                                        self.d.kill()
                                        self.g.kill()
                                    else:
                                        self.instruct=""
                                elif event.scancode != 14:
                                    self.instruct += event.unicode
                        self.code = pg.image.load("codeSource.png")
                        self.code.blit(pg.font.SysFont('arialblack', 13).render(self.instruct, True, (209, 188, 165), (31 ,31, 39)), (30, 96))
                        fenetre.blit(self.code, (0, 585))
                        groupe.draw(fenetre)
                        tous.draw(fenetre)
                        pg.display.update()
            self.g.rect.y = self.rect.y+20
            self.d.rect.y = self.rect.y-110
        self.delai -= 1
        self.cd -= 1


class MirorSheild(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("main.png")
        self.rect = Rect(800, 0, 50, 50)

    def update(self):
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                i[0].kill()
                ProjBoule(i[0].rect.x, i[0].rect.y, "simple", 20)
            if type(i[0]) == Bombe and self in i[1]:
                i[0].kill()
                ProjBoule(i[0].rect.x, i[0].rect.y, "simple", 100)


class Satan(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("satan.png")
        self.rect = Rect(850, 333, 100, 200)
        self.hp = 666
        self.delai1 = 100
        self.delai2 = 30
        self.counter = 5
        self.mask = pg.mask.from_surface(self.image)
        HealthBar(self)

    def update(self):
        global collisions
        if self.delai1 <= 0:
            if self.delai2 <= 0:
                ProjBoule(self.rect.x,self.rect.y,["rebond","tripleTir","simpleVise"][randint(0,2)],30)
                self.rect.y = randint(90, 500)
                self.rect.x = randint(700, 850)
                self.delai2 = 30
                self.counter -= 1
            else:
                self.delai2 -= 1
        else:
            self.delai1 -= 1
        if self.counter == 0:
            self.counter = 5
            self.delai1 = 100
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp<=0:
            self.kill()

class BossSecret(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("fantomeNoir.png")
        self.rect = Rect(900, 325, 50, 50)
        self.hp = 500
        self.delai = 150
        self.y2 = randint(120,650)
        self.cmpt = 6
        self.numAtt = 0
        self.randomNbr = randint(0, 1)
        if self.randomNbr==1:
            self.nb = -pi*100
        else:
            self.nb = pi*100
        HealthBar(self)

    def update(self):
        global collisions
        if ["murOpp", "tournant", "murTir", "special"][self.numAtt]=="special" and self.delai<=0:
            for i in range(70, self.y2-100, 50):
                ProjBoule(999, i, "simpleVise", 50, (-1, 0))
            for i in range(self.y2+50, 750, 50):
                ProjBoule(999, i, "simpleVise", 50, (-1, 0))
            if self.randomNbr==1:
                for i in range(self.y2-50, self.y2+50, 50):
                    ProjCassable(1000, i, "suivantSpe", 50)
            self.randomNbr = randint(0, 1)
            self.delai = 60
            self.cmpt -= 1
            self.y2 = randint(120,650)
        elif ["murOpp", "tournant", "murTir", "special"][self.numAtt]=="murOpp" and self.delai<=0:
            self.rect.x, self.rect.y = 900, 325
            if self.randomNbr==1:
                for i in range(0, 350, 50):
                    ProjBoule(-49, i, "simpleVise", 50, (1, 0))
                for i in range(350, 700, 50):
                    ProjBoule(1000, i, "simpleVise", 50, (-1, 0))
            else:
                for i in range(0, 350, 50):
                    ProjBoule(1000, i, "simpleVise", 50, (-1, 0))
                for i in range(350, 700, 50):
                    ProjBoule(-49, i, "simpleVise", 50, (1, 0))
            self.delai = 70
            self.cmpt -= 1
        elif ["murOpp", "tournant", "murTir", "special"][self.numAtt]=="tournant" and self.delai<=0:
            self.rect.x, self.rect.y =  p1.rect.x+cos(self.nb/100)*210, p1.rect.y+sin(self.nb/100)*210
            ProjBoule(self.rect.x, self.rect.y, "simpleVise", 50)
            if self.randomNbr==1:
                self.nb+=100
            else:
                self.nb-=100
            self.delai = 20
            self.cmpt -= 1
        elif ["murOpp", "tournant", "murTir", "special"][self.numAtt]=="tournant":
            pg.draw.rect(fenetre, (255, 0, 0), Rect(p1.rect.x+cos(self.nb/100)*250, p1.rect.y+sin(self.nb/100)*250, 10, 40))
            pg.draw.rect(fenetre, (255, 0, 0), Rect(p1.rect.x+cos(self.nb/100)*250, p1.rect.y+sin(self.nb/100)*250+50, 10, 10))
        elif ["murOpp", "tournant", "murTir", "special"][self.numAtt]=="murTir" and self.delai<=0:
            if self.randomNbr==1:
                self.rect.x, self.rect.y = 900, 325
                for i in range(-150, 200, 50):
                    ProjBoule(self.rect.x-50, self.rect.y+i, "simpleVise", 50) #Tres sympa mais pas ce que je veux
            else:
                self.rect.x, self.rect.y = 100, 325
                for i in range(-150, 200, 50):
                    ProjBoule(self.rect.x+50, self.rect.y+i, "simpleVise", 50) #Tres sympa mais pas ce que je veux
            self.delai = 100
            self.randomNbr = randint(0,1)
            self.cmpt -= 1
        self.delai -= 1
        if self.cmpt==0:  # enchainement des differentes attaques
            if self.numAtt==0:
                self.numAtt = 1
                self.cmpt = 20
            elif self.numAtt==1:
                self.numAtt = 2
                self.cmpt = 5
            elif self.numAtt==2:
                self.numAtt = 0
                self.cmpt = 6
            elif self.numAtt==3:
                self.numAtt = 0
                self.cmpt = 6
            self.delai = 150
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                hpAv = self.hp
                self.hp += - i[0].damage
                i[0].kill()
                if self.hp<=250 and hpAv>250:
                    self.numAtt = 3
                    self.cmpt = 10
                    self.delai = 100
            if type(i[0]) == Explosion and self in i[1]:
                if not self in i[0].mobsHitted:
                    self.hp -= i[0].damage
                    i[0].mobsHitted.append(self)
        if self.hp<=0:
            self.kill()


class HealthBar(pg.sprite.Sprite):
    def __init__(self,mob):
        pg.sprite.Sprite.__init__(self)
        groupe.add(self)
        self.proprio = mob
        self.image = pg.image.load("healthBar.png")
        self.hpMax = self.proprio.hp
        self.bg = Rect(333,650,300,40)
        self.rect = Rect(333,650,300,40)

    def update(self):
        self.hp = (self.proprio.hp*300)//self.hpMax
        self.rect = Rect(633-self.hp,650,self.hp,40)
        self.image = pg.image.load("HealthBar.png")
        if self.hp>0:
            pg.draw.rect(fenetre, (0, 0, 0), self.bg)
            self.image = pg.transform.scale(self.image,(self.hp,40))
            if type(self.proprio)==MiniBossDemon:
                pg.draw.rect(self.image,(255, 255, 255),Rect(99+self.hp-300,0,self.hp/(self.hp*5/10),40))
                pg.draw.rect(self.image,(255, 255, 255),Rect(199+self.hp-300,0,self.hp/(self.hp*5/10),40))
            elif type(self.proprio)==BossSecret:
                pg.draw.rect(self.image,(255, 255, 255),Rect(150+self.hp-300,0,self.hp/(self.hp*5/10),40))
        else:
            self.image = pg.transform.scale(self.image,(0,40))

class KarmaBar(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        groupe.add(self)
        self.image = pg.image.load("karmaIndicNeutre.png")
        self.rect = Rect(435, 15, 5, 30)

    def update(self):
        global karma
        pg.draw.rect(fenetre, (0, 0, 0), Rect(500, 15, 100, 30))
        pg.draw.rect(fenetre, (88, 41, 0), Rect(400, 15, 100, 30))
        pg.draw.rect(fenetre, (255, 255, 255), Rect(300, 15, 100, 30))
        self.rect.x = 450 - karma*1.5 -2.5
        if karma>=33:
            self.image = pg.image.load("karmaIndicBon.png")
        elif karma<=-33:
            self.image = pg.image.load("karmaIndicMauvais.png")


class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("steve.png").convert_alpha()
        groupe.add(self)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
        self.speedx = 0
        self.speedy = 0
        self.delay = 0
        self.bomb_delay = 0
        self.max_delay = 8
        self.max_bomb_delay= 100
        self.mercy = 0
        self.vies = save["player"][0]
        self.pv = save["player"][1]
        self.bombs = save["player"][2]
        self.damage = save["player"][3]
        self.nbullet = save["player"][4]
        self.bomb_type = liste_bombes[save["player"][5]]
        self.sprites_pvs = []
        for i in range(self.pv):
            self.sprites_pvs.append(Coeur(15 + 45*i, 10))
            groupe.add(self.sprites_pvs[i])
        groupe.add(Bombe_icone(655, 15))
        groupe.add(Vie_icone())
        self.bullet_range = [[0], (-0.05, 0.05), (-0.06, 0, 0.1), (-0.07, -0.03, 0.04, 0.08), (-0.2, -0.125, 0, 0.125, 0.2)]
        self.pewSound = pg.mixer.Sound("pew.wav")
        self.hitSound = pg.mixer.Sound("hit.wav")
        self.puSound = pg.mixer.Sound("pu.wav")

    def update(self):
        global score
        global liste
        global dt
        global escap
        global collisions
        global cont
        #mouvements
        if liste[K_RIGHT] and self.rect.x < 885:
            self.speedx = 0.3
        elif liste[K_LEFT] and self.rect.x > 0:
            self.speedx = -0.3
        else:
            self.speedx = 0
        if liste[K_DOWN] and self.rect.y < 639:
            self.speedy = 0.3
        elif liste[K_UP] and self.rect.y > 45:
            self.speedy = -0.3
        else:
            self.speedy = 0
        #tirs
        if liste[K_w] and self.delay == 0:
            self.pewSound.play()
            for i in range(self.nbullet):
                groupe.add(Bullet(self.rect.x + self.rect.width,   self.rect.y + (i+1) * self.rect.height//(self.nbullet+1), self.damage, self.bullet_range[self.nbullet - 1][i]))
            self.delay = self.max_delay
        if self.delay > 0:
            self.delay += -1
        if liste[K_x] and self.bomb_delay == 0 and self.bombs > 0:
            groupe.add(Bombe(self.rect.x + self.rect.width,   self.rect.y + (1/2) * self.rect.height, self.bomb_type, self))
            self.bomb_delay = self.max_bomb_delay
            self.bombs -= 1
        if self.bomb_delay > 0:
            self.bomb_delay -= 1
        #collisions
        for i in collisions.items():
            if i[0] == self and i[1] != None:
                for j in i[1]:
                    if type(j) == Upgrade:
                        self.puSound.play()
                        if j.mod == "bullet":
                            if self.nbullet < 4:
                                self.nbullet += 1
                            else :
                                score += 500
                        if j.mod == "damage":
                            if self.damage < 12:
                                self.damage += 2
                            else :
                                score += 500
                        if j.mod == "hp":
                            if self.pv < 5:
                                self.pv += 1
                                self.sprites_pvs.append(Coeur(self.sprites_pvs[-1].rect.x + 45,10))
                                groupe.add(self.sprites_pvs[-1])
                            else :
                                score += 500
                        if j.mod == "bomb":
                            if self.bombs < 50:
                                self.bombs += 1
                            else :
                                score += 500
                        if j.mod == "make_regular":
                            if self.bomb_type != "regular":
                                self.bomb_type = "regular"
                            else :
                                score += 500
                        if j.mod == "make_burst":
                            if self.bomb_type != "burst":
                                self.bomb_type = "burst"
                            else :
                                score += 500
                        if j.mod == "make_shield":
                            if self.bomb_type != "shield":
                                self.bomb_type = "shield"
                            else :
                                score += 500
                    elif self.mercy == 0:
                        self.hitSound.play()
                        self.pv += -1
                        self.sprites_pvs[-1].kill()
                        self.sprites_pvs.pop(-1)
                        self.mercy = 300
        if self.mercy > 0:
            self.mercy += -1
            if self.mercy % 30 == 0:
                self.image = pg.image.load("steve_white.png").convert_alpha()
                self.mask = pg.mask.from_surface(self.image)
            if self.mercy % 30 == 15 or self.mercy == 0:
                self.image = pg.image.load("steve.png").convert_alpha()
                self.mask = pg.mask.from_surface(self.image)
        #mort et fin
        fenetre.blit(font_hud.render(str(100 + self.bombs)[1:], True,(0, 0, 0),(185, 122, 87)), (705, 7))
        fenetre.blit(font_hud.render(str(100 + self.vies)[1:], True,(0, 0, 0),(185, 122, 87)), (230, 7))
        self.rect.x += self.speedx * dt
        self.rect.y += self.speedy * dt
        if self.pv <= 0:
            if self.vies == 0:
                self.kill()
                self = None
                cont = game_over()
            elif self.mercy == 299:
                self.vies -= 1
                groupe.add(Death(self.rect.x, self.rect.y))
                self.pv = 3
                self.sprites_pvs = [Coeur(15, 10), Coeur(60, 10), Coeur(105, 10)]
                for i in self.sprites_pvs:
                    groupe.add(i)
                self.bombs = 3
                self.nbullet = 1
                self.damage = 4




class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, damage, speedy):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("p_bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.speedx = 1
        self.speedy = speedy

    def update(self):
        global dt
        self.rect.x += self.speedx * dt
        self.rect.y += self.speedy * dt
        if self.rect.x >= 1000:
            self.kill()

class Bombe(pg.sprite.Sprite):
    def __init__(self, x, y, mod, caster):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("bombe.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mod = mod
        self.mask = pg.mask.from_surface(self.image)
        if mod == "regular":
            self.speedx = 1
        elif self.mod == "burst":
            self.speedx = 0
        self.delay = 70
        self. caster = caster

    def update(self):
        global dt
        global collisions
        if self.mod == "regular":
            self.rect.x += self.speedx * dt
            if self.rect.x >= 1000:
                groupe.add(Explosion(self.rect.x - 400, self.rect.y-90))
                self.kill()
            else:
                for i in collisions.items():
                    if i[0] == self and not(i[1] is None):
                        for j in i[1]:
                            if type(j) in [Fantome, Demon, Ange, MiniBossAnge, MiniBossDemon, MiniBossFantome, UFOBoss]:
                                groupe.add(Explosion(self.rect.x - 260, self.rect.y - 90))
                                self.kill()
        elif self.mod == "burst":
            self.rect.x = -100
            self.rect.y = -100
            if self.delay%6 == 0 and self.delay > 0:
                for i in range(20):
                    groupe.add(Bullet(self.caster.rect.x + self.caster.rect.width, self.caster.rect.y + (i+1) * self.caster.rect.height//20, 6, (i-10)/30))
            self.delay -= 1
            if self.delay == 0:
                self.kill()
                self = None
        elif self.mod == "shield":
            groupe.add(Shield(self.caster.rect.x, self.caster.rect.y, self.caster))
            self.kill()
            self = None



class Explosion(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("explosion.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.damage = 70
        self.delay = 80
        self.mobsHitted = []
        pg.mixer.Sound("explosion.wav").play()

    def update(self):
        if self.delay <= 0:
            self.kill()
            self = None
        else:
            self.delay -= 1


class Shield(pg.sprite.Sprite):
    def __init__(self, x, y, caster):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("shield.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.delay = 250
        self.caster = caster
        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        global collisions
        self.rect.x = self.caster.rect.x - 15
        self.rect.y = self.caster.rect.y - 15
        for i in collisions.items():
            if i[0] == self:
                for j in i[1]:
                    if type(j) in (ProjBoule, ProjCassable):
                        j.kill()
                        j = None
        self.delay -= 1
        if self.delay <= 0:
            self.kill()
            self = None


class Villain(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("diable_template.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
        self.hp = 500
        self.speedx = 0
        self.speedy = 0

    def update(self):
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
        if self.hp <= 0:
            self.kill()


class Death(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("dead.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0
        self.counter = 100

    def update(self):
        self.counter += -1
        if self.counter <= 0:
            self.kill()

class Coeur(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("coeur.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Bombe_icone(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("bombe.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Vie_icone(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("icone_vie.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = 200
        self.rect.y = 15

class Upgrade(pg.sprite.Sprite):
    def __init__(self, x, y, mod):
        pg.sprite.Sprite.__init__(self)
        self.mod = mod
        if self.mod == "damage":
            self.image = pg.image.load("upgrade_dmg.png").convert_alpha()
        if self.mod == "bullet":
            self.image = pg.image.load("upgrade_bull.png").convert_alpha()
        if self.mod == "hp":
            self.image = pg.image.load("upgrade_hp.png").convert_alpha()
        if self.mod == "bomb":
            self.image = pg.image.load("bombe_plus.png").convert_alpha()
        if self.mod == "make_regular":
            self.image = pg.image.load("bombe_regular.png").convert_alpha()
        if self.mod == "make_burst":
            self.image = pg.image.load("bombe_burst.png").convert_alpha()
        if self.mod == "make_shield":
            self.image = pg.image.load("bombe_shield.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y

    def update(self):
        global collisions, niv
        if type(niv) != Tuto:
            self.rect.x -= 0.1 * dt
        for i in collisions.items():
            if type(i[0]) == Player and self in i[1]:
                self.kill()

class Curseur(pg.sprite.Sprite):
    def __init__(self, x, y, maxpos, dist_boutons, xmax_boutons):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("curseur.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.y_first = y
        self.rect.x = x
        self.rect.y = y
        self.pos = maxpos
        self.maxpos = maxpos
        self.dist = dist_boutons
        self.xmax = xmax_boutons
        self.curs_value = 0

    def update(self):
        global liste
        global menuSound
        clic = pg.mouse.get_pressed(1)[0]
        souris = pg.mouse.get_pos()
        bonne_pos = False
        posAV = self.pos
        if self.rect.x + 70 <= souris[0] and souris[0] <= self.xmax:
            bonne_pos = True
            self.pos = self.maxpos - (souris[1] - self.y_first)//self.dist
            if self.pos < 1:
                self.pos = 1
            if self.pos > self.maxpos:
                self.pos = self.maxpos
        if liste[K_UP] and self.pos < self.maxpos:
            self.pos += 1
            self.rect.y -= self.dist
            pg.time.wait(200)
        if liste[K_DOWN] and self.pos > 1:
            self.pos += -1
            self.rect.y += self.dist
            pg.time.wait(200)
        self.rect.y = self.y_first + (self.maxpos - self.pos)*self.dist
        if liste[K_RETURN] or liste[K_w] or (clic and bonne_pos):
            self.curs_value = self.pos
            pg.time.wait(200)
        if posAV!=self.pos:
            menuSound.play()


#___________________________________________definition de tous les differents patterns/move___________________________________________
"""
dicMove(move:pattern1/pattern2/...) :
    simple:devant/derriere/haut/bas(traverse l'ecran depuis un des bords)
    traverse:asc/dsc(ascendant/descendant)  (traverse l'ecran de haut en bas ou de bas en haut en arc de cercle)
    doubleTravese:asc/dsc (traverse X 2 ...)
    piegeuageu:rush (tire en avancant puis lache des pieges puis s'enfuit)
    devantDerriere:asc/dsc (spawn devant passe derriere puis revient devant)
    passage:asc/dsc/devant/derriere (traverse ~1/3 de l'ecran puis repart dans l'autre sens(depuis un des bords))
"""

def simple(mob):
    mob.tirer()
    if mob.pattern=="devant":
        mob.rect.x-= 2
        if mob.rect.x<=-20:
            mob.kill()
    elif mob.pattern=="derriere":
        mob.rect.x+= 2
        if mob.rect.x>=1000:
            mob.kill()
    elif mob.pattern=="dsc":
        mob.rect.y+= 2
        if mob.rect.y>=700:
            mob.kill()
    elif mob.pattern=="asc":
        mob.rect.y-= 2
        if mob.rect.y<=-95:
            mob.kill()

def traverse(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 2
    elif mob.pattern=="asc":
        mob.rect.y-= 2
    mob.const +=0.02
    mob.rect.x = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+10)/5))*300+mob.x2 #C'EST A PEU PRES CA
    #mob.rect.y = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+5)/5))*300 # HEY MAIS C'EST MARRANT DE RAJOUTER CA
    if mob.const>=4:
        mob.kill()

def doubleTraverse(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 2
    elif mob.pattern=="asc":
        mob.rect.y-= 2
    mob.const +=0.02
    mob.rect.x = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+10)/5))*300+mob.x2
    if mob.const<=-4:
        mob.kill()
    elif mob.const>=4:
        if mob.pattern=="asc":
            mob.pattern="dsc"
        elif mob.pattern=="dsc":
            mob.pattern="asc"
        mob.const=-4

def piegeuageu(mob):    #DEMON?
    if mob.pattern=="rush":
        mob.rect.x -= 1.3
        mob.tirer()
    elif mob.pattern=="fuite":
        mob.rect.x += 4
    if mob.rect.x<400:
        for i in range(5):
            ProjCassable(mob.rect.x, mob.rect.y, "piege", 50)
        mob.pattern="fuite"
    if mob.pattern=="fuite" and mob.rect.x>1000:
            mob.kill()

def devantDerriere(mob):         #FANTOME?
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 1
    elif mob.pattern=="asc":
        mob.rect.y-= 1
    mob.const +=0.01
    mob.rect.x = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2-5)/2))*300+mob.x2
    if mob.const>=4:
        mob.kill()

def passage(mob):                #ANGE?
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 2
        mob.rect.y = 1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300-95
    elif mob.pattern=="asc":
        mob.rect.y-= 2
        mob.rect.y = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300+700
    elif mob.pattern=="devant":
        mob.rect.x-= 2
        mob.rect.x = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300+1000
    elif mob.pattern=="derriere":
        mob.rect.x-= 2
        mob.rect.x = 1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300-35
    mob.const +=0.02
    if mob.const>=4:
        mob.kill()


#______________________________________________________Definition des niveaux____________________________________________________________________
class Niveaux:
    """Classe hérité par les niveaux"""
    def __init__(self):
        if type(self)!=Tuto:
            Cristal()
        self.val = randint(-5, 5)
        self.tmp = 0
        self.prochain = 500
        self.warningTime = True
        self.etapes = 0
        pg.mixer.music.load("level.mp3")
        pg.mixer.music.play()
        if str(type(self))[-8:-3]=="Level":
            self.cmpt = self.nbrMob[0]

    def chainSpawn(self, x, y, hp, move, pattern, tir, delai, cd=2000, tt=30):#Fait apparaitre un ou plusieurs ennemies du meme type avec un delai entre chaque apparition
        if pattern=="derriere" and (move=="simple" or move=="passage"):
            pg.draw.rect(fenetre, (255, 0, 0), Rect(20, y, 10, 40))
            pg.draw.rect(fenetre, (255, 0, 0), Rect(20, y+50, 10, 10))
            if self.warningTime:
                self.prochain+=150
                self.warningTime = False
        if self.tmp>=self.prochain:#Detecte si la varible temps self.prochain est entre le temps lors de la derniere image et celui de cette image
            spawn(x, y, hp, move, pattern, tir, self.val, cd, tt)
            self.cmpt -= 1
            if self.cmpt<=0:
                self.etapes += 1
                self.val = randint(-5 ,5)
                self.warningTime = True
            else:
                self.prochain += delai

    def update(self):
        self.action()

class Tuto(Niveaux):
    def __init__(self):
        Niveaux.__init__(self)


    def action(self):
        global tutoMob, karma, p1, dialogue_i, liste, dialogues, no_dialogue, niv
        if  self.etapes==0:
            no_dialogue = False
            dialogue("intro")
            if dialogue_i == len(dialogues["intro"]):
                dialogue_i = 0
                no_dialogue = True
                self.etapes = 1
        if self.etapes == 1:
            p1.bombs = 0
            if (liste[pg.K_RIGHT] or liste[pg.K_LEFT] or liste[pg.K_UP] or liste[pg.K_DOWN]):
                pg.time.wait(400)
                self.etapes = 2
                self.tmp=pg.time.get_ticks()
        elif self.etapes==2:
            if pg.time.get_ticks()-self.tmp>3000:
                tutoMob=Ange(500,300,60,None,None,"rien","tuto")
                self.etapes = 3
        elif self.etapes==3:
                fenetre.blit(pg.image.load("icone_z.png").convert_alpha(),(300,200))
                if not tutoMob.alive():
                    self.etapes = 4
        elif self.etapes==4:
            tutoMob=Ange(500,randint(-30,650),60,"spe","devant","rien","tuto") # Ca serait difficile mais on peut lui faire garder ses anciens hps
            self.etapes = 5
        elif self.etapes==5:
            if not tutoMob.alive():
                if tutoMob.hp>0:
                    self.etapes = 3
                else:
                    self.etapes = 6
                    self.tmp = pg.time.get_ticks()
        elif self.etapes==6:
            if pg.time.get_ticks()-self.tmp>3000:
                tutoMob=Ange(None,randint(0,640),150,"spe","devant","simple","tuto")
                self.etapes = 7
            if pg.time.get_ticks()-self.tmp>15000 and not Upgrade in [type(e) for e in tous] and p1.damage==4:
                if p1.rect.y<350:
                    tous.add(Upgrade(350, 500, "damage"))
                    tous.add(Upgrade(400, 500, "damage"))
                    tous.add(Upgrade(450, 500, "damage"))
                else:
                    tous.add(Upgrade(350, 200, "damage"))
                    tous.add(Upgrade(400, 200, "damage"))
                    tous.add(Upgrade(450, 200, "damage"))
        elif self.etapes==7:
            if not tutoMob.alive():
                if tutoMob.hp>0:
                    self.etapes = 6
                else:
                    self.etapes = 8
                    heal=tous.add(Upgrade(tutoMob.rect.x, tutoMob.rect.y, "hp"))
                    p1.damage = 4
        elif self.etapes==8:
            if not Upgrade in [type(e) for e in tous]:
                self.etapes = 9
                self.y = p1.rect.y
        elif self.etapes==9:
            fenetre.blit(pg.image.load("icone_x.png").convert_alpha(),(300,200))
            if len(tous)<30:
                if pg.time.get_ticks()-self.tmp>220:
                    if self.y>350:
                        ProjCassable(800, 200, "piege", 50)
                    else:
                        ProjCassable(800, 500, "piege", 50)
                    self.tmp = pg.time.get_ticks()
                if p1.nbullet<=2 or p1.bombs == 0:
                    self.etapes = 8
                    if p1.nbullet<=2:
                        tous.add(Upgrade(400, 350, "bullet"))
                        tous.add(Upgrade(450, 350, "bullet"))
                    if p1.bombs == 0:
                        tous.add(Upgrade(400, 450, "bomb"))
                if not ProjCassable in [type(e) for e in tous]: # jusqu'a que tu les pete tous
                    self.etapes = 10
        elif self.etapes==10:
            niv = Level1()
            karma = 0
            p1.pv = 3
            p1.bombs = 3
            p1.nbullet = 1
            p1.damage = 4
            sauvegarde()

class Level1(Niveaux):
    """Niveau contenant la suite d'apparition des ennemis dans le temps"""
    def __init__(self):
        self.nbrMob = [1, 1, 2, 1, 1, 3, 2, 4, 1, None] #le nbr d'ennemies pour chaque chainspawn/etape
        Niveaux.__init__(self)

    def action(self):
        global niv
        etapeAv = self.etapes
        if self.etapes==0:
            self.chainSpawn(400, 0, 15, "tentacule", "haut", "normal", 10)
        elif self.etapes==1 and (self.prochain+5<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain = 5
                self.resetProchain = False
            self.chainSpawn(300, 0, 15, "tentacule", "bas", "normal", 10)
        elif self.etapes==2 and (self.prochain+10<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain += 10
                self.resetProchain = False
            self.chainSpawn(0, 400, 15, "simple", "devant", "simple", 50)
        elif self.etapes==3 and (self.prochain+75<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=75
                self.resetProchain = False
            self.chainSpawn(750, 0, 20, "traverse", "asc", "tripleTir", 50, 2500)
        elif self.etapes==4 and (self.prochain+50<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=50
                self.resetProchain = False
            self.chainSpawn(500, 150, 15, "traverse", "dsc", "tripleTir", 50)
        elif self.etapes==5 and (self.prochain+100<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=100
                self.resetProchain = False
            self.chainSpawn(500, 150, 15, "simple", "derriere", "vacillant", 50, 3000)
        elif self.etapes==6 and (self.prochain+150<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=150
                self.resetProchain = False
            self.chainSpawn(500, 150, 25, "simple", "dsc", "suivant", 50, 2500, 50)
        elif self.etapes==7 and (self.prochain+100<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=100
                self.resetProchain = False
            self.chainSpawn(500, 150, 25, "simple", "devant", "rebond", 50)
        elif self.etapes==8 and (self.prochain+200<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=200
                self.resetProchain = False
            self.chainSpawn(900, 250, 25, "faucheur", "devant", "rebond", 50)
        elif self.etapes==9 and tous.sprites()==[]:
            if self.prochain>0:
                BossNuage()
                self.prochain = 0
            elif not BossNuage in [type(e) for e in tous]:
                niv = Level2()
                sauvegarde()
        if self.etapes!=etapeAv and self.etapes<=8:
            self.cmpt = self.nbrMob[self.etapes]
            self.tmp,self.prochain = 0,0
            self.resetProchain = True
        self.tmp+=1

class Level2(Niveaux):
    """Niveau contenant la suite d'apparition des ennemis dans le temps"""
    def __init__(self):
        self.nbrMob = [2, 3, 2, 5, 1, 3, 1, 1, None]
        Niveaux.__init__(self)

    def action(self):
        global niv, karma
        self.tmp = pg.time.get_ticks()
        etapeAv = self.etapes
        if self.etapes==0:
            self.chainSpawn(400, 150, 20, "traverse", "asc", "suivant", 300, 3000)
        elif self.etapes==1 and (self.prochain+5<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain = 5
                self.resetProchain = False
            self.chainSpawn(900, 150, 20, "spe", "asc", "simple", 40, 2800, 20)
        elif self.etapes==2 and (self.prochain+75<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=75
                self.resetProchain = False
            self.chainSpawn(350, 630, 15, "simple", "derriere", "tripleTir", 50, 3000, 15)
        elif self.etapes==3 and (self.prochain+100<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=100
                self.resetProchain = False
            self.chainSpawn(800, 700, 20, "spe", "devant", "simple", 75)
        elif self.etapes==4 and (self.prochain+200<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=200
                self.resetProchain = False
            self.chainSpawn(500, 150, 20, "simple", "dsc", "simple", 100)
        elif self.etapes==5 and (self.prochain+100<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=100
                self.resetProchain = False
            self.chainSpawn(500, 150, 15, "simple", "derriere", "rebond", 75)
        elif self.etapes==6 and (self.prochain+150<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=150
                self.resetProchain = False
            self.chainSpawn(200, 500, 20, "spe", "dsc", "simpleVise", 75)
        elif self.etapes==7 and (self.prochain+15<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=15
                self.resetProchain = False
            self.chainSpawn(800, 150, 20, "spe", "asc", "simpleVise", 75)
        elif self.etapes==8 and self.prochain+400<self.tmp:
            if self.prochain>0:
                UFOBoss()
                self.prochain = 0
            elif not UFOBoss in [type(e) for e in tous]:
                BossFaucheur()
            elif not UFOBoss in [type(e) for e in tous] and not BossFaucheur in [type(e) for e in tous]:
                niv = Level3()
                sauvegarde()
        if self.etapes!=etapeAv and self.etapes<=7:
            self.cmpt = self.nbrMob[self.etapes]
            self.tmp,self.prochain = 0,0
            self.resetProchain = True
        self.tmp+=1

class Level3(Niveaux):
    """Niveau contenant la suite d'apparition des ennemis dans le temps"""
    def __init__(self):
        self.nbrMob = [3, 5, 3, 1, 1, 1, 1, 3, None]
        Niveaux.__init__(self)
        self.credits = False

    def action(self):
        global niv, karma, liste, no_dialogue
        self.tmp = pg.time.get_ticks()
        etapeAv = self.etapes
        if self.etapes==0:
            self.chainSpawn(800, 600, 25, "traverse", "dsc", "rebond", 100, 1500, 50)
        elif self.etapes==1 and (self.prochain+200<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=200
                self.resetProchain = False
            self.chainSpawn(500, 150, 30, "spe", "derriere", "simpleVise", 300, 1500, 40)
        elif self.etapes==2 and (self.prochain+350<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=350
                self.resetProchain = False
            self.chainSpawn(800, 150, 30, "spe", "dsc", "simple", 75)
        elif self.etapes==3 and (self.prochain+250<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=250
                self.resetProchain = False
            self.chainSpawn(900, 150, 0, "tentacule", "haut", "demon", 75)
        elif self.etapes==4 and (self.prochain+130<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=130
                self.resetProchain = False
            self.chainSpawn(700, 150, 0, "tentacule", "bas", "demon", 75)
        elif self.etapes==5 and (self.prochain+150<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=150
                self.resetProchain = False
            self.chainSpawn(400, 150, 0, "tentacule", "haut", "demon", 75)
        elif self.etapes==6 and (self.prochain+105<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=105
                self.resetProchain = False
            self.chainSpawn(100, 150, 0, "tentacule", "bas", "demon", 75)
        elif self.etapes==7 and (self.prochain+125<self.tmp or not self.resetProchain):
            if self.resetProchain:
                self.prochain+=125
                self.resetProchain = False
            self.chainSpawn(200, 550, 25, "traverse", "asc", "suivant", 75, 2800, 15)
        elif self.etapes==8 and self.prochain+8000<self.tmp:
            if self.prochain>0:
                if karma<-33:
                    Dieu()
                elif karma>33:
                    Satan()
                else:
                   TheNest()
                self.delai = 300
                self.prochain = 0
            elif cristauxDetruits==0:
                if Dieu in [type(e) for e in tous] or Satan in [type(e) for e in tous] or TheNest in [type(e) for e in tous]:
                    groupe.add(Bullet(randint(0, 750), 50, 10, 0.6))
                    self.delai = 300
                else:
                    if self.delai>0:
                        fenetre.blit(pg.font.SysFont('arialblack', 20).render("Tu pouvais pas te contenter de détruire les cristaux comme je te l'ait dit!", True,(255, 0, 0),(0 ,255, 255)), (100, 650))
                    elif self.delai==0:
                        BossSecret()
                    elif not BossSecret in [type(e) for e in tous]:
                        self.delai = -1
                        while not liste[K_RETURN] and self.delai>-300:
                            no_dialogue = False
                            fenetre.blit(pg.image.load("finSecrete.png"),(0,0))
                            fenetre.blit(pg.font.SysFont('arialblack', 25).render("Apres ce combat acharné, Steve compris l'importance des cristaux.", True,(255, 0, 0),(255 ,255, 255)), (50, 450))
                            fenetre.blit(pg.font.SysFont('arialblack', 25).render("Il decida alors de dedié sa vie à leur protection.", True,(255, 0, 0),(255 ,255, 255)), (50, 550))
                            fenetre.blit(pg.font.SysFont('arialblack', 25).render("Steve est depuis surnommé \"Le Gardien des Mondes\".", True,(255, 0, 0),(255 ,255, 255)), (50, 650))
                        credits()
                        cont = False
            elif not Dieu in [type(e) for e in tous] and karma<-33:
                no_dialogue = False
                fenetre.blit(pg.image.load("finMauvais.png"),(0,0))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Apres ce combat acharné, Steve compris l'importance de l'égalité.", True,(255, 0, 0),(255 ,255, 255)), (50, 450))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Il decida alors de dedié sa vie à faire souffrir tout le monde autant.", True,(255, 0, 0),(255 ,255, 255)), (50, 550))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Steve est depuis surnommé \"L'impitoyable Tortionnaire\".", True,(255, 0, 0),(255 ,255, 255)), (50, 650))
                if liste[K_RETURN]:
                    self.credits=True
                if self.credits:
                    credits()
                    cont = False
            elif not Satan in [type(e) for e in tous] and karma>33: # pareil qu'au dessus
                no_dialogue = False
                fenetre.blit(pg.image.load("finBon.png"),(0,0))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Apres ce combat acharné, Steve compris l'importance de la paix.", True,(255, 0, 0),(255 ,255, 255)), (50, 450))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Il decida alors de dedié sa vie à son maintient.", True,(255, 0, 0),(255 ,255, 255)), (50, 550))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Steve est depuis surnommé \"Le Protecteur Pacifiste\".", True,(255, 0, 0),(255 ,255, 255)), (50, 650))
                if liste[K_RETURN]:
                    self.credits=True
                if self.credits:
                    credits()
                    cont = False
            elif not TheNest in [type(e) for e in tous] and -33<=karma<=33:
                no_dialogue = False
                fenetre.blit(pg.image.load("finNeutre.png"),(0,0))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Apres ce combat acharné, Steve compris l'impotance du repos.", True,(255, 0, 0),(255 ,255, 255)), (50, 450))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Il decida alors de dedié sa vie à se reposer.", True,(255, 0, 0),(255 ,255, 255)), (50, 550))
                fenetre.blit(pg.font.SysFont('arialblack', 25).render("Steve est depuis surnommé \"Le Sommeilleur Eternel\".", True,(255, 0, 0),(255 ,255, 255)), (50, 650))
                if liste[K_RETURN]:
                    self.credits=True
                if self.credits:
                    credits()
                    cont = False
            self.delai -= 1

        if self.etapes!=etapeAv and self.etapes<=7:
            self.cmpt = self.nbrMob[self.etapes]
            self.tmp,self.prochain = 0,0
            self.resetProchain = True
        self.tmp+=1

def spawn(x, y, hp, move, pattern, tir, nbr, cd, tt):
#proba à mieux faire_________________________________________________
        if move=="faucheur":
            Faucheur(x, y)
        elif move=="tentacule":
            Tentacule(x, "normal", pattern)
        elif move=="demonTentacule":
            Tentacule(x, "demon", pattern)
        elif move=="lostSoul":
            LostSoul(x, y)
        elif karma//10-nbr>=3:
            Demon(x,y,hp,move,pattern,tir, cd, tt)
        elif karma//10-nbr<=-3:
            Ange(x,y,hp,move,pattern,tir, cd, tt)
        else:
            Fantome(x,y,hp,move,pattern,tir, cd, tt)


class Nuage(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        background.add(self)
        self.image = pg.image.load("nuage"+str(randint(1,4))+".png").convert_alpha()
        self.rect = Rect(1000, randint(-50,680), 0, 0)

    def update(self):
        self.rect.x-=4
        if self.rect.x<-100:
            self.kill()

#Définition de tous les menus______________________________________________________________________

def menu_global():
    global code
    global fenetre
    global game_state
    global parametres
    pg.mouse.set_visible(True)
    pg.mixer.music.load("menuMusic.mp3")
    pg.mixer.music.play()
    while game_state != 6 and game_state != 1:
        if parametres["fullscr"][0]:
            fenetre = pg.display.set_mode((1000, 700), pg.FULLSCREEN)
        else:
            fenetre = pg.display.set_mode((1000, 700))

        game_state = startMenu()

        if game_state == 1:#quit
            return None

        elif game_state == 5:
            code = code_menu()
            print(code)

        elif game_state == 4:
            option_menu()

        elif game_state == 3:#controles
            controles()

        elif game_state == 2:
            credits()

def startMenu():
    pg.time.wait(500)
    lancer = True
    global liste
    global font, font_titre
    global game_state
    curs = Curseur(180, 200, 6, 50, 350)
    curs_value = 0
    menu = pg.sprite.Group(curs)
    while lancer and curs_value == 0:
        titre = font_titre.render('EXAM RESIT', True, (120, 50, 150))
        text = [font.render('PLAY', True, (255, 200, 0)), font.render('PASSWORD', True,(255, 200, 0)), font.render('OPTIONS', True,(255, 200, 0)), font.render('CONTROLES', True,(255, 200, 0)), font.render('CREDITS', True,(255, 200, 0)), font.render('QUIT', True,(255, 200, 0))]
        liste = pg.key.get_pressed()
        curs.update()
        for event in pg.event.get():
            if event.type == QUIT:
                lancer = False
                game_state = 1
                return 1
        curs_value = curs.curs_value
        fenetre.blit(pg.image.load("menu.png").convert_alpha(),(0,0))
        fenetre.blit(titre, (240, 100))
        fenetre.blit(font_hud.render('SpaghettiCode Inc - Copyright 2022', True, (0, 0, 0)), (20, 20))
        fenetre.blit(font_hud.render('Version 0.' + str(randint(1,9)) + "." + str(randint(4,7)) + "." + str(randint(8, 12)) , True, (0, 0, 0)), (700, 20))
        for i in range(len(text)):
            fenetre.blit(text[i], (250, 200 + i*50))
        menu.draw(fenetre)
        pg.display.update()
    curs.kill()
    return curs_value


def option_menu():
    pg.time.wait(500)
    lancer = True
    global parametres
    global liste
    global font
    global game_state
    global save
    parametres_temp = dict(parametres)
    curs1 = Curseur(180, 200, 3, 50, 350)
    menu = pg.sprite.Group(curs1)
    curs_value = 0
    while lancer and curs_value != 1:
        curs1.curs_value = 0
        text = [font.render('Paramètres:', True,(255, 200, 0)), font.render('Plein écran :', True,(255, 200, 0)), font.render('Appliquer', True,(255, 200, 0)), font.render('Retour', True,(255, 200, 0))]
        icones = [font.render(parametres_temp["fullscr"][1], True,(255, 200, 0))]
        liste = pg.key.get_pressed()
        curs1.update()
        for event in pg.event.get():
            if event.type == QUIT:
                lancer = False
                game_state = 1
                return None
        curs_value = curs1.curs_value
        fenetre.blit(pg.image.load("menu.png").convert_alpha(),(0,0))
        for i in range(len(text)):
            fenetre.blit(text[i], (250, 150 + i*50))
        for j in range(len(icones)):
            fenetre.blit(icones[j], (450, 200 + j*50))
        if curs_value == 3:
            if parametres_temp["fullscr"] == [False, "NON"]:
                parametres_temp["fullscr"] = [True, "OUI"]
            else:
                parametres_temp["fullscr"] = [False, "NON"]
        if curs_value == 2:
            parametres = dict(parametres_temp)
        menu.draw(fenetre)
        pg.display.update()
    save["param"] = []
    for k in parametres.values():
        save["param"].append(k[0])
    curs1.kill()
    sauvegarde()
    return None

def code_menu():
    pg.time.wait(500)
    lancer = True
    global liste
    global font
    text_input = ""
    liste = pg.key.get_pressed()
    while lancer and not(liste[K_RETURN]) and not(liste[K_ESCAPE]):
        text = [font.render('Entrez votre mot de passe :', True,(255, 255, 255),(200, 0, 0)), font.render(text_input, True,(255, 255, 255),(200 ,0, 0)), font.render('Appuyez sur Entrée pour appliquer le code', True,(255, 255, 255),(200 ,0, 0)), font.render('Ou sur Echap pour revenir au menu', True,(255, 255, 255),(200 ,0, 0))]
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                lancer = False
                sys.exit()
            if event.type == 2:
                if event.scancode == 14 and len(text_input) >= 1:
                    text_input = text_input[:-1]
                elif event.scancode == 28:
                    return text_input
                elif event.scancode == 1:
                    return ""
                elif event.scancode != 14:
                    text_input += event.unicode
        fenetre.fill((0,0,0))
        for i in range(len(text)):
            fenetre.blit(text[i], (200, 150 + i*50))
        pg.display.update()

def controles():
    pg.time.wait(500)
    lancer = True
    global liste
    global font
    liste = pg.key.get_pressed()
    text = [font.render('Controles:', True,(255, 255, 255),(200, 0, 0)), font.render('Bouger : Flèches', True,(255, 255, 255),(200 ,0, 0)), font.render('Tirer : Z', True,(255, 255, 255),(200 ,0, 0)), font.render('Bombe : X', True,(255, 255, 255),(200 ,0, 0)), font.render('Pressez X ou Echap pour revenir au menu', True,(255, 255, 255),(200 ,0, 0))]
    fenetre.fill((0,0,0))
    for i in range(len(text)):
            fenetre.blit(text[i], (200, 150 + i*50))
    pg.display.update()
    while lancer and not(liste[K_x]) and not(liste[K_ESCAPE]):
        liste = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                lancer = False
                sys.exit()

def credits():
    pg.time.wait(500)
    lancer = True
    global liste
    global font
    global game_state
    liste = pg.key.get_pressed()
    text = [font_credits.render('Directeurs de projet : Bocquel Raphaël et Yanis Bouchilloux', True,(255, 200, 0)), font_credits.render('Game design et scenario : Bocquel Raphaël et Yanis Bouchilloux', True,(255, 200, 0)), font_credits.render('Concepts artistes, Designers graphiques, Sprite managers : Bocquel Raphaël et Yanis Bouchilloux (et Paint)', True,(255, 200, 0)), font_credits.render('Programmation additionnelle : Bocquel Raphaël et Yanis Bouchilloux', True,(255, 200, 0)), font_credits.render('Responsables des chevreuils : Bocquel Raphaël et Yanis Bouchilloux', True,(255, 200, 0)), font_credits.render('Testeurs : Bocquel Raphaël et Yanis Bouchilloux', True,(255, 200, 0)), font_credits.render('Merci à Mme Livoti et à l ensemble de la classe de NSI de Terminale 2021/2022 !', True,(255, 200, 0)), font_hud.render('Pressez X ou Echap pour revenir au menu', True,(255, 200, 0))]
    img = pg.image.load("menu.png").convert_alpha()
    fenetre.blit(pg.transform.scale(img,(1000,700)),(0,0))
    for i in range(len(text)):
            fenetre.blit(text[i], (25, 150 + i*50))
    pg.display.update()
    while lancer and not(liste[K_x]) and not(liste[K_ESCAPE]):
        liste = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == QUIT:
                lancer = False
                game_state = 1
                return None

def pause_menu():
    pg.time.wait(500)
    lancer = True
    global liste
    global font
    global game_state
    curs = Curseur(180, 200, 2, 50, 350)
    pg.mouse.set_visible(True)
    curs_value = 0
    menu = pg.sprite.Group(curs)
    while lancer and curs_value == 0:
        text = [font.render('PAUSE', True,(255, 200, 0)), font.render('Reprendre', True,(255, 200, 0)), font.render('Retour au menu principal', True,(255, 200, 0))]
        liste = pg.key.get_pressed()
        curs.update()
        for event in pg.event.get():
            if event.type == QUIT:
                game_state = 1
                lancer = False
                return False
        curs_value = curs.curs_value
        img = pg.image.load("menu_pause.png").convert_alpha()
        fenetre.blit(pg.transform.scale(img,(1000,700)),(0,0))
        for i in range(len(text)):
            fenetre.blit(text[i], (250, 150 + i*50))
        menu.draw(fenetre)
        pg.display.update()
    curs.kill()
    pg.mouse.set_visible(False)
    if curs_value == 1:
        return False
    return True

def game_over():
    pg.time.wait(500)
    lancer = True
    global liste
    global font
    global game_state, flavor_texts
    curs = Curseur(180, 200, 2, 50, 350)
    pg.mouse.set_visible(True)
    curs_value = 0
    menu = pg.sprite.Group(curs)
    indice = randint(0,len(flavor_texts)-1)
    while lancer and curs_value == 0:
        text = [font.render(flavor_texts[indice], True,(255, 200, 0)), font.render('Recommencer le niveau', True,(255, 200, 0)), font.render('Retour au menu principal', True,(255, 200, 0))]
        liste = pg.key.get_pressed()
        curs.update()
        for event in pg.event.get():
            if event.type == QUIT:
                game_state = 1
                lancer = False
                return False
        curs_value = curs.curs_value
        fenetre.blit(pg.image.load("game_over.png").convert_alpha(),(0,0))
        for i in range(len(text)):
            fenetre.blit(text[i], (250, 150 + i*50))
        menu.draw(fenetre)
        pg.display.update()
    curs.kill()
    pg.mouse.set_visible(False)
    if curs_value == 2:
        game_state = 7
    return False

#Boucle principale du jeu_____________________________________________

def jeu_main():
    global liste, code, tous, collisions, groupe, dt, game_state, karma, p1, score, font, no_dialogue
    cont = True
    bgDelai = 0
    lstMob=[]
    p1 = Player(100, 100)
    KarmaBar()
    pg.mouse.set_visible(False)
    while cont:
        pg.event.pump()
        for event in pg.event.get():
            if event.type == QUIT:
                game_state = 1
                return None
        fenetre.fill((0,255,255))
        liste = pg.key.get_pressed()
        Niveaux.update(niv)
        collisions = pg.sprite.groupcollide(groupe, tous, False, False, pg.sprite.collide_mask)
        dt = clock.tick(60)
        if liste[K_ESCAPE]:
            cont = pause_menu()
        fenetre.blit(pg.image.load("barre_hud.png").convert_alpha(),(0,0))
        fenetre.blit(font_hud.render(str(1000000 + score)[1:], True,(0, 0, 0),(185, 122, 87)), (850, 7))
        if no_dialogue:
            if pg.time.get_ticks()-bgDelai>1500:
                Nuage()
                bgDelai = pg.time.get_ticks()
            tous.update()
            groupe.update()
            background.update()
            tous.draw(fenetre)
            groupe.draw(fenetre)
            background.draw(fenetre)
        pg.display.update()
    for i in tous:
        i.kill()
    for j in groupe:
        j.kill()
    if game_state == 7:
        game_state = 6
    elif game_state != 1:
        game_state = 0

def dialogue(scene):
    global dialogues, liste, dialogue_i
    i = dialogues[scene][dialogue_i]
    if i[0] == "steve.png":
        icone = pg.image.load("steve.png").convert_alpha()
        pg.transform.scale(icone,(1000,333))
        fenetre.blit(icone,(5, 320))
    else:
        icone = pg.image.load(i[0]).convert_alpha()
        fenetre.blit(icone,(750,280))
    fenetre.blit(pg.image.load("cadre.png").convert_alpha(),(55,400))
    fenetre.blit(font_dialogue.render(i[1], True, (36,36,185)), (120, 470))
    if liste[K_w]:
        pg.time.wait(400)
        dialogue_i += 1

def sauvegarde():
    global save, karma, liste_bombes, score, niv
    save["level"] = 3
    save["karma"] = karma
    save["cristals_killed"] = cristauxDetruits
    save["score"] = score
    save["player"] = str(p1.vies) + str(p1.pv) + str(p1.bombs) + str(p1.damage) + str(p1.nbullet) + str(liste_bombes.index(p1.bomb_type))
    save_player = ""
    for k in save["player"]:
        save_player += str(k) + ","
    save_player = save_player[:-1]
    save["param"]
    param = ""
    for l in save["param"]:
        if l:
            param += "1"
        else:
            param += "0"
    with open("save.txt", "w") as f:
        f.write(str(save["level"]) + "\n" + str(save["karma"]) + "\n" + str(save["cristals_killed"]) + "\n" + str(save["score"]) + "\n" + save_player  + "\n" + param)
        f.close()



#Début du programme_____________________________________________
save = {}
menuSound, menuSound2 = pg.mixer.Sound("menu.wav"), pg.mixer.Sound("menu2.wav")
liste_bombes = ["regular", "burst", "shield"]
with open("save.txt", "r") as f:
    save["level"] = int(f.readline())
    save["karma"] = int(f.readline())
    save["cristals_killed"] = int(f.readline())
    save["score"] = int(f.readline())
    save["player"] = [int(j) for j in f.readline().split(",")]
    save["param"] = []
    for i in f.readline():
        if i == "0":
            save["param"].append(False)
        else:
            save["param"].append(True)
    f.close()
font_hud = pg.font.SysFont('arialblack', 32)
font_credits = pg.font.SysFont('arialblack', 16)
font_dialogue = pg.font.Font('IMMORTAL.ttf', 22)
font = pg.font.Font('ENDOR___.ttf', 30)
font_titre = pg.font.Font('ENDOR___.ttf', 60)
dialogue_i = 0
no_dialogue = True
code = ""
escap = False
parametres ={'fullscr':[save["param"][0], "NON "]}
game_state = 0
score = 0
vies = 3
pg.key.set_repeat(250)
parametres = {'fullscr':[save["param"][0], "NON"]}
game_state = 0
score = save["score"]
karma = save["karma"]
cristauxDetruits = save["cristals_killed"]
collisions = None
dt = None
liste = None
p1 = None
tous=pg.sprite.Group()
groupe = pg.sprite.Group()
background = pg.sprite.Group()
liste_niveaux = [Tuto(), Level1(),Level2(),Level3()]
for i in tous:
    i.kill()
niv = liste_niveaux[save["level"]]
while game_state != 1:
    menu_global()
    if game_state != 1:
        jeu_main()
pg.quit()
sys.exit()