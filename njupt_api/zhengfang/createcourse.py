import re

from bs4 import BeautifulSoup

from .types import Course


def normalize_course_str(course_str: str) -> str:
    """
    规范化课程字符串，确保 create_course 能正确解析。

    Returns:
        字符串。
    """
    parts = course_str.split("<br>")
    while parts and parts[0] == "":
        parts.pop(0)
    while len(parts) < 4:
        parts.append(" ")
    for i in range(2, 4):
        if parts[i] == "":
            parts[i] = " "
    return "<br>".join(parts)


def create_course_schedule(html: str) -> list[Course]:
    """解析给定 HTML 字符串，返回包含数个 Course 对象的列表。
    Args:
        html: HTML 字符串。应该有且只有一个 <table> 标签，其中是课程表数据。

    Returns:
        list[Course]

    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")

    courses: list[Course] = []
    rowspan_map: dict[int, int] = {}

    # 解析第一行表头，建立列索引到星期几的映射
    # 表头格式：第1列是"时间"(colspan=2)，然后是 星期一 到 星期日
    day_map: dict[int, int] = {}  # col_idx -> day (1-7)
    if rows:
        header_cells = rows[0].find_all(["td", "th"])
        col_idx = 0
        for cell in header_cells:
            text = cell.get_text(strip=True)
            colspan = int(cell.get("colspan", 1))

            # 跳过"时间"单元格
            if text != "时间":
                # 映射星期几到数字
                day_mapping = {
                    "星期一": 1,
                    "星期二": 2,
                    "星期三": 3,
                    "星期四": 4,
                    "星期五": 5,
                    "星期六": 6,
                    "星期日": 7,
                    "星期天": 7,
                }
                day = day_mapping.get(text)
                if day is not None:
                    for c in range(col_idx, col_idx + colspan):
                        day_map[c] = day

            col_idx += colspan

    for row_idx, row in enumerate(rows):
        if row_idx == 0:
            continue

        cells = row.find_all(["td", "th"])
        col_idx = 0
        class_start: int | None = None

        for cell in cells:
            while col_idx in rowspan_map and rowspan_map[col_idx] > 0:
                rowspan_map[col_idx] -= 1
                if rowspan_map[col_idx] == 0:
                    del rowspan_map[col_idx]
                col_idx += 1

            text = cell.get_text(strip=True)
            colspan = int(cell.get("colspan", 1))
            rowspan = int(cell.get("rowspan", 1))

            if text.startswith("第") and text.endswith("节"):
                class_start = int(text[1:-1])
                if rowspan > 1:
                    for c in range(col_idx, col_idx + colspan):
                        rowspan_map[c] = rowspan - 1
                col_idx += colspan
                continue

            if text in ("早晨", "上午", "下午", "晚上"):
                if rowspan > 1:
                    for c in range(col_idx, col_idx + colspan):
                        rowspan_map[c] = rowspan - 1
                col_idx += colspan
                continue

            td_str = str(cell)
            start = td_str.find(">") + 1
            end = td_str.rfind("</td>")
            inner_html = td_str[start:end]

            if "&nbsp;" not in inner_html and inner_html.strip():
                inner_html = re.sub(r"<br\s*/?>", "<br>", inner_html)
                course_strs = [
                    s.strip() for s in re.split(r"(?:<br>){2,}", inner_html) if s.strip() and "&nbsp;" not in s
                ]
                # 获取当前列对应的星期几
                day = day_map.get(col_idx, 1)  # 默认为1（星期一）
                for course_str in course_strs:
                    course_str = normalize_course_str(course_str)
                    courses.append(
                        create_course(
                            course_str,
                            day,
                            default_classes_start=class_start,
                        ),
                    )

            if rowspan > 1:
                for c in range(col_idx, col_idx + colspan):
                    rowspan_map[c] = rowspan - 1

            col_idx += colspan

    return courses


def create_course(
    raw: str,
    day: int,
    default_classes_start: int | None = None,
) -> Course:
    """根据从 HTML 中提取出的原字符串解析课程信息
    Args:
        raw: 原字符串，以 <br> 作为换行符
        day: 周内的星期几
        default_classes_start: 如果没有解析出课程的 classes，则使用此参数。
            此参数应当从表格的行标题解析。

    Returns:
        Course

    """
    #  0                1              2        3         4
    # ['概率论与数理统计', '1-17单(1,2)', '王雪红', '教3-520', '']
    raw_list = raw.split("<br>")

    # 首先去除列表头部的所有空字符串
    while True:
        if raw_list[0] == "":
            raw_list.pop(0)
        else:
            break

    # 对于大部分课程，raw_list[1] 都是形如以下格式
    # 1-17(3,4)
    # 1-17单(1,2)  *（也可能是双）
    # 2节/周
    # 2节/单周  *（也可能是双）
    # 周三第3,4节{第1-17周}
    # 周五第3,4节{第2-16周|双周}
    raw_time = raw_list[1]
    weeks = []
    classes = []
    single = False  # 内部变量
    double = False  # 内部变量
    # 处理前两种形式
    if "-" in raw_time and "第" not in raw_time:
        #                          也可能是 '1-17单'
        t = raw_time.split("(")  # ['1-17', '3-4)']
        #                                     也可能是 '17单'
        start, end = t[0].split("-")  # ['1', '17']
        if end.endswith("单"):
            end = end[:-1]
            single = True
        elif end.endswith("双"):
            end = end[:-1]
            double = True
        for i in range(int(start), int(end) + 1):
            if single and i % 2 == 0:
                continue
            if double and i % 2 == 1:
                continue
            weeks.append(i)
        raw_classes = t[1].removesuffix(")")
        classes = [int(i) for i in raw_classes.split(",")]
    # 处理中两种形式
    elif "/" in raw_time:
        # 默认学期 1-16 周
        if "/单周" in raw_time:
            single = True
        elif "/双周" in raw_time:
            double = True
        for i in range(1, 17):
            if single and i % 2 == 0:
                continue
            if double and i % 2 == 1:
                continue
            weeks.append(i)

        # 获取多少节课
        t_num = int(raw_time.split("节")[0])
        for i in range(0, t_num):
            classes.append(default_classes_start + i)
    # 处理后两种形式
    elif "第" in raw_time:
        # '周三', '3,4节{', '1-17周}'
        # '周五', '3,4节{', '2-16周|双周}'
        u = raw_time.split("第")
        classes = [int(u_c) for u_c in u[1].split("节")[0].split(",")]

        # '1-17', '}'
        # '2-16', '|双', '}'
        u_w = u[2].split("周")
        if "单" in u_w[1]:
            single = True
        elif "双" in u_w[1]:
            double = True
        u_start, u_end = u_w[0].split("-")
        for i in range(int(u_start), int(u_end) + 1):
            if single and i % 2 == 0:
                continue
            if double and i % 2 == 1:
                continue
            weeks.append(i)

    teacher = raw_list[2] if raw_list[2] != " " else None
    classroom = raw_list[3] if raw_list[3] != " " else None

    return Course(raw_list[0], weeks, day, classes, teacher, classroom)


def convert_dict_schedule_to_tuple(schedule: list[dict]) -> list[tuple]:
    """将字典格式的课表转换为压缩的元组格式。

    Args:
        schedule: list[dict]，标准格式的课程数据

    Returns:
        list[tuple]: 压缩后的元组格式 (name, teacher, classroom, weeks_str, day, classes)
                     其中 weeks 尽量压缩为字符串格式（如 "1-17"）

    """
    result = []
    for course in schedule:
        name = course.get("name", "")
        teacher = course.get("teacher")
        classroom = course.get("classroom")
        weeks = course.get("weeks", [])
        day = course.get("day", 1)
        classes = course.get("classes", [])

        # 压缩 weeks 为字符串
        weeks_str = compress_weeks_to_string(weeks) if weeks else ""

        result.append((name, teacher, classroom, weeks_str, day, classes))

    return result


def compress_weeks_to_string(weeks: list[int]) -> str:
    """将周数列表压缩为最短的字符串表示。

    例如：
        [1,2,3,4,5]     -> "1-5"
        [1,3,5,7]       -> "1,3,5,7"
        [1,2,3,5,6,7,8] -> "1-3,5-8"
        [1]             -> "1"

    Args:
        weeks: 周数列表

    Returns:
        str: 压缩后的周数字符串

    """
    if not weeks:
        return ""

    # 去重并排序
    weeks = sorted({int(w) for w in weeks})

    ranges = []
    start = end = weeks[0]

    for w in weeks[1:]:
        if w == end + 1:
            # 连续，扩展当前范围
            end = w
        else:
            # 不连续，保存当前范围，开始新范围
            ranges.append((start, end))
            start = end = w

    # 保存最后一个范围
    ranges.append((start, end))

    # 格式化为字符串
    parts = []
    for start, end in ranges:
        if start == end:
            parts.append(str(start))
        else:
            parts.append(f"{start}-{end}")

    return ",".join(parts)
