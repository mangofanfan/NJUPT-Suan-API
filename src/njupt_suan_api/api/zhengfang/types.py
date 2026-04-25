from dataclasses import dataclass


@dataclass
class Course:
    """Course 是对课程表中的 **某一节课** 的抽象。

    Examples:
        1-17周，星期一，1-2节，数据结构，是一个 Course 对象；

        1-17周，星期三，3-4节，数据结构，是另一个 Course 对象；

        1-17周中的单周，星期四，3-4节，英语，是一个 Course 对象；

        1-17周中的双周，星期四，3-4节，物理，是另一个 Course 对象。

    """

    name: str
    weeks: list[int]
    day: int
    classes: list[int]
    teacher: str | None
    classroom: str | None


def course_dict_serializer(course: Course) -> dict[str, str | list[int] | int | None]:
    return {
        "name": course.name,
        "weeks": course.weeks,
        "day": course.day,
        "classes": course.classes,
        "teacher": course.teacher,
        "classroom": course.classroom,
    }


def course_list_serializer(course_list: list[Course]) -> list[dict]:
    final_list = []
    for course in course_list:
        final_list.append(course_dict_serializer(course))
    return final_list
