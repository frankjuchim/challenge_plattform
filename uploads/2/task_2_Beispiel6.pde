/* Autor: Ylva Brandt, Juli 2019
*
* Dieses Werk ist lizenziert unter einer Creative Commons Namensnennung - Nicht-kommerziell - Weitergabe unter gleichen Bedingungen
* 4.0 International Lizenz (http://creativecommons.org/licenses/by-nc-sa/4.0/).
*/

void setup(){  //diese Methode wird nur einmalig beim Programmstart ausgeführt
  size(400, 300);
  background(255, 255, 0);
  fill(255, 0, 0);
}

void draw(){  //diese Methode wird immer wieder von vorne durchlaufen
}

void mouseClicked(){  //diese Methode wird immer dann ausgeführt, wenn eine Maustaste 
                      //gedrückt wurde
  square(mouseX, mouseY, 30);   //mouseX und mouseY liefern die aktuelle Position der Maus
}     
