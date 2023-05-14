# Créé par campa, le 29/05/2022 en Python 3.7
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

