void setup() {
  size(800, 800);
}

void draw() {
  for (int i = 0; i < 800; i=i+100) { 
    for (int j = 0; j < 800; j=j+100) { 
      if ((i + j) % 200 == 0) {
        fill(0,0,255);
      } else {
        fill(0,255,0);
      } 
      circle(i+50,j+50,100);
    }
  }
}
