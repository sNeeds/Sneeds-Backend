import copy


class ValueRange:
    class Range:
        def __init__(self, start: float, end: float, **kwargs):
            self.start = start
            self.end = end
            for k, w in kwargs.items():
                setattr(self, k, w)

    def __init__(self, ranges_creator):
        ranges_creator = copy.deepcopy(ranges_creator)  # Dict is mutable
        self.ranges = []

        for r in ranges_creator:
            new_range = self.Range(
                start=r.pop("start"),
                end=r.pop("end"),
                **r
            )
            self.ranges.append(new_range)

    def find_value_attrs(self, value, attr: str):
        for r in self.ranges:
            print(value , r.start, r.end)
            if r.start is None and r.end <= value:
                return getattr(r, attr)
            elif r.end is None and value < r.start:
                return getattr(r, attr)
            elif r.start and r.end and r.start <= value < r.end:
                return getattr(r, attr)

        raise Exception("No label for value={} found".format(value))
