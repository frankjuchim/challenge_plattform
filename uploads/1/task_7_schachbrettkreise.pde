void setup(){
  size(640,640);
  for(int i=0;i<8;i=i+1){
    for(int j=0;j<8;j=j+1){
      if((i+j)%2==0){
        fill(255);
      } else{
        fill(0);
      }
      circle(40+i*80,40+j*80,80);
    }
  }
}
