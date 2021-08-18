import json

# DeviceType
DEVICE_TYPE_SENSOR = 0x00
DEVICE_TYPE_MOTION = 0x02
DEVICE_TYPE_WEIGHT = 0x10
DEVICE_TYPE_BLOOD_PRESSURE = 0x11
DEVICE_TYPE_HEALTH_THERMOMETER = 0x12

# Sensor Constant
TEMPERATURE_FLAG = 0x01
HUMIDITY_FLAG = 0x02
BRIGHTNESS_FLAG = 0x04
MOTION_FLAG = 0x08

# Weight Constant
FAT_FLAG = 0x01
HEIGHT_FLAG = 0x02
METABOLISM_FLAG = 0x04
WEIGHT_USER_FLAG = 0x08

# Blood Pressure Constant
BLOOD_PRESSURE_USER_FLAG = 0x01

# Health Thermometer Constant
HEALTH_THERMOMETER_USER_FLAG = 0x01


def str_to_xbyte(data, n, byte):
    """ 16進文字列を整数に変換する

    :param data: 16進テキスト文字列
    :type data: string
    :param n: スタートバイト位置
    :type n: int
    :param byte: 読み取るバイト数
    :type byte: int
    :return: 読み取り値
    :rtype: int
    """
    b = ""
    for i in range(n, n + byte):
        b = data[i * 2:i * 2 + 2] + b
    return int(b, 16)


def sensor_handler(data):
    """　sensorパケットをjsonに変換する

    :param data: 16進テキスト文字列
    :type data: string
    :return: jsonテキスト
    :rtype: string
    """
    n = 1
    flags = str_to_xbyte(data, n, 1)
    n = n + 1

    if flags & TEMPERATURE_FLAG == TEMPERATURE_FLAG:
        temperature = (str_to_xbyte(data, n, 2) - 200) / 8.0
        temperature = round(temperature, 1)
    else:
        temperature = 0
    n = n + 2

    if flags & HUMIDITY_FLAG == HUMIDITY_FLAG:
        humidity = str_to_xbyte(data, n, 1) / 2.0
        humidity = round(humidity, 1)
    else:
        humidity = 0
    n = n + 1

    if flags & BRIGHTNESS_FLAG == BRIGHTNESS_FLAG:
        brightness = str_to_xbyte(data, n, 2) * 100 / 96.0
        brightness = round(brightness, 1)
    else:
        brightness = 0
    n = n + 2

    if flags & MOTION_FLAG == MOTION_FLAG:
        motion = str_to_xbyte(data, n, 1)
        motion = motion | 0x7f
    else:
        motion = 0

    return {
        'flags': flags,
        'temperature': temperature,
        'humidity': humidity,
        'brightness': brightness,
        'motion': motion,
    }


def motion_handler(data):
    """　motionパケットをjsonに変換する

    :param data: 16進テキスト文字列
    :type data: string
    :return: jsonテキスト
    :rtype: string
    """
    n = 1
    flags = str_to_xbyte(data, n, 1)
    n = n + 6
    motion = str_to_xbyte(data, n, 1)

    return {
        'flags': flags,
        'motion': motion,
    }


def weight_handler(data):
    """　weightパケットをjsonに変換する

    :param data: 16進テキスト文字列
    :type data: string
    :return: jsonテキスト
    :rtype: string
    """
    n = 1
    flags = str_to_xbyte(data, n, 1)
    n = n + 1

    weight = str_to_xbyte(data, n, 2) * 0.005
    weight = round(weight, 2)
    n = n + 2

    if flags & FAT_FLAG == FAT_FLAG:
        fat = str_to_xbyte(data, n, 2) * 0.1
        fat = round(fat, 1)
    else:
        fat = 0
    n = n + 2

    if flags & HEIGHT_FLAG == HEIGHT_FLAG:
        height = str_to_xbyte(data, n, 2)
    else:
        height = 0
    n = n + 2

    if flags & METABOLISM_FLAG == METABOLISM_FLAG:
        bm = str_to_xbyte(data, n, 2) / 4.184
        basalmetabolism = round(bm)
    else:
        basalmetabolism = 0
    n = n + 2

    if flags & WEIGHT_USER_FLAG == WEIGHT_USER_FLAG:
        userid = str_to_xbyte(data, n, 1)
    else:
        userid = 0

    return {
        'flags': flags,
        'weight': weight,
        'fat': fat,
        'height': height,
        'basalmetabolism': basalmetabolism,
        'userid': userid
    }


def blood_pressure_handler(data):
    """　 blood_pressureパケットをjsonに変換する

    :param data: 16進テキスト文字列
    :type data: string
    :return: jsonテキスト
    :rtype: string
    """
    n = 1
    flags = str_to_xbyte(data, n, 1)
    n = n + 1

    systolic = str_to_xbyte(data, n, 2) * 0.1
    systolic = round(systolic, 1)
    n = n + 2

    diastolic = str_to_xbyte(data, n, 2) * 0.1
    diastolic = round(diastolic, 1)
    n = n + 2

    mean = str_to_xbyte(data, n, 2) * 0.1
    mean = round(mean, 1)
    n = n + 2

    pulserate = str_to_xbyte(data, n, 2) * 0.1
    pulserate = round(pulserate, 1)
    n = n + 2

    if flags & BLOOD_PRESSURE_USER_FLAG == BLOOD_PRESSURE_USER_FLAG:
        userid = str_to_xbyte(data, n, 1)
    else:
        userid = 0

    return {
        'flags': flags,
        'systolic': systolic,
        'diastolic': diastolic,
        'mean': mean,
        'pulserate': pulserate,
        'userid': userid,
    }


def health_thermometer_handler(data):
    """　 health_thermometerパケットをjsonに変換する

    :param data: 16進テキスト文字列
    :type data: string
    :return: jsonテキスト
    :rtype: string
    """
    n = 1
    flags = str_to_xbyte(data, n, 1)
    n = n + 1

    body_temperature = str_to_xbyte(data, n, 2) * 0.01
    body_temperature = round(body_temperature, 2)
    n = n + 2

    if flags & HEALTH_THERMOMETER_USER_FLAG == HEALTH_THERMOMETER_USER_FLAG:
        userid = str_to_xbyte(data, n, 1)
    else:
        userid = 0

    return {
        'body_temperature': body_temperature,
        'userid': userid,
    }


def lambda_handler(event, context):
    if event["devicetype"] == DEVICE_TYPE_SENSOR:
        output = sensor_handler(event["data"])

    elif event["devicetype"] == DEVICE_TYPE_MOTION:
        output = motion_handler(event["data"])

    elif event["devicetype"] == DEVICE_TYPE_WEIGHT:
        output = weight_handler(event["data"])

    elif event["devicetype"] == DEVICE_TYPE_BLOOD_PRESSURE:
        output = blood_pressure_handler(event["data"])

    elif event["devicetype"] == DEVICE_TYPE_HEALTH_THERMOMETER:
        output = health_thermometer_handler(event["data"])

    else:
        output = {}

    # print(json.dumps(output))

    output.update(event)

    return {
        # 'context': context,
        'statusCode': 200,
        'body': json.dumps(output)
    }

