void setup() {
size(400, 400);
}
void draw() {
background(255);

for (int y = 0; y <= height; y += 15) {
line(0, y, width, y);
}
}
