#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "sensor.h"

using namespace std;

void read_file(char *filename, vector<Sensor> *sensors);

int main(int argc, char *argv[])
{
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <file name>" << endl;
        exit(1);
    }

    vector<Sensor> sensors;
    read_file(argv[1], &sensors);

    for (int i = 0; i < (int)sensors.size(); i++) {
        cout << sensors.at(i).range << endl;
    }
    
    return 0;
}

void read_file(char *filename, vector<Sensor> *sensors)
{
    FILE *fp = fopen(filename, "r");

    while (!feof(fp)) {
        Position sensor;
        Position beacon;
        fscanf(fp, "Sensor at x=%d, y=%d: closest beacon is at x=%d, y=%d\n",
               &sensor.x, &sensor.y, &beacon.x, &beacon.y);
        
        sensors->push_back(Sensor(sensor, beacon));
    }

    fclose(fp);
}