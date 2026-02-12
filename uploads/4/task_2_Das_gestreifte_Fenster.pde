void setup(){
  size(300,300);

}

void draw(){
   for (int i=0; i<height; i = i+15){
    line(0, i, width, i);
}
}
