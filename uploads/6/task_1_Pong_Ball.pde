float x=25;
float speed = 2;
float r=25;

void setup () {
  size (400, 400);
}

void draw () {
  background (220);
  ellipse (x, 200, r*2, r*2);
  x=x+speed;

  if (x >= width-r || x <=r){
  
    speed = speed *-1;
  }
}
