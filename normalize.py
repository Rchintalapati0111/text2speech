# normalize.py
import re
from num2words import num2words

ABBREV = {
    # general latinisms / refs
    "e.g.": "for example", "E.g.": "for example",
    "i.e.": "that is",     "I.e.": "that is",
    "etc.": "etcetera",    "Etc.": "etcetera",
    "vs.": "versus",       "Vs.": "versus",
    "cf.": "compare",      "Cf.": "compare",
    "viz.": "namely",      "Viz.": "namely",
    "approx.": "approximately", "Approx.": "approximately",
    "ca.": "approximately",     "Ca.": "approximately",
    "et al.": "and others",     "Et al.": "and others",

    # titles
    "Mr.": "Mister",
    "Mrs.": "Missus",
    "Ms.": "Ms",          # keep neutral (pronounced “miz” by most TTS)
    "Dr.": "Doctor",
    "Prof.": "Professor",
    "Sr.": "Senior",
    "Jr.": "Junior",

    # business/org
    "Inc.": "Incorporated",
    "Ltd.": "Limited",
    "Co.": "Company",
    "Corp.": "Corporation",
    "Univ.": "University",
    "Dept.": "Department",
    "No.": "Number", "no.": "number",
    "Fig.": "Figure", "fig.": "figure",

    # time
    "a.m.": "a m",
    "p.m.": "p m",

    # countries
    "U.S.": "United States",
    "U.K.": "United Kingdom",
    "USA": "United States",
    "UK": "United Kingdom",

    # weekdays
    "Mon.": "Monday",
    "Tue.": "Tuesday", "Tues.": "Tuesday",
    "Wed.": "Wednesday",
    "Thu.": "Thursday", "Thur.": "Thursday", "Thurs.": "Thursday",
    "Fri.": "Friday",
    "Sat.": "Saturday",
    "Sun.": "Sunday",

    # months
    "Jan.": "January",
    "Feb.": "February",
    "Mar.": "March",
    "Apr.": "April",
    "Jun.": "June",
    "Jul.": "July",
    "Aug.": "August",
    "Sep.": "September", "Sept.": "September",
    "Oct.": "October",
    "Nov.": "November",
    "Dec.": "December",
}

def normalize_text(text: str) -> str:
    t = text
    # abbreviation expansion (simple pass; safe because keys include punctuation/periods)
    for k, v in ABBREV.items():
        t = t.replace(k, v)
    # numbers → words (keep simple)
    t = re.sub(r"\b(\d{1,6})\b", lambda m: num2words(int(m.group(1))), t)
    # collapse spaces
    t = re.sub(r"\s+", " ", t).strip()
    return t
