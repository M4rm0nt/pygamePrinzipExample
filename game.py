import pygame
import sys

pygame.init()

BREITE, HÖHE = 800, 600

WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)

bildschirm = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Rechtecksteuerung")

spieler_größe = 50
spieler_x = BREITE // 2 - spieler_größe // 2
spieler_y = HÖHE // 2 - spieler_größe // 2
spieler_geschwindigkeit = 5
spieler_energie = 100
spieler_gesammelte_objekte = 0

energielieferant_x = BREITE - 50
energielieferant_y = HÖHE - 50
energielieferant_größe = 30

sammelObjekt_x = BREITE - 200
sammelObjekt_y = HÖHE - 200
sammelObjekt_größe = 30

ablagePlatz_x = 100
ablagePlatz_y = 100
ablagePlatz_größe = 30
abgelegte_objekte = []

uhr = pygame.time.Clock()

läuft = True
while läuft:
    for ereignis in pygame.event.get():
        if ereignis.type == pygame.QUIT:
            läuft = False

    tasten = pygame.key.get_pressed()
    if tasten[pygame.K_LEFT] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_x -= spieler_geschwindigkeit
        spieler_energie -= 0.15
    if tasten[pygame.K_RIGHT] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_x += spieler_geschwindigkeit
        spieler_energie -= 0.15
    if tasten[pygame.K_UP] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_y -= spieler_geschwindigkeit
        spieler_energie -= 0.15
    if tasten[pygame.K_DOWN] and spieler_energie > 0 and len(abgelegte_objekte) != 5:
        spieler_y += spieler_geschwindigkeit
        spieler_energie -= 0.15

    spieler_x = max(0, min(spieler_x, BREITE - spieler_größe))
    spieler_y = max(0, min(spieler_y, HÖHE - spieler_größe))

    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, spieler_größe, spieler_größe)
    energielieferant_rechteck = pygame.Rect(energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe)
    sammelObjekt_rechteck = pygame.Rect(sammelObjekt_x, sammelObjekt_y, sammelObjekt_größe, sammelObjekt_größe)
    ablageplatz_rechteck = pygame.Rect(ablagePlatz_x, ablagePlatz_y, ablagePlatz_größe, ablagePlatz_größe)

    if spieler_rechteck.colliderect(energielieferant_rechteck):
        spieler_energie = 100
        energielieferant_x = BREITE - 50
        energielieferant_y = HÖHE - 50

    spieler_energie = max(0, min(spieler_energie, 100))

    if spieler_rechteck.colliderect(sammelObjekt_rechteck) and spieler_gesammelte_objekte < 5:
        spieler_gesammelte_objekte = 1
        sammelObjekt_x = 100
        sammelObjekt_y = 100

    if spieler_rechteck.colliderect(ablageplatz_rechteck) and spieler_gesammelte_objekte > 0 and len(abgelegte_objekte) < 5:
        abgelegte_objekte.append((ablagePlatz_x, ablagePlatz_y))
        spieler_gesammelte_objekte -= 1
        sammelObjekt_x = BREITE - 200
        sammelObjekt_y = HÖHE - 200

    bildschirm.fill(WEISS)

    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, spieler_größe, spieler_größe))
    pygame.draw.rect(bildschirm, ROT, (energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe))
    pygame.draw.rect(bildschirm, GRÜN, (sammelObjekt_x, sammelObjekt_y, sammelObjekt_größe, sammelObjekt_größe))
    pygame.draw.rect(bildschirm, SCHWARZ, (ablagePlatz_x, ablagePlatz_y, ablagePlatz_größe, ablagePlatz_größe))

    energie_balken_breite = spieler_energie * spieler_größe / 100
    energie_balken = pygame.Rect(spieler_x, spieler_y - 10, energie_balken_breite, 5)
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)

    schrift = pygame.font.SysFont(None, 24)

    energie_text = schrift.render(f'Energie: {spieler_energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    objekte_text = schrift.render(f'Objekte: {spieler_gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))

    abgelegte_objekte_text = schrift.render(f'Abgelegte Objekte: {len(abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))

    if spieler_energie <= 0:
        nachricht_schrift = pygame.font.SysFont(None, 24)
        nachricht_text = nachricht_schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    if spieler_energie <= 0:
        if tasten[pygame.K_e]:
            spieler_energie = 100

    if len(abgelegte_objekte) == 5:
        nachricht_schrift = pygame.font.SysFont(None, 24)
        nachricht_text = nachricht_schrift.render("Glückwunsch, du hast alle Objekte abgelegt! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    if len(abgelegte_objekte) == 5:
        if tasten[pygame.K_r]:
            spieler_x = BREITE // 2 - spieler_größe // 2
            spieler_y = HÖHE // 2 - spieler_größe // 2
            spieler_energie = 100
            spieler_gesammelte_objekte = 0
            abgelegte_objekte = []

    pygame.display.flip()

    uhr.tick(60)

pygame.quit()
sys.exit()
