void setup(){
  size(600,600);
  background (200,0,200);

}

void draw (){
if (mouseX<400 && mouseX>200 && mouseY<400 && mouseY>200) {fill(255,0,0);
rect(200,200,200,200);
} else {fill(255);
rect(200,200,200,200);}
}
