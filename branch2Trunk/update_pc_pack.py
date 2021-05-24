import os
os.system('taskkill /f /im %s' % 'xzj.exe')
os.system(r'svn up --accept tc E:\svn\Dev\xzj_win64_dev')