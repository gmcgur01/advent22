#include "interval.h"
#include "sensor.h"

using namespace std;

Interval::Interval(Sensor *sensor, int)
{
    this->start = sensor->sensor_x - sensor->range;
    this->end = sensor->sensor_x + sensor->range;

    this->left = nullptr;
    this->right = nullptr;
}

