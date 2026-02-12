float[] xPos = new float[20];
float[] yPos = new float[20];
int k=0;
int i=0;

void setup(){
  size(800,800);
  background(255,255,255);
  frameRate(1);
  for (int i=0; i<20;i=i+1){
    xPos[i] = random (50,750);
    yPos[i] = random (50,750);
  }
}

void draw() {
  background(255,255,255);
  for (i=0; i<20; i=i+1){
    circle(xPos[i],yPos[i]-k,40);
    k=k+1;
  }
}
