boolean maus=false;
float[] xKoor= new float [20];
float[] yKoor= new float [20];

void setup () {
  size(500, 500);
  for (int i=0; i<xKoor.length; i++) {
    xKoor[i]=random(width);
    yKoor[i]=random(height);
    frameRate=2;
  }
}


void draw() {
  background(100);
  for (int i=0; i<xKoor.length; i++) {
    if (maus==false) {

      circle(xKoor[i], yKoor[i], 10);
      yKoor[i]-=random(-0.5, 0.5);
      xKoor[i]-=random(-0.5, 0.5);
    } else {
      float d=dist(mouseX,mouseY,xKoor[i],yKoor[i]);
      float farbe= map(xKoor[i], yKoor[i], d, 0, 255);
      
      fill(farbe);
      if (mouseX>xKoor[i]) { 
        if(mouseY>yKoor[i]){
        circle(xKoor[i], yKoor[i], 10);
        xKoor[i]=xKoor[i]+1;
        yKoor[i]=yKoor[i]+1;
        }
        else { circle(xKoor[i], yKoor[i], 10);
        xKoor[i]=xKoor[i]+1;
        yKoor[i]=yKoor[i]-1;
      }} else if(mouseX<xKoor[i] ) 
      if(mouseY>yKoor[i]){
      {circle(xKoor[i], yKoor[i], 10);
        xKoor[i]=xKoor[i]-1;
        yKoor[i]=yKoor[i]+1;
        }}
        else { circle(xKoor[i], yKoor[i], 10);
        xKoor[i]=xKoor[i]-1;
        yKoor[i]=yKoor[i]-1;
      }}
    
    }

    if (mousePressed ) {
      maus=true;
      
    } else maus=false;
  }
