package pacco;

import java.util.Scanner;

/**
 * main di debug con testo e inserimento da linea di comando
 */
public class MainProva {
    public static String decodeDir(int in) {
        return switch (in) {
            case 0 -> "davanti";
            case 1 -> "destra";
            case 2 -> "dietro";
            case 3 -> "sinistra";
            default -> "strano";
        };
    }

    public static void main(String[] args) {

        Esploratore lb = new Esploratore();
        int choose;
        Scanner sc = new Scanner(System.in);
        do {
            System.out.println(lb + "\n\ninserire la propria scelta:\n0: set muri\n1: set flag\n2: go to checkpoint\n3: go tu unk\n4: esci");
            choose= sc.nextInt();
            switch (choose) {
                case 0 -> {
                    int tmp;
                    for (int i = 0; i < 4; i++) {
                        System.out.println("inserire muro " + decodeDir(i) + ": ");
                        tmp = sc.nextInt();
                        lb.setWall(i, 0 != tmp);
                    }
                }
                case 1 -> {
                    char f;
                    System.out.println("inserire flag: ");
                    f = sc.next().charAt(0);
                    switch (f) {
                        case 'd' -> lb.setDanger(0);
                        case 'c' -> lb.setLastCheckpoint();
                        default -> System.out.println("non valido");
                    }
                }
                case 2 -> lb.goToCheckpoint();
                case 3 -> {
                    int[] track = lb.getMovements();
                    System.out.println("Percorso per cella sconosciuta: \nlen: " + track.length);
                    for (int i : track) {
                        System.out.println("Mossa:" + i + "\n");
                        switch (i) {
                            case 0 -> lb.forward();
                            case 1 -> lb.right();
                            case 3 -> lb.left();
                            case 2 -> lb.back();
                        }
                    }
                }
            }
        } while (choose != 4);

    }
}
