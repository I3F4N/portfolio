js = open('script.js', 'r', encoding='utf-8').read()

vars_to_check = [
    'isBooting', 'commandIndex', 'commands', 'charIndex',
    'commandInputEl', 'outputEl', 'terminalBody',
    'bootSequenceTimeout', 'skipBootSequence', 'lastTime',
    'drawMatrix'
]

for v in vars_to_check:
    used = v in js
    declared = (f'let {v}' in js or f'const {v}' in js or
                f'var {v}' in js or f'function {v}' in js)
    if used and not declared:
        print(f'MISSING: {v} - used but never declared!')
    elif declared:
        print(f'OK:      {v} - declared')
    else:
        print(f'UNUSED:  {v} - not found at all')
