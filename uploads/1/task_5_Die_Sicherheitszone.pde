void setup() {
  size(400, 400);
}


void draw() {

  background (255, 255, 255);
  circle(mouseX, mouseY, 50);

  if (mouseX > width/2 && mouseY>height/2) {
    fill (255, 0, 0);
  } else {
    fill (0, 255, 0);
  }
}
