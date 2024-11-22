
# `num` Class: High-Precision Arithmetic Library

The `num` class is a Python library for handling **high-precision arithmetic** using a segment-based representation of numbers. It enables accurate operations with very large or small numbers.

## Features

- **Segment-Based Representation**: Efficient handling of large numbers by splitting them into chunks.
- **Precision Arithmetic**: Perform addition, subtraction, multiplication, and division with arbitrary precision.
- **Rounding and Truncation**:
  - Support for `round()`, `ceil()`, and `floor()`.
  - Specify precision levels.
- **Signed Numbers**: Handles positive and negative numbers seamlessly.
- **Comparisons**: Supports equality and inequality checks with `==`, `>`, `<`, etc.

## Download and Installation

### Option 1: Clone the Repository

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/num-library.git
   cd num-library
   ```

2. Install the library:
   ```bash
   pip install .
   ```

### Option 2: Download the ZIP

1. Go to the [GitHub repository](https://github.com/yourusername/num-library).
2. Click on the **Code** button and select **Download ZIP**.
3. Extract the ZIP file, navigate to the extracted folder, and run:
   ```bash
   pip install .
   ```

## Usage

Import the library and use it in your Python code:

```python
from num import num

# Initialize numbers
a = num(12345)
b = num("67890.123")

# Perform arithmetic
print(a + b)  # num("80235.123")

# Round, floor, and ceiling
print(b.__round__(2))  # num("67890.12")
print(b.__ceil__())    # num("67891")
print(b.__floor__())   # num("67890")
```

## Development and Contribution

To contribute to the project:

1. Fork this repository.
2. Create a feature branch.
3. Write and test your code.
4. Submit a pull request.

Install the development dependencies:

```bash
pip install -e .[dev]
```

Run the tests to ensure everything works correctly:

```bash
pytest
```

## License

This project is licensed under the [MIT License](LICENSE).

## Author

Created by **Your Name**. Feel free to reach out via GitHub for feedback or questions!
