# html_logger.py

# Import datetime for timestamps, Path for filesystem paths,
# and html.escape to safely escape text for HTML output.
from datetime import datetime
from pathlib import Path
import html


class HTMLLogger:
    def __init__(self, output_dir="reports", filename=None):
        """
        Initialize the HTML logger.

        - Creates the output directory (default: 'reports')
        - Generates a timestamped filename if none is provided
        - Prepares a list to store log messages
        """
        project_root = Path(__file__).resolve().parent.parent
        # Force reports folder to be created at project root
        self.output_dir = project_root / output_dir

        # Ensure the directory exists (create if missing)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # If no filename is provided, generate one using a timestamp
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            filename = f"log-{timestamp}.html"

        # Full path to the HTML report file
        self.filepath = self.output_dir / filename

        # List to store log entries (category, timestamp, message)
        self.messages = []

    def _timestamp(self):
        """
        Returns the current timestamp in a readable format.
        Example: '2026-02-17 12:45:30'
        """
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, category, message):
        """
        Core logging function.

        - Escapes HTML characters in the message
        - Adds a timestamp
        - Stores the log entry in the messages list
        """

        # Escape HTML special characters to avoid breaking the HTML file
        safe = html.escape(message)

        # Get current timestamp
        ts = self._timestamp()

        # Store the log entry as a tuple
        self.messages.append((category.upper(), ts, safe))

    # Convenience methods for different log types
    def verify(self, msg):
        """Log a verification step (green)."""
        self.log("VERIFY", msg)

    def step(self, msg):
        """Log a normal step (black)."""
        self.log("STEP", msg)

    def error(self, msg):
        """Log an error message (red)."""
        self.log("ERROR", msg)

    def save(self):
        """
        Writes all collected log messages into an HTML file.

        - Adds CSS styling
        - Writes each log entry with color coding and timestamps
        """

        # Open the HTML file for writing
        with open(self.filepath, "w", encoding="utf-8") as f:

            # Start HTML document and CSS styles
            f.write("<html><head><style>")
            f.write("""
                body { font-family: Arial, sans-serif; padding: 20px; }
                .entry { margin-bottom: 8px; }
                .timestamp { color: #555; margin-right: 8px; }

                .VERIFY { color: #2ecc71; font-weight: bold; }   /* green */
                .STEP   { color: #000000; }                      /* black */
                .ERROR  { color: #e74c3c; font-weight: bold; }   /* red */
            """)
            f.write("</style></head><body>")

            # Header for the report
            f.write("<h2>Test Log Output</h2>")

            # Write each log entry into the HTML file
            for category, ts, msg in self.messages:
                f.write(
                    f'<div class="entry {category}">'
                    f'<span class="timestamp">{ts}</span>'
                    f'[{category}] {msg}'
                    f'</div>'
                )

            # Close HTML document
            f.write("</body></html>")
