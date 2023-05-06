# Elevator Dispatch Simulator

The Elevator Dispatch Simulator is a simple application built with PyQt5 that simulates the elevator control panel in a building. Here's an overview of the project.

![Elevator Dispatch Simulator Screenshot](https://github.com/mao1207/Elevator-Dispatch-Simulator/blob/main/Resources/images/myElevator.png?raw=true)


## Key Features

1. Elevator cabin view: Each elevator has floor buttons, LCD displays, open/close buttons, and an alarm button.
2. Floor view: Each floor has up and down buttons, an LCD display for the current floor, and a combo box to select a floor.
3. Menu bar and status bar.

## Code Structure

1. `Ui_MainWindow` class: Sets up the main user interface for the application.
2. Slot functions:
   - `up_down_button`: Handles clicks on the up and down buttons in the floor view.
   - `press_button`: Handles clicks on the floor buttons in the elevator cabin view.
   - `switch_floor`: Handles changes in the selected floor in the combo box.
3. `Controller` class (imported from the `dispatch` module): Handles the elevator dispatch logic.

This project can also be considered analogous to an operating system, as it manages the flow of resources (elevators) and services (moving between floors) for multiple users. The dispatch algorithm can be thought of as a scheduling algorithm that determines which elevator should be sent to which floor, similar to how an operating system schedules tasks on a processor.

## How to Run

Ensure that you have Python and PyQt5 installed. To run the project, navigate to the project directory in a terminal or command prompt and run the following command:

```bash
python myElevator.py
```

## How to Package as an EXE File

To package the project as an executable file, ensure that you have `pyinstaller` installed. Then, run the following command in the project root directory:

```bash
pyinstaller --onefile --windowed myElevator.py
```

Once packaging is complete, you will find the generated EXE file in the `dist` folder located in the project root directory.
