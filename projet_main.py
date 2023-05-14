import pygame as pg
import sys
from pygame.locals import *
from random import randint
from math import sin,exp,pi,sqrt

pg.init()
fenetre = pg.display.set_mode((1000, 700))
clock = pg.time.Clock()



class Player(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("joueur1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pg.mask.from_surface(self.image)
        self.pv = 3
        self.speedx = 0
        self.speedy = 0
        self.delay = 0
        self.max_delay = 8
        self.mercy = 0
        self.nbullet = 1
        self.damage = 4

    def update(self):
        global dt
        global escap
        global collisions
        liste = pg.key.get_pressed()
        if liste[K_ESCAPE]:
            escap = True
        if liste[K_RIGHT] and self.rect.x < 885:
            self.speedx = 0.3
        elif liste[K_LEFT] and self.rect.x > 0:
            self.speedx = -0.3
        else:
            self.speedx = 0
        if liste[K_DOWN] and self.rect.y < 639:
            self.speedy = 0.3
        elif liste[K_UP] and self.rect.y >0:
            self.speedy = -0.3
        else:
            self.speedy = 0
        if liste[K_w] and self.delay == 0:
            for i in range(self.nbullet):
                groupe.add(Bullet(self.rect.x + self.rect.width,   self.rect.y + (i+1) * self.rect.height//(self.nbullet+1), self.damage))
            self.delay = self.max_delay
        if self.delay > 0:
            self.delay += -1
        for i in collisions.items():
            if i[0] == self and i[1] != None:
                for j in i[1]:
                    if type(j) == Upgrade:
                        if j.mod == "bullet":
                            self.nbullet += 1
                        if j.mod == "damage":
                            self.damage += 2
                        if j.mod == "hp":
                            self.pv += 1
                            pvs.append(Coeur(pvs[-1].rect.x + 45,20))
                            groupe.add(pvs[-1])
                    elif self.mercy == 0:
                        self.pv += -1
                        pvs[-1].kill()
                        pvs.pop(-1)
                        print(self.pv)
                        self.mercy = 300
        if self.mercy > 0:
            self.mercy += -1
        if self.pv <= 0:
            dead = Death(self.rect.x, self.rect.y)
            groupe.add(dead)
            self.kill()
        self.rect.x += self.speedx * dt
        self.rect.y += self.speedy * dt


class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y, damage):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("p_bullet1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.damage = damage
        self.speedx = 1

    def update(self):
        global dt
        self.rect.x += self.speedx * dt
        if self.rect.x >= 1000:
            self.kill()


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
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.x = x
        self.rect.y = y
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.rect.x -= 1 #A prendre ou à laisser (en tout cas faut éviter de pouvoir stacker les buffs)
        if self.rect.x<0:
            self.kill()
        global collisions
        for i in collisions.items():
            if type(i[0]) == Player and self in i[1]:
                self.kill()

class Curseur(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load("curseur.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.pos = 5
        self.count = 1
        self.curs_value = 0

    def update(self):
        liste = pg.key.get_pressed()
        clic = pg.mouse.get_pressed(1)[0]
        souris = pg.mouse.get_pos()
        bonne_pos = False
        if 200 <= souris[0] and souris[0] <= 350:
            if 200 <= souris[1] < 250:
                self.pos = 5
                bonne_pos = True
            if 250 <= souris[1] < 300:
                self.pos = 4
                bonne_pos = True
            if 300 <= souris[1] < 350:
                self.pos = 3
                bonne_pos = True
            if 350 <= souris[1] < 400:
                self.pos = 2
                bonne_pos = True
            if 400 <= souris[1] < 450:
                self.pos = 1
                bonne_pos = True
        if liste[K_UP] and self.pos < 5:
            self.pos += 1
            pg.time.wait(120)
        if liste[K_DOWN] and self.pos > 1:
            self.pos += -1
            pg.time.wait(120)
        if self.pos == 5:
            self.rect.y = 200
        if self.pos == 4:
            self.rect.y = 250
        if self.pos == 3:
            self.rect.y = 300
        if self.pos == 2:
            self.rect.y = 350
        if self.pos == 1:
            self.rect.y = 400
        if liste[K_RETURN] or liste[K_w] or (clic and bonne_pos):
            self.curs_value = self.pos
            if self.count == 1:
                self.count += -1
            else:
                self.kill()

#DÃƒÆ’Ã‚Â©but du jeu______________________________________________________________________

def startMenu():
    lancer = True
    global font
    curs = Curseur(130, 150)
    curs_value = 0
    menu = pg.sprite.Group(curs)
    while lancer and curs_value == 0:
        text = [font.render('Welcome to GAME', True,(255, 255, 255),(200, 0, 0)), font.render('PLAY', True,(255, 255, 255),(200 ,0, 0)), font.render('PASSWORD', True,(255, 255, 255),(200 ,0, 0)), font.render('OPTIONS', True,(255, 255, 255),(200 ,0, 0)), font.render('CONTROLES', True,(255, 255, 255),(200 ,0, 0)), font.render('QUIT', True,(255, 255, 255),(200 ,0, 0))]
        liste = pg.key.get_pressed()
        curs.update()
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                lancer = False
                sys.exit()
        curs_value = curs.curs_value
        fenetre.fill((0,0,0))
        for i in range(len(text)):
            fenetre.blit(text[i], (200, 150 + i*50))
        menu.draw(fenetre)
        pg.display.update()

    return 1, curs_value



tous=pg.sprite.Group()
font = pg.font.SysFont('arialblack', 32)
game_state = 0
code = ""
while game_state != 5 and game_state != 1:
    cont, game_state = startMenu()

    if game_state == 1:#quit
        pg.quit()
        sys.exit()

    elif game_state == 2:#controles
        print("")

#    elif game_state == 3:
#        code = code_menu()

#    elif game_state == 4:
#        option_menu()



#/////////////////////////////////////////////////////////////////////////Partie nul/////////////////////////////////////////////////////////////////////////////
#_________________________________________ptet faire class pour tt mob________________________________________________________________
tous=pg.sprite.Group()

class ProjBoule(pg.sprite.Sprite):
    def __init__(self,x,y,type,taille,traj=None,speed=7):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        self.image = pg.image.load("bouBoule.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))
        self.rect = pg.Rect(x-25-(14*self.taille/30-30), y+10-(14*self.taille/30-30),self.taille+10,self.taille)
        self.type = type
        self.speed = speed
        self.rebond = 0
        if self.type[:9]=="vacillant":
            self.x2 = pg.time.get_ticks()/4
            self.y2 = self.rect.y
        if traj==None:
            self.vect = pg.math.Vector2(p1.rect.x+40 - self.rect.x, p1.rect.y+30 - self.rect.y)
        else:
            self.vect = pg.math.Vector2(traj[0],traj[1])
        if self.type=="tripleTir":
            self.vect = pg.math.Vector2(-2,1)
            ProjBoule(self.rect.x+7,self.rect.y-25,"tripleTir1",self.taille)
        elif self.type=="tripleTir1":
            self.vect = pg.math.Vector2(-2,0)
            ProjBoule(self.rect.x+7,self.rect.y-25,"tripleTir2",self.taille)
        elif self.type=="tripleTir2":
            self.vect = pg.math.Vector2(-2,-1)
        self.vect.scale_to_length(self.speed)


    def update(self):
        if self.type=="simple":
            self.rect.x -=7
        elif self.type=="simpleVise" or self.type[:9]=="tripleTir":
            self.rect.move_ip([round(self.vect[0]),round(self.vect[1])])
        elif self.type[:9]=="vacillant":
            self.x2 -= 4
            self.rect.x -= 4
            if len(self.type)==9:
                self.rect.y = sin(self.x2/50)*100+self.y2
            else:
                self.rect.y = sin(self.x2/200)*150+self.y2
        elif self.type=="rebond":
            if (self.rect.y>=700-self.taille or self.rect.y<0) and self.rebond<3:
                self.vect = pg.math.Vector2(self.vect[0],-self.vect[1])
                self.vect.scale_to_length(self.speed)
                self.rebond+=1
            if (self.rect.x<0 or self.rect.x>1000-self.taille) and self.rebond<3:
                self.vect = pg.math.Vector2(-self.vect[0],self.vect[1])
                self.vect.scale_to_length(self.speed)
                self.rebond+=1
            self.rect.move_ip([round(self.vect[0]),round(self.vect[1])])
        elif self.type=="suivant":
            self.autoguidage(p1,"lent")
        #elif self.type=="missile":
        #    self.autoguidage(p1,"vite")
        if self.rect.y>=700 or self.rect.y<-self.taille or self.rect.x<=-self.taille or self.rect.x>=1000:
            self.kill()

    def autoguidage(self, joueur, vit):
        if vit=="lent":
            self.vect = pg.math.Vector2(joueur.rect.x+self.taille+ - self.rect.x, joueur.rect.y+30 - self.rect.y)
            if self.vect[0]!=0 or self.vect[1]!=0:
                if abs(self.vect[0])+abs(self.vect[1])<150:
                    self.speed = 3.5
                else:
                    self.speed = 4
                self.vect.scale_to_length(self.speed)
                self.rect.move_ip(self.vect)
        """
        elif vit=="vite":
            self.speed+=0.05
            if self.rect.x-20>joueur.rect.x:
                vect = pg.math.Vector2(joueur.rect.x+40 - self.rect.x, joueur.rect.y+30 - self.rect.y)
                print(self.rect.x-40,joueur.rect.x)
            vect.scale_to_length(self.speed)
            self.rect.move_ip(vect)
        """

class ProjCassable(pg.sprite.Sprite):
    def __init__(self,x,y,type,taille):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.taille = taille
        self.image = pg.image.load("piege.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))
        self.rect = pg.Rect(x-25-(14*self.taille/30-30), y+10-(14*self.taille/30-30),self.taille+10,self.taille)
        self.type = type
        self.hp = 15
        self.speed = 5
        if self.type=="piege":
            self.trajP = pg.math.Vector2(-5, randint(-5,5))
        elif self.type=="meteor":
            self.trajP = pg.math.Vector2(-1,2)

    def update(self):
        if self.type=="meteor":
            self.trajP.scale_to_length(self.speed)
            self.rect.move_ip(self.trajP)
        elif self.type=="piege":
            if self.speed>0:
                self.trajP.scale_to_length(self.speed)
                self.rect.move_ip(self.trajP)
                self.speed -= 0.1
        if self.rect.y>=700 or self.rect.y<-30 or self.rect.x<=-30 or self.rect.x>=1000:
            self.kill()
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
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

class File:
    def __init__(self,tailleMax):
        self.lst=[]
        self.tailleMax = tailleMax
    def est_pleine(self):
        return len(self.lst)==self.tailleMax
    def enfiler(self,e):
        if not self.est_pleine():
            self.lst.append(e)
    def tete(self):
        if self.lst!=[]:
            return self.lst[0]
    def defiler(self):
        if self.lst!=[]:
            return self.lst.pop(0)
    def __str__(self):
        print("(tete)")
        for i in self.lst:
            print("|"+str(i)+"|")
        return "Cette file contient {} ÃƒÆ’Ã†â€™Ãƒâ€ Ã¢â‚¬â„¢ÃƒÆ’Ã¢â‚¬Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ÃƒÆ’Ã†â€™ÃƒÂ¢Ã¢â€šÂ¬Ã…Â¡ÃƒÆ’Ã¢â‚¬Å¡Ãƒâ€šÃ‚Â©lement(s) et sa tete est {}".format(len(self.lst),self.tete())

class Cible(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("Cible.png").convert_alpha()
        self.pos = File(50)
        self.rect = pg.Rect(500,350,30,30)
        self.traj = pg.math.Vector2(0,0)
        self.speed = 10

    def update(self):
        if self.pos.est_pleine():
            x,y=self.pos.defiler()
            self.traj = pg.math.Vector2(x-self.rect.x+35,y-self.rect.y+20)
        self.pos.enfiler((p1.rect.x,p1.rect.y))
        if (self.traj[0]<=-5 or self.traj[0]>=5) or (self.traj[1]<=-5 or self.traj[1]>=5):
            self.traj.scale_to_length(self.speed)
            self.rect.move_ip(self.traj)

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
                self.rect = pg.Rect(x, 720,40,92)
            elif self.pattern=="dsc":
                self.rect = pg.Rect(x, -70,40,92)
            elif self.pattern=="devant" or self.pattern=="rush":
                self.rect = pg.Rect(1000, y, 40, 92)
            elif self.pattern=="derriere":
                self.rect = pg.Rect(-20, y, 40, 92)
        elif self.move=="devantDerriere":
            if self.pattern=="asc":
                self.rect = pg.Rect(1000, 700, 40, 92)
            elif self.pattern=="dsc":
                self.rect = pg.Rect(1000, -200, 40, 92)
        else:
            self.rect = pg.Rect(x, y, 40, 92)
        self.x2 = self.rect.x

    def setCooldown(self,cooldown):
        self.cooldown = cooldown

    def tirer(self):
        if self.rect.y<650 and self.rect.y>0 and self.rect.x>40 and self.rect.x<960:
            if pg.time.get_ticks()-self.dernierTir>self.cooldown and self.tire!="rien":
                self.dernierTir = pg.time.get_ticks()
                ProjBoule(self.rect.x,self.rect.y,self.tire,self.tailleTir)

    def update(self):
        global karma
        if self.move=="simple":
            simple(self)
        elif self.move=="traverse":
            traverse(self)
        elif self.move=="doubleTraverse":
            doubleTraverse(self)
        elif self.move=="piegeuageu": #Un ptit dragon qui crache des ptites flammes?
            piegeuageu(self)
        elif self.move=="devantDerriere":
            devantDerriere(self)
        elif self.move=="passage":
            passage(self)
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
        if self.hp <= 0:
            self.kill()
            nbr = randint(0,100)
            if type(self)==Ange:
                karma-=20
                if nbr>79:
                    if nbr>=94:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    if nbr+<=86:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
            elif type(self)==Demon:
                karma+=20
                if nbr>95:
                    if nbr>=99:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    if nbr<=97:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
            elif type(self)==Fantome:
                if nbr>86:
                    if nbr>=99:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "damage"))
                    if nbr<=97:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "hp"))
                    else:
                        tous.add(Upgrade(self.rect.x, self.rect.y, "bullet"))
                karma+=5

class Ange(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=1500,tailleTir=30):
        trashMob.__init__(self,x,y,hp,move,pattern,tire)
        self.tailleTir = tailleTir
        self.cooldown = cooldown
        self.image = pg.image.load("archange_superieur_divin_genial.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(30,92))



class Demon(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=2000,tailleTir=30):
        trashMob.__init__(self,x,y,hp,move,pattern,tire)
        self.tailleTir = tailleTir
        self.cooldown = cooldown
        self.image = pg.image.load("archidemon_superieur_demoniaque_trop_dark.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(30,92))


class Fantome(trashMob):
    def __init__(self,x,y,hp,move,pattern,tire,cooldown=1800,tailleTir=30):
        trashMob.__init__(self,x,y,hp,move,pattern,tire)
        self.tailleTir = tailleTir
        self.cooldown = cooldown
        self.image = pg.image.load("fantome.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(30,92))


class miniBossFantome(pg.sprite.Sprite): #ATTENTION PERTE DE FPS
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.rect = Rect(700,325,50,50)
        self.image = pg.image.load("miniBossFantome.png").convert_alpha()
        self.taille = 50
        self.hp = 250
        self.pattern = "gonflage"
        self.dernierTir = pg.time.get_ticks()

    def tirer(self):
        if pg.time.get_ticks()-self.dernierTir>1500 and self.pattern=="gonflage":
            if self.taille>=80:
                self.taille-=30
                self.rect.x+=15
                self.rect.y+=15
            elif self.taille>50:
                nbr = self.taille-30
                self.taille-=nbr
                self.rect.x+=nbr//2
                self.rect.y+=nbr//2
            self.dernierTir = pg.time.get_ticks()
            ProjBoule(self.rect.x-((self.taille+50)/30),self.rect.y+(14*self.taille/30-30),"simpleVise",self.taille//3)
        elif pg.time.get_ticks()-self.dernierTir>150 and self.pattern=="degonflage":
            self.taille-=10
            self.rect.x+=5
            self.rect.y+=5
            ProjBoule(self.rect.x-((self.taille+50)/30),self.rect.y+(14*self.taille/30-30),"simpleVise",50,(-10,randint(-10,10)))
            self.dernierTir = pg.time.get_ticks()
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
        if self.taille >= 500:
            self.pattern = "degonflage"
        if self.hp<=0:
            self.kill()
        self.image = pg.image.load("miniBossFantome.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(self.taille,self.taille))

class miniBossAnge(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("miniBossAnge.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(100,100))
        self.rect = pg.Rect(900, 300,100,100)
        self.tmp=pg.time.get_ticks()
        self.tmp2=pg.time.get_ticks()
        self.hp = 350
        self.move = "asc"

    def update(self):
        if pg.time.get_ticks()-self.tmp>2000:
            ProjBoule(self.rect.x,self.rect.y,"simple",50)
            self.tmp = pg.time.get_ticks()
        if pg.time.get_ticks()-self.tmp2>150:
            ProjBoule(850,150,"vacillantSpe",5)
            ProjBoule(850,470,"vacillantSpe",5)
            self.tmp2 = pg.time.get_ticks()
        global collisions
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                self.hp += - i[0].damage
                i[0].kill()
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


class miniBossDemon(pg.sprite.Sprite): #Il est plus trop "mini" mais bon...
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        tous.add(self)
        self.image = pg.image.load("miniBossDemon.png").convert_alpha()
        self.image = pg.transform.scale(self.image,(300,300))
        self.rect = Rect(1000,200,300,300)
        self.triggerx = 500
        self.hp = 500
        self.passage = 3
        self.tmp = pg.time.get_ticks()
        self.enTir = False
        self.cible = (-1,0)


    def tirer(self):
        if pg.time.get_ticks()-self.tmp>3000 and not self.enTir:
            self.enTir = True
            self.tmp = pg.time.get_ticks()
            self.cible = p1.rect.x-self.rect.x-20,p1.rect.y-self.rect.y-85
        elif pg.time.get_ticks()-self.tmp>300 and pg.time.get_ticks()-self.tmp<500 and self.enTir:
            self.enTir = False
        if self.enTir:
            ProjBoule(self.rect.x+20,self.rect.y+85,"rebond",50,self.cible)

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
                    ProjCassable(self.rect.x+20, self.rect.y+80, "piege", 70)
        for i in collisions.items():
            if type(i[0]) == Bullet and self in i[1]:
                hpAv = self.hp
                self.hp += - i[0].damage
                hpAp = self.hp
                i[0].kill()
                if hpAv>350 and hpAp<350:
                    self.passage += 5
                elif hpAv>150 and hpAp<150:
                    self.passage += 7
        if self.hp <= 0:
            self.kill()

#FAIRE PHASE OU FAUT PAS ATTAQUER?

#___________________________________________definition de tous les differents patterns/move___________________________________________
"""
dicMove(move:pattern1/pattern2/...) :
    simple:devant/derriere/haut/bas(traverse l'ecran depuis un des bords)
    traverse:asc/dsc(ascendant/descendant)  (traverse l'ecran de haut en bas ou de bas en haut en arc de cercle)
    doubleTravese:asc/dsc (traverse X 2 ...(on dirait du step))
    piegeuageu:rush (tire en avanÃƒÆ’Ã‚Â§ant puis lache des pieges puis s'enfuit(je l'ai pompÃƒÆ’Ã‚Â© d'un jeu mais bon...))
    devantDerriere:asc/dsc (spawn devant passe derriere puis revient devant)
    passage:asc/dsc/devant/derriere (traverse ~1/3 de l'ecran puis repart dans l'autre sens(depuis un des bords))
"""

def simple(mob):
    mob.tirer()
    if mob.pattern=="devant":
        mob.rect.x-= 3
        if mob.rect.x<=-20:
            mob.kill()
    elif mob.pattern=="derriere":
        mob.rect.x+= 3
        if mob.rect.x>=1000:
            mob.kill()
    elif mob.pattern=="haut":
        mob.rect.y+= 3
        if mob.rect.y>=700:
            mob.kill()
    elif mob.pattern=="bas":
        mob.rect.y-= 3
        if mob.rect.y<=-95:
            mob.kill()

def traverse(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 3
    elif mob.pattern=="asc":
        mob.rect.y-= 3
    mob.const +=0.03
    mob.rect.x = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+10)/5))*300+mob.x2 #C'EST A PEU PRES CA
    #mob.rect.y = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+5)/5))*300 # HEY MAIS C'EST MARRANT DE RAJOUTER CA
    if mob.const>=4:
        mob.kill()

def doubleTraverse(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 3
    elif mob.pattern=="asc":
        mob.rect.y-= 3
    mob.const +=0.03
    mob.rect.x = 1/sqrt(2*pi)*5*exp(-1/2*((mob.const**2+10)/5))*300+mob.x2
    if mob.const<=-4:
        mob.kill()
    elif mob.const>=4:
        if mob.pattern=="asc":
            mob.pattern="dsc"
        elif mob.pattern=="dsc":
            mob.pattern="asc"
        mob.const=-4

def piegeuageu(mob):
    if mob.pattern=="rush":
        mob.rect.x -= 2
        mob.tirer()
    elif mob.pattern=="fuite":
        mob.rect.x += 4.5
    if mob.rect.x<300:
        for i in range(5):
            ProjCassable(mob.rect.x, mob.rect.y, "piege", 50)
            mob.pattern="fuite"
    if mob.pattern=="fuite" and mob.rect.x>1000:
            mob.kill()

def devantDerriere(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 1
    elif mob.pattern=="asc":
        mob.rect.y-= 1
    mob.const +=0.01
    mob.rect.x = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2-5)/2))*300+mob.x2
    if mob.const>=4:
        mob.kill()

def passage(mob):
    mob.tirer()
    if mob.pattern=="dsc":
        mob.rect.y+= 3
        mob.rect.y = 1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300-95
    elif mob.pattern=="asc":
        mob.rect.y-= 3
        mob.rect.y = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300+700
    elif mob.pattern=="devant":
        mob.rect.x-= 3
        mob.rect.x = -1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300+1000
    elif mob.pattern=="derriere":
        mob.rect.x-= 3
        mob.rect.x = 1/sqrt(2*pi)*2*exp(-1/2*((mob.const**2)/2))*300-35
    mob.const +=0.03
    if mob.const>=4:
        mob.kill()

class Niveaux:
    def __init__(self):
        level = "tuto" #juste pur l'instant
        with open("save.txt", "r") as f:
            self.etapes = int(f.read(2))

    def update(self):
        self.action()

class Tuto(Niveaux):
    def __init__(self):
        Niveaux.__init__(self)
        self.tmp = 0
        if self.etapes==6:
            self.tmp = pg.time.get_ticks()
        elif self.etapes==8:
            self.tmp = 0
            self.y = 200

    def action(self):
        global tutoMob, t
        if  self.etapes==1:
            liste = pg.key.get_pressed()
            if (liste[pg.K_RIGHT] or liste[pg.K_LEFT] or liste[pg.K_UP] or liste[pg.K_DOWN]):
                self.etapes = 2
                self.tmp=pg.time.get_ticks()
        elif self.etapes==2:
            if pg.time.get_ticks()-self.tmp>3000:
                tutoMob=Ange(500,300,50,None,None,"rien")
                self.etapes = 3
        elif self.etapes==3:
                if not tutoMob.alive():
                    self.etapes = 4
                    with open("save.txt", "w") as f:
                        f.write("4")
        elif self.etapes==4:
            tutoMob=Ange(None,randint(-30,650),50,"passage","devant","rien") # Ca serait difficile mais on peut lui faire garder ses anciens hps
            self.etapes = 5
        elif self.etapes==5:
            if not tutoMob.alive():
                if tutoMob.hp>0:
                    self.etapes = 4
                else:
                    self.etapes = 6
                    with open("save.txt", "w") as f:
                        f.write("6")
                    self.tmp = pg.time.get_ticks()
        elif self.etapes==6: # Le moment est venu de vous tuer!
            if pg.time.get_ticks()-self.tmp>3000:
                tutoMob=Ange(None,randint(-30,650),100,"passage","devant","simple")
                self.etapes = 7
            if pg.time.get_ticks()-self.tmp>10000 and pg.time.get_ticks()-self.tmp<14300: # ~ 4288 ms pour un passage
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
                    p1.damage -= 6
                    with open("save.txt", "w") as f:
                        f.write("8")
                        self.y = tutoMob.rect.y
        elif self.etapes==8:
            if not Upgrade in [type(e) for e in tous]:# y a surement un truc a faire avec group.has() mais jsp
                self.etapes = 9
        elif self.etapes==9:
            if len(tous)<30:
                if pg.time.get_ticks()-self.tmp>300:
                    if self.y>350:
                        ProjCassable(800, 200, "piege", 50)
                    else:
                        ProjCassable(800, 500, "piege", 50)
                    self.tmp = pg.time.get_ticks()
                if p1.nbullet==1:
                    self.etapes = 8
                    tous.add(Upgrade(400, 350, "bullet"))
                    tous.add(Upgrade(450, 350, "bullet"))
                if not ProjCassable in [type(e) for e in tous]: # jusqu'a que tu les pete tous
                    self.etapes = 10
                    with open("save.txt", "w") as f:
                        f.write("10")
        elif self.etapes==10:
            #Brovo, t'as enfin fini le tuto (et j'ai enfin fini de le programmer)
            print("yay")
            miniBossFantome()
            t=Level1()

class Level1:
    def __init__(self):
        Niveaux.__init__(self)
        self.tmp = 0

    def action(self):
        """
        if pg.time.get_ticks()-self.tmp>1000:
            spawn(700, None, 15, "traverse", "asc", "tripleTir")
            self.tmp = pg.time.get_ticks()
        """



def spawn(x,y,hp,move,pattern,tir):
        nbr = randint(-5,5)
#proba à mieux faire_________________________________________________
        if karma//10-nbr>=4:
            Demon(x,y,hp,move,pattern,tir)
        elif karma//10-nbr<=-4:
            Ange(x,y,hp,move,pattern,tir)
        else:
            Fantome(x,y,hp,move,pattern,tir)
#__________________________________________________________________

#____________________________________________________debut du programme__________________________________________________________________


#----  juste pour tests
#p = PluieMeteors(500)
#c = Cible()
#tous.add(Upgrade(150, 450, "damage"))
#tous.add(Upgrade(150, 250, "bullet"))
#tous.add(Upgrade(150, 350, "hp"))
cont = startMenu()
t=Tuto()
karma = 0
#----
escap = False
p1 = Player(100, 100)
pvs = [Coeur(15, 20), Coeur(60, 20), Coeur(105, 20)]
groupe = pg.sprite.Group(p1)

for i in pvs:
    groupe.add(i)

while cont:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            cont = 0
            sys.exit()
        """
        if spawn>1:
            a=Ange(randint(-30,1000),randint(-30,650),50,"devantDerriere","asc","rebond",50)#pour pas de safe spot
            p.desActiver()
            spawn-=1
        elif spawn<-2:
            a=Demon(randint(-30,1000),randint(-30,650),50,"doubleTraverse","asc","vacillant")#pour pas de safe spot
            spawn-=1
        if not a.alive():
            spawn+=1
        """
    Niveaux.update(t)
    collisions = pg.sprite.groupcollide(groupe, tous, False, False, pg.sprite.collide_mask)
    fenetre.fill((255,255,255))
    dt = clock.tick(60)
    tous.update()
    groupe.update()
    tous.draw(fenetre)
    groupe.draw(fenetre)
    pg.display.flip()