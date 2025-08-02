import re
from gi.repository import GObject, Gtk, Gedit, GLib

WORD_RE = re.compile(r"[a-zA-Z0-9]+(?:[-'][a-zA-Z0-9]+)*")
DEBOUNCE_DELAY_MS = 300

def get_text(doc):
    try:
        start, end = doc.get_bounds()
        return doc.get_text(start, end, False)
    except Exception:
        return ""

class WordcountPlugin(GObject.Object, Gedit.WindowActivatable):
    __gtype_name__ = "WordcountPlugin"
    window = GObject.property(type=Gedit.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._label = Gtk.Label()
        self._doc_changed_id = None
        self._update_timer = None
        self._statusbar = None
        self._active_doc = None

    def do_activate(self):
        self._statusbar = self.window.get_statusbar()
        self._statusbar.pack_end(self._label, False, False, 5)
        self._label.show()

    def do_deactivate(self):
        if self._label:
            self._statusbar.remove(self._label)
        if self._doc_changed_id and self._active_doc:
            self._active_doc.disconnect(self._doc_changed_id)
        if self._update_timer:
            GLib.source_remove(self._update_timer)
        self._label = None
        self._active_doc = None
        self._doc_changed_id = None
        self._update_timer = None

    def do_update_state(self):
        doc = self.window.get_active_document()
        if self._active_doc and self._doc_changed_id:
            self._active_doc.disconnect(self._doc_changed_id)
            self._doc_changed_id = None

        self._active_doc = doc

        if doc is not None:
            self._doc_changed_id = doc.connect("changed", self.on_document_changed)
            self.schedule_update(doc)
        else:
            self._label.set_text("")

    def on_document_changed(self, doc):
        self.schedule_update(doc)

    def schedule_update(self, doc):
        if self._update_timer:
            GLib.source_remove(self._update_timer)

        def do_update():
            self.update_label(doc)
            self._update_timer = None
            return False

        self._update_timer = GLib.timeout_add(DEBOUNCE_DELAY_MS, do_update)

    def update_label(self, doc):
        if doc is None or doc != self._active_doc:
            return
        try:
            text = get_text(doc)
            word_count = len(WORD_RE.findall(text))
            char_count = len(text)
            self._label.set_text(f"words: {word_count} | chars: {char_count}")
        except Exception as e:
            self._label.set_text(f"error: {e}")
