//
// Created by samue on 01/02/2022.
//

#include "explorer.h"
using namespace robot;
Coor::Coor(int x, int y) {
    this->x=x;
    this->y=y;
}
Coor Coor::getInDir(int dir) {
    return (Coor)Coor(x+ix(dir),y+yp(dir));
}

int Coor::ix(int dir) {
    switch (dir) {
        case 1:
            return 1;
        case 3:
            return -1;
        default:
            return 0;
    }
}

int Coor::yp(int dir) {
    switch (dir) {
        case 0:
            return 1;
        case 2:
            return -1;
        default:
            return 0;
    }
}

