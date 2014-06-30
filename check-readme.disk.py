import io, sys, pwd, time, os

sys.stdout.write('<html><body>\n')
for line in sys.stdin.readlines():
  splits = line.split()
  if len(splits) < 2 or not os.path.isdir(splits[1]): 
    continue
  dir_path = splits[1]
  readme_path = dir_path +  '/readme.disk'
  last_modified = time.strftime('%c', time.localtime(os.path.getmtime(dir_path)))
  owner = pwd.getpwuid(os.stat(dir_path).st_uid)[0]
  if os.path.isfile(readme_path):
    with open(dir_path + '/readme.disk') as readme_file:
      readme = readme_file.read()
    emph_open, emph_close = '<b>', '</b>'
    readme = emph_open + readme + emph_close
  else:
    emph_open, emph_close = '<b>', '</b>'
    readme = 'file {} not found. {} blame {}{}'.format(readme_path, emph_open, owner, emph_close)
  sys.stdout.write('<p><ul>\n')
  sys.stdout.write('<li>dir: {}</li>\n'.format(dir_path))
  sys.stdout.write('<li>size: {}{}{}</li>\n'.format(emph_open, splits[0], emph_close))
  sys.stdout.write('<li>last modified: {}</li>\n'.format(last_modified))
  sys.stdout.write('<li>owner: {}</li>\n'.format(owner))
  sys.stdout.write('<li>readme: {}</li>\n'.format(readme))
  sys.stdout.write('</ul></p>\n')
sys.stdout.write('</body></html>\n')
