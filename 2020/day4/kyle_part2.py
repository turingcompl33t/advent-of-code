# kyle_part2.py
#
# Advent of Code Day 4 Puzzle 2.

from typing import FrozenSet

FILENAME   = "input.txt"
REQ_FIELDS = frozenset(["byr", "iyr", "eyr", "hgt", "hcl", "ecl",  "pid"])

def chunks():
    with open(FILENAME, "r") as f:
        data = f.read()
        chunks = data.split("\n\n")
        for chunk in chunks:
            yield " ".join(chunk.split("\n"))

def keys(chunk: str) -> FrozenSet[str]:
    return frozenset([kv.split(":")[0] for kv in chunk.split()])

def make_map(chunk: str):
    return {kv.split(":")[0]:kv.split(":")[1] for kv in chunk.split()}

def validate_byr(byr: str) -> bool:
    return byr != "" and len(byr) == 4 and int(byr) >= 1920 and int(byr) <= 2002

def validate_iyr(iyr: str) -> bool:
    return iyr != "" and len(iyr) == 4 and int(iyr) >= 2010 and int(iyr) <= 2020

def validate_eyr(eyr: str) -> bool:
    return eyr != "" and len(eyr) == 4 and int(eyr) >= 2020 and int(eyr) <= 2030

def validate_hgt(hgt: str) -> bool:
    if hgt == "":
        return False
    
    try:
        if hgt.endswith("cm"):
            hgt = hgt.strip("cm")
            return int(hgt) >= 150 and int(hgt) <= 193
        elif hgt.endswith("in"):
            hgt = hgt.strip("in")
            return int(hgt) >= 59 and int(hgt) <= 76
        else:
            return False
    except:
        return False

def validate_hcl(hcl: str) -> bool:
    return hcl != "" and len(hcl) == 7 and hcl.startswith("#") and set(hcl[1:]) <= set("0123456789abcdef")

def validate_ecl(ecl: str) -> bool:
    return ecl in set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])

def validate_pid(pid: str) -> bool:
    try:
        p = int(pid)
    except:
        return False
    return len(pid) == 9

VALIDATION = {
    "byr": validate_byr, 
    "iyr": validate_iyr, 
    "eyr": validate_eyr, 
    "hgt": validate_hgt, 
    "hcl": validate_hcl, 
    "ecl": validate_ecl,
    "pid": validate_pid,
    "cid": lambda x: True }

def valid_passport(chunk: str) -> bool:
    return len(keys(chunk).intersection(REQ_FIELDS)) == len(REQ_FIELDS) and\
         all([VALIDATION[k](v) for k, v in make_map(chunk).items()])

def main():
    s = sum([valid_passport(c) for c in chunks()])
    print(f"{s} valid passports")

if __name__ == "__main__":
    main()