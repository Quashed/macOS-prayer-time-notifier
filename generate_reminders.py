from bs4 import BeautifulSoup

def daily_xml_generator(prayer_times):
    soup = BeautifulSoup("", "xml")
    array = soup.new_tag("array")

    for time in prayer_times.values():
        hour, minutes = time.split(":")

        dict_tag = soup.new_tag("dict")

        key_tag_hour = soup.new_tag("key")
        key_tag_hour.string = "Hour"

        integer_tag_hour = soup.new_tag("integer")
        integer_tag_hour.string = hour

        key_tag_minute = soup.new_tag("key")
        key_tag_minute.string = "Minute"

        integer_tag_minute = soup.new_tag("integer")
        integer_tag_minute.string = minutes

        dict_tag.extend([key_tag_hour, integer_tag_hour, key_tag_minute, integer_tag_minute])

        array.append(dict_tag)

    return array

def write_times_to_file(path, times_xml):
    with open(path, "r") as f:
        data = f.read()
    
    soup = BeautifulSoup(data, "xml")
    key_tag = soup.find("key", string="StartCalendarInterval")
    
    key_tag.insert_after(times_xml)

    with open(path, "w") as f:
        f.write(soup.prettify())

