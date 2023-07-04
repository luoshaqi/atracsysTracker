import atracsys.ftk as tracker_sdk

def exit_with_error( error, tracking_system ):
  display(error)
  errors_dict = {}
  if tracking_system.get_last_error(errors_dict) == tracker_sdk.Status.Ok:
    for level in ['errors', 'warnings', 'messages']:
        if level in errors_dict:
            display(errors_dict[level])
  exit(1)

tracking_system = tracker_sdk.TrackingSystem()

if tracking_system.initialise() != tracker_sdk.Status.Ok:
   exit_with_error("Error, can't initialise the atracsys SDK api.", tracking_system)

if tracking_system.enumerate_devices() != tracker_sdk.Status.Ok:
   exit_with_error("Error, can't enumerate devices.", tracking_system)

frame = tracker_sdk.FrameData()

if tracking_system.create_frame(False, 10, 20, 20, 10) != tracker_sdk.Status.Ok:
    exit_with_error("Error, can't create frame object.", tracking_system)
    
print("Tracker with serial ID {0} detected".format(hex(tracking_system.get_enumerated_devices()[0].serial_number)))

tracking_system.get_last_frame(100, frame)