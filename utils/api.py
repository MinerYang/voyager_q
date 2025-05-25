from io import BytesIO
import openai
import boto3, logging, httpx, os
from botocore.exceptions import NoCredentialsError

def botclient():
    return openai.OpenAI(
        timeout=60.0,
        base_url=os.getenv("OPENAI_API_URL"),
        api_key=os.getenv("OPENAI_API_KEY"),
        http_client=httpx.Client(verify=False)
    )


def make_api_request(user_input):
    """
    Make request to gpt

    :param user_input: User input data
    :return: Content from reponse, else None
    """
    try:
        response = botclient().chat.completions.create(
            # model="deepseek-reasoner", 
            model="gpt-4o-mini",
            messages=[
                {
                "role": "user",
                "content": user_input,
                }
            ],
            max_tokens=500
        )
        text =  response.choices[0].message.content.strip()
        return text, None
    except openai.APIConnectionError as e:
        return None, e
    except openai.RateLimitError as e:
        return None, e
    except openai.APIStatusError as e:
        return None, e
    except openai.OpenAIError as e:
        return None, e


def upload_file_to_s3(data, bucket, object_name):
    """
    Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket name
    :param object_name: S3 object name.
    :return: True if upload succeeded, else False
    """

    # Create an S3 client
    s3_client = boto3.client('s3')

    try:
        s3_client.upload_fileobj(BytesIO(data.encode('utf-8')), bucket, object_name)
    except NoCredentialsError:
        logging.error("Credentials not available.")
        return False
    except Exception as e:
        logging.error(f"Error uploading file: {e}")
        return False
    return True