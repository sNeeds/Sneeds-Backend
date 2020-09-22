from sNeeds.apps.account.models import JournalReputation, WhichAuthor, RegularLanguageCertificate, \
    LanguageCertificateType
from sNeeds.apps.estimations import values


def compute_publication_value(publication):
    reputation = publication.journal_reputation
    reputation_value = 0
    if reputation == JournalReputation.ONE_TO_THREE:
        reputation_value = 1
    elif reputation == JournalReputation.FOUR_TO_TEN:
        reputation_value = 0.8
    elif reputation == JournalReputation.ABOVE_TEN:
        reputation_value = 0.6

    which_author = publication.which_author
    which_author_value = 0
    if which_author == WhichAuthor.FIRST:
        which_author_value = 1
    elif which_author == WhichAuthor.SECOND:
        which_author_value = 0.7
    elif which_author == WhichAuthor.THIRD:
        which_author_value = 0.5
    elif which_author == WhichAuthor.FOURTH_OR_MORE:
        which_author_value = 0.1

    value = (reputation_value ** 1.3) * which_author_value

    return value


def compute_language_certificate_value(certificate):
    """
    Returned format: (value number, value string) E.g: (0.9, A)
    """

    value = None
    value_str = None

    if certificate.certificate_type == LanguageCertificateType.TOEFL:
        if certificate.overall < values.TOEFL_D_END:
            value = values.TOEFL_D_VALUE
            value_str = "D"
        elif values.TOEFL_C_START <= certificate.overall < values.TOEFL_C_END:
            value = values.TOEFL_C_VALUE
            value_str = "C"
        elif values.TOEFL_B_START <= certificate.overall < values.TOEFL_B_END:
            value = values.TOEFL_B_VALUE
            value_str = "B"
        elif values.TOEFL_BP_START <= certificate.overall < values.TOEFL_BP_END:
            value = values.TOEFL_BP_VALUE
            value_str = "B+"
        elif values.TOEFL_A_START <= certificate.overall < values.TOEFL_A_END:
            value = values.TOEFL_A_VALUE
            value_str = "A"
        elif values.TOEFL_AP_START <= certificate.overall:
            value = values.TOEFL_AP_VALUE
            value_str = "A+"

    elif certificate.certificate_type == LanguageCertificateType.IELTS_GENERAL or certificate.certificate_type == LanguageCertificateType.IELTS_ACADEMIC:
        if certificate.overall < values.IELTS_D_END:
            value = values.IELTS_D_VALUE
            value_str = "D"
        elif values.IELTS_C_START <= certificate.overall < values.IELTS_C_END:
            value = values.IELTS_C_VALUE
            value_str = "C"
        elif values.IELTS_B_START <= certificate.overall < values.IELTS_B_END:
            value = values.IELTS_B_VALUE
            value_str = "B"
        elif values.IELTS_BP_START <= certificate.overall < values.IELTS_BP_END:
            value = values.IELTS_BP_VALUE
            value_str = "B+"
        elif values.IELTS_A_START <= certificate.overall < values.IELTS_A_END:
            value = values.IELTS_A_VALUE
            value_str = "A"
        elif values.IELTS_AP_START <= certificate.overall:
            value = values.IELTS_AP_VALUE
            value_str = "A+"

    return value, value_str
