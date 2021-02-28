import QtQuick 2.15
import QtQuick.Window 2.15
import QtGraphicalEffects 1.12
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

Window {
    id: window
    width: 550
    height: 650
    minimumWidth: 550
    minimumHeight: 650
    maximumWidth: 500
    maximumHeight: 650
    visible: true
    title: qsTr("SheepIt Render Client")

    function delay(delayTime, cb) {
        timer.interval = delayTime
        timer.repeat = false
        timer.triggered.connect(cb)
        timer.start()
    }
    Rectangle {
        id: background
        color: "#eeeeee"
        anchors.fill: parent

        Rectangle {
            id: appContainer
            color: "#00000000"
            anchors.fill: parent

            Rectangle {
                id: topBar
                height: 68
                color: "#111314"
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.topMargin: 0

                Image {
                    id: image
                    width: 60
                    height: 100
                    anchors.left: parent.left
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    source: "assets/Branding.png"
                    layer.textureSize.height: 3
                    layer.textureSize.width: 3
                    antialiasing: true
                    anchors.bottomMargin: 10
                    anchors.topMargin: 10
                    anchors.leftMargin: 10
                    fillMode: Image.PreserveAspectFit
                    z: 1
                }
            }

            DropShadow {
                x: 30
                y: 264
                source: content
                anchors.fill: content
                //horizontalOffset: 1
                verticalOffset: 1
                radius: 7
                samples: 20
                color: "#80000000"
            }

            Rectangle {
                id: content
                color: "#00000000"
                border.width: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: topBar.bottom
                anchors.bottom: parent.bottom
                anchors.topMargin: 0

                Rectangle {
                    id: statusContainer
                    height: parent.height * 0.25
                    color: "#ffffff"
                    radius: 20
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.topMargin: 30
                    anchors.rightMargin: 30
                    anchors.leftMargin: 30

                    Rectangle {
                        id: progressBar
                        width: progressBackground.width * 0.21
                        color: "#2cc056"
                        anchors.left: progressBackground.left
                        anchors.top: progressBackground.top
                        anchors.bottom: progressBackground.bottom
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.leftMargin: 0
                        z: 1
                    }

                    Rectangle {
                        id: progressBackground
                        y: 100
                        height: 36
                        color: "#402cc056"
                        radius: 18
                        border.color: "#95dfaa"
                        border.width: 0
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 20
                        anchors.leftMargin: 20
                        anchors.bottomMargin: 20
                    }

                    Rectangle {
                        id: progressRadiusCover
                        color: "#00000000"
                        radius: 32.5
                        border.color: "#ffffff"
                        border.width: 15
                        anchors.left: progressBackground.left
                        anchors.right: progressBackground.right
                        anchors.top: progressBackground.top
                        anchors.bottom: progressBackground.bottom
                        anchors.rightMargin: -15
                        anchors.leftMargin: -15
                        anchors.bottomMargin: -14
                        anchors.topMargin: -14
                        z: 3
                    }

                    Text {
                        id: status
                        color: "#2cc056"
                        text: qsTr("Rendering")
                        anchors.left: parent.left
                        anchors.top: parent.top
                        font.pixelSize: 32
                        font.family: "Roboto"
                        anchors.topMargin: 20
                        anchors.leftMargin: 20
                        font.bold: false
                    }

                    Text {
                        id: engineDetails
                        x: 20
                        color: "#777777"
                        text: qsTr("Cycles - CPU")
                        anchors.top: status.bottom
                        font.pixelSize: 16
                        anchors.topMargin: 5
                        font.family: "Roboto"
                        z: 3
                    }

                    Text {
                        id: percentage
                        x: 397
                        color: "#777777"
                        text: qsTr("21%")
                        anchors.right: parent.right
                        anchors.top: parent.top
                        font.pixelSize: 26
                        horizontalAlignment: Text.AlignRight
                        verticalAlignment: Text.AlignBottom
                        anchors.topMargin: 20
                        anchors.rightMargin: 20
                        font.family: "Roboto"
                    }

                    Text {
                        id: timeElasped
                        x: 377
                        color: "#777777"
                        text: "1 min 2 sec"
                        anchors.right: parent.right
                        anchors.top: percentage.bottom
                        font.pixelSize: 16
                        anchors.topMargin: 10
                        anchors.rightMargin: 20
                        z: 3
                        font.family: "Roboto"
                    }
                }

                Rectangle {
                    id: sessionContainer
                    color: "#00000000"
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: statusContainer.bottom
                    anchors.bottom: parent.bottom
                    anchors.topMargin: 20
                    anchors.bottomMargin: 30
                    anchors.rightMargin: 30
                    anchors.leftMargin: 30

                    Rectangle {
                        id: lowerCon
                        y: 177
                        height: 200
                        color: "#ffffff"
                        radius: 20
                        anchors.left: parent.left
                        anchors.right: controlsContainer.left
                        anchors.bottom: parent.bottom
                        anchors.rightMargin: 20
                        anchors.bottomMargin: 0
                        anchors.leftMargin: 0
                    }

                    Rectangle {
                        id: upperCon
                        y: 1
                        color: "#ffffff"
                        radius: 20
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: controlsContainer.top
                        anchors.bottomMargin: 20
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.topMargin: 0

                        Text {
                            id: sessionTitle
                            color: "#48acf0"
                            text: qsTr("Session Info")
                            anchors.left: parent.left
                            anchors.top: parent.top
                            font.letterSpacing: -1.5
                            anchors.leftMargin: 15
                            anchors.topMargin: 15
                            font.pointSize: 22
                            font.styleName: "Bold"
                            font.family: "Roboto"
                        }

                        Rectangle {
                            id: lastImageRounded
                            color: "#00000000"
                            radius: 30
                            border.color: "#ffffff"
                            border.width: 15
                            anchors.left: lastImage.left
                            anchors.right: lastImage.right
                            anchors.top: lastImage.top
                            anchors.bottom: lastImage.bottom
                            anchors.leftMargin: -15
                            anchors.bottomMargin: -15
                            anchors.topMargin: -15
                            anchors.rightMargin: -15
                            z: 2
                        }

                        Image {
                            id: lastImage
                            x: 219
                            width: 255
                            height: 148
                            //anchors.left: previousFrameContainer.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            source: "assets/Bulb.png"
                            anchors.topMargin: 20
                            anchors.rightMargin: 17
                            anchors.leftMargin: 10
                            autoTransform: false
                            asynchronous: true
                            layer.wrapMode: ShaderEffectSource.ClampToEdge
                            antialiasing: true
                            clip: false
                            fillMode: Image.PreserveAspectCrop
                            z: 1
                        }

                        Rectangle {
                            x: 219
                            width: 256
                            height: 40
                            color: "#ffffff"
                            border.width: 0
                            anchors.right: lastImage.left
                            anchors.top: parent.top
                            anchors.topMargin: 180
                            anchors.rightMargin: -255
                            Text {
                                id: titlePointsEarned1
                                color: "#575a68"
                                text: qsTr("Last Frame")
                                anchors.left: parent.left
                                anchors.top: parent.top
                                font.letterSpacing: -1
                                font.pixelSize: 18
                                anchors.topMargin: 0
                                font.styleName: "Bold"
                                font.capitalization: Font.AllUppercase
                                anchors.leftMargin: 0
                                font.family: "Roboto"
                            }

                            Text {
                                id: pointsEarned1
                                width: 248
                                height: 21
                                color: "#2d3142"
                                text: qsTr("3 mins 42 seconds")
                                anchors.left: parent.left
                                anchors.top: titlePointsEarned1.bottom
                                font.pixelSize: 20
                                anchors.topMargin: 0
                                anchors.leftMargin: 0
                                font.family: "Roboto"
                            }
                            Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                        }

                        ColumnLayout {
                            id: columnLayout
                            width: 157
                            anchors.left: parent.left
                            anchors.top: sessionTitle.bottom
                            anchors.bottom: parent.bottom
                            spacing: 20
                            anchors.bottomMargin: -105
                            anchors.topMargin: 10
                            anchors.leftMargin: 15

                            Rectangle {
                                width: 152
                                height: 40
                                color: "#ffffff"
                                Layout.alignment: Qt.AlignLeft | Qt.AlignTop

                                Text {
                                    id: titlePointsEarned
                                    color: "#575a68"
                                    text: qsTr("Points Earned")
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    font.letterSpacing: -1
                                    font.pixelSize: 18
                                    font.capitalization: Font.AllUppercase
                                    font.styleName: "Bold"
                                    anchors.leftMargin: 0
                                    anchors.topMargin: 0
                                    font.family: "Roboto"
                                }

                                Text {
                                    id: pointsEarned
                                    width: 126
                                    height: 21
                                    color: "#2d3142"
                                    text: qsTr("3,214")
                                    anchors.left: parent.left
                                    anchors.top: titlePointsEarned.bottom
                                    font.pixelSize: 20
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }
                            }

                            Rectangle {
                                width: 152
                                height: 40
                                color: "#ffffff"
                                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                                Text {
                                    id: titleCurrentPoints
                                    color: "#575a68"
                                    text: qsTr("Current Points")
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    font.letterSpacing: -1
                                    font.pixelSize: 18
                                    font.capitalization: Font.AllUppercase
                                    font.styleName: "Bold"
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }

                                Text {
                                    id: currentPoints
                                    width: 126
                                    height: 21
                                    color: "#2d3142"
                                    text: qsTr("85,392")
                                    anchors.left: parent.left
                                    anchors.top: titleCurrentPoints.bottom
                                    font.pixelSize: 20
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }
                            }

                            Rectangle {
                                width: 152
                                height: 40
                                color: "#ffffff"
                                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                                Text {
                                    id: titleFramesRendered
                                    color: "#575a68"
                                    text: qsTr("Frames Rendered")
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    font.letterSpacing: -1
                                    font.pixelSize: 18
                                    font.capitalization: Font.AllUppercase
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }

                                Text {
                                    id: framesRendered
                                    width: 126
                                    height: 21
                                    color: "#2d3142"
                                    text: qsTr("3")
                                    anchors.left: parent.left
                                    anchors.top: titleFramesRendered.bottom
                                    font.pixelSize: 20
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }
                            }

                            Rectangle {
                                width: 152
                                height: 40
                                color: "#ffffff"
                                Layout.alignment: Qt.AlignLeft | Qt.AlignTop
                                Text {
                                    id: titleSessionDuration
                                    color: "#575a68"
                                    text: qsTr("Session Duration")
                                    anchors.left: parent.left
                                    anchors.top: parent.top
                                    font.letterSpacing: -1
                                    font.pixelSize: 18
                                    font.capitalization: Font.AllUppercase
                                    font.styleName: "Bold"
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }

                                Text {
                                    id: sessionDuration
                                    width: 182
                                    height: 21
                                    color: "#2d3142"
                                    text: qsTr("8 mins 7 seconds")
                                    anchors.left: parent.left
                                    anchors.top: titleSessionDuration.bottom
                                    font.letterSpacing: 0
                                    font.pixelSize: 20
                                    anchors.topMargin: 0
                                    anchors.leftMargin: 0
                                    font.family: "Roboto"
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: controlsContainer
                        x: 268
                        y: 251
                        width: parent.width * 0.575
                        height: 100
                        color: "#ffffff"
                        radius: 20
                        border.width: 0
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        anchors.bottomMargin: 0
                        anchors.rightMargin: 0
                        z: 10

                        RowLayout {
                            id: rowLayout
                            height: 100
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.rightMargin: 20
                            anchors.leftMargin: 20
                            spacing: 17.5
                            z: 2

                            Rectangle {
                                id: pauseButton
                                y: (parent.height / 2) - this.height / 2
                                color: pauseMouseArea.containsMouse ? "#429EDC" : "#48ACF0"
                                radius: 10
                                Layout.topMargin: -4
                                Layout.bottomMargin: 0
                                Layout.fillWidth: true
                                height: this.width

                                MouseArea {
                                    id: pauseMouseArea
                                    anchors.fill: parent
                                    z: 2
                                    hoverEnabled: true
                                    onEntered: {
                                        delay(1000, () => toolTipPause.visible
                                              = pauseMouseArea.containsMouse)
                                    }
                                    onExited: {
                                        toolTipPause.visible = false
                                    }
                                    onClicked: {
                                        backend.togglePause()
                                    }
                                }

                                Image {
                                    id: pauseButtonIcon
                                    anchors.fill: parent
                                    source: "assets/Pause.svg"
                                    clip: true
                                    anchors.rightMargin: 15
                                    anchors.leftMargin: 15
                                    anchors.bottomMargin: 15
                                    anchors.topMargin: 15
                                    layer.mipmap: false
                                    antialiasing: true
                                    fillMode: Image.PreserveAspectFit
                                }

                                Rectangle {
                                    visible: false
                                    id: toolTipPause
                                    x: 0
                                    y: 17
                                    width: 131
                                    height: 38
                                    color: "#000000"
                                    radius: 8
                                    anchors.bottom: parent.top
                                    anchors.bottomMargin: 8
                                    anchors.horizontalCenter: parent.horizontalCenter

                                    Rectangle {
                                        id: toolTipPauseBackground
                                        x: 61
                                        y: 37
                                        width: 12
                                        height: 12
                                        color: "#000000"
                                        anchors.bottom: parent.bottom
                                        rotation: 45
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        anchors.bottomMargin: -6
                                    }

                                    Text {
                                        id: toolTipPauseText
                                        visible: true
                                        color: "#ffffff"
                                        text: qsTr("Pause")
                                        anchors.fill: parent
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        font.family: "Roboto"
                                        font.pointSize: 14
                                        font.styleName: "Medium"
                                        renderType: Text.NativeRendering
                                    }
                                    z: 100
                                }
                                //Layout.fillHeight: true
                            }
                            Rectangle {
                                id: blockButton
                                y: (parent.height / 2) - this.height / 2
                                color: blockMouseArea.containsMouse ? "#429EDC" : "#48ACF0"
                                radius: 10
                                Layout.topMargin: -4
                                Layout.bottomMargin: 0
                                Layout.fillWidth: true
                                height: this.width

                                MouseArea {
                                    id: blockMouseArea
                                    anchors.fill: parent
                                    z: 2
                                    hoverEnabled: true
                                    onEntered: {
                                        delay(1000, () => toolTipBlock.visible
                                              = blockMouseArea.containsMouse)
                                    }
                                    onExited: {
                                        toolTipBlock.visible = false
                                    }
                                }

                                Image {
                                    id: blockButtonIcon
                                    anchors.fill: parent
                                    source: "assets/Block.svg"
                                    clip: true
                                    anchors.rightMargin: 15
                                    anchors.leftMargin: 15
                                    anchors.bottomMargin: 15
                                    anchors.topMargin: 15
                                    layer.mipmap: false
                                    antialiasing: true
                                    fillMode: Image.PreserveAspectFit
                                }

                                Rectangle {
                                    visible: false
                                    id: toolTipBlock
                                    x: 0
                                    y: 17
                                    width: 131
                                    height: 38
                                    color: "#000000"
                                    radius: 8
                                    anchors.bottom: parent.top
                                    anchors.bottomMargin: 8
                                    anchors.horizontalCenter: parent.horizontalCenter

                                    Rectangle {
                                        id: toolTipBlockBackground
                                        x: 61
                                        y: 37
                                        width: 12
                                        height: 12
                                        color: "#000000"
                                        anchors.bottom: parent.bottom
                                        rotation: 45
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        anchors.bottomMargin: -6
                                    }

                                    Text {
                                        id: toolTipBlockText
                                        visible: true
                                        color: "#ffffff"
                                        text: qsTr("Block")
                                        anchors.fill: parent
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        font.family: "Roboto"
                                        font.pointSize: 14
                                        font.styleName: "Medium"
                                        renderType: Text.NativeRendering
                                    }
                                    z: 100
                                }
                                //Layout.fillHeight: true
                            }

                            Rectangle {
                                id: exitButton
                                y: (parent.height / 2) - this.height / 2
                                color: exitMouseArea.containsMouse ? "#429EDC" : "#48ACF0"
                                radius: 10
                                Layout.topMargin: -4
                                Layout.bottomMargin: 0
                                Layout.fillWidth: true
                                height: this.width

                                MouseArea {
                                    id: exitMouseArea
                                    anchors.fill: parent
                                    z: 2
                                    hoverEnabled: true
                                    onEntered: {
                                        delay(1000, () => toolTipExit.visible
                                              = exitMouseArea.containsMouse)
                                    }
                                    onExited: {
                                        toolTipExit.visible = false
                                    }
                                }

                                Image {
                                    id: exitButtonIcon
                                    anchors.fill: parent
                                    source: "assets/Exit.svg"
                                    clip: true
                                    anchors.rightMargin: 15
                                    anchors.leftMargin: 15
                                    anchors.bottomMargin: 15
                                    anchors.topMargin: 15
                                    layer.mipmap: false
                                    antialiasing: true
                                    fillMode: Image.PreserveAspectFit
                                }

                                Rectangle {
                                    visible: false
                                    id: toolTipExit
                                    x: 0
                                    y: 17
                                    width: 131
                                    height: 38
                                    color: "#000000"
                                    radius: 8
                                    anchors.bottom: parent.top
                                    anchors.bottomMargin: 8
                                    anchors.horizontalCenter: parent.horizontalCenter

                                    Rectangle {
                                        id: toolTipExitBackground
                                        x: 61
                                        y: 37
                                        width: 12
                                        height: 12
                                        color: "#000000"
                                        anchors.bottom: parent.bottom
                                        rotation: 45
                                        anchors.horizontalCenter: parent.horizontalCenter
                                        anchors.bottomMargin: -6
                                    }

                                    Text {
                                        id: toolTipExitText
                                        visible: true
                                        color: "#ffffff"
                                        text: qsTr("Exit")
                                        anchors.fill: parent
                                        horizontalAlignment: Text.AlignHCenter
                                        verticalAlignment: Text.AlignVCenter
                                        font.family: "Roboto"
                                        font.pointSize: 14
                                        font.styleName: "Medium"
                                        renderType: Text.NativeRendering
                                    }
                                    z: 100
                                }
                                //Layout.fillHeight: true
                            }
                        }
                    }
                }
            }
        }
    }
    Timer {
        id: timer
    }
    Connections {
        target: backend

        function onSetPause(paused) {
            console.log(paused)
            if (paused) {
                pauseButtonIcon.source = "assets/Start.svg"
            } else {
                pauseButtonIcon.source = "assets/Pause.svg"
            }
        }
    }
}

/*##^##
Designer {
    D{i:0;formeditorZoom:0.75}
}
##^##*/

