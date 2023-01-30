from PIL import Image
import boto3
import os
import sys

# this code was not running coz I don't have amazon buckets account.
# The code was written by my personal understanding. In my previous job, we use different data cloud calls "coscmd"
# It's basically the same with s3 buckets. So I can handle this problem after few attemps.
s3_client = boto3.client('s3',
                      aws_access_key_id='<your_access_key_id>',
                      aws_secret_access_key='<your_secret_access_key>'
                      )
s3 = boto3.resource(
            service_name='s3',
            region_name="<region_name>",
            aws_access_key_id='<your_access_key_id>',
            aws_secret_access_key='<your_secret_access_key>',
        )

def determine_transparent(source_bucket, destination_bucket):
    # connect & list all the objects
    try:
        objects = s3_client.list_objects_v2(Bucket=source_bucket)
    except:
        print("list objects error")
        return
    try:
        bucket = s3.Bucket(source_bucket)
    except:
        print("connect to the bucket error")
        return
    # create local folder to save the images
    target_dir = "output"
    os.makedirs(target_dir, exist_ok=True)
    # traverse all the files
    for obj in objects['Contents']:
        filename = obj['Key']
        # if the file is an image, then process it
        if(filename.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff'))):
            local_filename = os.path.join(target_dir, filename.split("/")[-1])
            try:
                # download the image file
                bucket.download_file(filename, local_filename)
            except:
                print(f"{filename} download error")
                continue
            try:
                # open and load the mode of the image
                image = Image.open(local_filename)
                mode = image.mode
            except:
                print(f"open local file failed {filename}")
                continue
            if mode != "RGBA":
                try:
                    # upload non RGBA image
                    s3_client.upload_file(local_filename, destination_bucket, "transparent_images/" + local_filename.split("/")[-1])
                except:
                    print(f"upload file failed : {filename}")
                    continue
            else:
                try:
                    # log the transparent image
                    with open("logs_with_transparent.txt", 'a+') as f:
                        f.write(filename + '\n')
                except:
                    print(f"log transparent file failed : {filename}")


if __name__ == '__main__':
    args_length = len(sys.argv) if sys.argv else 0
    if args_length != 2:
        print("wrong parameter")

    determine_transparent(sys.argv[1], sys.argv[2])
