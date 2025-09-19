from rapidfuzz import fuzz
from rapidfuzz import process

grading = {
    'A': 95,
    'A-': 90, 
    'B+': 85, 
    'B': 80, 
    'B-': 75, 
    'C+': 70, 
    'C': 65,
    'C-': 60, 
    'D+': 55, 
    'D': 50,
    'F': 0
}

def match(assessments, grades):
    choice = [cur_assessment.name for cur_assessment in assessments]
    get_match = []
    for i in range (0, len(grades)):
        best_assessment = (process.extractOne(grades[i].name, choice, scorer=fuzz.token_sort_ratio))[2]
        get_match.append(best_assessment)
    return get_match

def calculate_current(match, assessments, grades):
    assessment_count = [0.0] * len(assessments)
    for i in range (0, len(grades)):
        assessment_count[match[i]] += 1
    
    assessment_grade = [0.0] * len(assessments)
    for i in range(0, len(grades)):
        cur_grade = grades[i]
        index = match[i]
        assessment_grade[index] += float(cur_grade.value) / assessments[index].amount
    for i in range(0, len(assessment_grade)):
        assessment_grade[i] += 100.0 * (assessments[i].amount - assessment_count[i]) / assessments[i].amount
    total_grade = 0.0 
    for i in range(0, len(assessment_grade)):
        #print(assessments[i].name, assessments[i].weight, assessment_grade[i])
        total_grade += assessments[i].weight * assessment_grade[i] / 100
    return total_grade


def calculate_total(match, assessments, grades):
    assessment_grade = [0.0] * len(assessments)
    for i in range(0, len(grades)):
        cur_grade = grades[i]
        index = match[i]
        assessment_grade[index] += float(cur_grade.value) / assessments[index].amount
    total_grade = 0.0
    for i in range(0, len(assessment_grade)):
        total_grade += assessments[i].weight * assessment_grade[i] / 100
    return total_grade

def calculate_weights(match, assessments, grades):
    assessment_count = [0.0] * len(assessments)
    for i in range (0, len(grades)):
        assessment_count[match[i]] += 1
    completed = 0.0
    remaining = 0.0
    for i in range(0, len(assessments)):
        cur_weight = assessments[i].weight * (assessment_count[i] / assessments[i].amount)
        completed += cur_weight
        remaining += assessments[i].weight - cur_weight
    return completed, remaining

def avg_to_get(needed_grade, total_grade, remaining_weight):
    if remaining_weight == 0.0:
        remaining_weight = 1.0
    need_perc = grading[needed_grade]
    if not need_perc:
        return "Invalid grade."
    need_perc -= total_grade
    need_perc /= remaining_weight
    need_perc *= 100
    return need_perc



    