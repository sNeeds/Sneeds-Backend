from abroadin.apps.data.applydata.comments.language import *

# language certificate values
LANGUAGE_AP_VALUE = 1
LANGUAGE_A_VALUE = 0.9
LANGUAGE_AM_VALUE = 0.7
LANGUAGE_BP_VALUE = 0.5
LANGUAGE_B_VALUE = 0.4
LANGUAGE_BM_VALUE = 0.2
LANGUAGE_C_VALUE = 0.05
LANGUAGE_D_VALUE = 0

LANGUAGE_ATTRS = {
    "toefl": [
        {
            "start": None,
            "end": 110,
            "value": LANGUAGE_AP_VALUE,
            "label": "A+",
            "comment": TOEFL_ABOVE_110
        },
        {
            "start": 110,
            "end": 105,
            "value": LANGUAGE_A_VALUE,
            "label": "A",
            "comment": TOEFL_105_109
        },
        {
            "start": 105,
            "end": 100,
            "value": LANGUAGE_AM_VALUE,
            "label": "A-",
            "comment": TOEFL_100_104
        },
        {
            "start": 100,
            "end": 95,
            "value": LANGUAGE_BP_VALUE,
            "label": "B+",
            "comment": TOEFL_95_99
        },
        {
            "start": 95,
            "end": 90,
            "value": LANGUAGE_B_VALUE,
            "label": "B",
            "comment": TOEFL_90_94
        },
        {
            "start": 90,
            "end": 85,
            "value": LANGUAGE_BM_VALUE,
            "label": "B-",
            "comment": TOEFL_85_89
        },
        {
            "start": 85,
            "end": 79,
            "value": LANGUAGE_C_VALUE,
            "label": "C",
            "comment": TOEFL_79_84
        },
        {
            "start": 79,
            "end": None,
            "value": LANGUAGE_D_VALUE,
            "label": "D",
            "comment": TOEFL_BELOW_79
        },
    ],
    "ielts_academic_and_general": [
        {
            "start": None,
            "end": 8.5,
            "value": LANGUAGE_AP_VALUE,
            "label": "A++",
            "comment": IELTS_ACADEMIC_ABOVE_8H
        },

        {
            "start": 8.5,
            "end": 8,
            "value": LANGUAGE_A_VALUE,
            "label": "A+",
            "comment": IELTS_ACADEMIC_8
        },
        {
            "start": 8,
            "end": 7.5,
            "value": LANGUAGE_AM_VALUE,
            "label": "A",
            "comment": IELTS_ACADEMIC_7H
        },
        {
            "start": 7.5,
            "end": 7,
            "value": LANGUAGE_BP_VALUE,
            "label": "A-",
            "comment": IELTS_ACADEMIC_7
        },
        {
            "start": 7,
            "end": 6.5,
            "value": LANGUAGE_B_VALUE,
            "label": "B+",
            "comment": IELTS_ACADEMIC_6H
        },
        {
            "start": 6.5,
            "end": 6,
            "value": LANGUAGE_BM_VALUE,
            "label": "B",
            "comment": IELTS_ACADEMIC_6
        },
        {
            "start": 6,
            "end": 5.5,
            "value": LANGUAGE_C_VALUE,
            "label": "C",
            "comment": IELTS_ACADEMIC_5H
        },
        {
            "start": 5.5,
            "end": None,
            "value": LANGUAGE_D_VALUE,
            "label": "D",
            "comment": IELTS_ACADEMIC_BELOW_5H
        },
    ],
}
