class Interval {
    public:
        Interval(Sensor *sensor);

        void add_range(int start, int end);

        int start;
        int end;
        Interval *left;
        Interval *right;
        
};