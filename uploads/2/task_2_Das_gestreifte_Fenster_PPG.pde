//Das gestreifte Fenster


void setup () {
  background(0, 255, 0);
  size (500, 500);
}

void draw () {
  for (int y = 1 ; y < height; y = y + 15) {
      line (0, y, width, y);
    }
  }
