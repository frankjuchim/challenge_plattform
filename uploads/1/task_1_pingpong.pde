int i=10;
int speed=5;
void setup() {
  size(500, 500);
}
void draw() {

  background(255, 255, 255);
  fill(0, 0, 0);
  circle(i, 100, 20);
  i=i+speed;
  if (i>width-10 || i<10 ) {
   speed=-1*speed;
  }
}
