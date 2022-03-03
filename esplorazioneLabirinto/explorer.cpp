#include "explorer.h"

#include <queue>
#include <vector>

using namespace robot;

int Cell::nCelle = 0;

int Cell::opposite(int in) {
    if(in>=0 && in <=4)
        return (in+2)%4;
    else
        return in;
}
Cell::Cell() {
    nCelle=1;
    //vicini= (Cell**)calloc(4, sizeof(*vicini));
    links=(char*) calloc(4,sizeof(char));
    flag='u';
    for(int i=0;i<4;i++)
        links[i]='u';
    isExplored=false;
    flag='k';
}
Cell::Cell(int dir, Cell *from) {
    nCelle++;
    isExplored= false;
    //vicini=(Cell**) calloc(4,sizeof(Cell*));
    links=(char*) calloc(4,sizeof(char));
    flag='u';
    for(int i=0;i<4;i++)
        links[i]='u';
    vicini[dir]=from;
    links[dir]=from->getLinks()[opposite(dir)];
    from->addCell(opposite(dir),this);
}
void Cell::setFlag(char f) {
    flag=f;
}
char Cell::getFlag() {
    return flag;
}
char* Cell::getLinks() {
    return links;
}
int Cell::getNCelle() {
    return Cell::nCelle;
}
void Cell::setLink(int dir, char nflag) {
    if(links[dir]=='u'){
        links[dir]=nflag;
        if(vicini[dir]==nullptr){
            vicini[dir]=new Cell(opposite(dir),this);
            insertNewCell(this,dir,vicini[dir]);
        }else{
            //il costruttore con direzione copia anche il flag del wall
            vicini[dir]->setLink(opposite(dir),nflag);
        }
    }
}
/**
 * aggiungo una cella, inoltre aggiungo questa cella e questo link per la cella aggiunta, con controllo si sovrascrittura
 * @param dir direzione in cui aggiungere la cella
 * @param in cella da aggiungere
 */
void Cell::addCell(int dir, Cell *in) {
    if(vicini[dir]==nullptr){
        vicini[dir]=in;
        in->addCell(opposite(dir),this);
        //se succede questo è perchè in quella direzione non c'era niente, se ci fosse stato qualcosa era perche' avevo prima assegnato un link
        links[dir]=in->links[opposite(dir)];
    }
}
/*
 * aggiungo una cella nella struttura di celle, partendo dalla cella indicata, nella direzione indicata.
 * Per farlo controllo tra tutte le celle se ce ne sono di adiacenti. Con una bfs le scorro tutte,
 * associandogli una coordinata relativa alla cella nuova(0;0), in modi che qualunque forma e porzione di labirinto io abbia
 * esplorato possa aggiungere la cella perfettamente.
 */
void Cell::insertNewCell(Cell *from, int dir, Cell *in) {

    //queue parallele per bfs
    std::queue<Cell*> left;//celle mancanti da controllare
    std::queue<Coor> coordOfCells;

    //tmp per bfs, la cella da cui si ricavano i vicini
    Cell *currentCell;
    Coor current(0,0);

    //le celle di partenza sono gia' esplorate, non vanno aggiunte alla lista di nuovo
    from->isExplored=true;
    in->isExplored=true;

    //tmp per vicino da aggiungere alla queue
    Cell* tmp;

    //la cella dalla quale viene aggiunta la nuova e' la prima della bfs
    coordOfCells.push(current.getInDir(opposite(dir)));//la coordinata in direzione opposta a dir vicino a 0;0
    left.push(from);


    while(!left.empty()){

        //prendo la nuova cella da controllare
        currentCell=left.front();
        current=coordOfCells.front();
        //la tolgo dalle queue
        left.pop();
        coordOfCells.pop();

        //aggiungo i suoi vicini, se non sono gia' stati esplorati
        for(int i=0;i<4;i++){
            tmp=currentCell->getInDir(i);
            if(tmp!=nullptr && !tmp->isExplored){
                left.push(tmp);
                tmp->isExplored=true;
                coordOfCells.push(current.getInDir(i));//coordinata in direzione dir rispetto alla cella corrente
            }
        }
        //controllo se e vicina alla cella 0:0, la aggiungo nella giusta direzione
        if(current.x==0){
            if(current.y==-1){
                currentCell->addCell(0,in);
            }else if(current.y==1){
                currentCell->addCell(2,in);
            }
        }else if(current.y==0){
            if(current.x==-1){
                currentCell->addCell(1,in);
            }else if(current.x==1){
                currentCell->addCell(3,in);
            }
        }
    }



    //preparo per una bfs inversa, non ho bisogno delle coordinate, riassegno a tutti il non esplorato
    in->isExplored= false;
    left.push(from);

    //metto a posto tutti gli isExplored
    while(!left.empty()){
        //nuova cella da cui prendere i vicini
        currentCell=left.front();
        left.pop();
        //prendo i vicini, solo se sono stati esplorati(non ancora de-esplorati)
        for(int i=0;i<4;i++){
            tmp=currentCell->getInDir(i);
            if(tmp!=nullptr && tmp->isExplored){
                left.push(tmp);
                tmp->isExplored=false;
            }
        }
    }
}
Cell* Cell::getInDir(int dir) {
    return vicini[dir];
}

/*
 * calcolo il percorso veloce per una cella sconosciuta.
 * Uso una bfs che finisce anche quando la cella corrente e' sconosciuta, quindi alla piu'
 * vicina cella sconosciuta. Per ogni cella che elaboro salvo un vettore con le celle da passare per arrivarci.
 * Per avere un percorso valido non prendo tutte le celle vicine, ma solo quelle che sono collegate da un collegamento libero e
 * che non hanno il flag di pericolo.
 * Alla fine decodifico il vettore di celle in una vettore di int con la direzione della cella successiva(assoluta).
 */
std::vector<int> Cell::trackToUnk() {
    //bfs per la cella sconosciuta piu vicina, con salvataggio del percorso
    std::queue<Cell*> checks;
    std::queue<std::vector<Cell*>> previus;//lista parallela con le celle usate da quella corrente(percorso)
    std::vector<Cell*> explored;//lista di celle esplorate per velocizzare il reset di isExplored

    //tmp per il vettore della cella corrente e per quello della cella da aggiungere alla queue
    std::vector<Cell*> tmpVec,tmpVecNear;

    std::vector<int> out;

    tmpVec.push_back(this);
    this->isExplored=true;
    explored.push_back(this);

    Cell *tmp=this,*tmpNear;

    //aggiungo la prima cella alla queue
    checks.push(tmp);
    previus.push(tmpVec);

    //per ogni cella controllo quelle vicine, se vanno bene le aggiungo, dopo aver controllato se sono free
    while(!checks.empty() && tmp->getFlag()!='u'){

        tmpVec=previus.front();
        previus.pop();
        tmp=checks.front();
        checks.pop();

        if(tmp->getFlag()!='u'){//se la cella attuale e' sconosciuta salto questo pezzo e poi esco
            for (int i = 0; i < 4; i++) {
                tmpNear = tmp->getInDir(i);

                if (tmpNear != nullptr && !tmpNear->isExplored && tmp->getLinks()[i] == 'f' &&
                    tmpNear->getFlag() != 'd') {

                    tmpNear->isExplored = true;
                    explored.push_back(tmpNear);
                    tmpVecNear = tmpVec;//deep copy
                    tmpVecNear.push_back(tmpNear);

                    previus.push(tmpVecNear);
                    checks.push(tmpNear);
                }
            }
        }

    }
    //adesso che e' uscito trovo in tmp l'ultima cella che ho controllato, che se sono uscito e tutto e' andato bene e' 'u'.
    //cosi' in tmpVec trovo il vettore di celle per raggiungerla


    //se cosi non fosse vuol dire che ho esplorato tutto il labirinto
    if(tmp->getFlag()=='u'){
        //decompongo la lista di celle il lista di direzioni della cella successiva
        int add;

        //per ogni cella tranne l'ultima cerco la direzione della cella dopo
        for (int i=0;i < tmpVec.size()-1;i++) {

            add = 0;
            while (tmpVec[i]->getInDir(add) != tmpVec[i+1])
                add++;

            out.push_back(add);

        }


    }
    for (auto &i: explored)
        i->isExplored = false;

    return out;
}

std::string Cell::toString(int dir) {
    std::queue<Cell*> bfs;
    std::queue<Coor> bfsC;
    std::vector<Cell*> all;//tutte le coordinate
    std::vector<Coor> coor;//array parallelo ad all, con le coordinate della cella
    int minX=0,maxX=0,minY=0,maxY=0;

    Cell *tmp,*tmpN;
    this->isExplored=true;
    Coor tmpC(0,0),tmpCNear(0,0);

    bfsC.push(Coor(0,0));
    bfs.push(this);

    all.push_back(this);
    coor.emplace_back(0,0);

    //bfs per associare a tutte le celle una coordinata, e salvare tutto
    while(!bfs.empty()){

        tmpC=bfsC.front();
        tmp=bfs.front();

        bfs.pop();
        bfsC.pop();

        for(int i=0;i<4;i++){
            tmpN=tmp->getInDir(i);
            if(tmpN!= nullptr && !(tmpN->isExplored)){
                bfs.push(tmpN);
                tmpCNear=tmpC.getInDir(i);
                tmpN->isExplored=true;
                bfsC.push(tmpCNear);

                all.push_back(tmpN);
                coor.push_back(tmpCNear);

                //controllo il minimo,massimo...
                if(tmpCNear.x>maxX)
                    maxX=tmpCNear.x;
                else if(tmpCNear.x<minX)
                    minX=tmpCNear.x;

                if(tmpCNear.y>maxY)
                    maxY=tmpCNear.y;
                else if(tmpCNear.y<minY)
                    minY=tmpCNear.y;

            }
        }

    }

    for (auto & i : all)
        i->isExplored=false;

    int deltaX=maxX-minX+1,deltaY=maxY-minY+1,x=abs(minX*2)+1,y=abs(minY*2)+1;//x e y sono dei tmp per lo scostamento, trovo la cella sommandoli alla coor*2
    int lx=deltaX*2+1,ly=deltaY*2+1;//len della griglia
    char mappa[ly][lx];

    for(int i=0;i<ly;i++){
        for (int j = 0; j < lx; j++){
            mappa[i][j]=' ';
        }
    }

    //metto gli angoli
    for(int i=0;i<ly;i=i+2){
        for (int j = 0; j < lx; j=j+2)
            mappa[i][j]=char(206);
    }

    char car;
    for(int i=0;i<all.size();i++){
        if(i==0){
            switch(dir){
                case 0:
                    car='^';
                    break;
                case 1:
                    car='>';
                    break;
                case 2:
                    car='v';
                    break;
                case 3:
                    car='<';
                    break;
            }
        }else{
            switch (all[i]->getFlag()) {
                case 'u':
                    car = 'u';
                    break;
                case 'c':
                    car = char(184);//c copyright;
                    break;
                case 'd':
                    car = char(157);//insieme vuoto
                    break;
                case 'k':
                    car = char(176);//nebbiolina
                    break;
                default:
                    car = char(178);
            }
        }
        mappa[coor[i].y*2+y][coor[i].x*2+x]=car;

        for (int j = 0; j < 4; ++j) {
            switch(all[i]->getLinks()[j]){
                case 'w':
                    switch (j) {
                        case 0:
                        case 2:
                            car=char(205);//barra bella orizzontale
                            break;
                        default:
                            car=char(186);//barra spessa verticale
                    }
                    break;
                case 'u':
                    car='?';
                    break;
                case 'f':
                    car=' ';
                    break;
                default:
                    car=char(178);
            }
            mappa[coor[i].y*2+y+Coor::yp(j)][coor[i].x*2+x+Coor::ix(j)]=car;
        }
    }
    std::string out;
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
