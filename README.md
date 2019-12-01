 raycaster
============

![raycaster](.github/Screenshot.png "raycaster screenshot")


Hinweise:
=========

- benötigt Python und Pygame
- Steuerung mit WASD (vorwärts, rückwärts, seitwärts laufen) und Maus (drehen)
- mit F12 kann die Minimap (die zudem auch das Raycasting visualisiert) ein- und ausgeblendet werden

Was ist Raycasting:
===================

> In der Computerspielentwicklung bezeichnet der Begriff Raycasting das auf einer zweidimensionalen Karte basierte Berechnen einer Pseudo-3D-Ansicht. Auf Basis der Entfernung zu einem Objekt, den ein „Sichtstrahl“ trifft, wird zum einen die Objektfarbe vertikal zentriert dargestellt und zum anderen der Anteil an Decke oder Boden der entsprechenden Pixel-Spalte berechnet. Im Gegensatz zur normalen Raytracing-Technik wird hier nur eine einzelne Bildzeile abgetastet, um das gesamte Bild zu berechnen; die Verdeckungsberechnung findet also nur in einer Ebene und nicht im Raum statt. Diese Art des Raycasting findet zum Beispiel im Computerspiel Wolfenstein 3D Anwendung.
Entsprechend der oberen Grafik wird die Bildpunktfarbe festgestellt (oberer „Streifen“) und entsprechend der Entfernung wird ein vertikaler Bereich in dieser Farbe gezeichnet. Alle übrigen Bereiche sind Himmel bzw. Decke oder Boden.
>

>Da diese Technik keinem echten 3D entspricht, unterliegt sie diversen Einschränkungen: Es können keine dreidimensionalen Objekte wie Personen und Gegenstände dargestellt werden, Boden und Decke sind immer gleich hoch und Schrägen sind nicht möglich. 
> *(aus der [Wikipedia](https://de.wikipedia.org/wiki/Raycasting))*
