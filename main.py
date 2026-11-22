"""ZCalc: calculadora de escritorio para Ubuntu con GTK 4."""

from pathlib import Path
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gdk, Gtk, Pango

from calculator import Calculator


class ZCalc(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="app.zcalc.desktop")
        self.calculator = Calculator()

    def do_activate(self):
        window = self.props.active_window
        if window:
            window.present()
            return

        provider = Gtk.CssProvider()
        provider.load_from_path(str(Path(__file__).with_name("style.css")))
        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        window = Gtk.ApplicationWindow(application=self)
        window.set_title("ZCalc")
        window.set_default_size(360, 510)
        window.set_resizable(False)

        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="ZCalc"))
        window.set_titlebar(header)

        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        content.set_margin_top(20)
        content.set_margin_bottom(20)
        content.set_margin_start(20)
        content.set_margin_end(20)

        self.history_label = Gtk.Label(xalign=1)
        self.history_label.add_css_class("history")
        self.history_label.set_ellipsize(Pango.EllipsizeMode.START)
        content.append(self.history_label)

        self.display_label = Gtk.Label(label="0", xalign=1)
        self.display_label.add_css_class("display")
        self.display_label.set_ellipsize(Pango.EllipsizeMode.START)
        self.display_label.set_selectable(True)
        content.append(self.display_label)

        grid = Gtk.Grid()
        grid.set_row_spacing(10)
        grid.set_column_spacing(10)
        grid.set_row_homogeneous(True)
        grid.set_column_homogeneous(True)
        grid.set_vexpand(True)

        rows = [
            ("C", "⌫", "%", "÷"),
            ("7", "8", "9", "×"),
            ("4", "5", "6", "−"),
            ("1", "2", "3", "+"),
            ("±", "0", ".", "="),
        ]
        for row_index, row in enumerate(rows):
            for col_index, symbol in enumerate(row):
                button = Gtk.Button(label=symbol)
                button.set_size_request(60, 60)
                button.add_css_class("calc-key")
                if symbol == "=":
                    button.add_css_class("equals")
                elif symbol in ("÷", "×", "−", "+"):
                    button.add_css_class("operator")
                elif symbol in ("C", "⌫", "%", "±"):
                    button.add_css_class("utility")
                button.connect("clicked", self.on_button_clicked, symbol)
                grid.attach(button, col_index, row_index, 1, 1)

        content.append(grid)
        window.set_child(content)

        keyboard = Gtk.EventControllerKey.new()
        keyboard.set_propagation_phase(Gtk.PropagationPhase.CAPTURE)
        keyboard.connect("key-pressed", self.on_key_pressed)
        window.add_controller(keyboard)
        window.present()

    def on_button_clicked(self, _button, symbol):
        key = {"×": "*", "÷": "/", "−": "-"}.get(symbol, symbol)
        self.handle_input(key)

    def on_key_pressed(self, _controller, keyval, _keycode, state):
        if state & (Gdk.ModifierType.CONTROL_MASK | Gdk.ModifierType.ALT_MASK):
            return False

        name = Gdk.keyval_name(keyval)
        special = {
            "Return": "=", "KP_Enter": "=", "BackSpace": "⌫",
            "Escape": "C", "Delete": "C", "KP_Add": "+",
            "KP_Subtract": "-", "KP_Multiply": "*",
            "KP_Divide": "/", "KP_Decimal": ".",
        }
        if name in special:
            self.handle_input(special[name])
            return True
        if name and name.startswith("KP_") and name[3:].isdigit():
            self.handle_input(name[3:])
            return True

        codepoint = Gdk.keyval_to_unicode(keyval)
        character = chr(codepoint) if codepoint else ""
        if character in "0123456789+-*/%=.," and character:
            self.handle_input("." if character == "," else character)
            return True
        return False

    def handle_input(self, key):
        self.calculator.press(key)
        self.display_label.set_text(self.calculator.screen)
        self.history_label.set_text(self.calculator.history)


if __name__ == "__main__":
    ZCalc().run(None)
