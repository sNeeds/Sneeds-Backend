from abroadin.apps.estimation.estimations import review_comments

# language certificate values
LANGUAGE_AP_VALUE = 1
LANGUAGE_A_VALUE = 0.9
LANGUAGE_B_VALUE = 0.6
LANGUAGE_C_VALUE = 0.3
LANGUAGE_D_VALUE = 0

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
            "value": LANGUAGE_AP_VALUE,
            "label": "A+",
            "comment": review_comments.TOEFL_GREAT
        },
        {
            "start": 110,
            "end": 100,
            "value": LANGUAGE_A_VALUE,
            "label": "A",
            "comment": review_comments.TOEFL_GOOD
        },
        {
            "start": 100,
            "end": 92,
            "value": LANGUAGE_B_VALUE,
            "label": "B",
            "comment": review_comments.TOEFL_AVERAGE
        },
        {
            "start": 92,
            "end": 79,
            "value": LANGUAGE_C_VALUE,
            "label": "C",
            "comment": review_comments.TOEFL_BAD
        },
        {
            "start": 79,
            "end": None,
            "value": LANGUAGE_D_VALUE,
            "label": "D",
            "comment": review_comments.TOEFL_VERY_BAD
        },
    ],
    "ielts_academic_and_general": [
        {
            "start": None,
            "end": 7.5,
            "value": LANGUAGE_AP_VALUE,
            "label": "A+",
            "comment": review_comments.IELTS_ACADEMIC_GREAT
        },
        {
            "start": 7.5,
            "end": 7,
            "value": LANGUAGE_A_VALUE,
            "label": "A",
            "comment": review_comments.IELTS_ACADEMIC_GOOD
        },
        {
            "start": 7,
            "end": 6.5,
            "value": LANGUAGE_B_VALUE,
            "label": "B",
            "comment": review_comments.IELTS_ACADEMIC_AVERAGE
        },
        {
            "start": 6.5,
            "end": 6,
            "value": LANGUAGE_C_VALUE,
            "label": "C",
            "comment": review_comments.IELTS_ACADEMIC_BAD
        },
        {
            "start": 6,
            "end": None,
            "value": LANGUAGE_D_VALUE,
            "label": "D",
            "comment": review_comments.IELTS_ACADEMIC_VERY_BAD
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
    "1_20_university_rank_admission_chance": [
        {
            "start": None,
            "end": 4 / 5,
            "admission": 0.8,
            "scholarship": 0.6,
            "full_fund": 0.5
        },
        {
            "start": 4 / 5,
            "end": 3 / 5,
            "admission": 0.5,
            "scholarship": 0.2,
            "full_fund": 0.1
        },
        {
            "start": 3 / 5,
            "end": 2 / 5,
            "admission": 0.3,
            "scholarship": 0,
            "full_fund": 0
        },
        {
            "start": 2 / 5,
            "end": None,
            "admission": 0,
            "scholarship": 0,
            "full_fund": 0
        },
    ],
    "21_100_university_rank_admission_chance": [
        {
            "start": None,
            "end": 4 / 5,
            "admission": 1,
            "scholarship": 0.95,
            "full_fund": 0.85
        },
        {
            "start": 4 / 5,
            "end": 3 / 5,
            "admission": 0.7,
            "scholarship": 0.6,
            "full_fund": 0.55
        },
        {
            "start": 3 / 5,
            "end": 2 / 5,
            "admission": 0.5,
            "scholarship": 0.2,
            "full_fund": 0.15
        },
        {
            "start": 2 / 5,
            "end": None,
            "admission": 0.35,
            "scholarship": 0,
            "full_fund": 0
        },
    ],
    "101_400_university_rank_admission_chance": [
        {
            "start": None,
            "end": 4 / 5,
            "admission": 1,
            "scholarship": 1,
            "full_fund": 1
        },
        {
            "start": 4 / 5,
            "end": 3 / 5,
            "admission": 1,
            "scholarship": 0.8,
            "full_fund": 0.7
        },
        {
            "start": 3 / 5,
            "end": 2 / 5,
            "admission": 0.6,
            "scholarship": 0.3,
            "full_fund": 0.2
        },
        {
            "start": 2 / 5,
            "end": None,
            "admission": 0.4,
            "scholarship": 0,
            "full_fund": 0
        },
    ],
    "401_above_university_rank_admission_chance": [
        {
            "start": None,
            "end": 4 / 5,
            "admission": 1,
            "scholarship": 1,
            "full_fund": 1
        },
        {
            "start": 4 / 5,
            "end": 3 / 5,
            "admission": 1,
            "scholarship": 1,
            "full_fund": 1
        },
        {
            "start": 3 / 5,
            "end": 2 / 5,
            "admission": 0.9,
            "scholarship": 0.5,
            "full_fund": 0.4
        },
        {
            "start": 2 / 5,
            "end": None,
            "admission": 0.6,
            "scholarship": 0.2,
            "full_fund": 0.1
        },
    ],
    "admission_chance_value_to_label": [
        {
            "start": None,
            "end": 0.7,
            "label": "High"
        },
        {
            "start": 0.7,
            "end": 0.4,
            "label": "Medium"
        },
        {
            "start": 0.4,
            "end": None,
            "label": "Low"
        },
    ],
}

# Universities

GREAT_UNIVERSITY_RANK = 100
GOOD_UNIVERSITY_RANK = 600
AVERAGE_UNIVERSITY_RANK = 1200
BAD_UNIVERSITY_RANK = 3000
