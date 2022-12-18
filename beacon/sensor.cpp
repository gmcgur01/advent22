#include "sensor.h"
#include <cmath>

using namespace std;

Sensor::Sensor(Position sensor, Position beacon) 
{
    this->sensor_x = sensor.x;
    this->sensor_y = sensor.y;
    this->beacon_x = beacon.x;
    this->beacon_y = beacon.y;
    this->range = abs(sensor.x - beacon.x) + abs(sensor.y - beacon.y);
}
