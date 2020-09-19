from sNeeds.apps.account.models import JournalReputation, WhichAuthor, RegularLanguageCertificate


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
    if isinstance(certificate, RegularLanguageCertificate):
        print("WOW")


    return 0