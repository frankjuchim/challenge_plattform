void setup(){
  size (500,500);
  background (255, 255, 255);
}

void draw() {  
  for (int y = 0; y < height; y = y + 15) {
      line(0, y, width, y);
  }
}
