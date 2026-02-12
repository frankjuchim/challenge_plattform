int x1;
int y1;

void setup () {
  size(400, 300);
  background (255, 255, 0);
  fill(255, 0, 0);
}

void draw() {
  if (mousePressed) {
    circle (x1, y1, 60);
  }
}
void mousePressed() {
  x1 = mouseX;
  y1 = mouseY;
}
