import decoder

ev0 = {"data": "100dcc3d0d0190065f1c0100",
       "device": "730CFA",
       "time": "1628577957",
       "devicetype": 0x10,
       "devicetypeid": "60868b60113a4807ab6ba7a2",
       }

ev1 = {"data": "1101b004bc02480370030100",
       "device": "730CFA",
       "time": "1628577957",
       "devicetype": 0x11,
       "devicetypeid": "60868b60113a4807ab6ba7a2",
       }

ev2 = {"data": "12012e0e0100000000000000",
       "device": "730CFA",
       "time": "1628577957",
       "devicetype": 0x12,
       "devicetypeid": "60868b60113a4807ab6ba7a2",
       }

ev3 = {"data": "000f9e0165f2020000000000 ",
       "device": "730CFA",
       "time": "1628577957",
       "devicetype": 0x00,
       "devicetypeid": "60868b60113a4807ab6ba7a2",
       }

# Press the green button in the gutter to run the script.
print(decoder.lambda_handler(ev3, ""))
