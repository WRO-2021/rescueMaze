package pacco;

import java.util.LinkedList;

/**
 * classe contenitore per LabyNode, tiene conto della cella corrente, la direzione del
 * robot(e converte i dati inseriti dall'esterno in direzioni assolute per la mappa), salva
 * l'ultimo checkpoint passato e ha la possibilità di ritornarci
 *
 * ha il metodo getMovement() che ritorna un array di movimenti, lo 0 vuol dire avanti, la notazione è quella direzionale
 * standard descritta in LabyNode.
 */
public class Esploratore {
    private LabyNode current;
    private LabyNode lastCheckpoint;
    private int direction;

    public Esploratore(){
        current=new LabyNode();
        lastCheckpoint=current;
        direction=0;
    }

    /**
     * direzione assoluta da direzione relativa
     * @param dir direzione data dal robot
     * @return direzione da usare nella mappa
     */
    public int dir(int dir){
        return (dir+direction)%4;
    }

    public void forward(){
        current=current.getNear(direction);
        current.setVisited(true);
        if(current.isCheckpoint())
            setLastCheckpoint();
    }
    public void left(){
        direction=dir(3);
    }
    public void right(){
        direction=dir(1);
    }
    public void back(){
        direction=dir(2);
    }
    public void goToCheckpoint(){
        current=lastCheckpoint;
        direction=0;
    }
    public void setLastCheckpoint(){
        lastCheckpoint=current;
        current.setCheckpoint(true);
    }
    public void setWall(int dir, boolean b){
        current.setWall(b,dir(dir));
    }

    /**
     * se il valore della posizione è maggiore di 3 setta il danger alla cella corrente
     * se è minore di 0 lo setta nella direzione attuale
     * se no nella direzione indicata
     * @param dir
     */
    public void setDanger(int dir){
        if(dir>3)
            current.setDanger(true);
        else if(dir>0)
            current.getNear(dir(dir)).setDanger(true);
        else
            current.getNear(direction).setDanger(true);
    }
    public int[] getMovements(){
        int[] raw=current.trackToUnkown();
        int last=direction,tmp;
        LinkedList<Integer> movements=new LinkedList<>();
        //in base all'ultima direzione calcola il movimento da fare per ogni direzione
        for(int i=0;i<raw.length;i++){
            tmp=(4-last+raw[i])%4;
            if(tmp!=0)
                movements.add(tmp);
            movements.add(0);
            last=raw[i];
        }
        return movements.stream().mapToInt(i->i).toArray();
    }
    @Override
    public String toString(){
        return "current direction:"+direction+"\n"+ current.toString(direction);
    }
}
