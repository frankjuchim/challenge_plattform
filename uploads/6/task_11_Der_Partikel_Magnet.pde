int[] y = new int[50];
int[] x = new int [50];
float zittern = 1;

void setup() {
  size (500, 500);
  background (255, 255, 255);
  for (int i = 0; i < y.length; i = i + 1) {
    y[i] = (int) random (20, 480);
    x[i] = (int) random (20, 480);
  }
  fill (0, 0, 0);
  for (int i = 0; i < y.length; i = i + 1) {
    circle (x[i], y[i], 3);
  }
}

void draw() {
  background (255, 255, 255);
  fill (0, 0, 0);
  for (int i = 0; i < y.length; i = i + 1) {
    circle (x[i]+zittern, y[i]+zittern, 3);
  zittern = random ( -1, 1);
  }  
}
