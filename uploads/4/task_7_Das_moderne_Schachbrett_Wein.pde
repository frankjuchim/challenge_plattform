boolean wechsel=true;
void setup(){
 size(400,400); 
 background(120,0,120);
 frameRate(1);
}

void draw(){
  
  if(wechsel==true) {
    background(120,0,120);
  float größe=width/8;
    for(int i=0;i<8;i++){
      for (int j=0;j<8;j++) {
        if ((i + j) % 2 == 0) { 
          fill(255);
        }else { 
      fill(0);  
    
      
      }
      circle(i * größe+24, j * größe+24, größe); 
    }
   
    }
  wechsel=false;
   }
   else {
     background(120,0,120);
       float größe=width/8;
       for(int i=0;i<8;i++){
      for (int j=0;j<8;j++) {
        if ((i + j) % 2 == 0) { 
          fill(0);
        }else { 
      fill(255);  
      }
      circle(i * größe+24, j * größe+24, größe); 
    }
   
    }
  wechsel=true;
   }
  }
