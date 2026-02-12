int[] xPos=new int[20];
int[] yPos=new int[20];
void setup() {
  size(500, 500);
  for (int i=0; i<20; i=i+1) {
    xPos[i]=(int) random(0, 500);
    yPos[i]=(int) random(0, 500);
  }
}
void draw() {
  background(0, 0, 0);
  fill(255, 255, 255);
  for (int i=0; i<20; i=i+1) {
    circle(xPos[i], yPos[i], 20);
    yPos[i]=yPos[i]-2;
   if(yPos[i]<0){
     yPos[i]=height;
    // xPos[i]=(int)random(0,500);
   }
  }
}
