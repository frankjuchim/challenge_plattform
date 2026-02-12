void setup ( ) {

  background (0);
  size (1000 ,900);
}

void draw () {
  for (int i = 0; i < height; i = i +15) {
    strokeWeight(1);
    stroke(255,0,0);
    line(0,i,width,i);
  }
  
 
 
}
