#ifndef BASICMODULEMAPPER_H_DPQ8TMFW
#define BASICMODULEMAPPER_H_DPQ8TMFW

#include "traci/ModuleMapper.h"
#include <omnetpp/csimplemodule.h>

namespace traci
{

class BasicModuleMapper : public ModuleMapper, public omnetpp::cSimpleModule
{
public:
    void initialize() override;
    omnetpp::cModuleType* vehicle(NodeManager&, const std::string&);

private:
    omnetpp::cModuleType* m_type;
};

} // namespace traci

#endif /* BASICMODULEMAPPER_H_DPQ8TMFW */

