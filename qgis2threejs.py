# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Qgis2threejs
                                 A QGIS plugin
 export terrain data, map canvas image and vector data to web browser
                              -------------------
        begin                : 2013-12-21
        copyright            : (C) 2013 Minoru Akagi
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

from PyQt5.QtCore import QFile    #, QSettings, QTranslator, qVersion
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon

from qgis.core import QgsProject

from .qgis2threejstools import logMessage, removeTemporaryOutputDir
from .q3dviewercontroller import Q3DViewerController
from .q3dwindow import Q3DWindow


class Qgis2threejs:

  def __init__(self, iface):
    # Save reference to the QGIS interface
    self.iface = iface

    # initialize plugin directory
    self.plugin_dir = os.path.dirname(QFile.decodeName(__file__))

    # initialize locale
    #locale = QSettings().value("locale/userLocale")[0:2]
    #localePath = os.path.join(self.plugin_dir, 'i18n', 'qgis2threejs_{0}.qm'.format(locale))

    #if os.path.exists(localePath):
    #  self.translator = QTranslator()
    #  self.translator.load(localePath)

    #  if qVersion() > '4.3.3':
    #    QCoreApplication.installTranslator(self.translator)


    self.exportSettings = {}
    self.lastTreeItemData = None
    self.settingsFilePath = None

    self.currentProjectPath = None

    # exporter
    self.controller = None    # Q3DController

  def initGui(self):
    # Create action that will start plugin configuration
    icon = QIcon(os.path.join(self.plugin_dir, "icon.png"))
    self.action = QAction(icon, "Qgis2threejs Exporter", self.iface.mainWindow())
    self.action.setObjectName("Qgis2threejsExporter")

    self.actionNP = QAction(icon, "Qgis2threejs Exporter (No Preview)", self.iface.mainWindow())
    self.actionNP.setObjectName("Qgis2threejsExporterNoPreview")

    # connect the action to the launchExporter method
    self.action.triggered.connect(self.launchExporter)
    self.actionNP.triggered.connect(self.launchExporterWithPreviewDisabled)

    # Add toolbar button and web menu items
    name = "Qgis2threejs"
    self.iface.addWebToolBarIcon(self.action)
    self.iface.addPluginToWebMenu(name, self.action)
    self.iface.addPluginToWebMenu(name, self.actionNP)

  def unload(self):
    # Remove the web menu items and icon
    name = "Qgis2threejs"
    self.iface.removeWebToolBarIcon(self.action)
    self.iface.removePluginWebMenu(name, self.action)
    self.iface.removePluginWebMenu(name, self.actionNP)

    # remove temporary output directory
    removeTemporaryOutputDir()

  def launchExporter(self, _, preview=True):
    if self.controller is None:
      self.controller = Q3DViewerController(self.iface)

    if self.controller.iface is None:
      logMessage("Launching Qgis2threejs Exporter...")

      proj_path = QgsProject.instance().fileName()
      if proj_path != self.currentProjectPath:
        self.controller.settings.loadSettingsFromFile()   # load export settings from settings file for current project
        self.currentProjectPath = proj_path

      self.controller.previewEnabled = preview

      self.liveExporter = Q3DWindow(self.iface.mainWindow(), self.iface, self.controller, isViewer=True, preview=preview)
      self.liveExporter.show()
    else:
      logMessage("Qgis2threejs Exporter is already running.")

      self.liveExporter.activateWindow()

  def launchExporterWithPreviewDisabled(self):
    self.launchExporter(False, False)

  def loadExportSettings(self, filename):
    import json
    with open(filename) as f:
      self.exportSettings = json.load(f)

  def saveExportSettings(self, filename):
    import json
    try:
      with open(filename, "w", encoding="UTF-8") as f:
        json.dump(self.exportSettings, f, ensure_ascii=False, indent=2, sort_keys=True)
      return True
    except Exception as e:
      logMessage("Failed to save export settings: " + str(e))
      return False
