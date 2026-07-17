import re

def fix_file(filepath, replacements):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for old, new in replacements:
        content = content.replace(old, new)
        # Also try regex if it's a regex pattern
        if old.startswith('r:'):
            content = re.sub(old[2:], new, content)
            
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed {filepath}")
    else:
        print(f"No changes made to {filepath}")

# 1. dashboard/exams/index.tsx
fix_file(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\exams\index.tsx', [
    ('user.is_teacher', '(user as any).is_teacher'),
    ('user.is_staff', '(user as any).is_staff'),
    ('user.id', '(user as any).id'),
    ('data.students', '(data as any).students'),
    ('data.eligible', '(data as any).eligible'),
    ('data.student', '(data as any).student'),
    ('data.message', '(data as any).message'),
    ('data.admit_card', '(data as any).admit_card')
])

# 2. finance/challan.tsx
fix_file(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\finance\challan.tsx', [
    ('amount: formData.amount,', 'amount: Number(formData.amount),')
])

# 3. dashboard/index.tsx
fix_file(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\index.tsx', [
    ('r:setActivities\(([^)]+)\)', r'setActivities(\1 as any)')
])

# 4. student/courses/[id]/exams/[examId].tsx
fix_file(r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\student\courses\[id]\exams\[examId].tsx', [
    ('data.has_attempted', '(data as any).has_attempted'),
    ('data.submit_time', '(data as any).submit_time')
])

print("Done fixing remaining TS errors.")
