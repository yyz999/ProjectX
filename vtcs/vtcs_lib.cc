// Vehicle traction control system
#include "vtcs_lib.h"

#include <cmath>

using namespace std;

namespace vtcs_lib {
bool TractionControlSystem::StartService() {
  // Initialize Register configuration

  // Initialize socket server and start
}

bool TractionControlSystem::ProcessCommand(uint32 command) {
  switch (command & 0xff000000) {
  case 0x01000000: // Traction configuration
    if (CalculateTraction(command & 0xffffff)) {
      return SetRegisters();
    }
    break;
  default:
    // LOG error
    break;
  }
  return false;
}

bool TractionControlSystem::CalculateTraction(uint32 command) {
  direction_ = (command & 0xff00) >> 8;
  magnitude_ = command & 0xff;
  double dir = (double)direction_ / 256.0 * 360.0;
  double mag = (double)magnitude_ / 255.0;
}

bool TractionControlSystem::SetRegisters() {}

void TractionControlSystem::LeftCounterCallback() {
  // lockleft
  left_counter_++;
  // releaseleft
}

void TractionControlSystem::RightCounterCallback() {
  // lockright
  right_counter_++;
  // releaseright
}

void TractionControlSystem::TractionCalibrateCallback() {}

} // namespace vtcs_lib