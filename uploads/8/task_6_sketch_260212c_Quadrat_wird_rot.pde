void setup() {
  size(500,500);
}

void draw() {
  background(255);
  rect(width/2,height/2,100,100);
  
  if (mouseX > width/2-100 && mouseX < width/2+100 && mouseY > height/2-100 && mouseY < height/2+100) {
    fill(255,0,0);
  } else {
    fill(255);
  }
}
