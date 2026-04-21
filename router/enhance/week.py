"""学期-星期计算"""

from datetime import date, timedelta


def get_semester_week_info(start: date, target: date) -> tuple[int, int]:
    """
    给定学期开始日期（第一周周一）和另一指定日期，计算指定的日期是第几周的星期几。
    Args:
        start: 学期开始的日期，date
        target: 指定日期，date

    Returns:
        包含两个数字的元组，分别为第几周和星期几。
    """
    return (target - start).days // 7 + 1, target.isoweekday()


def get_week_day_info(target: date) -> tuple[date, date]:
    """
    给定一个指定日期，获取该日所在的星期的周一和周日的日期。
    Args:
        target: 指定日期，date

    Returns:
        包含两个 date 的元组，分别为周一和周日。
    """
    weekday_int = target.weekday()
    return target - timedelta(days=weekday_int), target + timedelta(days=6 - weekday_int)
