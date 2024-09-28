import json
import boto3

client = boto3.client("dynamodb")


def lambda_handler(event, context):
    ##
    response = client.scan(TableName="VisitorCountTable")

    ##
    if "Items" in response:
        # Save the response (JSON)
        count = response["Items"][0]["visitor_count"]["N"]
        count = int(count)
    else:
        count = 0
    count += 1

    response = client.update_item(
        ExpressionAttributeNames={
            "#VC": "visitor_count",
        },
        ExpressionAttributeValues={
            ":c": {
                "N": str(count),
            },
        },
        Key={
            "visitor_count_id": {
                "N": "1",
            },
        },
        ReturnValues="ALL_NEW",
        TableName="VisitorCountTable",
        UpdateExpression="SET #VC = :c",
    )

    return response
