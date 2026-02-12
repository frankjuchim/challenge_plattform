void setup ( ) {

  background (0);
  size (400, 300);
  mouseX=100;
  mouseY=100;
}

void draw () {


  if (mouseY<10 || mouseY>height-10 || mouseX<10 || mouseX>width-10) {
 println(mouseX);
 
  fill (255,0,0);
  rect(width/2-50, height/2-40, 100, 80);
  }
  else {
    fill (255);
    rect(width/2-50, height/2-40, 100, 80);
  }
}
