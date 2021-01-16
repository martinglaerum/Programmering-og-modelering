import pygame ,sys
from pygame.locals import *
import random as rd
import time as t

pygame.init()


# for å hente bilder
def hent_bilde(bilde, colorkey=None):
    img = pygame.image.load(bilde)
    img.set_colorkey(BLACK2)
    return img

#lager skjermen
screen = pygame.display.set_mode([892, 600])
pygame.display.set_caption("Falleting")
pygame.mouse.set_visible(False)


#Definerer bakgunnen så den kan bli "tegnet" senere
bakgrunn = pygame.image.load("hage1.png")
bakgrunn = pygame.transform.scale(bakgrunn, (892, 600))


#Setter fps
FPS = 60
FramePerSec = pygame.time.Clock()

#farger
BLACK = (0, 0, 1) # Denne brukes for tekst
BLACK2 = (0,0,0) #Denne brukes så jeg kan bruke kommandoen colorkey så bildene blir transparent
WHITE = (255, 255, 255)

#Fonten til ulike ting
font = pygame.font.SysFont("Verdana", 50)
font_poeng = pygame.font.SysFont("Verdana", 100)
font_small = pygame.font.SysFont("Verdana", 40)
font_smaller = pygame.font.SysFont("Verdana", 30)

#Tekst i spillet
hurratekst = font.render("Hurra!!", True, BLACK)
ferdigtekst = font_smaller.render("Din poengsum er", True, BLACK)
esctekst = font_small.render("Press Esc for å avslutte spillet",True, BLACK)
startekst = pygame.image.load("teskt1.png") #Det er et bilde, men det er bare teskt på bildet

#Variabler
skjermhøyde = 892
skjermbredde = 500
SCORE = 0 #Scoren til spilleren.
SPEED = 1 # for at eplene kan bevege seg
fart = 30 # bestemmer farten til eplene
clock = pygame.time.Clock() # for å kunne ha en timer
dt = 0 # brukes som timer og til farten
timer = 1 # tid mellom når hvert eple faller
versjon = 0 #Endrer seg til 1 når spillet starter #Endrer seg til 2 når spillet er ferdig.
nyeting = 10 # Hvor mange epler (ting) som faller samtidig. Øker jo mer man spiller. #Verdien nå er hvor mange epler som faller på starten
v_poeng = 0 # står for variabel_poeng. Brukt til å få poeng

#Lager hånden som skal plukke epler
class Hand(pygame.sprite.Sprite): #bruker engelsk for hånd så jeg slipper å skrive "å"
    def __init__(self,bilde): #definerer hvordan hånden ser ut
        super().__init__()
        self.image = hent_bilde(bilde).convert_alpha()
        self.rect = self.image.get_rect()
    def plukk(): #definerer at handen kan plukke epler
        global antall_epler
        global SCORE
        pygame.sprite.spritecollide(hand,eple_gruppe,True)
    def update(self):   #Definerer at hånden følger musen til spilleren
        self.rect.center = pygame.mouse.get_pos()

#Legger så hånden i en gruppe så den kan bli "tegnet" senere
hand = Hand("hånd2.png")
hand_gruppe = pygame.sprite.Group()
hand_gruppe.add(hand)

#Lager eplene som skal falle
class Eple(pygame.sprite.Sprite):
    def __init__(self,bilde,pos_x,pos_y): #Definerer hvordan eplene ser ut
        super().__init__()
        self.image = hent_bilde(bilde).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
    def move(self): #definerer hvordan eplene beveger seg
        global versjon
        self.rect.move_ip(0,SPEED)
        if (self.rect.top > 600):
            versjon = 2

#Legger så eplene i en gruppe så de kan bli "tegnet senere
nytt_eple = Eple("eple16.png",rd.randint(20,850),rd.randint(10,100))
eple_gruppe = pygame.sprite.Group()
eple_gruppe.add(nytt_eple)


#Løkken som inneholder spillet
running = True
while running:
    for event in pygame.event.get(): #Hvis du presser museknappen ned så plukker man
        if event.type == pygame.MOUSEBUTTONDOWN:
            if v_poeng == 0 and pygame.sprite.spritecollideany(hand, eple_gruppe): # Gjør så hvis hånden er over et eple så plukker man og v_poeng blir 1.
                Hand.plukk()
                v_poeng = 1 #Hver gang Variabelen v_poeng blir 1 får spilleren et poeng. Så går variabelen ned til 0 igjen.
        if event.type == pygame.KEYDOWN: #Hvis man presser Esc slutter spillet
            if event.key == K_ESCAPE:
                running = False
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT: #Så spillet stopper når du trykker på x-en i hjørnet.
                running = False
                pygame.quit()
                sys.exit()

    timer -= dt #Definerer timer


    if versjon == 0: #Startskjermen
        screen.blit(bakgrunn, (0,0))
        screen.blit(startekst,(180,100))
        pygame.display.flip()
        pygame.time.wait(6000)
        versjon = 1

    if versjon == 1:

        #Denne gjør at det dukker opp et varierende antall nye meteorer hvert sekund.
        #antall nye meteorer og farten varierer utifra poengsummen til spilleren.
        #timer = 1 starter en ny timer som vil telle ned til 0 på nytt.

        if v_poeng == 1:
                SCORE +=1
                v_poeng = 0

        if SCORE > 999:#Så spillet ikke varer for evig.
            versjon = 2
        if timer <= 0: #Løkken som får nye epler til å falle
            for eple in range(nyeting):
                eple_gruppe.add(Eple("eple16.png",rd.randint(20,850),rd.randint(10,100)))
                if SCORE <= 10:
                    nyeting = 1
                elif SCORE <= 30:
                    nyeting = 2
                elif SCORE <= 50:
                    nyeting = 3
                elif SCORE <= 70:
                    nyeting = 4
                elif SCORE <= 100:
                    nyeting = 5
                elif SCORE <= 150:
                    nyeting = 7
                    fart = 50
                elif SCORE <= 200:
                    nyeting = 9
                    fart = 200
                elif SCORE <= 300:
                    nyeting = 10
                    SPEED = 2
                else: fart = fart

                timer = 1 #Setter timer til 1 så kan den telle ned på nytt



        screen.blit(bakgrunn, (0,0))
        scores = font.render(str(SCORE), True, BLACK)

        eple_gruppe.draw(screen)
        eple_gruppe.update()
        hand_gruppe.draw(screen)
        hand_gruppe.update()

        for entity in eple_gruppe:
            screen.blit(entity.image, entity.rect)
            entity.move()

        #Viser scoren til spilleren
        if SCORE < 10:
            scores = font.render(str(SCORE), True, BLACK)
            screen.blit(scores,(446,0))
        if SCORE < 100 and SCORE >= 10:
            scores = font.render(str(SCORE), True, BLACK)
            screen.blit(scores,(426,0))
        if SCORE >= 100:
            scores = font.render(str(SCORE), True, BLACK)
            screen.blit(scores,(408,0))

        dt = clock.tick(fart)/1000 #her  farten til eplene.

        pygame.display.flip()

    #Når spilleren taper blir noe = 2. Da skjer dette
    if versjon == 2:
        ferdig = pygame.image.load("hage13.png")
        ferdig = pygame.transform.scale(ferdig, (892, 600))
        screen.blit(ferdig, (0,0))
        screen.blit(hurratekst,(220,110))
        screen.blit(ferdigtekst, (180,160))
        if SCORE < 10:
            scores = font_poeng.render(str(SCORE), True, BLACK)
            screen.blit(scores,(135,275))
        if SCORE < 100 and SCORE >= 10:
            scores = font_poeng.render(str(SCORE), True, BLACK)
            screen.blit(scores,(105,275))
        if SCORE >= 100:
            scores = font_poeng.render(str(SCORE), True, BLACK)
            screen.blit(scores,(75,275))

        screen.blit(esctekst,(150,555))

        pygame.display.update()
        for entity in eple_gruppe:
            entity.kill()

        pygame.display.flip()