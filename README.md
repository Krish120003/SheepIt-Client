![Promotional Banner](/Banner.png)

# SheepIt Client

**This project is outdated and no longer maintained.**

[SheepIt Renderfarm](https://www.sheepit-renderfarm.com/) is a community-driven, distributed render platform specifically designed for rendering 3D animations and scenes created with [Blender](https://blender.org). SheepIt is free to use, and relies on users contributing their own computers to the network in order to render their own projects. The more you contribute, the more you can render.

## Inspiration

SheepIt is a great platform, but it has a few shortcomings. The render client is provided as a .jar file, which can be a deterrent for some users, since it requires the correct version of Java to be installed. Additionally, the client provides a poor user experience, with only textual output on the UI. This project aims to solve these issues by providing a cross-platform, user-friendly GUI client for SheepIt.

## Design

Here is a sample of the design for the SheepIt Client. The design is subject to change, and is not final. Most of the design has been implemented in the current version of the client, using Qt's QML language.

![Design](/DesignDemo.png)

## Features

Some of these features are not yet implemented, but are planned for future releases.

- Cross-platform (Windows, macOS, Linux) support (due to Qt framework)
- Simplified, user-friendly GUI
- Progress bar for binary downloads
- Progress bar for project downloads/uploads
- Progress bar for current render time estimates
- Easy client configuration
- Automatic client updates
- No Java installation required
- Light/Dark mode support

## Installation

There is no current release of the SheepIt Client due to stagnated development, and updates to the SheepIt API.

## Built With

- [Python](https://www.python.org/) - Programming language
- [Qt](https://www.qt.io/) - Cross-platform application framework
- [PySide2](https://wiki.qt.io/Qt_for_Python) - Python bindings for Qt
- [PyInstaller](https://www.pyinstaller.org/) - Python application packaging
- [Requests](https://requests.readthedocs.io/en/master/) - HTTP library for Python
- [bpy](https://docs.blender.org/api/current/bpy.html) - Blender Python API for GPU detection
- [Blender](https://www.blender.org/) - 3D rendering suite

## Contributing

This project is no longer maintained, and is provided as-is. If you would like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [SheepIt Renderfarm](https://www.sheepit-renderfarm.com/) - For providing the SheepIt API service
- [PySide2](https://wiki.qt.io/Qt_for_Python) - For providing the Python bindings for Qt, licensed under the LGPLv3 license
