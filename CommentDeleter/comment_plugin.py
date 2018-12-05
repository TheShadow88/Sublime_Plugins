import sublime
import sublime_plugin
from os import path
import re

class CommentdeleterCommand(sublime_plugin.TextCommand):
	def regex_compiler(self, multi_start, multi_end, single):
		single_r = "|(?<!['\"]){0}.*\\n?".format(single)
		multi_full = "((?<!['\"]){0}(.*\\n)*?.*{1}\\n?)".format(multi_start, multi_end)
		if single is None:
			single = ""
		if multi_start == None and multi_end == None:
			return single_r[1:]
		return "{}{}".format(multi_full, single_r)
			
	def run(self, edit, one_delete=False, from_cursor_pos=False, files=[]):
		start_pos = self.view.sel()[0].begin() if from_cursor_pos else 0
		name = self.view.file_name()
		name = path.split(name)
		ext = name[1].split(".")[1]
		if ext in ["c", "cpp", "csharp"]:
			rg = self.regex_compiler("\\/\\*", "\\*\\/", "\\/\\/")
		if ext == "py":
			rg = self.regex_compiler(None, None, "#")
		if ext == "rb":
			rg = self.regex_compiler("=start", "=end", "#")
		if ext == "html":
			rg = self.regex_compiler("<!--", "-->", None)
		if ext == "css":
			rg = self.regex_compiler("\\/\\*", "\\*\\/", None)
		#print("New Call")
		while True: #\/\*.*\*\/\n\s*|(\/\*(.*\n)+.*\*\/)|\/\/.+\n\s*

			#"\\/\\*.*\\*\\/\\n\\s*|(\\/\\*(.*\\n)+.*\\*\\/)|\\/\\/.+\\n\\s*"
			#print(rg)

			region = self.view.find(rg, start_pos)
			if region.empty():
				break
			#print("COM:", self.view.substr(region))
			line = self.view.line(region.a)
			part = sublime.Region(line.a, region.a)
			part2 = sublime.Region(region.b, line.b)
			s_before = self.view.substr(part)	
			s_after = self.view.substr(part2)
			clear_space = False
			if not(part.empty()):
				if s_before.isspace() and s_after.isspace():
					clear_space = True
				elif not(s_before.isspace()):
					region.b = line.b
			 
			#print(has_space_after)
			self.view.erase(edit, region)
			
			if clear_space:
				self.view.erase(edit, part)
				#print("Double erase")

			if one_delete:
				break
			
