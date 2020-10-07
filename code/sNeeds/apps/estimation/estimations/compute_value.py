from sNeeds.apps.estimation.form.models import Publication


def compute_publication_value(publication):
    reputation = publication.journal_reputation
    reputation_value = 0
    if reputation == Publication.JournalReputationChoices.ONE_TO_THREE:
        reputation_value = 1
    elif reputation == Publication.JournalReputationChoices.FOUR_TO_TEN:
        reputation_value = 0.8
    elif reputation == Publication.JournalReputationChoices.ABOVE_TEN:
        reputation_value = 0.6

    which_author = publication.which_author
    which_author_value = 0
    if which_author == Publication.WhichAuthorChoices.FIRST:
        which_author_value = 1
    elif which_author == Publication.WhichAuthorChoices.SECOND:
        which_author_value = 0.7
    elif which_author == Publication.WhichAuthorChoices.THIRD:
        which_author_value = 0.5
    elif which_author == Publication.WhichAuthorChoices.FOURTH_OR_MORE:
        which_author_value = 0.1

    value = (reputation_value ** 1.3) * which_author_value

    return value

