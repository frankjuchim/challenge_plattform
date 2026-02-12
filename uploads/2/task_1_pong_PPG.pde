int x;
int speed; 

void setup () {
  size(500, 500);
  frameRate(3);
 
}
void draw(){
  background(255,100,255);
  fill(255, 255, 0);
  circle(x, 250, 50);
  x = x + speed+25;
if (x < 500){
} else{
  x = x + speed-25;
}
}
