# Example Integration

This is an example integration used to demonstrate how integrations can be created for Sporact

## Usage

- Copy this integration folder and rename it
- Make the required changes to the integration.json file
- Running tests:
    ```sh
    python -m unittest discover  # To run all tests
    python -m unittest tests.test_module_name.ClassName  # To run a class containing tests
    python -m unittest tests.test_module_name.ClassName.function   # To run a specific function containing a test
    ```
- To install the integration in sporact, zip this folder and drop it in the dropzone of the available integrations page in sporact

