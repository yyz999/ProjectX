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
        lr_ratio_(0), left_pwm_ratio_(0), right_pwm_ratio_(0),
        left_rigister_(0), right_rigister_(0) {}

  // Start to receive command
  bool StartService();

private:
  int calibration_freq_ = 5;
  int port_number = 8880;
  int8 direction_; // [-127, +127]
  int8 magnitude_; // [-127, +127]

  uint32 left_counter_;
  uint32 right_counter_;
  double left_pwm_ratio_;
  double right_pwm_ratio_;

  uint32 left_rigister_;
  uint32 right_rigister_;

  // socketservice

  bool ProcessCommand(uint32 command);
  void CalculateTraction(uint32 command);

  bool SetRegisters();

  void LeftCounterCallback();
  void RightCounterCallback();

  void TractionCalibrateCallback();
};

} // namespace vtcs_lib