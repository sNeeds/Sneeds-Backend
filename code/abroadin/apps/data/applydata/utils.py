from random import randint, choices


def convert_pbt_overall_to_ibt_overall(pbt_score):
    pbt_score = int(pbt_score)
    dic = {
        677: 120,
        673: 120,
        670: 119,
        667: 118,
        662: 117,
        657: 116,
        650: 114,
        653: 115,
        647: 113,
        643: 112,
        640: 111,
        637: 110,
        632: 109,
        627: 108,
        625: 107,
        623: 106,
        618: 105,
        613: 104,
        610: 102,
        607: 101,
        602: 100,
        597: 99,
        # 597: 98,
        593: 97,
        590: 96,
        587: 95,
        # 587: 94,
        583: 93,
        580: 92,
        577: 91,
        # 577: 90,
        573: 89,
        570: 88,
        567: 87,
        # 567: 86,
        563: 85,
        # 563: 84,
        558: 83,
        553: 82,
        533: 81,
        550: 80,
        # 550: 79,
        547: 78,
        # 547: 77,
        542: 76,
        537: 75,
        # 537: 74,
    }
    found = False
    i = 0
    j = -1
    lookup = pbt_score
    ibt_score = 0

    while not found and i < 10:
        lookup = lookup + (i * j)
        ibt_score = dic.get(lookup, None)
        found = ibt_score is not None
        i += 1
        j *= -1

    if not found:
        raise Exception("pbt score is out of bound. {}".format(pbt_score))
    return ibt_score


def get_toefl_fake_sub_scores_based_on_overall(toefl_score):
    base_sub_score = int(toefl_score/4)

    writing_tolerance = randint(-6, 3)
    writing = int(base_sub_score * (100 + writing_tolerance) / 100)

    reading_tolerance = randint(-2, 5)
    reading = int(base_sub_score * (100 + reading_tolerance) / 100)

    speaking_tolerance = randint(-4, 4)
    speaking = int(base_sub_score * (100 + speaking_tolerance) / 100)

    listening = int(toefl_score - (writing + reading + speaking))

    return writing, reading, speaking, listening


def get_ielts_fake_sub_scores_based_on_overall(ielts_score):
    ielts_score = float(ielts_score)

    tolerance = [-1, -0.5, 0, 0.5, 1]

    writing = ielts_score + choices(tolerance, [1, 4, 2, 2, 1], k=1)[0]
    reading = ielts_score + choices(tolerance, [1, 2, 2, 3, 1], k=1)[0]
    speaking = ielts_score + choices(tolerance, [1, 3, 3, 1, 1], k=1)[0]
    listening = ielts_score * 4 - (writing + reading + speaking)

    return writing, reading, speaking, listening
