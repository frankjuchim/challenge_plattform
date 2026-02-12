void setup () {
  size (500, 500);
  for (int x = -50; x < 500; x = x + 50) {
    fill (255-(x/2),255-(x/2),255-(x/2));  
    rect (x, x, 50,50);
  }

}

void draw () {

  }
