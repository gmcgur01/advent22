struct Position {
    int x, y;
};

class Sensor {
    public:
        Sensor(Position sensor, Position beacon);

        int sensor_x;
        int sensor_y;
        int beacon_x;
        int beacon_y;
        int range;
};