int[] y = new int[20];

void setup() {
  size (500, 500);
  background (255, 255, 255);
  for (int i = 0; i < y.length; i = i + 1) {
    y[i] = (int) random (20, 480);
  }
}
void draw() {
  background (255, 255, 255);
  for (int i = 0; i < y.length; i = i + 1) {
    circle (i * 25 + 10, y[i], 20);
  }
  for (int i = 0; i < y.length; i = i + 1) {
    y[i] = y[i] - 1;
    if (y[i] < 1) {
      y[i] = height;
    }
  }
}
