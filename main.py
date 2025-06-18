from pypdf import PdfReader
from datetime import datetime
import json
import re

reader = PdfReader("London Unified Prayer Timetable.pdf")
YEAR = reader.pages[0].extract_text().split("\n")[0].split(" ")[1]

def convert_to_24_hour(time):
    time_12hr = time.split(":")
    return f"{int(time_12hr[0]) + 12}:{time_12hr[1]}"

def convert_zuhr(time):
    if int(time.split(":")[0]) == 1:
        return convert_to_24_hour(time)
    return time

data = {}

for page in reader.pages:
    lines = page.extract_text().split("\n")
    page_month = lines[0].split(" ")[0].strip()
    pattern = re.compile(r"^(Mon|Tue|Wed|Thu|Fri|Sat|Sun) 1")

    for i in range(len(lines)):
        if pattern.match(lines[i].strip()):
            lines = lines[i:]
            break
        
    for line in lines:
        temp = line.strip().split(" ")
        month = datetime.strptime(page_month, "%B").month

        if temp == ['']: 
            break

        # YYYY-MM-DD
        date = f"{YEAR}-{month}-{temp[1]}"
        data[date] = {
            "fajr": f"0{temp[2]}",
            "sunrise": f"0{temp[4]}",
            "zuhr": convert_zuhr(temp[5]),
            "asr": convert_to_24_hour(temp[7]),
            "maghrib": convert_to_24_hour(temp[10]),
            "isha": convert_to_24_hour(temp[12])
        }

        if int(temp[1]) == 31:
            break

with open(f"{YEAR}-prayer-times.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)
