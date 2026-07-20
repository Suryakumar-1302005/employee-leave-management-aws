import pymysql
import boto3

# SNS Client
sns = boto3.client("sns")

TOPIC_ARN = "arn:aws:sns:ap-south-1:930069301173:Employeeleavenotification"
print("Starting Lambda")
connection = pymysql.connect(
    host="leavedb.crwek2okyy3g.ap-south-1.rds.amazonaws.com",
    user="admin",
    password="YOUR_PASSWORD",
    database="leavedb"
)
print("Connected to RDS")

def lambda_handler(event, context):

    cursor = connection.cursor()
    

    cursor.execute("""
        SELECT id, employee_name, leave_days
        FROM leaves
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    if row is None:
        return {
            "statusCode": 404,
            "body": "No leave requests found."
        }

    leave_id, employee_name, leave_days = row

    if leave_days <= 5:
        status = "Approved"
    else:
        status = "Pending Manager Approval"

    cursor.execute(
        "UPDATE leaves SET status=%s WHERE id=%s",
        (status, leave_id)
    )
    connection.commit()

    message = (
        f"Employee: {employee_name}\n"
        f"Leave Days: {leave_days}\n"
        f"Status: {status}"
    )

    sns.publish(
        TopicArn=TOPIC_ARN,
        Subject="Employee Leave Status",
        Message=message
    )

    return {
        "statusCode": 200,
        "body": message
    }