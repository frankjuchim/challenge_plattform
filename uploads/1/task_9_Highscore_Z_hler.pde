int Cx = (int)random(0, width);
int Cy = (int)random(0, height);


int score = 0;
void setup() {
  background (255);
  size (500, 500);
  fill(0, 0, 255);
  circle(Cx, Cy, 40);
}


void draw() {
}

void mouseClicked() {





  if (dist (mouseX, mouseY, Cx, Cy)< 20)
  {
    background (255);
    score = score + 1;
    Cx = (int)random(0, width);
    Cy = (int)random(0, height);
    circle(Cx, Cy, 40);
    println(score);
  }
}
