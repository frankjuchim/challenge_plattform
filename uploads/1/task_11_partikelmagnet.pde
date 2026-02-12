int[] xPos=new int[50];
int[] yPos=new int[50];
void setup() {
  size(500, 500);
  for (int i=0; i<50; i=i+1) {
    xPos[i]=(int) random(0, 500);
    yPos[i]=(int) random(0, 500);
  }
}
void draw() {
  background(0, 0, 0);
  fill(255, 255, 255);
  for (int i=0; i<50; i=i+1) {
    if(mousePressed==true){
     float farbe = map(dist(mouseX,mouseY,xPos[i],yPos[i]), 0, 255, 0, 255); 
     fill(farbe,0,0);
    }
    circle(xPos[i], yPos[i], 20);
    
    if (mousePressed==true) {
      if (mouseX>xPos[i]) {
        xPos[i]=xPos[i]+1;
        if (mouseY>yPos[i]) {
          yPos[i]=yPos[i]+1;
        } else {
          yPos[i]=yPos[i]-1;
        }
      } else {
        xPos[i]=xPos[i]-1;
        if (mouseY>yPos[i]) {
          yPos[i]=yPos[i]+1;
        } else {
          yPos[i]=yPos[i]-1;
        }
      }
    } else {
      int bewY=(int) random(-10, 10);
      int bewX=(int) random(-10, 10);
      yPos[i]=yPos[i]+bewY;
      xPos[i]=xPos[i]+bewX;
    }
  }
}
