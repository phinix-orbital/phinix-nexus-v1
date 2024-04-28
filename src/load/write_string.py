from load.write_data import WriteData
from validators.run_validator import RunValidator

class WriteString(WriteData):
    """
    Write String class using abstract write data class.
    """

    def __init__(
            self,
            file_path: str,
    ) -> None:
        super().__init__(file_path=file_path)
    
    @RunValidator.validate_instance_method(check="write_string")
    def write_file(
            self,
            output: str,
    ) -> None:
        with open(self.file_path, "wb") as f:
            f.write(output)