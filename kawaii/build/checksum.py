import click
import hashlib
from hashlib import algorithms_available
def get_checksum_config(source, sourcee):
    if "checksum" in sourcee:
        if "checksum_type" in sourcee:
            checksum_type = sourcee["checksum_type"]
            checksum = sourcee["checksum"]
        else: 
            splitted = sourcee["checksum"].split(":")
            
            if 1 in splitted:
                checksum_type = splitted[0]
                checksum = splitted[1:]
            else:
                click.echo(f"Checksum type for {source} not found", error=True)
                exit(1)
                        
        if not checksum_type in algorithms_available:
            click.echo(f"{checksum_type} is not an available checksum type!!", error=True) 
            exit(1)

        return (checksum, checksum_type)

def get_checksum(type, callback):
      m = hashlib.new(type)
      callback(m)
                            
      return m.hexdigest()

def file_checksum(type, path):
    return get_checksum(type, lambda m : _file_checksum(m, path))
    
def _file_checksum(m, path):
       with open(path, mode="r") as file:
            chunk = 0

            while chunk == b"":
                chunk = file.read(1024)
                m.update(chunk)