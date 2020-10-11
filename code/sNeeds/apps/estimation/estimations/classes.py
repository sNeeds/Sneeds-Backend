class ValueRange:
    available_labels = ["A+", "A", "A-", "B+", "B", "B-", "C+", "C", "D"]

    class Range:
        def __init__(self, start: float, end: float, label, available_labels):
            self._check_valid_label(label, available_labels)
            self.start = start
            self.end = end
            self.label = label

        def _check_valid_label(self, label, available_labels):
            if label not in available_labels:
                raise Exception("Wrong label")

    def __init__(self, ranges_creator):
        self.ranges = []

        for r in ranges_creator:
            new_range = self.Range(
                start=r.get("start"),
                end=r.get("end"),
                label=r.get("label"),
                available_labels=self.available_labels
            )
            self.ranges.append(new_range)

    def find_value_label(self, value):
        for r in self.ranges:
            if r.end is None:
                if r.start <= value:
                    return r.label
            elif r.start is None:
                if value < r.end:
                    return r.label
            else:
                if r.start <= value < r.end:
                    return r.label

        raise Exception("No label for value={} found".format(value))
