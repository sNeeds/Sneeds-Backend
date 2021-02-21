from abroadin.apps.data.applydata.comments.education import *

GREAT_UNIVERSITY_RANK = 100
GOOD_UNIVERSITY_RANK = 600
AVERAGE_UNIVERSITY_RANK = 1200
BAD_UNIVERSITY_RANK = 3000


EDUCATION_ATTRS = {
    "master": [
        {
            "start": 100,
            "end": None,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_TOP_100_GPA_ABOVE_18H,
                    "value": 1
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_TOP_100_GPA_ABOVE_18H,
                    "value": 0.9
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_TOP_100_GPA_17_18H,
                    "value": 0.8
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_TOP_100_GPA_16_17,
                    "value": 0.6
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_TOP_100_GPA_15_16,
                    "value": 0.5
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_TOP_100_GPA_14_15,
                    "value": 0.4
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_TOP_100_GPA_BELOW_14,
                    "value": 0.2
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_TOP_100_GPA_BELOW_14,
                    "value": 0.05
                },
            ]
        },
        {
            "start": 300,
            "end": 100,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_100_300_GPA_ABOVE_18H,
                    "value": 0.98
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_100_300_GPA_ABOVE_18H,
                    "value": 0.88
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_100_300_GPA_17_18H,
                    "value": 0.78
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_100_300_GPA_16_17,
                    "value": 0.58
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_100_300_GPA_15_16,
                    "value": 0.48
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_100_300_GPA_14_15,
                    "value": 0.38
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_100_300_GPA_BELOW_14,
                    "value": 0.18
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_100_300_GPA_BELOW_14,
                    "value": 0.03
                },
            ],
        },
        {
            "start": 500,
            "end": 300,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_300_500_GPA_ABOVE_18H,
                    "value": 0.97
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_300_500_GPA_ABOVE_18H,
                    "value": 0.87
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_300_500_GPA_17_18H,
                    "value": 0.76
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_300_500_GPA_16_17,
                    "value": 0.57
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_300_500_GPA_15_16,
                    "value": 0.46
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_300_500_GPA_14_15,
                    "value": 0.35
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_300_500_GPA_BELOW_14,
                    "value": 0.15
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_300_500_GPA_BELOW_14,
                    "value": 0.02
                },
            ],
        },
        {
            "start": 750,
            "end": 500,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_500_750_GPA_ABOVE_18H,
                    "value": 0.95
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_500_750_GPA_ABOVE_18H,
                    "value": 0.83
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_500_750_GPA_17_18H,
                    "value": 0.75
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_500_750_GPA_16_17,
                    "value": 0.55
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_500_750_GPA_15_16,
                    "value": 0.45
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_500_750_GPA_14_15,
                    "value": 0.35
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_500_750_GPA_BELOW_14,
                    "value": 0.14
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_500_750_GPA_BELOW_14,
                    "value": 0.01
                },
            ],
        },
        {
            "start": 1000,
            "end": 750,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_750_1000_GPA_ABOVE_18H,
                    "value": 0.93
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_750_1000_GPA_ABOVE_18H,
                    "value": 0.83
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_750_1000_GPA_17_18H,
                    "value": 0.73
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_750_1000_GPA_16_17,
                    "value": 0.53
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_750_1000_GPA_15_16,
                    "value": 0.43
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_750_1000_GPA_14_15,
                    "value": 0.33
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_750_1000_GPA_BELOW_14,
                    "value": 0.13
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_750_1000_GPA_BELOW_14,
                    "value": 0
                },
            ],
        },
        {
            "start": None,
            "end": 1000,
            "gpa_data": [
                {
                    "start": None,
                    "end": 19.5,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_ABOVE_18H,
                    "value": 0.9
                },
                {
                    "start": 19.5,
                    "end": 18.5,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_ABOVE_18H,
                    "value": 0.8
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_17_18H,
                    "value": 0.7
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_16_17,
                    "value": 0.5
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_15_16,
                    "value": 0.4
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_14_15,
                    "value": 0.25
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_BELOW_14,
                    "value": 0.03
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": MASTER_UNI_ABOVE_1000_GPA_BELOW_14,
                    "value": 0
                },
            ],
        },
    ],
    "bachelor_with_master_short_comment": [
        {
            "start": None,
            "end": 18,
            "comment": MASTER_WITH_BACHELOR_EXCELLENT_GPA
        },
        {
            "start": 18,
            "end": 16,
            "comment": MASTER_WITH_BACHELOR_GOOD_GPA
        },
        {
            "start": 16,
            "end": 14,
            "comment": MASTER_WITH_BACHELOR_MODERATE_GPA
        },
        {
            "start": 14,
            "end": None,
            "comment": MASTER_WITH_BACHELOR_BAD_GPA
        },

    ],
    "bachelor": [
        {
            "start": 100,
            "end": None,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_TOP_100_GPA_ABOVE_18H,
                    "value": 1
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_TOP_100_GPA_17_18H,
                    "value": 0.85
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_TOP_100_GPA_16_17,
                    "value": 0.7
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_TOP_100_GPA_15_16,
                    "value": 0.6
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_TOP_100_GPA_14_15,
                    "value": 0.45
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_TOP_100_GPA_BELOW_14,
                    "value": 0.15
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_TOP_100_GPA_BELOW_14,
                    "value": 0.05
                },
            ],
        },
        {
            "start": 300,
            "end": 100,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_100_300_GPA_ABOVE_18H,
                    "value": 0.98
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_100_300_GPA_17_18H,
                    "value": 0.82
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_100_300_GPA_16_17,
                    "value": 0.67
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_100_300_GPA_15_16,
                    "value": 0.57
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_100_300_GPA_14_15,
                    "value": 0.42
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_100_300_GPA_BELOW_14,
                    "value": 0.13
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_100_300_GPA_BELOW_14,
                    "value": 0.03
                },
            ]
        },
        {
            "start": 500,
            "end": 300,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_300_500_GPA_ABOVE_18H,
                    "value": 0.95
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_300_500_GPA_17_18H,
                    "value": 0.79
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_300_500_GPA_16_17,
                    "value": 0.64
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_300_500_GPA_15_16,
                    "value": 0.54
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_300_500_GPA_14_15,
                    "value": 0.39
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_300_500_GPA_BELOW_14,
                    "value": 0.1
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_300_500_GPA_BELOW_14,
                    "value": 0.02
                },
            ],
        },
        {
            "start": 750,
            "end": 500,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_500_750_GPA_ABOVE_18H,
                    "value": 0.92
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_500_750_GPA_17_18H,
                    "value": 0.75
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_500_750_GPA_16_17,
                    "value": 0.6
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_500_750_GPA_15_16,
                    "value": 0.5
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_500_750_GPA_14_15,
                    "value": 0.33
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_500_750_GPA_BELOW_14,
                    "value": 0.07
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_500_750_GPA_BELOW_14,
                    "value": 0.01
                },
            ],
        },
        {
            "start": 1000,
            "end": 750,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_750_1000_GPA_ABOVE_18H,
                    "value": 0.9
                },

                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_750_1000_GPA_17_18H,
                    "value": 0.7
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_750_1000_GPA_16_17,
                    "value": 0.56
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_750_1000_GPA_15_16,
                    "value": 0.45
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_750_1000_GPA_14_15,
                    "value": 0.29
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_750_1000_GPA_BELOW_14,
                    "value": 0.05
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_750_1000_GPA_BELOW_14,
                    "value": 0
                },
            ],
        },
        {
            "start": None,
            "end": 1000,
            "gpa_data": [
                {
                    "start": None,
                    "end": 18.5,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_ABOVE_18H,
                    "value": 0.87
                },
                {
                    "start": 18.5,
                    "end": 17,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_17_18H,
                    "value": 0.67
                },
                {
                    "start": 17,
                    "end": 16,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_16_17,
                    "value": 0.53
                },
                {
                    "start": 16,
                    "end": 15,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_15_16,
                    "value": 0.42
                },
                {
                    "start": 15,
                    "end": 14,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_14_15,
                    "value": 0.2
                },
                {
                    "start": 14,
                    "end": 12,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_BELOW_14,
                    "value": 0.01
                },
                {
                    "start": 12,
                    "end": None,
                    "comment": BACHELOR_UNI_ABOVE_1000_GPA_BELOW_14,
                    "value": 0
                },
            ],
        },
    ],
    "label": [
        {
            "start": None,
            "end": 0.83,
            "label": "A+"
        },
        {
            "start": 0.83,
            "end": 0.73,
            "label": "A"
        },
        {
            "start": 0.73,
            "end": 0.65,
            "label": "B+"
        },
        {
            "start": 0.65,
            "end": 0.60,
            "label": "B"
        },
        {
            "start": 0.60,
            "end": 0.50,
            "label": "C"
        },
        {
            "start": 0.50,
            "end": None,
            "label": "D"
        },
    ],
}
