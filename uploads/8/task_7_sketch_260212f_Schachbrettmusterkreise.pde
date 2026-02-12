void setup() {
 size(400,400);
}

 void draw() {
   int felder = 8;
   float größe = width/felder;
   
 for (int i=0;i<felder;i++) {
   for (int j=0;j<felder;j++) {
     if ((i+j)%2==0) {
       fill(0,0,255); }
       else {
         fill(200,45,100);
       }
         circle(i*größe+25,j*größe+25,größe);
}
 }
}
