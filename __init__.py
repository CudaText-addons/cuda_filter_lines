import re
from cudatext import *


def do_dialog(text, b_re, b_nocase):
    RES_TEXT = 1
    RES_REGEX = 2
    RES_NOCASE = 3
    RES_OK = 4
    c1 = chr(1)
    s_re = '1' if b_re else '0'
    s_i = '1' if b_nocase else '0'
    res = dlg_custom('Filter Lines', 406, 140, 
      '\n'.join([]
         +[c1.join(['type=label', 'pos=6,5,400,0', 'cap=&Text:'])]
         +[c1.join(['type=edit', 'pos=6,23,400,0', 'val='+text])]
         +[c1.join(['type=check', 'pos=6,51,400,0', 'cap=&Reg-ex', 'val='+s_re])]
         +[c1.join(['type=check', 'pos=6,76,400,0', 'cap=&Ignore case', 'val='+s_i])]
         +[c1.join(['type=button', 'pos=194,110,294,0', 'cap=&OK', 'props=1'])]
         +[c1.join(['type=button', 'pos=300,110,400,0', 'cap=Cancel'])]
      ) )
    if res is None: return
        
    res, s = res
    if res != RES_OK: return
    s = s.split('\n')
    text = s[RES_TEXT]
    if not text: return
    regex = s[RES_REGEX]=='1'
    nocase = s[RES_NOCASE]=='1'
    return (text, regex, nocase)


def is_ok(line, test, b_regex, b_nocase):
    if not b_regex:
        if b_nocase:
            ok = test.lower() in line.lower()
        else:
            ok = test in line
    else:
        flags = re.I if b_nocase else 0
        ok = bool(re.search(test, line, flags=flags))
    return ok


def do_filter():
    res = do_dialog('', False, False)
    if res is None: return
    text, regex, nocase = res    

    res = []
    for i in range(ed.get_line_count()):
        line = ed.get_text_line(i)
        if is_ok(line, text, regex, nocase):
            res.append(line)
    
    if not res:
        msg_status('Cannot find lines: '+text)
        return
            
    file_open('')
    flag = 'r' if regex else '' 
    flag += 'i' if nocase else ''
    ed.set_prop(PROP_TAB_TITLE, 'Filter['+flag+']: '+text)
    ed.set_text_all('\n'.join(res))
    msg_status('Found %d matching lines' % len(res))
        

class Command:
    def dlg(self):
        do_filter()
