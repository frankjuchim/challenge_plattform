int score=0;
boolean k = false;
float x=random(50,450);
float y=random(50,450);
void setup() {
size(500,500);
background(120,0,120);

}
void draw() {
if(k==false)
{
  circle(x,y,50);
k=true;
}
if(mousePressed && dist(mouseX ,mouseY, x,y)<50 )
{score= score+1; 
k=false;
background(120,0,120);
x=random(50,450);
y=random(50,450);
println(score);
}
}
