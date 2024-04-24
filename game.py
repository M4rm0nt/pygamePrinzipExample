import pygame  # Importiere die pygame-Bibliothek, die für die Spieleentwicklung in Python verwendet wird
import sys  # Importiere das sys-Modul, um Funktionen und Variablen zu nutzen, die mit der Python-Interpretation oder dem Betriebssystem interagieren

# Initialisiere Pygame
pygame.init()

# Definiere die Größe des Fensters
BREITE, HÖHE = 400, 300  # Definiere die Breite und Höhe des Spielfensters

# Definiere Farben, die im Spiel verwendet werden
WEISS = (255, 255, 255)  # Farbe Weiß, in RGB-Format (Rot, Grün, Blau)
SCHWARZ = (0, 0, 0)  # Farbe Schwarz
GRÜN = (0, 255, 0)  # Farbe Grün
ROT = (255, 0, 0)  # Farbe Rot

# Erstelle das Spielfenster
bildschirm = pygame.display.set_mode((BREITE, HÖHE))  # Erstelle das Spielfenster mit der definierten Breite und Höhe
pygame.display.set_caption("Rechtecksteuerung")  # Setze den Titel des Fensters auf "Rechtecksteuerung"

# Definiere Eigenschaften des Spielers (Rechteck)
spieler_größe = 50  # Größe des Spielers (Länge und Breite des Rechtecks)
spieler_x = BREITE // 2 - spieler_größe // 2  # X-Position des Spielers, zentriert im Fenster
spieler_y = HÖHE // 2 - spieler_größe // 2  # Y-Position des Spielers, zentriert im Fenster
spieler_geschwindigkeit = 5  # Geschwindigkeit, mit der sich der Spieler bewegt

# Energie des Spielers
spieler_energie = 100  # Startenergie des Spielers

# Position und Größe des Energielieferanten
energielieferant_x = BREITE - 50  # X-Position des Energielieferanten, rechts im Fenster
energielieferant_y = HÖHE - 50  # Y-Position des Energielieferanten, unten im Fenster
energielieferant_größe = 30  # Größe des Energielieferanten (Länge und Breite des Rechtecks)

uhr = pygame.time.Clock()  # Uhr zur Steuerung der Framerate des Spiels

# Hauptschleife des Spiels
läuft = True
while läuft:
    for ereignis in pygame.event.get():  # Schleife durch alle pygame-Ereignisse in der Ereigniswarteschlange
        if ereignis.type == pygame.QUIT:  # Wenn das Schließen-Ereignis ausgelöst wurde
            läuft = False  # Beende die Hauptschleife des Spiels

    # Spielerbewegung basierend auf Benutzereingaben
    tasten = pygame.key.get_pressed()  # Überprüfe, welche Tasten gedrückt sind
    if tasten[pygame.K_LEFT]:  # Wenn die linke Pfeiltaste gedrückt wird
        spieler_x -= spieler_geschwindigkeit  # Bewege den Spieler nach links
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_RIGHT]:  # Wenn die rechte Pfeiltaste gedrückt wird
        spieler_x += spieler_geschwindigkeit  # Bewege den Spieler nach rechts
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_UP]:  # Wenn die obere Pfeiltaste gedrückt wird
        spieler_y -= spieler_geschwindigkeit  # Bewege den Spieler nach oben
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_DOWN]:  # Wenn die untere Pfeiltaste gedrückt wird
        spieler_y += spieler_geschwindigkeit  # Bewege den Spieler nach unten
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung

    # Begrenze die Position des Spielers innerhalb des Spielfensters
    spieler_x = max(0, min(spieler_x, BREITE - spieler_größe))  # Begrenze die X-Position des Spielers
    spieler_y = max(0, min(spieler_y, HÖHE - spieler_größe))  # Begrenze die Y-Position des Spielers

    # Überprüfe Kollision des Spielers mit dem Energielieferanten
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, spieler_größe, spieler_größe)  # Erstelle Rechteck für den Spieler
    energielieferant_rechteck = pygame.Rect(energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe)  # Erstelle Rechteck für den Energielieferanten
    if spieler_rechteck.colliderect(energielieferant_rechteck):  # Wenn Spieler mit dem Energielieferanten kollidiert
        spieler_energie = 100  # Setze die Spielerenergie zurück auf 100
        # Platziere den Energielieferanten neu im Spielfenster
        energielieferant_x = BREITE - 50
        energielieferant_y = HÖHE - 50

    # Begrenze die Spielerenergie zwischen 0 und 100
    spieler_energie = max(0, min(spieler_energie, 100))

    # Zeichne den Hintergrund des Spiels
    bildschirm.fill(WEISS)

    # Zeichne das Rechteck des Spielers
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, spieler_größe, spieler_größe))

    # Zeichne das Rechteck des Energielieferanten
    pygame.draw.rect(bildschirm, ROT, (energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe))

    # Zeichne den Energiebalken des Spielers
    energie_balken_breite = spieler_energie * spieler_größe / 100
    energie_balken = pygame.Rect(spieler_x, spieler_y - 10, energie_balken_breite, 5)
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)

    # Zeige die aktuelle Spielerenergie an
    schrift = pygame.font.SysFont(None, 24)
    energie_text = schrift.render(f'Energie: {spieler_energie:.2f}', True, SCHWARZ)
    bildschirm.blit(energie_text, (10, 10))

    # Aktualisiere das Spielfenster
    pygame.display.flip()

    # Kontrolliere die Framerate des Spiels
    uhr.tick(60)

# Beende Pygame
pygame.quit()
sys.exit()
