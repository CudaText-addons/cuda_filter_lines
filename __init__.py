import re
from cudatext import *

def do_filter(by_str):
    if by_str:
        msg = 'Filter by string:'
    else:
        msg = 'Filter by reg-ex:'
    
    test = dlg_input_ex(2, 'Filter Lines', msg, '', 'Ignore case, if not empty:', '')
    if test is None: return
    test, nocase = test
    if not test: return
    nocase = bool(nocase)

    res = []
    for i in range(ed.get_line_count()):
        line = ed.get_text_line(i)
        if by_str:
            if nocase:
                ok = test.lower() in line.lower()
            else:
                ok = test in line
        else:
            flags = re.I if nocase else 0
            ok = bool(re.search(test, line, flags=flags))
            
        if ok:
            res.append(line)
    
    if not res:
        msg_status('Cannot find matching lines')
        return
            
    file_open('')
    ed.set_prop(PROP_TAB_TITLE, 'Filter: '+test)
    ed.set_text_all('\n'.join(res))
    msg_status('Found %d matching lines' % len(res))
        

class Command:
    def filter_str(self):
        do_filter(True)
    def filter_regex(self):
        do_filter(False)
    def fold_str(self):
        pass
    def fold_regex(self):
        pass
