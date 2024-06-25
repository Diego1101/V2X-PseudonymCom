/**
 * Periodical Pseudonym Change Service 
 *
 * @file    PeriodicalRandPCService.cc
 * @author  Samuel Müller
 * @date    05.01.2022
 */

#include "PeriodicalRandPCService.h"
#include <omnetpp/simtime.h>


namespace artery
{
    using namespace omnetpp;
    
    Define_Module(PeriodicalRandPCService);

    void PeriodicalRandPCService::initialize()
    {
        BasePCService::initialize();
        _pseudonymLifetime = par("pseudonymLifetime");
        if(simTime().dbl() < 0){
            _lastPseudonymChange = 0;
        } else {
            _lastPseudonymChange = simTime().dbl();
        }
    }

    bool PeriodicalRandPCService::triggerConditionsAreMet()
    {
        //std::cout<<mVehicleDataProvider->getStationId()<<": "<<(_lastPseudonymChange - simTime())<<" >= "<<_pseudonymLifetime<<endl;
        if ((simTime() - _lastPseudonymChange).dbl() >= _pseudonymLifetime)
        {
            std::cout << _pseudonymLifetime << endl;
            _pseudonymLifetime = rand()%10+1;
            
            _lastPseudonymChange = simTime().dbl();
            return true;
        }
        return false;
    }
}
