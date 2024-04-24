import pygame  # Importiere die pygame-Bibliothek für die Spieleentwicklung
import sys  # Importiere das sys-Modul für systembezogene Funktionalitäten

pygame.init()  # Initialisiere Pygame

BREITE, HÖHE = 800, 600  # Definiere die Breite und Höhe des Spielfensters

WEISS = (255, 255, 255)  # Definiere die Farbe Weiß in RGB-Format
SCHWARZ = (0, 0, 0)  # Definiere die Farbe Schwarz in RGB-Format
GRÜN = (0, 255, 0)  # Definiere die Farbe Grün in RGB-Format
ROT = (255, 0, 0)  # Definiere die Farbe Rot in RGB-Format

bildschirm = pygame.display.set_mode((BREITE, HÖHE))  # Erstelle das Spielfenster mit der definierten Breite und Höhe
pygame.display.set_caption("Rechtecksteuerung")  # Setze den Titel des Fensters auf "Rechtecksteuerung"

spieler_größe = 50  # Größe des Spielers (Länge und Breite des Rechtecks)
spieler_x = BREITE // 2 - spieler_größe // 2  # X-Position des Spielers, zentriert im Fenster
spieler_y = HÖHE // 2 - spieler_größe // 2  # Y-Position des Spielers, zentriert im Fenster
spieler_geschwindigkeit = 5  # Geschwindigkeit, mit der sich der Spieler bewegt

spieler_energie = 100  # Startenergie des Spielers

energielieferant_x = BREITE - 50  # X-Position des Energielieferanten, rechts im Fenster
energielieferant_y = HÖHE - 50  # Y-Position des Energielieferanten, unten im Fenster
energielieferant_größe = 30  # Größe des Energielieferanten (Länge und Breite des Rechtecks)

uhr = pygame.time.Clock()  # Uhr zur Steuerung der Framerate des Spiels

läuft = True  # Variable, um das Spiel zu steuern, Initialisierung auf True, um das Spiel zu starten
while läuft:  # Starte die Hauptschleife des Spiels
    for ereignis in pygame.event.get():  # Iteriere durch alle Ereignisse in der Ereigniswarteschlange
        if ereignis.type == pygame.QUIT:  # Wenn das Schließen-Ereignis ausgelöst wurde
            läuft = False  # Setze die Variable auf False, um die Hauptschleife zu beenden und das Spiel zu beenden

    # Spielerbewegung basierend auf Benutzereingaben
    tasten = pygame.key.get_pressed()  # Überprüfe, welche Tasten gedrückt sind
    if tasten[pygame.K_LEFT] and spieler_energie > 0:  # Wenn die linke Pfeiltaste gedrückt wird und die Spielerenergie > 0 ist
        spieler_x -= spieler_geschwindigkeit  # Verringere die X-Position des Spielers, um ihn nach links zu bewegen
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_RIGHT] and spieler_energie > 0:  # Wenn die rechte Pfeiltaste gedrückt wird und die Spielerenergie > 0 ist
        spieler_x += spieler_geschwindigkeit  # Erhöhe die X-Position des Spielers, um ihn nach rechts zu bewegen
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_UP] and spieler_energie > 0:  # Wenn die obere Pfeiltaste gedrückt wird und die Spielerenergie > 0 ist
        spieler_y -= spieler_geschwindigkeit  # Verringere die Y-Position des Spielers, um ihn nach oben zu bewegen
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung
    if tasten[pygame.K_DOWN] and spieler_energie > 0:  # Wenn die untere Pfeiltaste gedrückt wird und die Spielerenergie > 0 ist
        spieler_y += spieler_geschwindigkeit  # Erhöhe die Y-Position des Spielers, um ihn nach unten zu bewegen
        spieler_energie -= 0.15  # Verringere die Spielerenergie aufgrund der Bewegung

    # Begrenze die Position des Spielers innerhalb des Spielfensters
    spieler_x = max(0, min(spieler_x, BREITE - spieler_größe))  # Begrenze die X-Position des Spielers
    spieler_y = max(0, min(spieler_y, HÖHE - spieler_größe))  # Begrenze die Y-Position des Spielers

    # Überprüfe Kollision des Spielers mit dem Energielieferanten
    spieler_rechteck = pygame.Rect(spieler_x, spieler_y, spieler_größe, spieler_größe)  # Erstelle ein Rechteck für den Spieler
    energielieferant_rechteck = pygame.Rect(energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe)  # Erstelle ein Rechteck für den Energielieferanten
    if spieler_rechteck.colliderect(energielieferant_rechteck):  # Wenn der Spieler mit dem Energielieferanten kollidiert
        spieler_energie = 100  # Setze die Spielerenergie zurück auf 100
        # Platziere den Energielieferanten neu im Spielfenster
        energielieferant_x = BREITE - 50
        energielieferant_y = HÖHE - 50

    # Begrenze die Spielerenergie zwischen 0 und 100
    spieler_energie = max(0, min(spieler_energie, 100))  # Stelle sicher, dass die Spielerenergie zwischen 0 und 100 liegt

    # Zeichne den Hintergrund des Spiels
    bildschirm.fill(WEISS)

    # Zeichne das Rechteck des Spielers
    pygame.draw.rect(bildschirm, SCHWARZ, (spieler_x, spieler_y, spieler_größe, spieler_größe))

    # Zeichne das Rechteck des Energielieferanten
    pygame.draw.rect(bildschirm, ROT, (energielieferant_x, energielieferant_y, energielieferant_größe, energielieferant_größe))

    # Zeichne den Energiebalken des Spielers
    energie_balken_breite = spieler_energie * spieler_größe / 100  # Berechne die Breite des Energiebalkens basierend auf der Spielerenergie
    energie_balken = pygame.Rect(spieler_x, spieler_y - 10, energie_balken_breite, 5)  # Erstelle ein Rechteck für den Energiebalken
    pygame.draw.rect(bildschirm, GRÜN, energie_balken)  # Zeichne den Energiebalken in Grün

    # Zeige die aktuelle Spielerenergie an
    schrift = pygame.font.SysFont(None, 24)  # Definiere eine Schriftart für den Text
    energie_text = schrift.render(f'Energie: {spieler_energie:.2f}', True, SCHWARZ)  # Erstelle einen Text für die Spielerenergie
    bildschirm.blit(energie_text, (10, 10))  # Zeige den Text in der oberen linken Ecke des Spielfensters an

    # Überprüfe, ob die Spielerenergie erschöpft ist und zeige eine Nachricht an
    if spieler_energie <= 0:  # Wenn die Spielerenergie kleiner oder gleich 0 ist
        nachricht_schrift = pygame.font.SysFont(None, 24)  # Definiere eine Schriftart für die Nachricht
        nachricht_text = nachricht_schrift.render("Deine Energie ist leer, drücke E um sie wieder aufzuladen", True, SCHWARZ)  # Erstelle einen Text für die Nachricht
        bildschirm.blit(nachricht_text, (BREITE // 2 - 200, HÖHE // 2))  # Zeige die Nachricht in der Mitte des Spielfensters an

    # Wenn die Spielerenergie <= 0 ist
    if spieler_energie <= 0:
        # Überprüfe, ob die E-Taste gedrückt wird, um die Energie wieder aufzuladen
        if tasten[pygame.K_e]:
            spieler_energie = 100  # Setze die Spielerenergie zurück auf 100

    # Aktualisiere das Spielfenster
    pygame.display.flip()  # Aktualisiere den Bildschirm, um die Änderungen anzuzeigen

    # Kontrolliere die Framerate des Spiels
    uhr.tick(60)  # Begrenze die Framerate auf maximal 60 Frames pro Sekunde

# Beende Pygame
pygame.quit()  # Beende die Pygame-Bibliothek
sys.exit()  # Beende das Python-Skript
