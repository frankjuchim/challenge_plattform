IntList X;
IntList Y;
IntList dX;
IntList dY;

void setup(){size(512,512);background(200,200,200);frameRate(32);
  X = new IntList();Y = new IntList();
  dX = new IntList();dY = new IntList();
  for(int i = 0; i<50; i += 1){
  X.append(int(random(0,512)));Y.append(int(random(0,512)));
  //dX.append(int(random(-5,5.5)));dY.append(int(random(-5,5.5)));
  }
}

void draw(){
  background(200,200,200);
  if(mousePressed==false){
  
  for(int i = 0; i<50; i += 1){
  fill(dist(X.get(i),Y.get(i),mouseX,mouseY),255-dist(X.get(i),Y.get(i),mouseX,mouseY),0);
  rect(X.get(i),Y.get(i),5,5);
  X.add(i,int(random(-7.5,7.5)));Y.add(i,int(random(-7.5,7.5)));
  /*
  X.add(i,dX.get(i)); Y.add(i,dY.get(i));
  if(X.get(i)<0 || X.get(i)>509){dX.mult(i,-1);}
  if(Y.get(i)<0 || Y.get(i)>509){dY.mult(i,-1);}
  */
  }
  }
  else{
  for(int i = 0; i<50; i += 1){
  fill(dist(X.get(i),Y.get(i),mouseX,mouseY),255-dist(X.get(i),Y.get(i),mouseX,mouseY),0);
  dX.set(i,int(5*(mouseX-X.get(i))/dist(X.get(i),Y.get(i),mouseX,mouseY)));       //sqrt((mouseX-X.get(i))^2+(mouseY-Y.get(i))^2)));
  dY.set(i,int(5*(mouseY-Y.get(i))/dist(X.get(i),Y.get(i),mouseX,mouseY)));      //sqrt((mouseX-X.get(i))^2+(mouseY-Y.get(i))^2)));
  rect(X.get(i),Y.get(i),5,5);
  X.add(i,dX.get(i)); Y.add(i,dY.get(i));
  }
  }




}
