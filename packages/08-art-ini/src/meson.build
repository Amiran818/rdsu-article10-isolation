project('art-ini', 'c', version : '1.0', default_options : ['warning_level=2'])

glib = dependency('glib-2.0', version : '>= 2.56')
exe = executable('art-ini', 'ini.c', dependencies : glib, install : true)

ini = files('test.ini')
test('get', exe, args : [ini, 'build', 'tool'])
test('list', exe, args : ['--list', ini])
test('missing key', exe, args : [ini, 'build', 'nokey'], should_fail : true)
