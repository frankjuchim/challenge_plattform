void setup(){
  size(500,500);
  background(200);
}

void draw(){
  if(mouseX>=height/2 && mouseY>=width/2) {
    background (200);
    fill(200,0,0);
  circle(mouseX,mouseY,20);
  } else {background(200);
  fill(0,200,0);
  circle(mouseX,mouseY,20);}
  
}
