import os
import io
import tempfile
import boto3
import json
from docx2pdf import convert

s3_bucket_name = "store-pdf-new"

def lambda_handler(event, context):
    try:
       
        file_content = event['body']

       
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file = os.path.join(temp_dir, 'temp.docx')
            with open(temp_file, 'wb') as f:
                f.write(file_content)

            output_file = os.path.join(temp_dir, 'output.pdf')
            convert(temp_file, output_file)

            # Upload the PDF to S3 bucket
            s3 = boto3.client('s3')
            with open(output_file, 'rb') as f:
                s3.upload_fileobj(f, s3_bucket_name, 'converted-document.pdf')

        
        return {
            'statusCode': 200,
            'body': 'File converted and uploaded successfully.'
        }
    except Exception as e:
        
        return {
            'statusCode': 500,
             'body': f'An error occurred: {str(e)}'
        }