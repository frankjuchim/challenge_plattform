int AnzahlQuadrate = 10;

void setup() {
  size(500, 500);
}

void draw() {
  background(255);
  for (int i = 0; i < AnzahlQuadrate; i++) {
    float grau = map(i, 0, 10, 255, 0);
    fill(grau);
    rect(0 + i*50, 0 + i*50, 50, 50);
  }
}
