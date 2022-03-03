//
// Created by samue on 08/02/2022.
//
#include <iostream>
#include "explorer.h"


using namespace std;
std::string decodeDir(int in){
    switch (in) {
        case 0:
            return "davanti";
        case 1:
            return "destra";
        case 2:
            return "dietro";
        case 3:
            return "sinistra";
        default:
            return "strano";
    }
}


int main(){
    auto *lb=new robot::Labirynth();
    int choose;
    do{
        cout << lb->toString() << endl << endl << "inserire la propria scelta:\n0: set muri\n1: set flag\n2: go to checkpoint\n3: go tu unk\n4: esci" << endl;
        cin >> choose;
        switch(choose){
            case 0:
                int tmp;
                for(int i=0;i<4;i++){
                    cout << "inserire muro " << decodeDir(i) << ": ";
                    cin >> tmp;
                    lb->setWall(tmp,i);
                }
                break;
            case 1:
                char f;
                cout << endl << "inserire flag: ";
                cin >> f;
                switch(f){
                    case 'd':
                        lb->setDanger(0);
                        break;
                    case 'c':
                        lb->setCheckPoint();
                        break;
                    default:
                        cout << "non valido";
                }
                break;
            case 2:
                lb->setToCheckPoint();
                break;
            case 3:
                std::vector<int> track=lb->getTrackToU();
                cout << endl << "Percorso per cella sconosciuta: " << endl << "len: " << track.size() << endl;
                for(auto & i:track){
                    cout << "Mossa:" << i << endl ;
                    switch(i){
                        case 0:
                            lb->move();
                            break;
                        case 1:
                            lb->right();
                            break;
                        case 3:
                            lb->left();
                            break;
                    }
                }
        }
    }while(choose!=4);
}