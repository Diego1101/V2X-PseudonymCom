package artery.application;

import BasePCService;

simple PeriodicalRandPCService extends BasePCService
{
    parameters:
        // The time in seconds after which the pseudonym is changed.
        double pseudonymLifetime = default(0.5);

    @class(PeriodicalRandPCService);
}
