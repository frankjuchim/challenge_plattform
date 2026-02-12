
IntList Breite; 
IntList AnfHoehe; 

void setup () {
  background(0);
  size (400, 300);
  frameRate(50);
  Breite = new IntList();
  AnfHoehe = new IntList();

  for (int i=0; i <20; i++) {
    Breite.set(i,(int) random (5, width-5));
    AnfHoehe.set(i,(int) random (5, width-5));
  }

  for (int i=0; i <20; i++) {

    circle (AnfHoehe.get(i), Breite.get(i), 25);
  }
}


void draw() {

background(0,0,0);
  //for (int j=height; j<0; j=j-10) {
    for (int i=0; i <20; i++) {
      circle (Breite.get(i), AnfHoehe.get(i), 25);
      AnfHoehe.add(i,-1);
      if(AnfHoehe.get(i)<0){AnfHoehe.set(i,height);}
    }
  }
//}
