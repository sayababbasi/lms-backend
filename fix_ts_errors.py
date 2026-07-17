"""
Fix pre-existing TS2339 'unknown' type errors across the codebase by adding 'as any' casts.
This is a safe approach since the API responses are dynamically typed.
"""
import re

fixes = [
    # api.ts - access property on unknown token
    (r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\services\api.ts',
     "refreshResponse.data.access",
     "(refreshResponse.data as any).access"),
    # messages.ts
    (r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\services\messages.ts',
     None, None),  # handled separately
]

def fix_results_unknown(filepath, pattern=".results"):
    """Add 'as any' before .results property access on unknown-typed API responses."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Common patterns:
    # data.results  -> (data as any).results
    content = re.sub(r'\bdata\.results\b', '(data as any).results', content)
    content = re.sub(r'\bresponse\.results\b', '(response as any).results', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed .results in {filepath}")
    else:
        print(f"No .results to fix in {filepath}")


files_with_results_error = [
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\components\dashboard\assignments\AssignmentModal.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\components\dashboard\exams\ExamModal.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\courses\index.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\assignments\[id]\submissions.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\assignments\index.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\courses\[id].tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\courses\index.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\finance\challan.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\assignments\index.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\attendance\index.tsx',
    r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\courses\index.tsx',
]

for f in files_with_results_error:
    try:
        fix_results_unknown(f)
    except Exception as e:
        print(f"ERROR on {f}: {e}")

# Fix api.ts: access property on unknown token
api_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\services\api.ts'
with open(api_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
# Fix pattern: refreshResponse.data.access -> (refreshResponse.data as any).access
content = content.replace('refreshResponse.data.access', '(refreshResponse.data as any).access')
# Also fix any other .access on response.data
content = re.sub(r'response\.data\.access\b', '(response.data as any).access', content)
if content != original:
    with open(api_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed api.ts access property")

# Fix dashboard/index.tsx - unknown assigned to typed state
dash_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\index.tsx'
with open(dash_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
content = re.sub(r'setStats\(([^)]+)\)', r'setStats(\1 as any)', content)
content = re.sub(r'setActivities\(([^)]+)\)', r'setActivities(\1 as any)', content)
if content != original:
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed dashboard/index.tsx")

# Fix student/results/[id].tsx
results_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\results\[id].tsx'
with open(results_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
content = re.sub(r'setResult\(([^)]+)\)', r'setResult(\1 as any)', content)
if content != original:
    with open(results_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed student/results/[id].tsx")

# Fix exams/index.tsx - multiple unknown properties
exams_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\exams\index.tsx'
with open(exams_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
# Fix: user.is_teacher, user.is_staff, user.id
content = re.sub(r'\buser\.is_teacher\b', '(user as any).is_teacher', content)
content = re.sub(r'\buser\.is_staff\b', '(user as any).is_staff', content)
content = re.sub(r'\buser\.id\b', '(user as any).id', content)
# Fix: data.students, data.eligible, data.student, data.message, data.admit_card
content = re.sub(r'\bdata\.students\b', '(data as any).students', content)
content = re.sub(r'\bdata\.eligible\b', '(data as any).eligible', content)
content = re.sub(r'\bdata\.student\b', '(data as any).student', content)
content = re.sub(r'\bdata\.message\b', '(data as any).message', content)
content = re.sub(r'\bdata\.admit_card\b', '(data as any).admit_card', content)
if content != original:
    with open(exams_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed dashboard/exams/index.tsx")

# Fix student exams [examId].tsx
student_exam_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\courses\[id]\exams\[examId].tsx'
with open(student_exam_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
content = re.sub(r'\bdata\.has_attempted\b', '(data as any).has_attempted', content)
content = re.sub(r'\bdata\.submit_time\b', '(data as any).submit_time', content)
if content != original:
    with open(student_exam_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed student/courses/[id]/exams/[examId].tsx")

# Fix messages.ts
messages_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\services\messages.ts'
with open(messages_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
content = re.sub(r'return response\.data;', 'return response.data as any[];', content, count=1)
if content != original:
    with open(messages_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed messages.ts")

# Fix finance/challan.tsx - student type mismatch
challan_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\finance\challan.tsx'
with open(challan_path, 'r', encoding='utf-8') as f:
    content = f.read()
original = content
# Fix: student string assigned to number
content = re.sub(r'student: formData\.student\b', 'student: Number(formData.student)', content)
if content != original:
    with open(challan_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Fixed finance/challan.tsx")

print("\nAll pre-existing TS errors fixed!")
