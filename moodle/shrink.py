
#
# There are a lot of backup or same assessments with another time. They haven't graded, so not needed
# So, I should implement function that deletes unnecessary information in assessment links (such as Backup / 9-11am).
# And then delete all duplicates. Because they are all the same assessment, but only one is graded#
def delete_unneccessary(name): 
    if not name:
        return ""
    
    name = name.lower()

    #Delete spaces
    def delete_space(cur_name):
        while cur_name and cur_name[0] == ' ':
            cur_name = cur_name[1:]
        while cur_name and cur_name[-1] == ' ':
            cur_name = cur_name[:-1]
        return cur_name

    name = delete_space(name)

    #Delete "BACKUP", "MAKEUP", "Seminar", "Lockdown"
    name = name.replace("backup", "")
    name = name.replace("makeup", "")
    name = name.replace("seminar", "")
    name = name.replace("lockdown", "")
    
    name = delete_space(name)

    #Delete time

    #Delete day
    days = ["sunday", "monday", "tuesday", "thursday", "wednesday", "friday", "saturday"]
    for day in days:
        name = name.replace(day, "")

    #Be careful with quizz/assessment names that are look like '1.5'
    while ":" in name or "." in name:
        pos = name.rfind(":")
        if pos > 0 and name[pos - 1].isdigit() and pos < len(name) - 2 and name[pos + 2].isdigit():
            name = name[:pos] + name[pos + 1:]
            # if ':'/'.' occurs with 'am'/'pm' then extra 'am'/'pm' will be in the name
            pos1 = name.rfind("am")
            if pos1 == -1: 
                pos1 = name.rfind("pm")
            while name and pos1 < len(name) and name[pos1] == " ":
                name = name[:pos1] + name[pos1 + 1:]
                pos1 -= 1
            pos1 += 1
            if name and pos1 > 0 and name[pos1 - 1].isdigit():
                name = name[:pos1] + name[pos1 + 2:]
            else:
                pos1 = name.rfind("pm")
                if pos1 != -1:
                    pos1 -= 1
                    while name and pos1 < len(name) and name[pos1] == " ":
                        name = name[:pos1] + name[pos1 + 1:]
                        pos1 -= 1
                    pos1 += 1
                    if name and pos1 > 0 and name[pos1 - 1].isdigit():
                        name = name[:pos1] + name[pos1 + 2:]
            # Checked prev comm, now continue
            while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"): 
                name = name[:pos] + name[pos + 1:]
            pos -= 1
            while name and pos and (name[pos].isdigit() or name[pos] == "-"):
                name = name[:pos] + name[pos + 1:]
                pos -= 1
        else:
            pos = name.rfind(".")
            if pos > 0 and name[pos - 1].isdigit() and pos < len(name) - 2 and name[pos + 2].isdigit():
                name = name[:pos] + name[pos + 1:]
                pos1 = name.rfind("am")
                if pos1 == -1: 
                    pos1 = name.rfind("pm")
                while name and pos1 < len(name) and name[pos1] == " ":
                    name = name[:pos1] + name[pos1 + 1:]
                    pos1 -= 1
                pos1 += 1
                if name and pos1 > 0 and name[pos1 - 1].isdigit():
                    name = name[:pos1] + name[pos1 + 2:]
                else:
                    pos1 = name.rfind("pm")
                    if pos1 != -1:
                        pos1 -= 1
                        while name and pos1 < len(name) and name[pos1] == " ":
                            name = name[:pos1] + name[pos1 + 1:]
                            pos1 -= 1
                        pos1 += 1
                        if name and pos1 > 0 and name[pos1 - 1].isdigit():
                            name = name[:pos1] + name[pos1 + 2:]
                # Checked prev comm, now continue
                while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"): 
                   name = name[:pos] + name[pos + 1:]
                pos -= 1
                while name and pos and (name[pos].isdigit() or name[pos] == "-"):
                    name = name[:pos] + name[pos + 1:]
                    pos -= 1
            else: 
                break

    #Be careful with words that contain "am" or "pm"
    while "am" in name or "pm" in name: 
        pos = name.rfind("am")
        if pos == -1: 
            pos = name.rfind("pm")
        pos -= 1
        while name and pos < len(name) and name[pos] == " ":
            name = name[:pos] + name[pos + 1:]
            pos -= 1
        pos += 1
        if name and pos > 0 and name[pos - 1].isdigit():
            name = name[:pos] + name[pos + 2:]
            pos -= 1
            while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"):
                name = name[:pos] + name[pos + 1:]
                pos -= 1
        else: 
            pos = name.rfind("pm")
            if pos == -1:
                break
            pos -= 1
            while name and pos < len(name) and name[pos] == " ":
                name = name[:pos] + name[pos + 1:]
                pos -= 1
            pos += 1
            if name and pos > 0 and name[pos - 1].isdigit():
                name = name[:pos] + name[pos + 2:]
                pos -= 1
                while name and pos < len(name) and (name[pos].isdigit() or name[pos] == "-"):
                    name = name[:pos] + name[pos + 1:]
                    pos -= 1
            else:
                break

    if "(" in name:
        pos = name.rfind("(")
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos < len(name) - 1 and name[pos + 1] == '-':
            name = name[:pos + 1] + name[pos + 2:]
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos < len(name) - 1 and name[pos + 1] == ')':
            name = name[:pos] + name[pos + 2:]

    if "-" in name:
        pos = name.rfind("-")
        while pos < len(name) - 1 and name[pos + 1] == ' ':
            name = name[:pos + 1] + name[pos + 2:]
        if pos == len(name) - 1: 
            name = name[:pos]
    name = delete_space(name)

    while name and (name[-1] == ' ' or name[-1] == ':' or name[-1] == '-'):
        name = name[:-1]
    name = name.title()
    return name