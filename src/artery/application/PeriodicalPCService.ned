package artery.application;

import BasePCService;

simple PeriodicalPCService extends BasePCService
{
    parameters:
        // The time in seconds after which the pseudonym is changed.
        double pseudonymLifetime = default(0.5);

    @class(PeriodicalPCService);
}
