void setup() {
  size(500, 500);
  for (int i=0; i<width; i=i+15) {
    line(0, i, width, i);
  }
}
