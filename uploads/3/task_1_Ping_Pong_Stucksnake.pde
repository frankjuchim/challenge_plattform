int x = 50;
int i = 2; 

void setup(){
  size(500,500);
  frameRate(60);
}

void draw() {
  background(0);
  fill(255);
  circle(x,200,50);
  x = x + i;
  if (x >= 475 || x <= 25) {
    i = -i;
  }
}
