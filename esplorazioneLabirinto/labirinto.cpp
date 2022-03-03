//
// Created by samue on 01/02/2022.
//

#include "explorer.h"

using namespace robot;

Labirynth::Labirynth() {
    dir=0;
    current=new Cell();
    latestCheckpoint = current;
}
void Labirynth::move(){
    current=current->getInDir(dir);
    if(current->getFlag()=='c')
        latestCheckpoint=current;
    if(current->getFlag()=='u')
        current->setFlag('k');
}
void Labirynth::left() {
    dir=(dir+3)%4;
}
void Labirynth::right() {
    dir=(dir+1)%4;
}
void Labirynth::setToCheckPoint() {
    dir=0;
    current=latestCheckpoint;
}
int Labirynth::dirInMap(int dir) {
    return (dir+this->dir)%4;
}
void Labirynth::setDanger(int dir) {
    current->getInDir(dirInMap(dir))->setFlag('d');
}
void Labirynth::setCheckPoint() {
    current->setFlag('c');
    latestCheckpoint=current;
}
void Labirynth::setWall(bool *isWall) {
    for(int i=0;i<4;i++)
        current->setLink(dirInMap(dir),isWall[i]?'w':'f');
}
void Labirynth::setWall(bool isWall, int dirW) {
    current->setLink(dirInMap(dirW),isWall?'w':'f');
}
/**
 * prendo la direzione delle celle da seguire con il metodo della classe Cell, lo converto in movimenti da far fare al robot.
 * Partendo dalla direzione attuale(modificata dopo ogni moviemento virtuale con la nuova direzione), calcolo il movimento
 * da fare(di rotazione) per raggiungere la cella dopo, e aggiunngo un movimento in avanti.
 * Alla fine di questo controllo di non aver messo movimenti opposti vicini, ma non dovrebbe succedere
 * @return
 */
std::vector<int>  Labirynth::getTrackToU(){
    std::vector<int> raw=current->trackToUnk(),out;


    int tmpDir=dir;//salvo la direzione del robot dopo i movimenti per capire gli spostamenti laterali da fare
    for(int i=0;i<raw.size();i++){//per ogni direzione calcolo il movimento da fare
        switch((4-tmpDir+raw[i])%4){
            case 2:
                out.push_back(1);//senza break;
            case 1:
                out.push_back(1);
                break;
            case 3:
                out.push_back(3);//default per 0 vuoto
        }
        out.push_back(0);
        tmpDir=raw[i];
    }


    //se ce ne seno due opposti li tolgo
    for(int i=0;i<out.size()-1;i++){
        if(out[i]+out[i+1]==4){
            for (int j = 0; j < out.size()-2; ++j)
                out[j]=out[j+2];
            out.pop_back();
            out.pop_back();
        }
    }
    return out;

}

std::string Labirynth::toString() {
    return current->toString(dir)+"\ndirezione: "+std::to_string(dir);
}
