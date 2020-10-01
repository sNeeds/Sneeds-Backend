from sNeeds.apps.users.account import models as account_models


def compute_publication_value(publication):
    reputation = publication.journal_reputation
    reputation_value = 0
    if reputation == account_models.JournalReputation.ONE_TO_THREE:
        reputation_value = 1
    elif reputation == account_models.JournalReputation.FOUR_TO_TEN:
        reputation_value = 0.8
    elif reputation == account_models.JournalReputation.ABOVE_TEN:
        reputation_value = 0.6

    which_author = publication.which_author
    which_author_value = 0
    if which_author == account_models.Publication.WhichAuthorChoices.FIRST:
        which_author_value = 1
    elif which_author == account_models.Publication.WhichAuthorChoices.SECOND:
        which_author_value = 0.7
    elif which_author == account_models.Publication.WhichAuthorChoices.THIRD:
        which_author_value = 0.5
    elif which_author == account_models.Publication.WhichAuthorChoices.FOURTH_OR_MORE:
        which_author_value = 0.1

    value = (reputation_value ** 1.3) * which_author_value

    return value

