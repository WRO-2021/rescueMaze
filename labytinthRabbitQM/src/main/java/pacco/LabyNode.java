package pacco;

import java.util.ArrayList;
import java.util.Queue;

import static java.lang.Math.abs;

public class LabyNode {
    private LabyNode[] near;
    private static ArrayList<LabyNode> alls;
    private char[] wall;
    private boolean isDanger, isCheckpoint;
    private boolean isVisited, bfsFlag;

    public LabyNode(){
        alls=new ArrayList<>();
        alls.add(this);
        near = new LabyNode[4];
        wall = new char[4];
        isDanger = false;
        isCheckpoint = false;
        isVisited = true;
        bfsFlag = false;
        for (int i = 0; i < 4; i++) {
            wall[i] = 'u';
            near[i] = null;
        }
    }
    public LabyNode(LabyNode n, int i){
        near = new LabyNode[4];
        wall = new char[4];
        isDanger = false;
        isCheckpoint = false;
        isVisited = false;
        bfsFlag = false;
        for (int j = 0; j < 4; j++) {
            wall[j] = 'u';
            near[j] = null;
        }
        near[i] = n;
        n.setNear(this, getOpposite(i));
        setWall(n.getWall(getOpposite(i)), i);
        alls.add(this);
    }

    public static int getOpposite(int i){
        return (i+2)%4;
    }

    public void setNear(LabyNode n, int i){
        if(near[i] == null){
            near[i] = n;
            n.setNear(this, getOpposite(i));
        }
    }

    public void setWall(boolean wallo, int i){
        if(wall[i] == 'u'){
            wall[i] = wallo?'w':'f';
            if(near[i] == null){
                near[i] = new LabyNode(this, getOpposite(i));
                insertNode(this, i, near[i]);
            }
        }
    }
    public void setWall(char wallo, int i){
        if(wall[i] == 'u'){
            wall[i] = wallo;
            if(near[i] == null){
                near[i] = new LabyNode(this, getOpposite(i));
                insertNode(this, i, near[i]);
            }
        }
    }

    private static void insertNode(LabyNode from, int i, LabyNode to){
        Queue<LabyNode> q = new java.util.LinkedList<LabyNode>();
        Queue<Coor> n = new java.util.LinkedList<Coor>();

        q.add(from);
        n.add(Coor.ZERO.move(getOpposite(i)));
        from.setBfsFlag(true);
        to.setBfsFlag(true);

        LabyNode tmp;

        while(!q.isEmpty()){
            LabyNode cur = q.poll();
            Coor c = n.poll();

            if(c.isAdiacent(Coor.ZERO))
                cur.setNear(to, getOpposite(Coor.ZERO.getDir(c)));

            for (int j = 0; j < 4; j++) {
                tmp=cur.getNear(j);
                if(tmp != null && !tmp.isBfsFlag()){
                    q.add(tmp);
                    n.add(c.move(j));
                    tmp.setBfsFlag(true);
                }
            }
        }

        for(LabyNode l : alls) l.setBfsFlag(false);

    }

    public int[] trackToUnkown() {
        Queue<LabyNode> nodeQueue = new java.util.LinkedList<LabyNode>();
        Queue<Coor> coorQueue = new java.util.LinkedList<Coor>();
        Queue<Queue<Coor>> tracksQueue = new java.util.LinkedList<Queue<Coor>>();

        nodeQueue.add(this);
        coorQueue.add(Coor.ZERO);
        this.setBfsFlag(true);

        Queue<Coor> tmpCoor=new java.util.LinkedList<Coor>();
        tmpCoor.add(Coor.ZERO);
        tracksQueue.add(tmpCoor);

        Queue<Coor> tmpCoor2;

        LabyNode cur=this,tmp;
        Coor c;

        while(!nodeQueue.isEmpty() && cur.isVisited()){
            cur = nodeQueue.poll();
            c = coorQueue.poll();
            tmpCoor = tracksQueue.poll();

            for (int j = 0; j < 4; j++) {
                tmp=cur.getNear(j);
                if(tmp != null && !tmp.isBfsFlag() && cur.getWall(j) == 'f'){

                    tmpCoor2=new java.util.LinkedList<Coor>(tmpCoor);
                    tmpCoor2.add(c.move(j));
                    tracksQueue.add(tmpCoor2);
                    nodeQueue.add(tmp);
                    coorQueue.add(c.move(j));
                    tmp.setBfsFlag(true);
                }
            }
        }

        for(LabyNode l : alls) l.setBfsFlag(false);


        int size = tmpCoor.size()-1;
        int[] out = new int[size];



        for (int i = 0; i < size; i++) {
            c = tmpCoor.poll();
            out[i] = c.getDir(tmpCoor.peek());
        }

        return out;
    }

    public void setDanger(boolean b){
        isDanger = b;
    }

    public void setCheckpoint(boolean b){
        isCheckpoint = b;
    }

    public void setVisited(boolean b){
        isVisited = b;
    }

    public void setBfsFlag(boolean b){
        bfsFlag = b;
    }

    public LabyNode getNear(int i){
        return near[i];
    }

    public char getWall(int i){
        return wall[i];
    }

    public boolean isDanger(){
        return isDanger;
    }

    public boolean isCheckpoint(){
        return isCheckpoint;
    }

    public boolean isVisited(){
        return isVisited;
    }

    private boolean isBfsFlag(){
        return bfsFlag;
    }


    public String toString(int dir){
            Queue<LabyNode> bfs = new java.util.LinkedList<LabyNode>();
            Queue<Coor> bfsC = new java.util.LinkedList<Coor>();
            ArrayList<LabyNode> all=new ArrayList<>();
            ArrayList<Coor> coor=new ArrayList<>();//array parallelo ad all, con le coordinate della cella
            int minX=0,maxX=0,minY=0,maxY=0;

            LabyNode tmp,tmpN;
            this.setBfsFlag(true);
            Coor tmpC=new Coor(0,0),tmpCNear=new Coor(0,0);

            bfsC.add(new Coor(0,0));
            bfs.add(this);

            all.add(this);
            coor.add(new Coor(0,0));

            //bfs per associare a tutte le celle una coordinata, e salvare tutto
            while(!bfs.isEmpty()){

                tmpC=bfsC.poll();
                tmp=bfs.poll();


                for(int i=0;i<4;i++){
                    tmpN=tmp.getNear(i);
                    if(tmpN!= null && !(tmpN.isBfsFlag())){
                        bfs.add(tmpN);
                        tmpCNear=tmpC.move(i);
                        tmpN.setBfsFlag(true);
                        bfsC.add(tmpCNear);

                        all.add(tmpN);
                        coor.add(tmpCNear);

                        //controllo il minimo,massimo...
                        if(tmpCNear.getX()>maxX)
                            maxX=tmpCNear.getX();
                        else if(tmpCNear.getX()<minX)
                            minX=tmpCNear.getX();

                        if(tmpCNear.getY()>maxY)
                            maxY=tmpCNear.getY();
                        else if(tmpCNear.getY()<minY)
                            minY=tmpCNear.getY();

                    }
                }

            }

            for (LabyNode  i : all)
                i.setBfsFlag(false);

            int deltaX=maxX-minX+1,deltaY=maxY-minY+1,x=abs(minX*2)+1,y=abs(minY*2)+1;//x e y sono dei tmp per lo scostamento, trovo la cella sommandoli alla coor*2
            int lx=deltaX*2+1,ly=deltaY*2+1;//len della griglia
            char[][] mappa=new char[ly][lx];

            for(int i=0;i<ly;i++){
                for (int j = 0; j < lx; j++){
                    mappa[i][j]=' ';
                }
            }

            //metto gli angoli
            for(int i=0;i<ly;i=i+2){
                for (int j = 0; j < lx; j=j+2)
                    mappa[i][j]=(char)206;
            }

            char car;
            for(int i=0;i<all.size();i++){
                if(i==0){
                    car = switch (dir) {
                        case 0 -> '^';
                        case 1 -> '>';
                        case 2 -> 'v';
                        case 3 -> '<';
                        default -> ' ';
                    };
                }else{
                    car = switch (all.get(i).getFlag()) {
                        case 'u' -> 'u';
                        case 'c' -> (char) 184;//c copyright;
                        case 'd' -> (char) 157;//insieme vuoto
                        case 'k' -> (char) 176;//nebbiolina
                        default -> (char) 178;
                    };
                }
                mappa[coor.get(i).getY()*2+y][coor.get(i).getX()*2+x]=car;

                for (int j = 0; j < 4; ++j) {
                    car = switch (all.get(i).getWall(j)) {
                        case 'w' -> switch (j) {
                            case 0, 2 -> (char) 205;//barra bella orizzontale
                            default -> (char) 186;//barra spessa verticale
                        };
                        case 'u' -> '?';
                        case 'f' -> ' ';
                        default -> (char) 178;
                    };
                    mappa[coor.get(i).getY()*2+y+Coor.yp(j)][coor.get(i).getX()*2+x+Coor.ix(j)]=car;
                }
            }
            String out="";
            for(int i=ly-1;i>=0;i--){
                for (int j = 0; j < lx; j++){
                    car=mappa[i][j];
                    if(car==0)
                        out+=' ';
                    else
                        out+=car;
                }
                out+="\n";
            }
            return out;

    }

    public char getFlag(){
        if(isCheckpoint())
            return 'c';
        else if(isDanger())
            return 'd';
        if(isVisited())
            return 'k';
        else
            return 'u';
    }
}
