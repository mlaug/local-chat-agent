import io
import os
import sys
import uuid

from pydub import AudioSegment

from flow.FlowStep import FlowStep


class ConvertToMp3(FlowStep):
    # Expects audio data (bytes) and returns a status message (string).
    expected_input_types = (bytes,)
    output_type = str

    def execute(self, input_data):
        audio = AudioSegment.from_file(io.BytesIO(input_data), format="wav")

        # Determine the root directory of the application
        root_dir = os.getenv("TMP_DIR") or os.path.dirname(os.path.abspath(sys.argv[0]))

        # Ensure the tmp directory exists in the root directory
        tmp_dir = os.path.join(root_dir, "tmp")
        os.makedirs(tmp_dir, exist_ok=True)

        # Generate a unique filename
        filename = f"{uuid.uuid4()}.mp3"
        pathname = os.path.join(tmp_dir, filename)

        # Export the AudioSegment to MP3 format and save to file
        audio.export(pathname, format="mp3")

        # Return the filename
        return filename
