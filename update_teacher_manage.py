import os

teacher_manage_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'
admin_manage_path = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\courses\[id]\manage.tsx'

with open(admin_manage_path, 'r', encoding='utf-8') as f:
    admin_lines = f.readlines()

# Extract Curriculum JSX
start_jsx_idx = -1
end_jsx_idx = -1
for i, line in enumerate(admin_lines):
    if '5. CURRICULUM TAB' in line:
        start_jsx_idx = i
    if '6. OTHER TABS' in line:
        end_jsx_idx = i
        break
curriculum_jsx = ''.join(admin_lines[start_jsx_idx:end_jsx_idx])

# Extract Curriculum Logic (Methods)
start_logic_idx = -1
end_logic_idx = -1
for i, line in enumerate(admin_lines):
    if 'const handleCreateModule = async () => {' in line:
        start_logic_idx = i
    if 'const handleFormSubmit' in line:
        end_logic_idx = i
        break
curriculum_logic = ''.join(admin_lines[start_logic_idx:end_logic_idx])

# States to add
states = '''    // Curriculum State
    const [isAddingModule, setIsAddingModule] = useState(false);
    const [newModuleTitle, setNewModuleTitle] = useState("");
    const [addingLessonToModule, setAddingLessonToModule] = useState<number | null>(null);
    const [newLessonTitle, setNewLessonTitle] = useState("");
    const [uploadingLessonId, setUploadingLessonId] = useState<number | null>(null);
    const [uploadingResourceId, setUploadingResourceId] = useState<number | null>(null);
'''

with open(teacher_manage_path, 'r', encoding='utf-8') as f:
    teacher_content = f.read()

# 1. Update Tab type
teacher_content = teacher_content.replace(
    "type Tab = 'overview' | 'assignments' | 'exams' | 'attendance' | 'results' | 'resources';",
    "type Tab = 'overview' | 'curriculum' | 'assignments' | 'exams' | 'attendance' | 'results' | 'resources';"
)

# 2. Add States
teacher_content = teacher_content.replace(
    "    const [videoDesc, setVideoDesc] = useState('');",
    "    const [videoDesc, setVideoDesc] = useState('');\n\n" + states
)

# 3. Modify loadCourseData
teacher_content = teacher_content.replace(
    '''    const loadCourseData = async () => {
        setLoading(true);
        try {
            if (activeTab === 'overview') {
                const data = await CoursesService.getById(Number(id));
                setCourse(data);''',
    '''    const loadCourseData = async () => {
        setLoading(true);
        try {
            const data = await CoursesService.getById(Number(id));
            setCourse(data);
            
            if (activeTab === 'overview') {'''
)

# 4. Add Methods
teacher_content = teacher_content.replace(
    '''        } finally {
            setLoading(false);
        }
    };

    // --- ATTENDANCE LOGIC ---''',
    '''        } finally {
            setLoading(false);
        }
    };

''' + curriculum_logic + '''
    // --- ATTENDANCE LOGIC ---'''
)

# 5. Update Tabs Map
teacher_content = teacher_content.replace(
    "{['overview', 'attendance', 'assignments', 'exams', 'resources', 'results'].map((t) => (",
    "{['overview', 'curriculum', 'attendance', 'assignments', 'exams', 'resources', 'results'].map((t) => ("
)

# 6. Add Curriculum JSX
teacher_content = teacher_content.replace(
    '''                    {/* OVERVIEW */}''',
    curriculum_jsx + '''
                    {/* OVERVIEW */}'''
)

with open(teacher_manage_path, 'w', encoding='utf-8') as f:
    f.write(teacher_content)

print("Teacher manage.tsx updated!")
