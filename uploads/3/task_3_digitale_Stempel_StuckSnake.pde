void setup() {
  size(500, 500);
  background(0);
}

void draw() {
}

void mouseClicked() {
  fill(random(255), random(255), random(255));
  circle(mouseX, mouseY, 50);
}
