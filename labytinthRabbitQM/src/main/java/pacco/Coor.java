package pacco;

public class Coor {

    public static Coor ZERO=new Coor(0,0);
    private final int x;
    private final int y;


    public Coor(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public int getX() {
        return x;
    }

    public int getY() {
        return y;
    }
    public static int ix(int dir) {
        return switch(dir) {
            case 1 -> 1;
            case 3 -> -1;
            default -> 0;
        };
    }
    public static int yp(int dir) {
        return switch(dir) {
            case 0 -> 1;
            case 2 -> -1;
            default -> 0;
        };
    }

    public Coor move(int dir) {
        return new Coor(x + ix(dir), y + yp(dir));
    }

    public boolean isAdiacent(Coor c) {
        return (Math.abs(x - c.x) + Math.abs(y - c.y)) == 1;
    }

    public int getDir(Coor c){
        if(c.x==x)
            return c.y>y?0:2;
        else
            return c.x>x?1:3;
    }
}
