from abroadin.apps.estimation.estimations import review_comments

VALUES_WITH_ATTRS = {
    "publication_qs": [
        {
            "start": None,
            "end": 0.95,
            "label": "A+"
        },
        {
            "start": 0.95,
            "end": 0.75,
            "label": "A"
        },
        {
            "start": 0.75,
            "end": 0.6,
            "label": "B+"
        },
        {
            "start": 0.6,
            "end": 0.5,
            "label": "B"
        },
        {
            "start": 0.5,
            "end": 0.4,
            "label": "C+"
        },
        {
            "start": 0.4,
            "end": 0.3,
            "label": "C"
        },
        {
            "start": 0.3,
            "end": None,
            "label": "D"
        }
    ],
    "university_through": [
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
    "toefl": [
        {
            "start": None,
            "end": 110,
            "label": "A+"
        },
        {
            "start": 110,
            "end": 105,
            "label": "A"
        },
        {
            "start": 105,
            "end": 100,
            "label": "B+"
        },
        {
            "start": 100,
            "end": 92,
            "label": "B"
        },
        {
            "start": 92,
            "end": 78,
            "label": "C"
        },
        {
            "start": 78,
            "end": None,
            "label": "D"
        },
    ],
    "ielts_academic_and_general": [
        {
            "start": None,
            "end": 8,
            "label": "A+"
        },
        {
            "start": 8,
            "end": 7.5,
            "label": "A"
        },
        {
            "start": 7.5,
            "end": 7,
            "label": "B+"
        },
        {
            "start": 7,
            "end": 6.5,
            "label": "B"
        },
        {
            "start": 6.5,
            "end": 6,
            "label": "C"
        },
        {
            "start": 6,
            "end": None,
            "label": "D"
        },
    ],
    "ielts_academic_comments": [
        {
            "start": None,
            "end": 7.5,
            "comment": review_comments.IELTS_ACADEMIC_GREAT
        },
        {
            "start": 7.5,
            "end": 7,
            "comment": review_comments.IELTS_ACADEMIC_GOOD
        },
        {
            "start": 7,
            "end": 6.5,
            "comment": review_comments.IELTS_ACADEMIC_AVERAGE
        },
        {
            "start": 6.5,
            "end": 6,
            "comment": review_comments.IELTS_ACADEMIC_BAD
        },
        {
            "start": 6,
            "end": None,
            "comment": review_comments.IELTS_ACADEMIC_VERY_BAD
        },
    ],
    "ielts_general_comments": [  # Customize later
        {
            "start": None,
            "end": 7.5,
            "comment": review_comments.IELTS_ACADEMIC_GREAT
        },
        {
            "start": 7.5,
            "end": 7,
            "comment": review_comments.IELTS_ACADEMIC_GOOD
        },
        {
            "start": 7,
            "end": 6.5,
            "comment": review_comments.IELTS_ACADEMIC_AVERAGE
        },
        {
            "start": 6.5,
            "end": 6,
            "comment": review_comments.IELTS_ACADEMIC_BAD
        },
        {
            "start": 6,
            "end": None,
            "comment": review_comments.IELTS_ACADEMIC_VERY_BAD
        },
    ],
    "toefl_comments": [
        {
            "start": None,
            "end": 110,
            "comment": review_comments.TOEFL_GREAT
        },
        {
            "start": 110,
            "end": 100,
            "comment": review_comments.TOEFL_GOOD
        },
        {
            "start": 100,
            "end": 92,
            "comment": review_comments.TOEFL_AVERAGE
        },
        {
            "start": 92,
            "end": 79,
            "comment": review_comments.TOEFL_BAD
        },
        {
            "start": 79,
            "end": None,
            "comment": review_comments.TOEFL_VERY_BAD
        },
    ],
    "work_experience_comments": [
        {
            "start": None,
            "end": 24,
            "comment": review_comments.LONG_WORK_EXPERIENCE
        },
        {
            "start": 24,
            "end": 12,
            "comment": review_comments.AVERAGE_WORK_EXPERIENCE
        },
        {
            "start": 12,
            "end": None,
            "comment": review_comments.SHORT_WORK_EXPERIENCE
        },
    ],
}

# TOEFL
TOEFL_AP_VALUE = 1
TOEFL_A_VALUE = 0.9
TOEFL_BP_VALUE = 0.8
TOEFL_B_VALUE = 0.7
TOEFL_C_VALUE = 0.3
TOEFL_D_VALUE = 0

# IELTS


IELTS_AP_VALUE = 1
IELTS_A_VALUE = 0.9
IELTS_BP_VALUE = 0.8
IELTS_B_VALUE = 0.7
IELTS_C_VALUE = 0.3
IELTS_D_VALUE = 0

# Universities

GREAT_UNIVERSITY_RANK = 100
GOOD_UNIVERSITY_RANK = 600
AVERAGE_UNIVERSITY_RANK = 1200
BAD_UNIVERSITY_RANK = 3000
