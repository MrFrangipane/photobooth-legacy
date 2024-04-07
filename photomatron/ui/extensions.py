from typing import TypeVar, Type

from PySide2.QtWidgets import QListWidget, QMessageBox, QWidget
from PySide2.QtCore import Qt


WARNING = QMessageBox.Icon.Warning
INFO = QMessageBox.Icon.Information


def update_list_widget(list_widget: QListWidget, items: [str], select=None):
    """
    Clears and updates a QListWidget with given items, and tries to restore selection without emitting a signal

    !!! note
        If the previously selected item is not found among new items, nothing is selected and a signal is emitted
    """
    if select is None:
        current = list_widget.currentItem()
        if current is not None:
            current = current.text()
        else:
            current = ""
    else:
        current = select
    dont_emit = current in items + ['']

    list_widget.blockSignals(True)
    list_widget.clear()
    list_widget.addItems(items)

    items = list_widget.findItems(current, Qt.MatchExactly)

    if dont_emit:
        if items:
            list_widget.setCurrentItem(items[0])
        list_widget.blockSignals(False)
    else:
        list_widget.blockSignals(False)
        if items:
            list_widget.setCurrentItem(items[0])


def confirmation_messagebox(message, title, icon, parent=None):
    _message_box = QMessageBox(parent)
    _message_box.setIcon(icon)
    _message_box.setWindowTitle(title)
    _message_box.setText(message)
    _message_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

    result = _message_box.exec_() == QMessageBox.Ok
    _message_box.deleteLater()

    return result


T = TypeVar('T')


def create_with_style_property(widget_class: Type[T], value, *arg, **kwargs) -> T:
    new_widget = widget_class(*arg, **kwargs)
    new_widget.setProperty("style", value)
    new_widget.style().unpolish(new_widget)
    new_widget.style().polish(new_widget)
    return new_widget
