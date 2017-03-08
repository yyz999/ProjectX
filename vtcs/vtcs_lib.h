// Vehicle traction control system
#include "common_type.h"

namespace vtcs_lib {

class TractionControlSystem {
public:
  // Constructor
  // calibration_freq: number of times calibrating per second
  TractionControlSystem(int calibration_freq, int port_number)
      : calibration_freq_(calibration_freq), port_number_(port_number),
        direction_(0), magnitude_(0), left_counter_(0), right_counter_(0),
        lr_ratio_(0), left_pwm_ratio_(0), right_pwm_ratio_(0) {}

  // Start to receive command
  bool StartService();

private:
  int calibration_freq_;
  int port_number;
  int8 direction_;
  int8 magnitude_;

  uint32 left_counter_;
  uint32 right_counter_;
  double lr_ratio_;
  double left_pwm_ratio_;
  double right_pwm_ratio_;

  // socketservice

  bool ProcessCommand(uint32 command);
  bool CalculateTraction(uint32 command);

  bool SetRegisters();

  void LeftCounterCallback();
  void RightCounterCallback();

  void TractionCalibrateCallback();
};

} // namespace vtcs_lib