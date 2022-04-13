package pacco;

import java.util.LinkedList;

public class Esploratore {
    private LabyNode current;
    private LabyNode lastCheckpoint;
    private int direction;

    public Esploratore(){
        current=new LabyNode();
        lastCheckpoint=current;
        direction=0;
    }

    public int dir(int dir){
        return (dir+direction)%4;
    }

    public void forward(){
        current=current.getNear(direction);
        current.setVisited(true);
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
    public void setDanger(int dir){
        if(dir>4)
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
