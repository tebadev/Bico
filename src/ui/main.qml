import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ApplicationWindow {
    visible: true
    width: 340
    height: 320
    title: "Grabadora"
    color: "#1e1e2e"

    property real nivelGlobal: 0.0

    ColumnLayout {
        anchors.centerIn: parent
        spacing: 16
        width: 260

        Text {
            Layout.alignment: Qt.AlignHCenter
            text: "Bico Grabadora"
            font.pixelSize: 20
            font.bold: true
            color: "#cdd6f4"
        }

        // Campo nombre
        Rectangle {
            Layout.fillWidth: true
            height: 38
            radius: 6
            color: "#313244"
            border.color: campoNombre.activeFocus ? "#89b4fa" : "#45475a"
            border.width: 1

            TextInput {
                id: campoNombre
                anchors {
                    fill: parent
                    leftMargin: 10; rightMargin: 10
                }
                verticalAlignment: TextInput.AlignVCenter
                text: "grabacion.wav"
                color: "#cdd6f4"
                font.pixelSize: 13
                selectByMouse: true
                enabled: !grabadora.grabando
            }
        }

        // Botón grabar / detener
        Rectangle {
            Layout.fillWidth: true
            height: 42
            radius: 6
            color: grabadora.grabando ? "#f38ba8" : "#89b4fa"

            Text {
                anchors.centerIn: parent
                text: grabadora.grabando ? "⏹  Detener" : "⏺  Grabar"
                font.pixelSize: 14
                font.bold: true
                color: "#1e1e2e"
            }

            MouseArea {
                anchors.fill: parent
                cursorShape: Qt.PointingHandCursor
                onClicked: {
                    if (grabadora.grabando) {
                        grabadora.detenerGrabacion()
                    } else {
                        var nombre = campoNombre.text.trim()
                        if (nombre === "") nombre = "grabacion.wav"
                        if (!nombre.endsWith(".wav")) nombre += ".wav"
                        grabadora.iniciarGrabacion(nombre)
                    }
                }
            }
        }

        Row {
            Layout.alignment: Qt.AlignHCenter
            spacing: 4

            Repeater {
                id: barras
                model: 20

                Rectangle {
                    width: 8
                    height: grabadora.grabando
                        ? Math.max(6, nivelGlobal * 50 * (0.3 + Math.random() * 0.7))
                        : 6
                    anchors.verticalCenter: parent.verticalCenter
                    radius: 3
                    color: nivelGlobal > 0.8 ? '#2cc7ff' : '#306ed2'

                    Behavior on height { NumberAnimation { duration: 80 } }
                }
            }
        }

        // invisible para guardar el nivel
        Item {
            id: nivelBar
            property real nivel: 0.0
        }

        Text {
            id: labelMensaje
            Layout.alignment: Qt.AlignHCenter
            text: "Listo para grabar"
            font.pixelSize: 12
            color: "#6c7086"
        }
    }
    Timer {
        interval: 80
        repeat: true
        running: grabadora.grabando
        onTriggered: nivelGlobal = nivelGlobal + 0.0001
    }

    Connections {
        target: grabadora
        function onMensajeCambiado(msg) { labelMensaje.text = msg }
        function onNivelAudioCambiado(n) { nivelGlobal = n }
    }
}
