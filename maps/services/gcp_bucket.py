from google.cloud import storage
from google.api_core.exceptions import BadRequest
from config import Config

class GCPBucketService:
    def __init__(self):
        # Inicializa el cliente de Google Cloud Storage
        self.client = storage.Client()
    
    def clear_bucket(self, bucket_name):
        """
        Elimina todos los archivos del bucket especificado.

        :param bucket_name: El nombre del bucket de GCP que se limpiará.
        """
        try:
            bucket = self.client.bucket(bucket_name)
            blobs = bucket.list_blobs()
            for blob in blobs:
                blob.delete()
                print(f"Archivo {blob.name} eliminado del bucket {bucket_name}.")
            print(f"Todos los archivos en el bucket {bucket_name} han sido eliminados.")
        except Exception as e:
            print(f"Error al limpiar el bucket: {e}")

    def upload_file(self, bucket_name, source_file_path, destination_blob_name):
        """
        Sube un archivo al bucket de Google Cloud Storage.
        """
        if bucket_name == Config.BUCKET_TO_CHECK:
            self.clear_bucket(bucket_name)

        try:
            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_filename(source_file_path)
            print(f"Archivo {source_file_path} subido a {destination_blob_name} en el bucket {bucket_name}.")
        except BadRequest as e:
            print(f"Error 400 al subir el archivo: {e.message}")
            raise Exception(f"Error 400 al subir el archivo a GCP: {e.message}")
        except Exception as e:
            print(f"Error general al subir el archivo: {e}")
            raise Exception(f"Error general al subir el archivo a GCP: {e}")