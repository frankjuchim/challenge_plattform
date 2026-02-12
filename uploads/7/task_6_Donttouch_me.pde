void setup () {
  size (600, 600);
  background (0, 0, 0);
}
void draw() {
  fill (255, 255, 255);
  rect (200, 200, 200, 200);
    if (mouseX >200 && mouseX <400 && mouseY >200 && mouseY <400){
      fill (255, 0, 0);
      rect (200, 200, 200, 200);
  }

}
