#ifndef LABYRINTHEXPLORER_EXPLORER_H
#define LABYRINTHEXPLORER_EXPLORER_H

#include <vector>
#include <string>



/**
 * Le prossime righe sono note per gli utilizzatori, a cui non importa il codice sotto.
 * La classe che vi importa è la classe Labirynth, o come l'ho chiamata.
 * Ha solo pochi metodi pubblici, quelli per informarla dei movimenti che sta facendo il robot,
 * e quello per andare a una nuova cella.
 * Questo(getTrackToU()) ritorna un vettore, di movimenti in int, in cui lo 0 zero vuol dire avanti, 1 destra(90 dg), 3 sinistra(90 dg).
 * Non ci dovrebbero essere 2(180 dg).
 * <br><br>
 * I metodi per informare dei movimenti sono: move(), left() e right(), che informano
 * di un movimento in avanti e di rotazione di 90dg a sinistra e destra.
 * Per informare dei muri che si vedono c'e' il metodo setWall, che da parametro
 * vuole o la direzione e il booleano relativo al fatto che il muro ci sia o meno,
 * oppure un puntatore a un vettore di 4 elementi con i booleani della presenza dei
 * muri nella 'I'esima direzione.
 * Poi abbiamo i metodi per settare i flag delle celle:
 * setCheckPoint() segna che la cella attuale e' un checkpoint, setDanger(int dir)
 * segnala che la cella in direzione dir e' pericolosa e non va attraversata.
 * Realativo ai checkpoint abbiamo il metodo setToCheckPoint(), che segnala che
 * il robot e' stato spostato all'ultimo checkpoint attraversato, in direzione uguale
 * a quella in cui e' stato posizionato all'inizio.
 * C'e' anche un metodo toString(), usato nel debug, che da una rappresentazione del labirinto
 *
 */






namespace robot{
    /**
     * classe per il salvataggio di coordinate, con alcuni metodi di utilita.
     * Gli attributi sono pubblici, non ci sono get e set, di tipo int
     */
    class Coor {
    public:
        int x, y;

        Coor(int x, int y);

        /**
         * restituisce una coordinata adiacente spostata di uno rispetto a questa, la
         * direzone usa il codice sotto delle celle, orario, +1 = 90 gradi.
         * @param dir direzione, da 0 a 4
         * @return indirizzo di una coordinata nella direzoine dir
         */
        Coor getInDir(int dir);

        /**
         * resituisce un numero da sommara a una x per otterere una
         * coordinata x nella data posizione(sinistra -1, destra 1, sopra e sotto 0)
         * @param dir dorezione nel codice standard
         * @return signed int da sommare
         */
        static int ix(int dir);

        /**
         * resituisce un numero da sommara a una y per otterere una
         * coordinata x nella data posizione(sopra 1, sotto -1, destra e sinistra 0)
         * @param dir dorezione nel codice standard
         * @return signed int da sommare
         */
        static int yp(int dir);
    };


    /**
     * ogni cella ha il numero di quelle vicine, -1 se queste non sono accessibili,
     * il codice delle direzioni e: 0 sopra, 1 destra, 3 sotto, 4 sinistra
     * , il tutto e dinamico, adesso provo e poi aggiorno la bio.
     * Per i link: f e` free, colelgamento libero; w e` wall, u e` undefined
     * . Per i flag: f e` undefined(yet), k e n sono knowed e not knowed, c e` checkpoint,
     * d e` danger, non ci si puo andare su
     *
     *.
     * Ho fatto tutto dinamico, non si ha una lista completa delle celle, ogni cella conosce
     * solo le sue vicine.
     * Forse non e la cosa piu efficiente, ma e` un buon esercizio.
     * Un problema e` l'aggiunta di nuove celle, che va fatta solo quando una cella
     * arriva a conoscere un muro(le celle cosi create non conosceranno muri, se non di
     * celle gia esistenti, cosi non creo celle all'infinito).
     * Quando aggiungo una nuova cella cerco con una bfs se celle adiacenti in orizzontale,
     * che non per forza sono facilmente accessibili, quindi insieme alla lista delle celle
     * da esplorare(bfs procedurale), ne ho una parallela con le coordinate astratte di ogni cella,
     * e tengo come riferimento 0;0 quella appena aggiunta.
     * Questo e` fatto dal metodo statico insertNewCell.
     * Il metodo addLink aggiunge una conoscenza su un muro, se questa non c'era allora
     * crea una nuova cella, e chiama il metodo insertNewCell.
     * Viene chiamato dal metodo setLink, che inoltre comunica il parametro del muro
     * all'altra cella interessata.
     *
     */
    class Cell {
    private:
        //array di 4 elementi con salvate le celle vicine, se presenti
        Cell *vicini[4]={};
        char *links;//array da 4 elementi che indica i muri, se esistono o no o se sono sconosciuti
        static int nCelle;//numero di celle create finora
        char flag;//ad esempio danger o checkpoint
        /**
         * ritorna un int che nel codice standard delle direzoini e' l'opposto dell'input
         * @param in direzione di cui si vuole l'opposto(0-4)
         * @return opposto della direzione input
         */
        static int opposite(int in);

        /**
         * metodo statico che permette di inserire una nuova cella nella mappa, tendo conto
         * del fatto che le celle adiacenti a quella nuova potrebbero non essere facilmente accessiibili,
         * se non dopo aver fatto una ricerca tra tutti i nodi. Il funzionamento poi per il
         * riconoscimento delle celle vicine e' piuttosto semplice, ho una lista parallela a
         * quella della bfs con le coordinate delle celle(astratte, cambiano ogni volta)
         * relative alla cella nuova(coor 0;0), con il medoto getInDir(dir) quando
         * aggiungo alla lista una nuova cella genero anche la relativa coordinata, cosi'
         * e' poi facile capire quelle e dove aggiungere i link alla nuova cella
         * @param from cella di partenza gia' inserita nella mappa
         * @param dir direzione dalla cella from nella quale viene aggiunta la cella
         * @param in cella da aggiungere
         */
        static void insertNewCell(Cell *from, int dir, Cell *in);

    public:
        /**
         * costruttore con inserimento nel labirinto, non controlla che from abbia this
         * salvata nella sua direzione
         * @param dir la direzione della cella chiamante, per la nuova cella
         * @param in cella chiamante
         */
        Cell(int dir, Cell *from);

        bool isExplored;//flag per bfs
        Cell();



        /**
         * @return numero totale di celle instanziate
         */
        static int getNCelle();

        char getFlag();

        /**
         * non sicuro da privacy leak
         * @return indirizzo dell'array di 4 char con i flag nelle direzioni per le celle vicine
         */
        char *getLinks();

        /**
         * metodo che controlla che il link non fosse gia assegnato, inoltre(importante)
         * se in quella direzione non e' insanziata nessuna celle ne crea una nuova e la
         * aggiunge alla mappa
         * @param dir direzone in cui settare il nflag
         * @param nflag nflag di muro
         */
        void setLink(int dir, char nflag);

        void setFlag(char f);

        /**
         * aggiunge la cella ai vicini se non ne esisteva gia' una in quella direzione,
         * setta inoltre il proprio link in quella direzione, visto che l'unico modo per
         * aggiungere vicini oltre a questo metodo e' settando per la prima volta un link,
         * allora se l'altra cella sa il flag del collegamento lo copia anche per se' stessa,
         * se no rimane 'u'
         * @param dir direzione in cui aggiungere la cella
         * @param in indirizzo della cella da aggiungere
         */
        void addCell(int dir, Cell *in);

        Cell *getInDir(int dir);

        /**
         * altro medoto molto importante, trova il primo percorso(bfs) per una cella sconosciuta,
         * passando solo da link 'f' e da cella non danger.
         * E' una bfs con array di vector parallelo, esso contiene le direzioni(assolute)
         * per la cella successiva per raggiugnerlo. Con una bfs con cui meorizzo il percorso
         * per ogni cella quando la aggiungo alla queue, c'e un break che cosi esce quando
         * trova una cella 'u'(unknow, sconosciuta, non ancora esplorata dal robot), forse lo
         * cambio con un controllo nel while.
         * @return lista di direzioni assolute per la prima cella unk
         */
        std::vector<int> trackToUnk();

        /**
         * restituiisce un panoramica della mappa, in via di miglioramento
         * @return stringa grossa da stampare
         */
        std::string toString(int dir);
    };


    /**
     * La classe Labirynth `e un gradino sopra a quella cell, la quale fornisce la maggior
     * parte dei metodi necessari per la memorizzazoine e esplorazione del labirinto.
     * Questa pero` fa da interfaccia di alto livello per il robot, e aggiune funzionalita
     * per la gara, come il movimento sull`ultimo checkpoint.
     * Si tiene conto che la direzone del robot `e diversa rispetto alla mappa, cosi si
     * convertono le direzoini da assolute e relative per il robot
     */
    class Labirynth {
    private:
        int dir;
        Cell *current, *latestCheckpoint;

        int dirInMap(int di);

    public:
        Labirynth();

        void move();

        void setToCheckPoint();

        void setDanger(int dir);

        void setCheckPoint();

        /**
         * metodo da interfaccia per il metodo trackToUnk() delle celle, ritorna una serie
         * di movimenti da fare, che seguono il codice di direzioni precedentemente addottatto:
         * lo 0 significa in avanti, l'uno rotazione di 90 a destra, il tre di 90 a sinistra.
         * Il due non viene scritto ma si troveranno due uno.
         * @return movimenti da fare per raggiungere la piu vicina cella inesplorata
         */
        std::vector<int> getTrackToU();

        void setWall(bool isWall, int dir);

        void setWall(bool *isWall);

        void left();

        void right();

        std::string toString();
    };

}
#endif //LABYRINTHEXPLORER_EXPLORER_H
