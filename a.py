from datetime import datetime

class DateConverter:
    def __init__(self, start):
        self.start = start

    def __format__(self, format_spec):
        if format_spec == "converter":
            return datetime.strptime(self.start, "%Y-%m-%d").strftime("%b %Y")

start = "2020-05-05"
stringer = '{start:date} -'
print(stringer.format(format_date=DateConverter,start=start))