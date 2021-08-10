import json

ev = {"data": "100dcc3d0d0190065f1c0100",
      "device": "730CFA",
      "time": "1628577957",
      "devicetype": 16,
      "devicetypeid": "60868b60113a4807ab6ba7a2",
      }

FATFLAG = 0x01
HEIGHTFLAG = 0x02
METABOLISMFLAG = 0x04
USERFLAG = 0x08

def weight_handler(data):
    n = 2
    flags = int(data[n: n + 2], 16)
    n = n + 2

    weight = int(data[n + 2: n + 4] + data[n: n + 2], 16) * 0.005
    weight = round(weight, 2)
    n = n + 4

    if flags & FATFLAG == FATFLAG:
        fat = int(data[n + 2: n + 4] + data[n: n + 2], 16) * 0.1
        fat = round(fat, 1)
    else:
        fat = 0
    n = n + 4

    if flags & HEIGHTFLAG == HEIGHTFLAG:
        height = int(data[n + 2: n + 4] + data[n: n + 2], 16)
    else:
        height = 0
    n = n + 4

    if flags & METABOLISMFLAG == METABOLISMFLAG:
        bm = int(data[n + 2: n + 4] + data[n: n + 2], 16) / 4.184
        basalmetabolism = round(bm)
    else:
        basalmetabolism = 0
    n = n + 4

    if flags & USERFLAG == USERFLAG:
        userid = int(data[n: n + 1], 16)
    else:
        userid = 0

    return {
        'weight': weight,
        'fat': fat,
        'height': height,
        'basalmetabolism': basalmetabolism,
        'userid': userid
    }


def lambda_handler(event, context):
    if event["devicetype"] == 16:
        output = weight_handler(event["data"])

    print(json.dumps(output))

    return {
        'context': context,
        'statusCode': 200,
        'body': json.dumps(output)
    }


# Press the green button in the gutter to run the script.
print(lambda_handler(ev, ""))
