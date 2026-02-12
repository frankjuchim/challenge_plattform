void setup ()
{size(400,400);
}

void draw () {

for(int i=0; i<=400;i=i+40) {
float farbe= map(i, 0, width, 255, 0);
  fill(farbe);
  square(i,i,40);
 
}
}
