import datetime
import enum


class GranularityEnum(enum.Enum):
    """
    Enum for describing granularity.
    """
    DAY = datetime.timedelta(days=1)
    TWELVE_HOURS = datetime.timedelta(hours=12)
    HOUR = datetime.timedelta(hours=1)
    THIRTY_MIN = datetime.timedelta(minutes=30)
    FIVE_MIN = datetime.timedelta(minutes=5)


def truncate_to_granularity(dt: datetime.datetime, gtd: GranularityEnum) -> datetime.datetime:
    """
    Truncate a datetime object to the specified granularity.

    :param dt: datetime to truncate
    :param gtd: granularity
    :return: resulted datetime
    """
    if gtd == GranularityEnum.DAY:
        return dt.replace(hour=0, minute=0, second=0, microsecond=0)
    elif gtd == GranularityEnum.TWELVE_HOURS:
        return dt.replace(hour=(dt.hour // 12) * 12, minute=0, second=0, microsecond=0)
    elif gtd == GranularityEnum.HOUR:
        return dt.replace(minute=0, second=0, microsecond=0)
    elif gtd == GranularityEnum.THIRTY_MIN:
        return dt.replace(minute=(dt.minute // 30) * 30, second=0, microsecond=0)
    elif gtd == GranularityEnum.FIVE_MIN:
        return dt.replace(minute=(dt.minute // 5) * 5, second=0, microsecond=0)
    else:
        raise ValueError("Unsupported granularity")


class DtRange:
    def __init__(self, before: int, after: int, shift: int, gtd: GranularityEnum) -> None:
        """
        Initialize the datetime range parameters.

        :param before: number of datetimes should take before `given datetime`
        :param after: number of datetimes should take after `given datetime`
        :param shift: shift of `given datetime`
        :param gtd: granularity
        """
        self._before = before
        self._after = after
        self._shift = shift
        self._gtd = gtd

    def __call__(self, dt: datetime.datetime) -> list[datetime.datetime]:
        """
        Generate a list of datetimes within the specified range.

        :param dt: given datetime
        :return: list of datetimes in range
        """
        truncated_dt = truncate_to_granularity(dt, self._gtd)
        shifted_dt = truncated_dt + (self._shift * self._gtd.value)
        return [shifted_dt + (i * self._gtd.value) for i in range(-self._before, self._after + 1)]


def get_interval(start_time: datetime.datetime, end_time: datetime.datetime, gtd: GranularityEnum) -> list[
    datetime.datetime]:
    """
    Get a list of datetimes according to the specified granularity within an interval.

    :param start_time: start of interval
    :param end_time: end of interval
    :param gtd: granularity
    :return: list of datetimes according to granularity
    """
    trc_start_time = truncate_to_granularity(start_time, gtd)
    datetimes = []
    current_time = trc_start_time

    while current_time < start_time:
        current_time += gtd.value

    while current_time <= end_time:
        datetimes.append(current_time)
        current_time += gtd.value

    return datetimes
