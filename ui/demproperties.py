# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Documents\minorua\QGIS\plugins\Qgis2threejs\ui\demproperties.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DEMPropertiesWidget(object):
    def setupUi(self, DEMPropertiesWidget):
        DEMPropertiesWidget.setObjectName("DEMPropertiesWidget")
        DEMPropertiesWidget.resize(335, 631)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(DEMPropertiesWidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox_Geometry = QtWidgets.QGroupBox(DEMPropertiesWidget)
        self.groupBox_Geometry.setObjectName("groupBox_Geometry")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_Geometry)
        self.verticalLayout_6.setContentsMargins(-1, 6, -1, 6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_Resampling = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Resampling.setObjectName("horizontalLayout_Resampling")
        self.label_Resampling = QtWidgets.QLabel(self.groupBox_Geometry)
        self.label_Resampling.setObjectName("label_Resampling")
        self.horizontalLayout_Resampling.addWidget(self.label_Resampling)
        self.horizontalSlider_DEMSize = QtWidgets.QSlider(self.groupBox_Geometry)
        self.horizontalSlider_DEMSize.setEnabled(True)
        self.horizontalSlider_DEMSize.setMinimum(1)
        self.horizontalSlider_DEMSize.setMaximum(6)
        self.horizontalSlider_DEMSize.setSingleStep(1)
        self.horizontalSlider_DEMSize.setPageStep(1)
        self.horizontalSlider_DEMSize.setProperty("value", 2)
        self.horizontalSlider_DEMSize.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_DEMSize.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.horizontalSlider_DEMSize.setTickInterval(1)
        self.horizontalSlider_DEMSize.setObjectName("horizontalSlider_DEMSize")
        self.horizontalLayout_Resampling.addWidget(self.horizontalSlider_DEMSize)
        self.label_ResamplingLevel = QtWidgets.QLabel(self.groupBox_Geometry)
        self.label_ResamplingLevel.setMinimumSize(QtCore.QSize(10, 0))
        self.label_ResamplingLevel.setObjectName("label_ResamplingLevel")
        self.horizontalLayout_Resampling.addWidget(self.label_ResamplingLevel)
        self.verticalLayout_6.addLayout(self.horizontalLayout_Resampling)
        self.verticalLayout_Surroundings = QtWidgets.QVBoxLayout()
        self.verticalLayout_Surroundings.setObjectName("verticalLayout_Surroundings")
        self.checkBox_Surroundings = QtWidgets.QCheckBox(self.groupBox_Geometry)
        self.checkBox_Surroundings.setObjectName("checkBox_Surroundings")
        self.verticalLayout_Surroundings.addWidget(self.checkBox_Surroundings)
        self.gridLayout_Surroundings = QtWidgets.QGridLayout()
        self.gridLayout_Surroundings.setObjectName("gridLayout_Surroundings")
        self.label_3 = QtWidgets.QLabel(self.groupBox_Geometry)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_Surroundings.addWidget(self.label_3, 0, 2, 1, 1)
        self.spinBox_Roughening = QtWidgets.QSpinBox(self.groupBox_Geometry)
        self.spinBox_Roughening.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBox_Roughening.setMaximum(64)
        self.spinBox_Roughening.setProperty("value", 1)
        self.spinBox_Roughening.setObjectName("spinBox_Roughening")
        self.gridLayout_Surroundings.addWidget(self.spinBox_Roughening, 0, 3, 1, 1)
        self.spinBox_Size = QtWidgets.QSpinBox(self.groupBox_Geometry)
        self.spinBox_Size.setMinimumSize(QtCore.QSize(70, 0))
        self.spinBox_Size.setMinimum(3)
        self.spinBox_Size.setMaximum(9)
        self.spinBox_Size.setSingleStep(2)
        self.spinBox_Size.setProperty("value", 3)
        self.spinBox_Size.setObjectName("spinBox_Size")
        self.gridLayout_Surroundings.addWidget(self.spinBox_Size, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox_Geometry)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout_Surroundings.addWidget(self.label_2, 0, 0, 1, 1)
        self.verticalLayout_Surroundings.addLayout(self.gridLayout_Surroundings)
        self.verticalLayout_6.addLayout(self.verticalLayout_Surroundings)
        self.verticalLayout_Clip = QtWidgets.QVBoxLayout()
        self.verticalLayout_Clip.setObjectName("verticalLayout_Clip")
        self.checkBox_Clip = QtWidgets.QCheckBox(self.groupBox_Geometry)
        self.checkBox_Clip.setObjectName("checkBox_Clip")
        self.verticalLayout_Clip.addWidget(self.checkBox_Clip)
        self.comboBox_ClipLayer = QtWidgets.QComboBox(self.groupBox_Geometry)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_ClipLayer.sizePolicy().hasHeightForWidth())
        self.comboBox_ClipLayer.setSizePolicy(sizePolicy)
        self.comboBox_ClipLayer.setMaximumSize(QtCore.QSize(220, 16777215))
        self.comboBox_ClipLayer.setObjectName("comboBox_ClipLayer")
        self.verticalLayout_Clip.addWidget(self.comboBox_ClipLayer)
        self.verticalLayout_6.addLayout(self.verticalLayout_Clip)
        self.verticalLayout_2.addWidget(self.groupBox_Geometry)
        self.groupBox_Material = QtWidgets.QGroupBox(DEMPropertiesWidget)
        self.groupBox_Material.setObjectName("groupBox_Material")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox_Material)
        self.verticalLayout_4.setContentsMargins(-1, 6, -1, 6)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_5 = QtWidgets.QLabel(self.groupBox_Material)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_4.addWidget(self.label_5)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(6, -1, -1, -1)
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton_MapCanvas = QtWidgets.QRadioButton(self.groupBox_Material)
        self.radioButton_MapCanvas.setChecked(True)
        self.radioButton_MapCanvas.setObjectName("radioButton_MapCanvas")
        self.verticalLayout.addWidget(self.radioButton_MapCanvas)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.radioButton_LayerImage = QtWidgets.QRadioButton(self.groupBox_Material)
        self.radioButton_LayerImage.setObjectName("radioButton_LayerImage")
        self.horizontalLayout_5.addWidget(self.radioButton_LayerImage)
        self.label_LayerImage = QtWidgets.QLabel(self.groupBox_Material)
        self.label_LayerImage.setEnabled(False)
        self.label_LayerImage.setText("")
        self.label_LayerImage.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_LayerImage.setObjectName("label_LayerImage")
        self.horizontalLayout_5.addWidget(self.label_LayerImage)
        self.toolButton_SelectLayer = QtWidgets.QToolButton(self.groupBox_Material)
        self.toolButton_SelectLayer.setEnabled(False)
        self.toolButton_SelectLayer.setObjectName("toolButton_SelectLayer")
        self.horizontalLayout_5.addWidget(self.toolButton_SelectLayer)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_ImageFile = QtWidgets.QHBoxLayout()
        self.horizontalLayout_ImageFile.setObjectName("horizontalLayout_ImageFile")
        self.radioButton_ImageFile = QtWidgets.QRadioButton(self.groupBox_Material)
        self.radioButton_ImageFile.setEnabled(True)
        self.radioButton_ImageFile.setObjectName("radioButton_ImageFile")
        self.horizontalLayout_ImageFile.addWidget(self.radioButton_ImageFile)
        self.lineEdit_ImageFile = QtWidgets.QLineEdit(self.groupBox_Material)
        self.lineEdit_ImageFile.setEnabled(False)
        self.lineEdit_ImageFile.setObjectName("lineEdit_ImageFile")
        self.horizontalLayout_ImageFile.addWidget(self.lineEdit_ImageFile)
        self.toolButton_ImageFile = QtWidgets.QToolButton(self.groupBox_Material)
        self.toolButton_ImageFile.setEnabled(False)
        self.toolButton_ImageFile.setObjectName("toolButton_ImageFile")
        self.horizontalLayout_ImageFile.addWidget(self.toolButton_ImageFile)
        self.verticalLayout.addLayout(self.horizontalLayout_ImageFile)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.radioButton_SolidColor = QtWidgets.QRadioButton(self.groupBox_Material)
        self.radioButton_SolidColor.setObjectName("radioButton_SolidColor")
        self.horizontalLayout_7.addWidget(self.radioButton_SolidColor)
        self.colorButton_Color = QgsColorButton(self.groupBox_Material)
        self.colorButton_Color.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.colorButton_Color.sizePolicy().hasHeightForWidth())
        self.colorButton_Color.setSizePolicy(sizePolicy)
        self.colorButton_Color.setObjectName("colorButton_Color")
        self.horizontalLayout_7.addWidget(self.colorButton_Color)
        self.verticalLayout.addLayout(self.horizontalLayout_7)
        self.verticalLayout_4.addLayout(self.verticalLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalSlider_Opacity = QtWidgets.QSlider(self.groupBox_Material)
        self.horizontalSlider_Opacity.setMaximum(100)
        self.horizontalSlider_Opacity.setProperty("value", 100)
        self.horizontalSlider_Opacity.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Opacity.setObjectName("horizontalSlider_Opacity")
        self.gridLayout.addWidget(self.horizontalSlider_Opacity, 2, 2, 1, 1)
        self.label_17 = QtWidgets.QLabel(self.groupBox_Material)
        self.label_17.setObjectName("label_17")
        self.gridLayout.addWidget(self.label_17, 2, 0, 1, 1)
        self.label_TextureSize = QtWidgets.QLabel(self.groupBox_Material)
        self.label_TextureSize.setObjectName("label_TextureSize")
        self.gridLayout.addWidget(self.label_TextureSize, 0, 0, 1, 1)
        self.spinBox_Opacity = QtWidgets.QSpinBox(self.groupBox_Material)
        self.spinBox_Opacity.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinBox_Opacity.sizePolicy().hasHeightForWidth())
        self.spinBox_Opacity.setSizePolicy(sizePolicy)
        self.spinBox_Opacity.setPrefix("")
        self.spinBox_Opacity.setMinimum(0)
        self.spinBox_Opacity.setMaximum(100)
        self.spinBox_Opacity.setSingleStep(1)
        self.spinBox_Opacity.setProperty("value", 100)
        self.spinBox_Opacity.setObjectName("spinBox_Opacity")
        self.gridLayout.addWidget(self.spinBox_Opacity, 2, 3, 1, 1)
        self.comboBox_TextureSize = QtWidgets.QComboBox(self.groupBox_Material)
        self.comboBox_TextureSize.setEditable(True)
        self.comboBox_TextureSize.setObjectName("comboBox_TextureSize")
        self.gridLayout.addWidget(self.comboBox_TextureSize, 0, 1, 1, 3)
        self.verticalLayout_4.addLayout(self.gridLayout)
        self.checkBox_TransparentBackground = QtWidgets.QCheckBox(self.groupBox_Material)
        self.checkBox_TransparentBackground.setObjectName("checkBox_TransparentBackground")
        self.verticalLayout_4.addWidget(self.checkBox_TransparentBackground)
        self.checkBox_Shading = QtWidgets.QCheckBox(self.groupBox_Material)
        self.checkBox_Shading.setChecked(True)
        self.checkBox_Shading.setObjectName("checkBox_Shading")
        self.verticalLayout_4.addWidget(self.checkBox_Shading)
        self.verticalLayout_2.addWidget(self.groupBox_Material)
        self.groupBox_Others = QtWidgets.QGroupBox(DEMPropertiesWidget)
        self.groupBox_Others.setObjectName("groupBox_Others")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_Others)
        self.gridLayout_2.setContentsMargins(-1, 6, -1, 6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.toolButton_SideColor = QgsColorButton(self.groupBox_Others)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_SideColor.sizePolicy().hasHeightForWidth())
        self.toolButton_SideColor.setSizePolicy(sizePolicy)
        self.toolButton_SideColor.setObjectName("toolButton_SideColor")
        self.gridLayout_2.addWidget(self.toolButton_SideColor, 0, 1, 1, 1)
        self.checkBox_Sides = QtWidgets.QCheckBox(self.groupBox_Others)
        self.checkBox_Sides.setChecked(True)
        self.checkBox_Sides.setObjectName("checkBox_Sides")
        self.gridLayout_2.addWidget(self.checkBox_Sides, 0, 0, 1, 1)
        self.toolButton_EdgeColor = QgsColorButton(self.groupBox_Others)
        self.toolButton_EdgeColor.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_EdgeColor.sizePolicy().hasHeightForWidth())
        self.toolButton_EdgeColor.setSizePolicy(sizePolicy)
        self.toolButton_EdgeColor.setObjectName("toolButton_EdgeColor")
        self.gridLayout_2.addWidget(self.toolButton_EdgeColor, 1, 1, 1, 1)
        self.checkBox_Frame = QtWidgets.QCheckBox(self.groupBox_Others)
        self.checkBox_Frame.setObjectName("checkBox_Frame")
        self.gridLayout_2.addWidget(self.checkBox_Frame, 1, 0, 1, 1)
        self.checkBox_Visible = QtWidgets.QCheckBox(self.groupBox_Others)
        self.checkBox_Visible.setChecked(True)
        self.checkBox_Visible.setObjectName("checkBox_Visible")
        self.gridLayout_2.addWidget(self.checkBox_Visible, 3, 0, 1, 2)
        self.checkBox_Wireframe = QtWidgets.QCheckBox(self.groupBox_Others)
        self.checkBox_Wireframe.setObjectName("checkBox_Wireframe")
        self.gridLayout_2.addWidget(self.checkBox_Wireframe, 2, 0, 1, 1)
        self.toolButton_WireframeColor = QgsColorButton(self.groupBox_Others)
        self.toolButton_WireframeColor.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toolButton_WireframeColor.sizePolicy().hasHeightForWidth())
        self.toolButton_WireframeColor.setSizePolicy(sizePolicy)
        self.toolButton_WireframeColor.setObjectName("toolButton_WireframeColor")
        self.gridLayout_2.addWidget(self.toolButton_WireframeColor, 2, 1, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox_Others)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)

        self.retranslateUi(DEMPropertiesWidget)
        self.checkBox_Clip.toggled['bool'].connect(self.comboBox_ClipLayer.setVisible)
        self.radioButton_LayerImage.toggled['bool'].connect(self.label_LayerImage.setEnabled)
        self.radioButton_LayerImage.toggled['bool'].connect(self.toolButton_SelectLayer.setEnabled)
        self.radioButton_ImageFile.toggled['bool'].connect(self.lineEdit_ImageFile.setEnabled)
        self.radioButton_ImageFile.toggled['bool'].connect(self.toolButton_ImageFile.setEnabled)
        self.checkBox_Clip.toggled['bool'].connect(self.checkBox_Frame.setDisabled)
        self.horizontalSlider_DEMSize.valueChanged['int'].connect(self.label_ResamplingLevel.setNum)
        self.horizontalSlider_Opacity.valueChanged['int'].connect(self.spinBox_Opacity.setValue)
        self.spinBox_Opacity.valueChanged['int'].connect(self.horizontalSlider_Opacity.setValue)
        self.radioButton_SolidColor.toggled['bool'].connect(self.colorButton_Color.setEnabled)
        self.checkBox_Sides.toggled['bool'].connect(self.toolButton_SideColor.setEnabled)
        self.checkBox_Clip.toggled['bool'].connect(self.checkBox_Wireframe.setDisabled)
        self.checkBox_Frame.toggled['bool'].connect(self.toolButton_EdgeColor.setEnabled)
        self.checkBox_Wireframe.toggled['bool'].connect(self.toolButton_WireframeColor.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(DEMPropertiesWidget)
        DEMPropertiesWidget.setTabOrder(self.horizontalSlider_DEMSize, self.checkBox_Surroundings)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Surroundings, self.spinBox_Size)
        DEMPropertiesWidget.setTabOrder(self.spinBox_Size, self.spinBox_Roughening)
        DEMPropertiesWidget.setTabOrder(self.spinBox_Roughening, self.checkBox_Clip)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Clip, self.comboBox_ClipLayer)
        DEMPropertiesWidget.setTabOrder(self.comboBox_ClipLayer, self.radioButton_MapCanvas)
        DEMPropertiesWidget.setTabOrder(self.radioButton_MapCanvas, self.radioButton_LayerImage)
        DEMPropertiesWidget.setTabOrder(self.radioButton_LayerImage, self.toolButton_SelectLayer)
        DEMPropertiesWidget.setTabOrder(self.toolButton_SelectLayer, self.radioButton_ImageFile)
        DEMPropertiesWidget.setTabOrder(self.radioButton_ImageFile, self.lineEdit_ImageFile)
        DEMPropertiesWidget.setTabOrder(self.lineEdit_ImageFile, self.toolButton_ImageFile)
        DEMPropertiesWidget.setTabOrder(self.toolButton_ImageFile, self.radioButton_SolidColor)
        DEMPropertiesWidget.setTabOrder(self.radioButton_SolidColor, self.colorButton_Color)
        DEMPropertiesWidget.setTabOrder(self.colorButton_Color, self.comboBox_TextureSize)
        DEMPropertiesWidget.setTabOrder(self.comboBox_TextureSize, self.horizontalSlider_Opacity)
        DEMPropertiesWidget.setTabOrder(self.horizontalSlider_Opacity, self.spinBox_Opacity)
        DEMPropertiesWidget.setTabOrder(self.spinBox_Opacity, self.checkBox_TransparentBackground)
        DEMPropertiesWidget.setTabOrder(self.checkBox_TransparentBackground, self.checkBox_Shading)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Shading, self.checkBox_Sides)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Sides, self.toolButton_SideColor)
        DEMPropertiesWidget.setTabOrder(self.toolButton_SideColor, self.checkBox_Frame)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Frame, self.toolButton_EdgeColor)
        DEMPropertiesWidget.setTabOrder(self.toolButton_EdgeColor, self.checkBox_Wireframe)
        DEMPropertiesWidget.setTabOrder(self.checkBox_Wireframe, self.toolButton_WireframeColor)
        DEMPropertiesWidget.setTabOrder(self.toolButton_WireframeColor, self.checkBox_Visible)

    def retranslateUi(self, DEMPropertiesWidget):
        _translate = QtCore.QCoreApplication.translate
        DEMPropertiesWidget.setWindowTitle(_translate("DEMPropertiesWidget", "Form"))
        self.groupBox_Geometry.setTitle(_translate("DEMPropertiesWidget", "&Geometry"))
        self.label_Resampling.setText(_translate("DEMPropertiesWidget", "Resampling level"))
        self.label_ResamplingLevel.setText(_translate("DEMPropertiesWidget", "2"))
        self.checkBox_Surroundings.setText(_translate("DEMPropertiesWidget", "Surrounding blocks"))
        self.label_3.setText(_translate("DEMPropertiesWidget", "Roughness"))
        self.label_2.setText(_translate("DEMPropertiesWidget", "Size"))
        self.checkBox_Clip.setText(_translate("DEMPropertiesWidget", "Clip DEM with polygon layer"))
        self.groupBox_Material.setTitle(_translate("DEMPropertiesWidget", "&Material"))
        self.label_5.setText(_translate("DEMPropertiesWidget", "Display type"))
        self.radioButton_MapCanvas.setText(_translate("DEMPropertiesWidget", "Map canvas image"))
        self.radioButton_LayerImage.setText(_translate("DEMPropertiesWidget", "Layer image"))
        self.toolButton_SelectLayer.setText(_translate("DEMPropertiesWidget", "Select layer(s)..."))
        self.radioButton_ImageFile.setText(_translate("DEMPropertiesWidget", "Image file"))
        self.toolButton_ImageFile.setText(_translate("DEMPropertiesWidget", "Browse..."))
        self.radioButton_SolidColor.setText(_translate("DEMPropertiesWidget", "Solid color"))
        self.label_17.setText(_translate("DEMPropertiesWidget", "Opacity (%)"))
        self.label_TextureSize.setText(_translate("DEMPropertiesWidget", "Texture width (px)"))
        self.checkBox_TransparentBackground.setText(_translate("DEMPropertiesWidget", "Transparent background"))
        self.checkBox_Shading.setText(_translate("DEMPropertiesWidget", "Enable shading"))
        self.groupBox_Others.setTitle(_translate("DEMPropertiesWidget", "&Other Options"))
        self.checkBox_Sides.setText(_translate("DEMPropertiesWidget", "Build sides"))
        self.checkBox_Frame.setText(_translate("DEMPropertiesWidget", "Add edges"))
        self.checkBox_Visible.setText(_translate("DEMPropertiesWidget", "Visible on load"))
        self.checkBox_Wireframe.setText(_translate("DEMPropertiesWidget", "Add quad wireframe"))
from qgis.gui import QgsColorButton
