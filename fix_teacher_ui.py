import re

filepath = r'd:\Business\Revotic AI Pvt Ltd\Development\Under Developing\Revotic AI Development\UniversityLMS\UniversityLMS\Development\university-lms\frontend\src\pages\teacher\dashboard\courses\[id]\manage.tsx'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Module Header
old_module_header = r'''                                    <div className="bg-dark-surface px-6 py-4 border-b border-dark-border flex justify-between items-center">
                                        <h4 className="font-bold text-dark-text text-lg">Module \{index \+ 1\}: \{module\.title\}</h4>
                                        <button onClick=\{\(\) => setAddingLessonToModule\(module\.id\)\} className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 flex items-center gap-1">
                                            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth=\{2\} d="M12 4v16m8-8H4" /></svg> Add Lesson
                                        </button>
                                    </div>'''

new_module_header = '''                                    <div className="bg-dark-surface px-6 py-4 border-b border-dark-border flex justify-between items-center">
                                        {editingModuleId === module.id ? (
                                            <div className="flex items-center gap-2 flex-1 mr-3">
                                                <input
                                                    type="text"
                                                    value={editModuleTitle}
                                                    onChange={e => setEditModuleTitle(e.target.value)}
                                                    onKeyDown={e => { if (e.key === 'Enter') handleUpdateModuleTitle(module.id); if (e.key === 'Escape') setEditingModuleId(null); }}
                                                    className="flex-1 bg-white dark:bg-dark-bg border border-primary-500/50 rounded-lg px-3 py-1.5 text-slate-800 dark:text-dark-text text-sm focus:outline-none focus:border-primary-500 focus:ring-1 focus:ring-primary-500"
                                                    autoFocus
                                                />
                                                <button onClick={() => handleUpdateModuleTitle(module.id)} disabled={saving} className="px-3 py-1.5 bg-primary-600 text-white text-sm font-medium rounded-lg hover:bg-primary-500 transition-colors shadow-sm">Save</button>
                                                <button onClick={() => setEditingModuleId(null)} className="px-3 py-1.5 border border-slate-300 dark:border-dark-border text-slate-600 hover:bg-slate-50 dark:text-slate-400 dark:hover:bg-white/5 text-sm font-medium rounded-lg transition-colors">Cancel</button>
                                            </div>
                                        ) : (
                                            <h4 className="font-bold text-slate-800 dark:text-dark-text text-lg">Module {index + 1}: {module.title}</h4>
                                        )}
                                        <div className="flex items-center gap-2">
                                            <button
                                                onClick={() => { setEditingModuleId(module.id); setEditModuleTitle(module.title); }}
                                                title="Rename module"
                                                className="p-2 text-slate-400 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-500/10 rounded-lg transition-all"
                                            >
                                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                                            </button>
                                            <button onClick={() => setAddingLessonToModule(module.id)} className="text-sm text-primary-600 dark:text-primary-400 hover:text-primary-700 dark:hover:text-primary-300 flex items-center gap-1 font-medium bg-primary-50 hover:bg-primary-100 dark:bg-primary-900/20 dark:hover:bg-primary-900/40 px-3 py-1.5 rounded-lg transition-all">
                                                <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m8-8H4" /></svg> Add Lesson
                                            </button>
                                            <button
                                                onClick={() => handleDeleteModule(module.id)}
                                                disabled={deletingModuleId === module.id}
                                                title="Delete module"
                                                className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-lg transition-all"
                                            >
                                                {deletingModuleId === module.id
                                                    ? <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg>
                                                    : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>
                                                }
                                            </button>
                                        </div>
                                    </div>'''

content = re.sub(old_module_header, new_module_header, content)


# 2. Lesson Header
old_lesson_header = r'''                                            <div key=\{lesson\.id\} className="bg-dark-bg border border-dark-border p-4 rounded-lg flex flex-col md:flex-row gap-4 justify-between group">
                                                <div className="flex-1">
                                                    <h5 className="font-medium text-slate-800 dark:text-slate-200">Lecture \{lIndex \+ 1\}: \{lesson\.title\}</h5>'''

new_lesson_header = '''                                            <div key={lesson.id} className="bg-white dark:bg-dark-bg border border-slate-200 dark:border-dark-border p-5 rounded-xl flex flex-col gap-4 group">
                                                <div className="flex justify-between items-start w-full">
                                                    {editingLessonId === lesson.id ? (
                                                        <div className="flex items-center gap-2 flex-1 max-w-lg mr-4">
                                                            <input
                                                                type="text"
                                                                value={editLessonTitle}
                                                                onChange={e => setEditLessonTitle(e.target.value)}
                                                                onKeyDown={e => { if (e.key === 'Enter') handleUpdateLessonTitle(lesson.id); if (e.key === 'Escape') setEditingLessonId(null); }}
                                                                className="flex-1 bg-white dark:bg-dark-surface border border-primary-500/50 rounded-lg px-3 py-1.5 text-slate-800 dark:text-dark-text text-sm focus:outline-none focus:border-primary-500"
                                                                autoFocus
                                                            />
                                                            <button onClick={() => handleUpdateLessonTitle(lesson.id)} disabled={saving} className="px-3 py-1.5 bg-primary-600 text-white text-xs font-medium rounded-lg shadow-sm hover:bg-primary-500 transition-colors">Save</button>
                                                            <button onClick={() => setEditingLessonId(null)} className="px-3 py-1.5 border border-slate-200 dark:border-dark-border text-slate-600 hover:bg-slate-50 dark:text-slate-400 dark:hover:bg-white/5 text-xs font-medium rounded-lg transition-colors">Cancel</button>
                                                        </div>
                                                    ) : (
                                                        <div className="flex items-center gap-3">
                                                            <h5 className="font-medium text-slate-800 dark:text-slate-200 text-base">Lecture {lIndex + 1}: {lesson.title}</h5>
                                                            <button onClick={() => { setEditingLessonId(lesson.id); setEditLessonTitle(lesson.title); }} title="Rename lesson" className="p-1.5 text-slate-400 hover:text-primary-600 hover:bg-primary-50 dark:hover:bg-primary-500/10 rounded-md transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100">
                                                                <svg className="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" /></svg>
                                                            </button>
                                                        </div>
                                                    )}
                                                    
                                                    <button onClick={() => handleDeleteLesson(lesson.id)} disabled={deletingLessonId === lesson.id} title="Delete lesson" className="p-1.5 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded-md transition-colors opacity-0 group-hover:opacity-100 focus:opacity-100">
                                                        {deletingLessonId === lesson.id ? <svg className="animate-spin w-4 h-4" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path></svg> : <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" /></svg>}
                                                    </button>
                                                </div>
                                                <div className="flex-1">'''

content = re.sub(old_lesson_header, new_lesson_header, content)

# 3. Video Header
old_video = r'''                                                    \{lesson\.youtube_video_id && \(
                                                        <div className="mt-3 relative w-full rounded-lg overflow-hidden border border-dark-border aspect-video bg-black flex items-center justify-center">
                                                            <iframe width="100%" height="100%" src=\{`https://www\.youtube\.com/embed/\$\{lesson\.youtube_video_id\}\?modestbranding=1&rel=0`\} title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
                                                        </div>
                                                    \)\}'''

new_video = '''                                                    {lesson.youtube_video_id && (
                                                        <div className="mt-3 relative w-full rounded-xl overflow-hidden border border-slate-200 dark:border-dark-border aspect-video bg-black shadow-sm group/video">
                                                            <iframe width="100%" height="100%" src={`https://www.youtube.com/embed/${lesson.youtube_video_id}?modestbranding=1&rel=0`} title="YouTube video player" frameBorder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowFullScreen></iframe>
                                                            <div className="absolute top-3 right-3 opacity-0 group-hover/video:opacity-100 transition-opacity">
                                                                <button
                                                                    onClick={() => handleDeleteVideo(lesson.id)}
                                                                    disabled={deletingVideoId === lesson.id}
                                                                    className="flex items-center gap-1.5 px-3 py-1.5 bg-red-600/95 hover:bg-red-500 text-white text-sm rounded-lg font-medium backdrop-blur-sm shadow-xl border border-red-500/50 transition-colors"
                                                                >
                                                                    {deletingVideoId === lesson.id ? 'Removing...' : '✕ Remove Video'}
                                                                </button>
                                                            </div>
                                                        </div>
                                                    )}'''

content = re.sub(old_video, new_video, content)

# 4. Resources
old_resource = r'''                                                    \{\/\* Resources List \/\*\}
                                                    \{lesson\.resources && lesson\.resources\.length > 0 && \(
                                                        <div className="mt-3 flex flex-wrap gap-2">
                                                            \{lesson\.resources\.map\(\(res: any\) => \(
                                                                <div key=\{res\.id\} className="flex items-center gap-2 bg-dark-surface border border-dark-border px-3 py-1\.5 rounded-lg text-sm text-slate-700 dark:text-slate-300">
                                                                    <svg className="w-4 h-4 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth=\{2\} d="M15\.172 7l-6\.586 6\.586a2 2 0 102\.828 2\.828l6\.414-6\.586a4 4 0 00-5\.656-5\.656l-6\.415 6\.585a6 6 0 108\.486 8\.486L20\.5 13" \/><\/svg>
                                                                    <a href=\{res\.file\} target="_blank" rel="noreferrer" className="hover:text-primary-600 dark:hover:text-primary-400 truncate max-w-\[200px\]">\{res\.title\}<\/a>
                                                                <\/div>
                                                            \)\)\}
                                                        <\/div>
                                                    \)\}'''

new_resource = '''                                                    {/* Resources List */}
                                                    {lesson.resources && lesson.resources.length > 0 && (
                                                        <div className="mt-4 flex flex-wrap gap-2">
                                                            {lesson.resources.map((res: any) => (
                                                                <div key={res.id} className="group/res flex items-center gap-2 bg-slate-50 hover:bg-slate-100 dark:bg-dark-surface dark:hover:bg-white/5 border border-slate-200 dark:border-dark-border px-3 py-1.5 rounded-lg text-sm text-slate-700 dark:text-slate-300 transition-colors shadow-sm">
                                                                    <svg className="w-4 h-4 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" /></svg>
                                                                    <a href={res.file} target="_blank" rel="noreferrer" className="hover:text-primary-600 dark:hover:text-primary-400 truncate max-w-[200px] font-medium">{res.title}</a>
                                                                    <button
                                                                        onClick={() => handleDeleteResource(res.id)}
                                                                        disabled={deletingResourceId === res.id}
                                                                        title="Delete this file"
                                                                        className="p-1 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-500/10 rounded opacity-0 group-hover/res:opacity-100 transition-all ml-1"
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

content = re.sub(old_resource, new_resource, content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Teacher dashboard UI correctly updated with CRUD buttons")
