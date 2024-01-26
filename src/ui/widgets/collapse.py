# import pysignal pyslot
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QApplication,
    QTreeWidget,
    QTreeWidgetItem,
    QVBoxLayout,
    QWidget,
)


class StatusWidget(QWidget):
    person_double_clicked = pyqtSignal(str,str, int)

    def __init__(self, data, header_label: str):
        super(StatusWidget, self).__init__()

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels([header_label])
        self.populate_tree(data)
        self.header = header_label
        layout = QVBoxLayout()
        layout.addWidget(self.tree_widget)
        self.setLayout(layout)
        self.tree_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
    def on_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        parent_depth = 0
        parent = item.parent()
        while parent:
            parent_depth += 1
            parent = parent.parent()
        print(parent_depth)
        # Emit the person_double_clicked signal with the name of the person and the parent depth
        self.person_double_clicked.emit(self.header,item.text(column), parent_depth)

    def populate_tree(self, data):
        if data == {}:
            return

        def __listcount(dictlist: dict[dict[str:list]]):
            ret = 0
            for _, value in dictlist.items():
                for _, value2 in value.items():
                    ret += len(value2)
            return ret

        listitems = __listcount(data)
        for action, items in data.items():
            action_item = QTreeWidgetItem(
                self.tree_widget, [f"{action} ({str(listitems)})"]
            )
            for person, entries in items.items():
                person_item = QTreeWidgetItem(
                    action_item, [f"{person} ({str(len(entries))})"]
                )
                for entry in entries:
                    entry_item = QTreeWidgetItem(person_item, [entry])
                # Make the person entry collapsible
                person_item.setExpanded(False)

            # Make the action entry collapsible
            action_item.setExpanded(True)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    data = {"test": {"test2": ["test3", "test4"]}}
    widget = StatusWidget(data, "test")

    widget.show()
    #detect emit signal 
    widget.person_double_clicked.connect(lambda x: print(x))

    sys.exit(app.exec())
