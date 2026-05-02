def analyze_grades(grades=[85, 90, 78, 92, 88]):
    result = {
        "average": sum(grades) / len(grades),
        "highest": max(grades),
        "lowest": min(grades)
    }
    return result

print(analyze_grades())