
void setup () {
  size (400, 400);
}

void draw () {
  background (220);

  if (
    (mouseX >= 150 && mouseX<=153&&mouseY>=150&&mouseY<=250) ||
    (mouseX>=247&&mouseX<=250&&mouseY>=150&&mouseY<=250) ||
    (mouseX>=150&&mouseX<=153&&mouseY>=150&&mouseY<=250) ||
    (mouseX>=247&&mouseX<=250&&mouseY>=150&&mouseY<=250)
    ) {
    fill (255, 0, 0);
  } else {
    fill (255, 255, 255);
  }
  rect (150, 150, 100, 100);
}
