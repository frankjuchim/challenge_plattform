void setup(){
size(1000,1000);
for(int i=0;i<1000;i=i+100){
for(int j=0;j<1000;j=j+100){
  fill(255-(i*0.2),255-(i*0.2),255-(i*0.2));
  if(i==j){square(i,j,100);}
}}
}
