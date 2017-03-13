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
    if (!command & 0xffffff) {
      Brake();
    }
    if (CalculateTraction(command & 0xffffff)) {
      SetRegisters();
      break;
    }
  default:
    // LOG error
    break;
  }
  return false;
}

void TractionControlSystem::CalculateTraction(uint32 command) {
  direction_ = (command & 0xff00) >> 8;
  magnitude_ = command & 0xff;
  double dir = (double)direction_ / 127.0;
  double mag = (double)magnitude_ / 127.0;
  double l = dir + mag;
  double r = mag - dir;
  int ls = l >= 0 ? 1 : -1;
  int rs = r >= 0 ? 1 : -1;
  double m = min(abs(l), abs(r));
  left_pwm_ratio_ = (abs(l) + m) * ls;
  right_pwm_ratio_ = (abs(r) + m) * rs;
}
bool TractionControlSystem::Brake() {}
bool TractionControlSystem::SetPWMsRegister(int left, int right) {}

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

// 10Hz for calibration
void TractionControlSystem::TractionCalibrateCallback() {
  // lockleft
  // lockright
  double left = left_counter_;
  double right = right_counter_;
  // releaseleft
  // releaseright
  if (left_pwm_ratio_ > right_pwm_ratio_) {

  } else {
  }
}

} // namespace vtcs_lib