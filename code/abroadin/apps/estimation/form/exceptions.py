from rest_framework.exceptions import APIException


class SDIDefectException(APIException):
    pretty_message = ''
    front_code = 0


class SDIWantToApplyMajorLeakage(SDIDefectException):
    pretty_message = 'Try adding more majors in analysis form’s destinations.'
    front_code = 1


class SDIWantToApplyUniversityLeakage(SDIDefectException):
    pretty_message = 'Try adding more universities in analysis form’s destinations.'
    front_code = 2


class SDIWantToApplyUniversityAndCountryLeakage(SDIDefectException):
    pretty_message = 'Try adding more universities or countries in analysis forms.'
    front_code = 3


class SDIWantToApplyCountryLeakage(SDIDefectException):
    pretty_message = 'Try adding more countries in analysis forms.'
    front_code = 4


class SDIEducationLeakage(SDIDefectException):
    pretty_message = 'Try adding education background in analysis forms.'
    front_code = 5
