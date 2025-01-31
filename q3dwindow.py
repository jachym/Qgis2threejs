# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Q3DWindow

                              -------------------
        begin                : 2016-02-10
        copyright            : (C) 2016 Minoru Akagi
        email                : akaginch@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import os
from datetime import datetime

from PyQt5.QtCore import Qt, QDir, QEvent, QObject, QSettings, QThread, QUrl, pyqtSignal
from PyQt5.QtGui import QColor, QDesktopServices, QIcon
from PyQt5.QtWidgets import (QAction, QActionGroup, QApplication, QCheckBox, QComboBox,
                             QDialog, QDialogButtonBox, QFileDialog, QMainWindow, QMessageBox, QProgressBar)
from qgis.core import Qgis, QgsProject

from . import q3dconst
from .conf import DEBUG_MODE, RUN_CNTLR_IN_BKGND, PLUGIN_VERSION
from .exportsettings import ExportSettings, Layer
from .pluginmanager import pluginManager
from .propertypages import ScenePropertyPage, DEMPropertyPage, VectorPropertyPage, PointCloudPropertyPage
from .q3dcontroller import Q3DController
from .q3dinterface import Q3DInterface
from .qgis2threejstools import pluginDir
from .ui.propertiesdialog import Ui_PropertiesDialog
from .ui.q3dwindow import Ui_Q3DWindow


class Q3DViewerInterface(Q3DInterface):

    abortRequest = pyqtSignal(bool)                  # param: cancel all requests in queue
    updateSceneRequest = pyqtSignal(object, bool)    # params: scene properties dict or 0 (if properties do not changes), update all
    updateLayerRequest = pyqtSignal(Layer)           # param: Layer object
    updateWidgetRequest = pyqtSignal(str, dict)      # params: widget name (e.g. Navi, NorthArrow, Label), properties dict

    exportSettingsUpdated = pyqtSignal(ExportSettings)    # param: export settings
    cameraChanged = pyqtSignal(bool)                 # params: is ortho camera
    navStateChanged = pyqtSignal(bool)               # param: enabled
    previewStateChanged = pyqtSignal(bool)           # param: enabled
    layerAdded = pyqtSignal(Layer)                   # param: Layer object
    layerRemoved = pyqtSignal(str)                   # param: layerId

    def __init__(self, settings, webPage, wnd, treeView, parent=None):
        super().__init__(settings, webPage, parent=parent)
        self.wnd = wnd
        self.treeView = treeView

    # @pyqtSlot(str, int, bool)
    def showMessage(self, msg, timeout=0, show_in_msg_bar=False):
        if show_in_msg_bar:
            self.wnd.qgisIface.messageBar().pushMessage("Qgis2threejs Error", msg, level=Qgis.Warning, duration=timeout)
        else:
            self.wnd.ui.statusbar.showMessage(msg, timeout)

    # @pyqtSlot(int, str)
    def progress(self, percentage=100, msg=None):
        bar = self.wnd.ui.progressBar
        if percentage == 100:
            bar.setVisible(False)
            bar.setFormat("")
        else:
            bar.setVisible(True)
            bar.setValue(percentage)
            if msg is not None:
                bar.setFormat(msg)

    def abort(self):
        self.abortRequest.emit(True)

    def requestSceneUpdate(self, properties=0, update_all=True):
        self.updateSceneRequest.emit(properties, update_all)

    def requestLayerUpdate(self, layer):
        self.updateLayerRequest.emit(layer)

    def requestWidgetUpdate(self, name, properties):
        self.updateWidgetRequest.emit(name, properties)


class Q3DWindow(QMainWindow):

    def __init__(self, qgisIface, settings, preview=True):
        QMainWindow.__init__(self, parent=qgisIface.mainWindow())
        self.setAttribute(Qt.WA_DeleteOnClose)

        # set map settings
        settings.setMapSettings(qgisIface.mapCanvas().mapSettings())

        self.qgisIface = qgisIface
        self.settings = settings
        self.lastDir = None

        self.thread = QThread(self) if RUN_CNTLR_IN_BKGND else None

        self.controller = Q3DController(settings, self.thread)
        self.controller.enabled = preview

        if self.thread:
            self.thread.finished.connect(self.controller.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)

            # start worker thread event loop
            self.thread.start()

        self.setWindowIcon(QIcon(pluginDir("Qgis2threejs.png")))

        self.ui = Ui_Q3DWindow()
        self.ui.setupUi(self)

        self.iface = Q3DViewerInterface(settings, self.ui.webView._page, self, self.ui.treeView, parent=self)
        self.controller.connectToIface(self.iface)

        self.setupMenu()
        self.setupContextMenu()
        self.setupStatusBar(self.iface, preview)
        self.ui.treeView.setup(self.iface)
        self.ui.treeView.addLayers(settings.getLayerList())
        self.ui.webView.setup(self.iface, settings, self, preview)
        self.ui.dockWidgetConsole.hide()

        if DEBUG_MODE:
            self.ui.actionInspector = QAction(self)
            self.ui.actionInspector.setObjectName("actionInspector")
            self.ui.actionInspector.setText("Web Inspector...")
            self.ui.menuWindow.addSeparator()
            self.ui.menuWindow.addAction(self.ui.actionInspector)
            self.ui.actionInspector.triggered.connect(self.ui.webView.showInspector)

        # signal-slot connections
        # map canvas
        self.controller.connectToMapCanvas(qgisIface.mapCanvas())

        # console
        self.ui.lineEditInputBox.returnPressed.connect(self.runInputBoxString)

        self.alwaysOnTopToggled(False)

        # restore window geometry and dockwidget layout
        settings = QSettings()
        self.restoreGeometry(settings.value("/Qgis2threejs/wnd/geometry", b""))
        self.restoreState(settings.value("/Qgis2threejs/wnd/state", b""))

    def closeEvent(self, event):
        self.iface.abort()

        # save export settings to a settings file
        self.settings.saveSettings()

        settings = QSettings()
        settings.setValue("/Qgis2threejs/wnd/geometry", self.saveGeometry())
        settings.setValue("/Qgis2threejs/wnd/state", self.saveState())

        # stop worker thread event loop
        if self.thread:
            self.thread.quit()
            self.thread.wait()

        # close dialogs
        for dlg in self.findChildren(QDialog):
            dlg.close()

        QMainWindow.closeEvent(self, event)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.iface.abort()
        QMainWindow.keyPressEvent(self, event)

    def setupMenu(self):
        self.ui.menuPanels.addAction(self.ui.dockWidgetLayers.toggleViewAction())
        self.ui.menuPanels.addAction(self.ui.dockWidgetConsole.toggleViewAction())

        self.ui.actionGroupCamera = QActionGroup(self)
        self.ui.actionPerspective.setActionGroup(self.ui.actionGroupCamera)
        self.ui.actionOrthographic.setActionGroup(self.ui.actionGroupCamera)
        self.ui.actionOrthographic.setChecked(self.settings.isOrthoCamera())
        self.ui.actionNavigationWidget.setChecked(self.settings.isNavigationEnabled())

        # signal-slot connections
        self.ui.actionExportToWeb.triggered.connect(self.exportToWeb)
        self.ui.actionSaveAsImage.triggered.connect(self.saveAsImage)
        self.ui.actionSaveAsGLTF.triggered.connect(self.saveAsGLTF)
        self.ui.actionLoadSettings.triggered.connect(self.loadSettings)
        self.ui.actionSaveSettings.triggered.connect(self.saveSettings)
        self.ui.actionClearSettings.triggered.connect(self.clearSettings)
        self.ui.actionPluginSettings.triggered.connect(self.pluginSettings)
        self.ui.actionSceneSettings.triggered.connect(self.showScenePropertiesDialog)
        self.ui.actionGroupCamera.triggered.connect(self.cameraChanged)
        self.ui.actionNavigationWidget.toggled.connect(self.iface.navStateChanged)
        self.ui.actionAddPointCloudLayer.triggered.connect(self.showAddPointCloudLayerDialog)
        self.ui.actionNorthArrow.triggered.connect(self.showNorthArrowDialog)
        self.ui.actionHeaderFooterLabel.triggered.connect(self.showHFLabelDialog)
        self.ui.actionResetCameraPosition.triggered.connect(self.ui.webView.resetCameraState)
        self.ui.actionReload.triggered.connect(self.ui.webView.reloadPage)
        self.ui.actionAlwaysOnTop.toggled.connect(self.alwaysOnTopToggled)
        self.ui.actionHelp.triggered.connect(self.help)
        self.ui.actionHomePage.triggered.connect(self.homePage)
        self.ui.actionSendFeedback.triggered.connect(self.sendFeedback)
        self.ui.actionAbout.triggered.connect(self.about)

    def setupContextMenu(self):
        # console
        self.ui.actionConsoleCopy.triggered.connect(self.copyConsole)
        self.ui.actionConsoleClear.triggered.connect(self.clearConsole)
        self.ui.listWidgetDebugView.addAction(self.ui.actionConsoleCopy)
        self.ui.listWidgetDebugView.addAction(self.ui.actionConsoleClear)

    def setupStatusBar(self, iface, previewEnabled=True):
        w = QProgressBar(self.ui.statusbar)
        w.setObjectName("progressBar")
        w.setMaximumWidth(250)
        w.setAlignment(Qt.AlignCenter)
        w.setVisible(False)
        self.ui.statusbar.addPermanentWidget(w)
        self.ui.progressBar = w

        w = QCheckBox(self.ui.statusbar)
        w.setObjectName("checkBoxPreview")
        w.setText("Preview")  # _translate("Q3DWindow", "Preview"))
        w.setChecked(previewEnabled)
        self.ui.statusbar.addPermanentWidget(w)
        self.ui.checkBoxPreview = w
        self.ui.checkBoxPreview.toggled.connect(iface.previewStateChanged)

    def changeEvent(self, event):
        if event.type() == QEvent.WindowStateChange:
            if self.windowState() & Qt.WindowMinimized:
                self.runScript("app.pause();")
            else:
                self.runScript("app.resume();")

    def runScript(self, string, message="", sourceID="Q3DWindow.py"):
        return self.ui.webView.runScript(string, message, sourceID=sourceID)

    # layer tree view
    def showLayerPropertiesDialog(self, layer):
        dialog = PropertiesDialog(self.settings, self.qgisIface, self)
        dialog.propertiesAccepted.connect(self.updateLayerProperties)
        dialog.showLayerProperties(layer)

    # @pyqtSlot(Layer)
    def updateLayerProperties(self, layer):
        orig_layer = self.settings.getLayer(layer.layerId)

        if layer.name != orig_layer.name:
            item = self.ui.treeView.getItemByLayerId(layer.layerId)
            if item:
                item.setText(layer.name)

        if layer.properties != orig_layer.properties:
            self.iface.requestLayerUpdate(layer)

    def getDefaultProperties(self, layer):
        dialog = PropertiesDialog(self.settings, self.qgisIface, self)
        dialog.setLayer(layer)
        return dialog.page.properties()

    # console
    def copyConsole(self):
        # copy selected item(s) text to clipboard
        indices = self.ui.listWidgetDebugView.selectionModel().selectedIndexes()
        text = "\n".join([str(index.data(Qt.DisplayRole)) for index in indices])
        if text:
            QApplication.clipboard().setText(text)

    def clearConsole(self):
        self.ui.listWidgetDebugView.clear()

    def printConsoleMessage(self, message, lineNumber="", sourceID=""):
        if sourceID:
            source = sourceID if lineNumber == "" else "{} ({})".format(sourceID.split("/")[-1], lineNumber)
            text = "{}: {}".format(source, message)
        else:
            text = message
        self.ui.listWidgetDebugView.addItem(text)

    def runInputBoxString(self):
        text = self.ui.lineEditInputBox.text()
        self.ui.listWidgetDebugView.addItem("> " + text)
        result = self.ui.webView._page.mainFrame().evaluateJavaScript(text)
        if result is not None:
            self.ui.listWidgetDebugView.addItem("<- {}".format(result))
        self.ui.listWidgetDebugView.scrollToBottom()
        self.ui.lineEditInputBox.clear()

    # File menu
    def exportToWeb(self):
        from .exporttowebdialog import ExportToWebDialog

        dialog = ExportToWebDialog(self.settings, self.ui.webView._page, self)
        dialog.show()
        dialog.exec_()

    def saveAsImage(self):
        if not self.ui.checkBoxPreview.isChecked():
            QMessageBox.warning(self, "Save Scene as Image", "You need to enable the preview to use this function.")
            return

        from .imagesavedialog import ImageSaveDialog
        dialog = ImageSaveDialog(self)
        dialog.exec_()

    def saveAsGLTF(self):
        if not self.ui.checkBoxPreview.isChecked():
            QMessageBox.warning(self, "Save Current Scene as glTF", "You need to enable the preview to use this function.")
            return

        filename, _ = QFileDialog.getSaveFileName(self, self.tr("Save Current Scene as glTF"),
                                                  self.lastDir or QDir.homePath(),
                                                  "glTF files (*.gltf);;Binary glTF files (*.glb)")
        if filename:
            self.ui.statusbar.showMessage("Exporting current scene to a glTF file...")

            self.ui.webView._page.loadScriptFile(q3dconst.SCRIPT_GLTFEXPORTER)
            self.runScript("saveModelAsGLTF('{0}');".format(filename.replace("\\", "\\\\")))

            self.ui.statusbar.clearMessage()
            self.lastDir = os.path.dirname(filename)

    def loadSettings(self):
        # file open dialog
        directory = self.lastDir or QgsProject.instance().homePath() or QDir.homePath()
        filterString = "Settings files (*.qto3settings);;All files (*.*)"
        filename, _ = QFileDialog.getOpenFileName(self, "Load Export Settings", directory, filterString)
        if not filename:
            return

        self.ui.treeView.uncheckAll()       # hide all 3D objects from the scene

        settings = self.settings.clone()
        settings.loadSettingsFromFile(filename)
        self.ui.treeView.updateLayersCheckState(settings)

        self.iface.exportSettingsUpdated.emit(settings)

        self.lastDir = os.path.dirname(filename)

    def saveSettings(self):
        # file save dialog
        directory = self.lastDir or QgsProject.instance().homePath() or QDir.homePath()
        filename, _ = QFileDialog.getSaveFileName(self, "Save Export Settings", directory, "Settings files (*.qto3settings)")
        if not filename:
            return

        # append .qto3settings extension if filename doesn't have
        if os.path.splitext(filename)[1].lower() != ".qto3settings":
            filename += ".qto3settings"

        self.settings.saveSettings(filename)

        self.lastDir = os.path.dirname(filename)

    def clearSettings(self):
        if QMessageBox.question(self, "Qgis2threejs", "Are you sure you want to clear export settings?") != QMessageBox.Yes:
            return

        self.ui.treeView.uncheckAll()       # hide all 3D objects from the scene
        self.ui.treeView.clearPointCloudLayers()
        self.ui.actionPerspective.setChecked(True)

        settings = self.settings.clone()
        settings.clear()
        settings.updateLayerList()

        self.iface.exportSettingsUpdated.emit(settings)

    def pluginSettings(self):
        from .pluginsettings import SettingsDialog
        dialog = SettingsDialog(self)
        if dialog.exec_():
            pluginManager().reloadPlugins()

    # Scene menu
    def showScenePropertiesDialog(self):
        dialog = PropertiesDialog(self.settings, self.qgisIface, self)
        dialog.propertiesAccepted.connect(self.updateSceneProperties)
        dialog.showSceneProperties()

    # @pyqtSlot(dict)
    def updateSceneProperties(self, properties):
        if self.settings.sceneProperties() != properties:
            self.iface.requestSceneUpdate(properties)

    def showAddPointCloudLayerDialog(self):
        dialog = AddPointCloudLayerDialog(self)
        if dialog.exec_():
            url = dialog.ui.lineEdit_Source.text()
            self.addPointCloudLayer(url)

    def addPointCloudLayer(self, url):
        try:
            name = url.split("/")[-2]
        except IndexError:
            name = "No name"

        layerId = "pc:" + name + datetime.now().strftime("%y%m%d%H%M%S")
        properties = {"url": url}

        layer = Layer(layerId, name, q3dconst.TYPE_POINTCLOUD, properties, visible=True)
        self.iface.layerAdded.emit(layer)
        self.ui.treeView.addLayer(layer)

    # View menu
    def cameraChanged(self, action):
        self.iface.cameraChanged.emit(action == self.ui.actionOrthographic)

    def showNorthArrowDialog(self):
        dialog = NorthArrowDialog(self.settings.widgetProperties("NorthArrow"), self)
        dialog.propertiesAccepted.connect(lambda p: self.iface.requestWidgetUpdate("NorthArrow", p))
        dialog.show()
        dialog.exec_()

    def showHFLabelDialog(self):
        dialog = HFLabelDialog(self.settings.widgetProperties("Label"), self)
        dialog.propertiesAccepted.connect(lambda p: self.iface.requestWidgetUpdate("Label", p))
        dialog.show()
        dialog.exec_()

    # Window menu
    def alwaysOnTopToggled(self, checked):
        if checked:
            self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)
        self.show()

    # Help menu
    def help(self):
        QDesktopServices.openUrl(QUrl("https://qgis2threejs.readthedocs.io/"))

    def homePage(self):
        QDesktopServices.openUrl(QUrl("https://github.com/minorua/Qgis2threejs"))

    def sendFeedback(self):
        QDesktopServices.openUrl(QUrl("https://github.com/minorua/Qgis2threejs/issues"))

    def about(self):
        QMessageBox.information(self, "Qgis2threejs Plugin", "Plugin version: {0}".format(PLUGIN_VERSION), QMessageBox.Ok)


class PropertiesDialog(QDialog):

    propertiesAccepted = pyqtSignal(object)     # dict if scene else Layer

    def __init__(self, settings, qgisIface, parent=None):
        QDialog.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        self.settings = settings
        self.qgisIface = qgisIface
        self.wnd = parent

        self.wheelFilter = WheelEventFilter()

        self.ui = Ui_PropertiesDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.clicked.connect(self.buttonClicked)

        # restore dialog geometry
        settings = QSettings()
        self.restoreGeometry(settings.value("/Qgis2threejs/propdlg/geometry", b""))

    def closeEvent(self, event):
        # save dialog geometry
        settings = QSettings()
        settings.setValue("/Qgis2threejs/propdlg/geometry", self.saveGeometry())
        QDialog.closeEvent(self, event)

    def setLayer(self, layer):
        self.layer = layer.clone()      # create a copy of Layer object
        if self.layer.geomType == q3dconst.TYPE_DEM:
            self.page = DEMPropertyPage(self)
            self.page.setup(self.layer,
                            self.settings.baseExtent(),
                            self.qgisIface.mapCanvas().mapSettings())
        elif self.layer.geomType == q3dconst.TYPE_POINTCLOUD:
            self.page = PointCloudPropertyPage(self)
            self.page.setup(self.layer)
        else:
            self.page = VectorPropertyPage(self)
            self.page.setup(self.layer,
                            self.settings.mapTo3d())
        self.ui.scrollArea.setWidget(self.page)

        # disable wheel event for ComboBox widgets
        for w in self.ui.scrollArea.findChildren(QComboBox):
            w.installEventFilter(self.wheelFilter)

    def buttonClicked(self, button):
        role = self.ui.buttonBox.buttonRole(button)
        if role in [QDialogButtonBox.AcceptRole, QDialogButtonBox.ApplyRole]:
            if isinstance(self.page, ScenePropertyPage):
                self.propertiesAccepted.emit(self.page.properties())
            else:
                if isinstance(self.page, PointCloudPropertyPage):
                    self.layer.name = self.page.lineEdit_Name.text()

                self.layer.properties = self.page.properties()
                self.propertiesAccepted.emit(self.layer)

    def showLayerProperties(self, layer):
        self.setWindowTitle("{0} - Layer Properties".format(layer.name))
        self.setLayer(layer)
        self.show()
        self.exec_()

    def showSceneProperties(self):
        self.setWindowTitle("Scene Settings")
        self.page = ScenePropertyPage(self)
        self.page.setup(self.settings.sceneProperties(), self.qgisIface.mapCanvas().mapSettings(), self.qgisIface.mapCanvas())
        self.ui.scrollArea.setWidget(self.page)
        self.show()
        self.exec_()


class WheelEventFilter(QObject):

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Wheel:
            return True
        return QObject.eventFilter(self, obj, event)


class NorthArrowDialog(QDialog):

    propertiesAccepted = pyqtSignal(dict)

    def __init__(self, properties, parent=None):
        QDialog.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        from .ui.northarrowdialog import Ui_NorthArrowDialog
        self.ui = Ui_NorthArrowDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.clicked.connect(self.buttonClicked)

        self.ui.groupBox.setChecked(properties.get("visible", False))
        self.ui.colorButton.setColor(QColor(properties.get("color", "0x666666").replace("0x", "#")))

    def buttonClicked(self, button):
        role = self.ui.buttonBox.buttonRole(button)
        if role in [QDialogButtonBox.AcceptRole, QDialogButtonBox.ApplyRole]:
            visible = self.ui.groupBox.isChecked()
            color = self.ui.colorButton.color().name().replace("#", "0x")
            self.propertiesAccepted.emit({"visible": visible,
                                          "color": color})


class HFLabelDialog(QDialog):

    propertiesAccepted = pyqtSignal(dict)

    def __init__(self, properties, parent=None):
        QDialog.__init__(self, parent)
        self.setAttribute(Qt.WA_DeleteOnClose)

        from .ui.hflabeldialog import Ui_HFLabelDialog
        self.ui = Ui_HFLabelDialog()
        self.ui.setupUi(self)
        self.ui.buttonBox.clicked.connect(self.buttonClicked)

        self.ui.textEdit_Header.setPlainText(properties.get("Header", ""))
        self.ui.textEdit_Footer.setPlainText(properties.get("Footer", ""))

    def buttonClicked(self, button):
        role = self.ui.buttonBox.buttonRole(button)
        if role in [QDialogButtonBox.AcceptRole, QDialogButtonBox.ApplyRole]:
            self.propertiesAccepted.emit({"Header": self.ui.textEdit_Header.toPlainText(),
                                          "Footer": self.ui.textEdit_Footer.toPlainText()})


class AddPointCloudLayerDialog(QDialog):

    def __init__(self, parent=None):
        QDialog.__init__(self, parent)

        from .ui.addpclayerdialog import Ui_AddPointCloudLayerDialog
        self.ui = Ui_AddPointCloudLayerDialog()
        self.ui.setupUi(self)
        self.ui.pushButton_Browse.clicked.connect(self.browseClicked)

    def browseClicked(self):
        url = self.ui.lineEdit_Source.text()
        if url.startswith("file:"):
            directory = QUrl(url).toLocalFile()
        else:
            directory = QDir.homePath()
        filterString = "All supported files (cloud.js ept.json);;Potree format (cloud.js);;Entwine Point Tile format (ept.json)"
        filename, _ = QFileDialog.getOpenFileName(self, "Select a Potree supported file", directory, filterString)
        if filename:
            self.ui.lineEdit_Source.setText(QUrl.fromLocalFile(filename).toString())
