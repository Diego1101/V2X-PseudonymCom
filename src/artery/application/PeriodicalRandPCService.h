/**
 * Periodical Pseudonym Change Service
 *
 * @file    PeriodicalRandPCService.h
 * @author  Samuel Müller
 * @date    05.01.2022
 */

#ifndef __VEINS_PeriodicalPC_H_
#define __VEINS_PeriodicalPC_H_

#include "BasePCService.h"
#include <omnetpp/simtime.h>

namespace artery
{
    class PeriodicalRandPCService : public BasePCService
    {

    public:
        void initialize() override;

    private:
        /**
         * The time in seconds after which the pseudonym is changed.
         */
        double _pseudonymLifetime;

        /**
         * Time of the last pseudonym change.
         */
        double _lastPseudonymChange;

    protected:
        bool triggerConditionsAreMet() override;
    };
}

#endif
