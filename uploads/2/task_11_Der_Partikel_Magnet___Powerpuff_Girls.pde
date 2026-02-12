float[] xPos = new float[50];
float[] yPos = new float[50];
float[] k = new float[100];
float b=0;
int p=0;

void setup(){
  size(800,800);
  background(255,255,255);
  frameRate(1);
  for (int i=0; i<50;i=i+1){
    xPos[i] = random (10,790);
    yPos[i] = random (10,790);
    k[i] = random(-10,10);
  }
}

void draw() {
  background(255,255,255);
  for (int i=0; i<50; i=i+1){
    circle(xPos[i]+b,yPos[i]-b,5);
  }
  b=b+k[p];
  p=p+1;
}
