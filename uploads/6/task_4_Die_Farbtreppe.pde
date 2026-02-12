int x=0;
int y=0;

void setup() {
  size (500, 500);
  background (255, 255, 255);
}

void draw(){
  fill(0, 0, 0);
  rect(x,y,50,50);
  x=x+50;
  y=y+50;
}
