package artery.application;

import BasePCService;

@namespace(artery);
simple DistanceRandPCService extends BasePCService
{
    parameters:
        double pseudonymChangeDistance = default(500);
        
    @class(DistanceRandPCService);
}
