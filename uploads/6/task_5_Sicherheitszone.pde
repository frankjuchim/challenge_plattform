void setup (){
  size (400,400);
  background (255,255,0);
}

void draw (){
  background (220);
  if (mouseX >width/2 && mouseX <width&&mouseY>height/2&&mouseY<height){
    fill(255,0,0);
  } else {
    fill (0,100,0);
  }
  ellipse(mouseX, mouseY, 20,20);
} 
