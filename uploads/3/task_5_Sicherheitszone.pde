void setup() {
  size(500, 500);
}

void draw() {
  background(0);
  if (mouseX >= width/2 && mouseY >= height/2) {
    fill(255, 0, 0); } else {
    fill(0, 255, 0);}
  circle(mouseX, mouseY, 50);
}
