# Inventory Management System

Welcome to the Inventory Management System, a Python-based application with a Tkinter GUI and MySQL backend for efficient inventory handling.

## Features 🚀

- **Inventory Operations (`inv` Table):**
  - Add, update, search, and remove items.
  - Visualize current inventory status.

- **Additional Inventory (`inv1` Table):**
  - Manage supplementary inventory items seamlessly.

- **Final Inventory Calculation:**
  - Calculate final quantities with smart inventory adjustments.

## Prerequisites 🛠️

- Python 3.x
- MySQL server

## Setup Guide 📋

1. **Database Setup:**
   - Install and start MySQL server.
   - Create a database named `inventory`.
   - Execute `schema.sql` to set up required tables (`inv`, `inv1`, `final`).

2. **Python Dependencies:**
   - Install necessary packages using `pip install -r requirements.txt`.

3. **Configuration:**
   - Adjust database settings in `main.py` to match your MySQL credentials.

## How to Use 📝

1. **Launch the Application:**
   - Run `python main.py` to open the user-friendly GUI.

2. **Perform Operations:**
   - Manage `inv` items: add, update, search, and remove.
   - Handle `inv1` items separately: add and remove.

3. **View Final Inventory:**
   - Check calculated final quantities in the `final` table.

## Screenshots 🖼️

![Screenshot](images/Screenshot%202024-06-23%20123550.png)
*Caption: Main Inventory Interface*


## Contributing 🤝

Contributions are welcome! Fork the repository and submit pull requests to enhance the system.

## License 📄

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

🌟 Thank you for using our Inventory Management System! For issues or queries, please [open an issue](https://github.com/yourusername/inventory-management/issues).

