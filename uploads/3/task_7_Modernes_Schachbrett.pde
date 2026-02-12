void setup (){
   size (400,400);
}

void draw () {
  int felder = 8;
  float groesse = width/felder;
  // background(0,255,0);
 
      for (int i = 0; i < felder; i++) {
     
     for (int r = 0; r < felder; r++){
      
       if ((i+r) % 2 == 0) { 
       
       fill(255,0,120); 
     } else {
       fill(0,255,0); 
     }
       
       rect (i*groesse, r*groesse, groesse,groesse);

     }
      }
  
  
}
