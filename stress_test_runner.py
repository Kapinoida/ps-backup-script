"""
This module contains functions for running stress tests on scripts.

It provides a function `run_stress_test` that executes a given script 
multiple times and logs the results.
"""

import subprocess
import time
import logging

# Configure logging
logging.basicConfig(
    filename="stress_test.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def run_stress_test(script, itera, n):
    """
    Run the stress test by executing the given script multiple times.

    Args:
        script (str): The path to the script to be executed.
        itera (int): The number of times to run the script.
        n (int): The argument to pass to the script.

    Returns:
        None
    """
    for i in range(itera):
        start_time = time.time()
        try:
            result = subprocess.run(
                ["python", script, str(n)],
                check=True,
                capture_output=True,
                text=True,
            )
            end_time = time.time()
            duration = end_time - start_time
            logging.info(
                "Iteration %d: Success - Duration: %.4f seconds - Output: %s",
                i + 1,
                duration,
                result.stdout.strip(),
            )
        except subprocess.CalledProcessError as e:
            end_time = time.time()
            duration = end_time - start_time
            logging.error(
                "Iteration %d: Failure - Duration: %.4f seconds - Error: %s",
                i + 1,
                duration,
                e.stderr.strip(),
            )


if __name__ == "__main__":
    SCRIPT_NAME = "api_writer.py"
    ITERATIONS = 10  # Number of times to run the script
    ARGUMENTS = 10000  # Argument to pass to the script (modify as needed)
    run_stress_test(SCRIPT_NAME, ITERATIONS, ARGUMENTS)
