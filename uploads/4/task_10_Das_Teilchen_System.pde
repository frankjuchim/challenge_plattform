float[] xKoor= new float [20];
float[] yKoor= new float [20];

void setup () {
  size(500, 500);
  for (int i=0; i<xKoor.length; i++) {
    xKoor[i]=random(width);
    yKoor[i]=random(height);
  }
}


void draw() {
  background(100);
  for (int i=0; i<xKoor.length; i++) {
   circle(xKoor[i],yKoor[i],10);
   yKoor[i]-=random(1,3);
    if (yKoor[i]<= 0) {
    yKoor[i]=height;
    }
  }
}
