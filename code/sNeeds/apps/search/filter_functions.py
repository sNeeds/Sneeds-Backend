
def filter_consultants(qs, university, country, major):

    # print("555555555")

    if university != [] or country != [] or major != []:
        # print("66666666")
        qs_for_university = qs.none()
        qs_for_country = qs.none()
        qs_for_major = qs.none()

        if university is not None:
            qs_for_university = qs.filter_consultants({"universities": university})

        if country is not None:
            qs_for_country = qs.filter_consultants({"countries": country})

        if major is not None:
            qs_for_major = qs.filter_consultants({"field_of_studies": major})

        result_qs = qs_for_university | qs_for_country | qs_for_major
        result_qs = result_qs.distinct()

        return result_qs

    # print("77777777777")

    return qs
