from __future__ import print_function
import json
import logging
import boto3
from botocore.exceptions import ClientError
from .exceptions import ProviderError
import settings
from .base_util import AWSUtil
import decimal
from boto3.dynamodb.conditions import Key, Attr

logger = logging.getLogger(__name__)

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)

class AWSProvider() :

    @staticmethod
    def send_event(ctx,messageDict,service_name):
        try:
            client = boto3.client('lambda', region_name=settings.AWS_REGION)
            ret = client.invoke(
                FunctionName=service_name,
                InvocationType='Event',
                LogType='None',
                Payload=bytes(json.dumps(messageDict), "utf8")
            )
            return ret
        except ClientError as e:
            #logger.error("Unexpected boto client Error", extra=dict(ctx, messageDict, e))
            raise ProviderError(e)

    @staticmethod
    def send_mail(req_context, vars, from1=None, to=None):
        from .ses import send_mail as send_mailx
        return send_mailx(req_context, vars, from1, to)

    @staticmethod
    def get_util(req_context):
        return AWSUtil()

    @staticmethod
    def get_context():
        """

        :return:
        """
        return AWSUtil().get_context()

    def get_db_item(self, item_id, table_name):
        """

        :return:
        """
        try:
            resp = self.dynamodb.get_item(
                TableName=table_name,
                Key={
                    'ItemId': {'S': item_id}
                }
            )
            item = resp.get('Item')
            if not item:
                raise ProviderError('Item does not exist')

            return item
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ProviderError(e.response['Error']['Message'])

    def put_db_item(self, item, table_name):
        try:
            resp = self.dynamodb.put_item(
                TableName=table_name,
                Item=item
            )

            itemx = resp.get('Item')
            if not itemx:
                raise ProviderError('Item does not save')

            return itemx
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ProviderError(e.response['Error']['Message'])

    def update_db_item(self,key, item, table_name):
        try:
            resp = self.dynamodb.update_item(
                TableName=table_name,
                Key=key,
                UpdateExpression="set info.rating = :r, info.plot=:p, info.actors=:a",
                ExpressionAttributeValues={
                    ':r': decimal.Decimal(5.5),
                    ':p': "Everything happens all at once.",
                    ':a': ["Larry", "Moe", "Curly"]
                },
                ReturnValues="UPDATED_NEW"
            )

            itemx = resp.get('Item')
            if not itemx:
                raise ProviderError('Item does not save')

            return itemx
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ProviderError(e.response['Error']['Message'])

    def query_db(self, table_name, proj=None, express=None,keycond=None):
        try:
            resp = self.dynamodb.query(TableName=table_name,
                ProjectionExpression=proj,#"#yr, title, info.genres, info.actors[0]",
                ExpressionAttributeNames=express,#{"#yr": "year"},  # Expression Attribute Names for Projection Expression only.
                KeyConditionExpression=keycond#Key('year').eq(1992) & Key('title').between('A', 'L')
            )

            items = []
            for i in resp[u'Items']:
                items.append(json.dumps(i, cls=DecimalEncoder))

            return items
        except ClientError as e:
            print(e.response['Error']['Message'])
            raise ProviderError(e.response['Error']['Message'])


