import pygame
import sys

# Initialisierung von Pygame
pygame.init()

# Fenstergröße
BREITE, HÖHE = 800, 600

# Farben
WEISS = (255, 255, 255)
SCHWARZ = (0, 0, 0)
GRÜN = (0, 255, 0)
ROT = (255, 0, 0)

# Initialisierung des Bildschirms
bildschirm = pygame.display.set_mode((BREITE, HÖHE))
pygame.display.set_caption("Rechtecksteuerung")

# Spieler- und Objektgrößen
SPIELER_GROESSE = 50
OBJEKT_GROESSE = 30

# Textschriftart
schrift = pygame.font.SysFont(None, 24)

class Spieler:
    def __init__(self):
        self.x = BREITE // 2 - SPIELER_GROESSE // 2
        self.y = HÖHE // 2 - SPIELER_GROESSE // 2
        self.geschwindigkeit = 1
        self.energie = 100
        self.gesammelte_objekte = 0

class Objekt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def hauptspiel():
    spieler = Spieler()
    energiegeber = Objekt(BREITE - 50, HÖHE - 50)
    objekt = Objekt(BREITE - 200, HÖHE - 200)
    ablageplatz = Objekt(100, 100)
    abgelegte_objekte = []

    # Spielhauptschleife
    läuft = True
    spiel_gewonnen = False
    while läuft:
        # Eventhandling
        for ereignis in pygame.event.get():
            if ereignis.type == pygame.QUIT:
                läuft = False

        # Tastatureingaben abfragen
        tasten = pygame.key.get_pressed()
        spieler_bewegen(tasten, spieler, abgelegte_objekte)

        # Kollisionsüberprüfung
        kollisionen_prüfen(spieler, energiegeber, objekt, ablageplatz, abgelegte_objekte)

        # Spielfeld aktualisieren
        bildschirm_aktualisieren(spieler, energiegeber, objekt, ablageplatz, abgelegte_objekte)

        # Bildschirm aktualisieren
        pygame.display.flip()

        # Spiel zurücksetzen, wenn alle Objekte abgelegt wurden und R gedrückt wird
        if len(abgelegte_objekte) == 5 and tasten[pygame.K_r]:
            spieler.x = BREITE // 2 - SPIELER_GROESSE // 2
            spieler.y = HÖHE // 2 - SPIELER_GROESSE // 2
            spieler.energie = 100
            spieler.gesammelte_objekte = 0
            abgelegte_objekte = []
            läuft = False
            spiel_gewonnen = True

    # Wenn das Spiel gewonnen wurde, starten Sie es erneut
    if spiel_gewonnen:
        hauptspiel()

    # Pygame beenden
    pygame.quit()
    sys.exit()

def spieler_bewegen(tasten, spieler, abgelegte_objekte):
    if tasten[pygame.K_LEFT] and spieler.energie > 0 and len(abgelegte_objekte) != 5:
        spieler.x -= spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_RIGHT] and spieler.energie > 0 and len(abgelegte_objekte) != 5:
        spieler.x += spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_UP] and spieler.energie > 0 and len(abgelegte_objekte) != 5:
        spieler.y -= spieler.geschwindigkeit
        spieler.energie -= 0.010
    if tasten[pygame.K_DOWN] and spieler.energie > 0 and len(abgelegte_objekte) != 5:
        spieler.y += spieler.geschwindigkeit
        spieler.energie -= 0.010

    spieler.x = max(0, min(spieler.x, BREITE - SPIELER_GROESSE))
    spieler.y = max(0, min(spieler.y, HÖHE - SPIELER_GROESSE))

def kollisionen_prüfen(spieler, energiegeber, objekt, ablageplatz, abgelegte_objekte):
    spieler_rechteck = pygame.Rect(spieler.x, spieler.y, SPIELER_GROESSE, SPIELER_GROESSE)
    energiegeber_rechteck = pygame.Rect(energiegeber.x, energiegeber.y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    objekt_rechteck = pygame.Rect(objekt.x, objekt.y, OBJEKT_GROESSE, OBJEKT_GROESSE)
    ablageplatz_rechteck = pygame.Rect(ablageplatz.x, ablageplatz.y, OBJEKT_GROESSE, OBJEKT_GROESSE)

    if spieler_rechteck.colliderect(energiegeber_rechteck):
        spieler.energie = 100
        energiegeber.x = BREITE - 50
        energiegeber.y = HÖHE - 50

    spieler.energie = max(0, min(spieler.energie, 100))

    if spieler_rechteck.colliderect(objekt_rechteck) and spieler.gesammelte_objekte < 5:
        spieler.gesammelte_objekte = 1
        objekt.x = 100
        objekt.y = 100

    if spieler_rechteck.colliderect(ablageplatz_rechteck) and spieler.gesammelte_objekte > 0 and len(abgelegte_objekte) < 5:
        abgelegte_objekte.append((ablageplatz.x, ablageplatz.y))
        spieler.gesammelte_objekte -= 1
        objekt.x = BREITE - 200
        objekt.y = HÖHE - 200

def bildschirm_aktualisieren(spieler, energiegeber, objekt, ablageplatz, abgelegte_objekte):
    bildschirm.fill(WEISS)

    pygame.draw.rect(bildschirm, SCHWARZ, (spieler.x, spieler.y, SPIELER_GROESSE, SPIELER_GROESSE))
    pygame.draw.rect(bildschirm, ROT, (energiegeber.x, energiegeber.y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, GRÜN, (objekt.x, objekt.y, OBJEKT_GROESSE, OBJEKT_GROESSE))
    pygame.draw.rect(bildschirm, SCHWARZ, (ablageplatz.x, ablageplatz.y, OBJEKT_GROESSE, OBJEKT_GROESSE))

    energie_balken_breite = spieler.energie * SPIELER_GROESSE / 100
    energie_balken = pygame.Rect(spieler.x, spieler.y - 10, energie_balken_breite, 5)
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)

    energie_text = schrift.render(f'Energie: {spieler.energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    objekte_text = schrift.render(f'Objekte: {spieler.gesammelte_objekte}', True, SCHWARZ)
    bildschirm.blit(objekte_text, (10, 30))

    abgelegte_objekte_text = schrift.render(f'Abgelegte Objekte: {len(abgelegte_objekte)}/5', True, SCHWARZ)
    bildschirm.blit(abgelegte_objekte_text, (10, 50))

    if spieler.energie <= 0:
        nachricht_text = schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    if spieler.energie <= 0:
        tasten = pygame.key.get_pressed()
        if tasten[pygame.K_e]:
            spieler.energie = 100

    if len(abgelegte_objekte) == 5:
        nachricht_text = schrift.render("Glückwunsch, du hast alle Objekte abgelegt! R für restart", True, SCHWARZ)
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))

    if len(abgelegte_objekte) == 5:
        tasten = pygame.key.get_pressed()
        if tasten[pygame.K_r]:
            spieler.x = BREITE // 2 - SPIELER_GROESSE // 2
            spieler.y = HÖHE // 2 - SPIELER_GROESSE // 2
            spieler.energie = 100
            spieler.gesammelte_objekte = 0
            abgelegte_objekte = []

# Hauptspiel starten
hauptspiel()