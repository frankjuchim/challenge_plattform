void setup() {
  size(400, 400);
}
void draw() {
  background (220);
  rect (150, 150, 100, 100);

  if (mouseX > 150 && mouseX < 250 && mouseY < 250 && mouseY>150) {
    fill (255, 0, 0);
  } else {
    fill (255);


  }
}
