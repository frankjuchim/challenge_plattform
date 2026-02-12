void setup() {

  size(800,800);
 } 
void draw() {
  int felder =8;
  float größe = width / felder;
  frameRate(3);
  
  
  
  for (int i = 1; i < felder; i++) 
  
  {
    for (int j = 1; j < felder; j++) {
      
      if ((i + j) % 2 == 0) {
        fill(random(200,150));

    
     } else {
       fill(random(150,200));
        
     }
        
        ellipse(i * größe, j * größe, größe, größe);
        
        
  }


}

}
  
  
