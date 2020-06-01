# -*- coding: utf-8 -*-
"""
/***************************************************************************
 buildpointcloud.py

 begin     : 2020-05-15
 copyright : (C) 2020 Minoru Akagi
 email     : akaginch@gmail.com
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
from .conf import DEBUG_MODE
from .buildlayer import LayerBuilder


class PointCloudLayerBuilder(LayerBuilder):

    def __init__(self, settings, layer, pathRoot="", urlRoot="", progress=None, logMessage=None):
        LayerBuilder.__init__(self, settings, None, layer, pathRoot, urlRoot, progress, logMessage)

    def build(self, build_blocks=False):
        d = {
            "type": "layer",
            "id": self.layer.jsLayerId,
            "properties": self.layerProperties()
        }

        if not self.settings.isPreview:
            url = d["properties"]["url"]
            self.logMessage("URL: {}".format(url))
            if url.startswith("file:"):
                self.logMessage("""
Point cloud data files in Potree format will not be copied to the output data directory.
You need to upload them to a web server and replace the cloud.js file URL in the scene.js{}
with valid one that points to the cloud.js file on the web server.""".format("" if self.settings.localMode else "on"))

        if DEBUG_MODE:
            d["PROPERTIES"] = self.properties

        return d

    def layerProperties(self):
        p = LayerBuilder.layerProperties(self)
        p["type"] = "pc"
        p["url"] = self.properties.get("url")
        p["opacity"] = self.properties.get("spinBox_Opacity", 100) / 100
        p["colorType"] = self.properties.get("comboBox_ColorType", "RGB")
        if p["colorType"] == "COLOR":
            p["color"] = int(self.properties.get("colorButton_Color", 0), 16)
        p["boxVisible"] = self.properties.get("checkBox_BoxVisible", False)
        return p

    def blocks(self):
        return []