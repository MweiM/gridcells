#include <armadillo>

using namespace arma;

const double dt = 20.;
const double arenaDiam = 180.;
const double h = 3.;

vec extractSpikePos(const vec& spikePosIdx, const vec& posData, double dt)
{
    arma::vec res(spikePosIdx.n_elem);
    for (int i = 0; i < spikePosIdx.n_elem; i++) {
        res(i) = posData(spikePosIdx(i));
    }
    return res;
}


mat SNSpatialRate2D(const vec& spikeTimes, const vec& pos_x, const vec&pos_y, double dt, double arenaDiam, double h)
{
    double precision = arenaDiam / h;
    vec xedges = arma::linspace(-arenaDiam/2, arenaDiam/2, precision+1);
    vec yedges = arma::linspace(-arenaDiam/2, arenaDiam/2, precision+1);

    mat rateMap = arma::zeros(xedges.n_elem, yedges.n_elem);
    vec spikePosIdx = spikeTimes / dt;
    vec neuronPos_x = extractSpikePos(spikePosIdx, pos_x, dt);
    vec neuronPos_y = extractSpikePos(spikePosIdx, pos_y, dt);


    int nIter = 0;
    for (int x_i = 0; x_i < xedges.n_elem; x_i++) {
        for (int y_i =0; y_i < yedges.n_elem; y_i++) {
            cout << "nIter: " << nIter << endl;
            double x = xedges(x_i);
            double y = yedges(y_i);

            vec posDist2 = arma::square(pos_x - x) + arma::square(pos_y - y);
            bool isNearTrack = arma::accu(arma::sqrt(posDist2) <= h) > 0;

            if (isNearTrack) {
                double normConst = arma::sum(arma::exp(-posDist2 / 2. / (h*h))) * dt;
                vec neuronPosDist2 = arma::square(neuronPos_x - x) + 
                                     arma::square(neuronPos_y - y);
                double spikes = arma::sum(exp( -neuronPosDist2 / 2. / (h*h)));
                rateMap(x_i, y_i) = spikes / normConst;
            }

            nIter++;
        }
    }

    return rateMap.t();
}


int main(void)
{
    vec spikeTimes;
    vec pos_x;
    vec pos_y;

    bool loadOK = true;
    loadOK &= spikeTimes.load("data/spikeTimes.txt", arma::raw_ascii);
    loadOK &= pos_x.load("data/pos_x.txt", arma::raw_ascii);
    loadOK &= pos_y.load("data/pos_y.txt", arma::raw_ascii);

    if (!loadOK){
        cerr << "Could not load data files!" << endl;
        return 1;
    }

    mat rateMap = SNSpatialRate2D(spikeTimes, pos_x, pos_y, dt, arenaDiam, h);
    (rateMap * 1e3).print();

    return 0;
}
