void setup() {
  size(400,400);
  frameRate(1);
}
int speed = 20;
boolean bewegungEnde = false;
void draw() {
  background(0,0,0);
  circle(speed, 100, 40);
  fill(random(255), random(255), random(255));
  if (speed > 360) {
    bewegungEnde = true;
  }
  if (bewegungEnde == true) {
    speed = speed - 40;
  } 
   if (speed <0) {
    bewegungEnde = false;
  }
  if (bewegungEnde == false) {
    speed = speed + 40;
  } 
  
}
