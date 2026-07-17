"""
Adds CRUD (delete module, delete lesson, delete video, delete resource, edit titles) 
to the Curriculum tab in admin manage.tsx
"""

admin_file = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\dashboard\courses\[id]\manage.tsx'

with open(admin_file, 'r', encoding='utf-8') as f:
    content = f.read()

# ---- 1. Add CRUD state variables after curriculum state ----
OLD_STATES = '''    const [uploadingLessonId, setUploadingLessonId] = useState<number | null>(null);
    const [uploadingResourceId, setUploadingResourceId] = useState<number | null>(null);'''

NEW_STATES = '''    const [uploadingLessonId, setUploadingLessonId] = useState<number | null>(null);
    const [uploadingResourceId, setUploadingResourceId] = useState<number | null>(null);
    const [deletingLessonId, setDeletingLessonId] = useState<number | null>(null);
    const [deletingModuleId, setDeletingModuleId] = useState<number | null>(null);
    const [deletingVideoId, setDeletingVideoId] = useState<number | null>(null);
    const [deletingResourceId, setDeletingResourceId] = useState<number | null>(null);
    const [editingModuleId, setEditingModuleId] = useState<number | null>(null);
    const [editModuleTitle, setEditModuleTitle] = useState('');
    const [editingLessonId, setEditingLessonId] = useState<number | null>(null);
    const [editLessonTitle, setEditLessonTitle] = useState('');'''

content = content.replace(OLD_STATES, NEW_STATES)

# ---- 2. Add CRUD handler methods after handleVideoUpload ----
OLD_HANDLERS_END = '''    useEffect(() => {
        if (id) {
            fetchData();
        }
    }, [id]);'''

NEW_HANDLERS = '''    const handleDeleteVideo = async (lessonId: number) => {
        if (!confirm('Remove this video? You can upload a new one after.')) return;
        setDeletingVideoId(lessonId);
        try {
            await CoursesService.deleteVideo(lessonId);
            toast.success('Video removed. Upload a new one now.');
            fetchData();
        } catch {
            toast.error('Failed to remove video');
        } finally {
            setDeletingVideoId(null);
        }
    };

    const handleDeleteResource = async (resourceId: number) => {
        if (!confirm('Delete this resource file?')) return;
        setDeletingResourceId(resourceId);
        try {
            await CoursesService.deleteResource(resourceId);
            toast.success('Resource deleted');
            fetchData();
        } catch {
            toast.error('Failed to delete resource');
        } finally {
            setDeletingResourceId(null);
        }
    };

    const handleDeleteLesson = async (lessonId: number) => {
        if (!confirm('Delete this lesson and all its content?')) return;
        setDeletingLessonId(lessonId);
        try {
            await CoursesService.deleteLesson(lessonId);
            toast.success('Lesson deleted');
            fetchData();
        } catch {
            toast.error('Failed to delete lesson');
        } finally {
            setDeletingLessonId(null);
        }
    };

    const handleDeleteModule = async (moduleId: number) => {
        if (!confirm('Delete this module and ALL its lessons? This cannot be undone.')) return;
        setDeletingModuleId(moduleId);
        try {
            await CoursesService.deleteModule(moduleId);
            toast.success('Module deleted');
            fetchData();
        } catch {
            toast.error('Failed to delete module');
        } finally {
            setDeletingModuleId(null);
        }
    };

    const handleUpdateModuleTitle = async (moduleId: number) => {
        if (!editModuleTitle.trim()) return;
        setSaving(true);
        try {
            await CoursesService.updateModule(moduleId, { title: editModuleTitle });
            toast.success('Module renamed');
            setEditingModuleId(null);
            fetchData();
        } catch {
            toast.error('Failed to rename module');
        } finally {
            setSaving(false);
        }
    };

    const handleUpdateLessonTitle = async (lessonId: number) => {
        if (!editLessonTitle.trim()) return;
        setSaving(true);
        try {
            await CoursesService.updateLessonTitle(lessonId, editLessonTitle);
            toast.success('Lesson renamed');
            setEditingLessonId(null);
            fetchData();
        } catch {
            toast.error('Failed to rename lesson');
        } finally {
            setSaving(false);
        }
    };

    useEffect(() => {
        if (id) {
            fetchData();
        }
    }, [id]);'''

content = content.replace(OLD_HANDLERS_END, NEW_HANDLERS)

# ---- 3. Replace old curriculum JSX module header (add edit/delete buttons) ----
OLD_MODULE_HEADER = '''                            <div key={module.id} className="bg-dark-surface border border-dark-border rounded-xl overflow-hidden">
                                <div className="flex items-center justify-between p-4 bg-dark-card border-b border-dark-border">
                                    <h3 className="font-bold text-dark-text">{module.title}</h3>
                                    <button
                                        onClick={() => setAddingLessonToModule(module.id)}
                                        className="text-xs px-3 py-1.5 bg-primary-600/10 text-primary-400 hover:bg-primary-600/20 rounded-lg border border-primary-500/20 font-medium transition-all"
                                    >
                                        + Add Lesson
                                    </button>
                                </div>'''

NEW_MODULE_HEADER = '''                            <div key={module.id} className="bg-dark-surface border border-dark-border rounded-xl overflow-hidden">
                                <div className="flex items-center justify-between p-4 bg-dark-card border-b border-dark-border">
                                    {editingModuleId === module.id ? (
                                        <div className="flex items-center gap-2 flex-1 mr-3">
                                            <input
                                                type="text"
                                                value={editModuleTitle}
                                                onChange={e => setEditModuleTitle(e.target.value)}
                                                onKeyDown={e => { if (e.key === 'Enter') handleUpdateModuleTitle(module.id); if (e.key === 'Escape') setEditingModuleId(null); }}
                                                className="flex-1 bg-dark-bg border border-primary-500/50 rounded px-3 py-1 text-dark-text text-sm focus:outline-none"
                                                autoFocus
                                            />
                                            <button onClick={() => handleUpdateModuleTitle(module.id)} disabled={saving} className="px-2 py-1 bg-primary-600 text-white text-xs rounded">Save</button>
                                            <button onClick={() => setEditingModuleId(null)} className="px-2 py-1 border border-dark-border text-slate-400 text-xs rounded">Cancel</button>
                                        </div>
                                    ) : (
                                        <h3 className="font-bold text-dark-text">{module.title}</h3>
                                    )}
                                    <div className="flex items-center gap-2">
                                        <button
                                            onClick={() => { setEditingModuleId(module.id); setEditModuleTitle(module.title); }}
                                            title="Rename module"
                                            className="p-1.5 text-slate-500 hover:text-primary-400 hover:bg-primary-500/10 rounded transition-colors"
                                        >
                                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                                        </button>
                                        <button
                                            onClick={() => setAddingLessonToModule(module.id)}
                                            className="text-xs px-3 py-1.5 bg-primary-600/10 text-primary-400 hover:bg-primary-600/20 rounded-lg border border-primary-500/20 font-medium transition-all"
                                        >
                                            + Add Lesson
                                        </button>
                                        <button
                                            onClick={() => handleDeleteModule(module.id)}
                                            disabled={deletingModuleId === module.id}
                                            title="Delete module"
                                            className="p-1.5 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded transition-colors"
                                        >
                                            {deletingModuleId === module.id
                                                ? <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                                                : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                            }
                                        </button>
                                    </div>
                                </div>'''

content = content.replace(OLD_MODULE_HEADER, NEW_MODULE_HEADER)

# ---- 4. Replace lesson header to add edit/delete ----
OLD_LESSON_HEADER = '''                                            {module.lessons?.map((lesson: any) => (
                                            <div key={lesson.id} className="border-b border-dark-border/50 last:border-b-0">
                                                <div className="flex items-start gap-3 p-4">
                                                    <div className="w-7 h-7 rounded-full bg-dark-bg border border-dark-border flex items-center justify-center text-xs text-slate-500 flex-shrink-0 mt-0.5">
                                                        {lesson.order}
                                                    </div>
                                                    <div className="flex-1">
                                                        <p className="font-medium text-slate-800 dark:text-slate-200">{lesson.title}</p>'''

NEW_LESSON_HEADER = '''                                            {module.lessons?.map((lesson: any) => (
                                            <div key={lesson.id} className="border-b border-dark-border/50 last:border-b-0">
                                                <div className="flex items-start gap-3 p-4">
                                                    <div className="w-7 h-7 rounded-full bg-dark-bg border border-dark-border flex items-center justify-center text-xs text-slate-500 flex-shrink-0 mt-0.5">
                                                        {lesson.order}
                                                    </div>
                                                    <div className="flex-1">
                                                        {editingLessonId === lesson.id ? (
                                                            <div className="flex items-center gap-2 mb-2">
                                                                <input
                                                                    type="text"
                                                                    value={editLessonTitle}
                                                                    onChange={e => setEditLessonTitle(e.target.value)}
                                                                    onKeyDown={e => { if (e.key === 'Enter') handleUpdateLessonTitle(lesson.id); if (e.key === 'Escape') setEditingLessonId(null); }}
                                                                    className="flex-1 bg-dark-bg border border-primary-500/50 rounded px-2 py-1 text-dark-text text-sm focus:outline-none"
                                                                    autoFocus
                                                                />
                                                                <button onClick={() => handleUpdateLessonTitle(lesson.id)} disabled={saving} className="px-2 py-1 bg-primary-600 text-white text-xs rounded">Save</button>
                                                                <button onClick={() => setEditingLessonId(null)} className="px-2 py-1 border border-dark-border text-slate-400 text-xs rounded">Cancel</button>
                                                            </div>
                                                        ) : (
                                                            <div className="flex items-center gap-2 mb-1">
                                                                <p className="font-medium text-slate-800 dark:text-slate-200">{lesson.title}</p>
                                                                <button onClick={() => { setEditingLessonId(lesson.id); setEditLessonTitle(lesson.title); }} title="Rename" className="p-1 text-slate-400 hover:text-primary-400 rounded"><svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg></button>
                                                                <button onClick={() => handleDeleteLesson(lesson.id)} disabled={deletingLessonId === lesson.id} title="Delete lesson" className="p-1 text-slate-400 hover:text-red-400 rounded ml-auto">{deletingLessonId === lesson.id ? <svg className="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg> : <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>}</button>
                                                            </div>
                                                        )}
                                                        <p className="font-medium text-slate-800 dark:text-slate-200 hidden">placeholder</p>'''

content = content.replace(OLD_LESSON_HEADER, NEW_LESSON_HEADER)

# ---- 5. Add delete button next to existing video + "Replace Video" option ----
OLD_VIDEO_SECTION = '''                                                        {lesson.youtube_video_id && (
                                                            <div className="mt-3 rounded-lg overflow-hidden border border-dark-border bg-black aspect-video relative">
                                                                <iframe
                                                                    src={`https://www.youtube.com/embed/${lesson.youtube_video_id}?modestbranding=1&rel=0&origin=${typeof window !== 'undefined' ? window.location.origin : ''}`}
                                                                    className="w-full h-full"
                                                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                                                    allowFullScreen
                                                                    title={lesson.title}
                                                                />
                                                            </div>
                                                        )}'''

NEW_VIDEO_SECTION = '''                                                        {lesson.youtube_video_id && (
                                                            <div className="mt-3 rounded-lg overflow-hidden border border-dark-border bg-black aspect-video relative group/video">
                                                                <iframe
                                                                    src={`https://www.youtube.com/embed/${lesson.youtube_video_id}?modestbranding=1&rel=0&origin=${typeof window !== 'undefined' ? window.location.origin : ''}`}
                                                                    className="w-full h-full"
                                                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                                                                    allowFullScreen
                                                                    title={lesson.title}
                                                                />
                                                                <div className="absolute top-2 right-2 opacity-0 group-hover/video:opacity-100 transition-opacity">
                                                                    <button
                                                                        onClick={() => handleDeleteVideo(lesson.id)}
                                                                        disabled={deletingVideoId === lesson.id}
                                                                        className="flex items-center gap-1 px-2 py-1 bg-red-600/90 hover:bg-red-500 text-white text-xs rounded font-medium backdrop-blur-sm shadow-lg"
                                                                    >
                                                                        {deletingVideoId === lesson.id ? 'Removing...' : '✕ Remove Video'}
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        )}'''

content = content.replace(OLD_VIDEO_SECTION, NEW_VIDEO_SECTION)

# ---- 6. Add delete button to each resource ----
OLD_RESOURCE = '''                                                        {lesson.resources && lesson.resources.length > 0 && (
                                                            <div className="mt-3 space-y-1">
                                                                {lesson.resources.map((res: any) => (
                                                                    <a
                                                                        key={res.id}
                                                                        href={res.file || res.external_url}
                                                                        target="_blank"
                                                                        rel="noreferrer"
                                                                        className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 py-1 px-2 rounded hover:bg-blue-500/10 transition-colors"
                                                                    >
                                                                        <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>
                                                                        {res.title}
                                                                    </a>
                                                                ))}
                                                            </div>
                                                        )}'''

NEW_RESOURCE = '''                                                        {lesson.resources && lesson.resources.length > 0 && (
                                                            <div className="mt-3 space-y-1">
                                                                {lesson.resources.map((res: any) => (
                                                                    <div key={res.id} className="flex items-center gap-2 group/res">
                                                                        <a
                                                                            href={res.file || res.external_url}
                                                                            target="_blank"
                                                                            rel="noreferrer"
                                                                            className="flex items-center gap-2 text-sm text-blue-400 hover:text-blue-300 py-1 px-2 rounded hover:bg-blue-500/10 transition-colors flex-1 min-w-0"
                                                                        >
                                                                            <svg className="w-4 h-4 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>
                                                                            <span className="truncate">{res.title}</span>
                                                                        </a>
                                                                        <button
                                                                            onClick={() => handleDeleteResource(res.id)}
                                                                            disabled={deletingResourceId === res.id}
                                                                            title="Delete this file"
                                                                            className="p-1 text-slate-500 hover:text-red-400 hover:bg-red-500/10 rounded opacity-0 group-hover/res:opacity-100 transition-all flex-shrink-0"
                                                                        >
                                                                            {deletingResourceId === res.id
                                                                                ? <svg className="animate-spin w-3.5 h-3.5" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                                                                                : <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                                                            }
                                                                        </button>
                                                                    </div>
                                                                ))}
                                                            </div>
                                                        )}'''

content = content.replace(OLD_RESOURCE, NEW_RESOURCE)

with open(admin_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Admin manage.tsx updated with CRUD!")
