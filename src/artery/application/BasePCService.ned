package artery.application;

import artery.application.CaService;

simple BasePCService extends CaService
{
    parameters:
        @signal[PseudonymChanged](type=double);
        @statistic[nPseudonymChanged](source=PseudonymChanged;title="nPseudonyms";record=last);
    
    @class(BasePCService);
}
