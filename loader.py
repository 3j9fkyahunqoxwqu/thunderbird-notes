import os
import yaml

release_dir = os.path.join(os.path.dirname(__file__), 'release')
beta_dir = os.path.join(os.path.dirname(__file__), 'beta')

class ReleaseNotes(object):
    def __init__(self):
        # Copy notes into the same dict. Release version notes overwrite beta version notes if any version numbers
        # are shared.
        self.notes = self.load_dir(beta_dir)
        self.notes.update(self.load_dir(release_dir))

        self.releases = {'52.0': {'major':'52.0', 'minor':['52.0.1', '52.1.0', '52.1.1', '52.2.0', '52.2.1']}}
        self.settings = {}
        with open(os.path.join(os.path.dirname(__file__), "settings.yml"), "r") as f:
            self.settings = yaml.load(f)


    def organize(self, notelist):
        organized_notelist = {}
        for k, n in notelist.iteritems():
            def get_bug_search_url():
                return n["release"]["bug_search_url"]
            n["release"]["get_bug_search_url"] = get_bug_search_url
            n["known_issues"] = []
            n["new_features"] = []
            n["version"] = k
            # Import system requirements from major version
            if not n["release"].get("system_requirements"):
                import_version = n["release"].get("import_system_requirements")
                if import_version:
                    n["release"]["system_requirements"] = notelist[import_version]["release"]["system_requirements"]
                else:
                    n["release"]["system_requirements"] = ""
            # Split notes into Known Issues and New Features sections.
            for note in n["notes"]:
                if note["tag"] == "unresolved":
                    n["known_issues"].append(note)
                else:
                    n["new_features"].append(note)
            organized_notelist[k] = n
        return organized_notelist


    def load_dir(self, path):
        notes = {}
        notefiles = os.listdir(path)
        for notefile in notefiles:
            if notefile.endswith(".yml"):
                with open(os.path.join(path, notefile), "r") as f:
                    doc = yaml.load(f)
                    notes[os.path.splitext(notefile)[0]] = doc
        sorted_notes = self.organize(notes)
        return sorted_notes


releasenotes = ReleaseNotes()
