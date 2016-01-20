import sublime, sublime_plugin
from collections import defaultdict

class TabWrangler(sublime_plugin.EventListener):
	def on_new_async(self, view):
		cull_views()

	def on_activated_async(self, view):
		cull_views()

	def on_post_save_async(self, view):
		cull_views()

def cull_views():
	views_closed = 0

	window = sublime.active_window()
	active_views = [window.active_view_in_group(group).id() for group in range(window.num_groups())]
	for dupe_set in find_dupes(window.views()):
		for dupe in dupe_set:
			if dupe.id() not in active_views and not dupe.is_dirty() and (views_closed+1) < len(dupe_set):
				dupe.close()
				views_closed += 1

	if views_closed > 0:
		message = 'Closed ' + str(views_closed) + ' Duplicate Tab'
		if views_closed > 1:
			message += 's'
		sublime.status_message(message)

def find_dupes(views):
	tally = defaultdict(list)
	for item in views:
		tally[item.buffer_id()].append(item)
	return (locs for _, locs in tally.items() if len(locs) > 1)
