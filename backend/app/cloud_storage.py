import boto3
from botocore.exceptions import NoCredentialsError, ClientError
import os
from fastapi import HTTPException, status
from io import BytesIO

class YandexStorageClient:
    """
    Клиент для работы с Yandex Object Storage (S3-совместимое API)
    Заменяет сохранение файлов на локальном диске.
    """
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            endpoint_url=os.getenv('YC_STORAGE_ENDPOINT'),
            aws_access_key_id=os.getenv('YC_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('YC_SECRET_ACCESS_KEY')
        )
        self.bucket_name = os.getenv('YC_BUCKET_NAME')

    async def upload_file(self, file_content: bytes, file_name: str) -> str:
        """
        Загружает файл в облачное хранилище и возвращает публичный URL
        """
        try:
            # Создаем файловый объект из байтов
            file_obj = BytesIO(file_content)
            
            # Загружаем в облачное хранилище
            self.s3_client.upload_fileobj(
                file_obj,
                self.bucket_name,
                file_name
            )
            
            # Формируем публичный URL к файлу
            return f"https://{self.bucket_name}.storage.yandexcloud.net/{file_name}"
            
        except NoCredentialsError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Cloud storage credentials not configured"
            )
        except ClientError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Cloud storage error: {str(e)}"
            )

# Создаем глобальный экземпляр клиента для использования во всем приложении
storage_client = YandexStorageClient()