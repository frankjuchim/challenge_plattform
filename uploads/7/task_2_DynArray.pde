public class DynArray{
  private ArrayList<Karte> liste;
  
  public DynArray(){
    liste = new ArrayList<Karte>();
  }
  
  public boolean isEmpty(){
    return liste.isEmpty();
  }
  
  public Karte getItem(int index){
    Karte k = (Karte) liste.get(index);
    return k;
  }
  
  public void append(Karte k){
    liste.add(k);
  }
  
  public void insertAt(int index, Karte k){
    liste.add(index, k);
  }
  
  public void setItem(int index, Karte k){
    liste.set(index, k);
  }
  
  public void delete(int index){
    liste.remove(index);
  }
  
  public int getLength(){
    return liste.size();
  }

/**
* Die Operation zeigt den aktuellen Inhalt des Kartendecks in der Konsole an (debugging)
*/
void printDeck(){
  int anzahl = this.liste.size();
  Karte k;
  String ausgabe = "";
  for(int i=0; i<anzahl;i++){
    k=(Karte) liste.get(i);
    ausgabe = ausgabe + "[" + k.titel + ";" + k.jahr + "]";
    if (!(i ==anzahl-1)){
      ausgabe = ausgabe + ";";
    }
  }
  println(ausgabe);
}
  
}
