from rest_framework.exceptions import APIException


class SDIDefectException(APIException):
    pretty_message = ''
    front_code = 0


class SDIWantToApplyMajorLeakage(SDIDefectException):
    pretty_message = ''
    front_code = 1


class SDIWantToApplyUniversityLeakage(SDIDefectException):
    pretty_message = ''
    front_code = 2


class SDIWantToApplyUniversityAndCountryLeakage(SDIDefectException):
    pretty_message = ''
    front_code = 3


class SDIWantToApplyCountryLeakage(SDIDefectException):
    pretty_message = ''
    front_code = 4


class SDIEducationLeakage(SDIDefectException):
    pretty_message = ''
    front_code = 5


# class