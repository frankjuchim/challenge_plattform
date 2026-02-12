void setup() {
size (400,400);
}
void draw () {

for (int x = 0; x <= width; x += 40) {
    
rect (x, x,40,40);
fill(x);
}
}
