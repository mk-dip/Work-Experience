import logging
import os
from Screenshot import Screenshot_Clipping
import shutil
import boto3


def screenshot():
    list_url = list_url.keys()  # list of urls to take a full-page screenshot of
    if not os.path.exists('Screenshots'):
        os.makedirs('Screenshots')
    agent = {"User-Agent": configurations["user_agent"]}  # this was based on a yaml file
    for i in list_url:
        screenshot_get(i, agent)
    shutil.make_archive('Screenshots', 'zip', 'Screenshots')  # convert folder into zip file
    shutil.rmtree(os.path.basename("Screenshots"))  # deletes folder after it gets converted into a zip file
    upload_file_to_s3("Screenshots.zip")


def screenshot_get(url, agent):
    ss = Screenshot_Clipping.Screenshot()
    browser = headless_browser_settings(agent)  # in the original script, we had created a "headless browser"
    browser.get(url)
    url = url.replace("http://", " ")
    url = url.replace("/", " ")
    url_message = url + ".png"  # each screenshot would be named after the url it accessed
    # print(url_message)
    ss.full_Screenshot(browser, save_path=os.path.basename("Screenshots"), image_name=url_message)
    browser.quit()


def upload_file_to_s3(file_name):
    session = boto3.Session(
        aws_access_key_id=configurations['aws_credentials']['aws_access_key_id'],  # this was based on a yaml file
        aws_secret_access_key=configurations['aws_credentials']['aws_secret_access_key']  # this was based on a yaml file
    )

    s3 = session.resource('s3')
    object = s3.Object(configurations['s3_bucket_name'], file_name)  # this was based on a yaml file that contained
    # the S3 bucket name that I am accessing
    object.put(Body=open(os.path.basename(file_name), 'rb'))
    if os.path.isdir(file_name) is True:
        shutil.rmtree(os.path.basename(file_name))  # deletes folder after it gets converted into a zip file
    elif os.path.isfile(file_name) is True:
        os.remove(os.path.basename(file_name))


def upload_log():
    upload_file_to_s3("activity.log")


def audit_log(message):
    logging.basicConfig(format='%(asctime)s - %(message)s', filename='activity.log', filemode='w', level=logging.INFO)
    logging.info(message)
