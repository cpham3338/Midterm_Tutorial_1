#!/usr/bin/env python
from constructs import Construct
from cdktf import App, TerraformStack, TerraformOutput
from cdktf_cdktf_provider_aws.provider import AwsProvider
from cdktf_cdktf_provider_aws.s3_bucket import S3Bucket, S3BucketWebsite
from cdktf_cdktf_provider_aws import s3_bucket_object, s3_bucket_ownership_controls


class MyStack(TerraformStack):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)


        # Define AWS provider and region
        AwsProvider(self, 'aws', region='us-west-1') 
        
        BUCKET_NAME = 'tutorial1-s3'
        
        s3_bucket = S3Bucket( self, "aws_s3_bucket",            
            bucket=BUCKET_NAME,             
            website=S3BucketWebsite(
                error_document='error.html', index_document='index.html'),
            tags={"Tutorial": "Static Website Host in S3 Bucket"},
            force_destroy=True,
        )   
        
        aws_s3_bucket_ownership_controls_example = s3_bucket_ownership_controls.S3BucketOwnershipControls(self, BUCKET_NAME,
            depends_on=[s3_bucket],
            bucket=BUCKET_NAME,
            rule=s3_bucket_ownership_controls.S3BucketOwnershipControlsRule(
                object_ownership="BucketOwnerEnforced"
            )
        )
        
        s3_bucket_object.S3BucketObject(self, 'upload_file',
            bucket=BUCKET_NAME,
            key="/demo/index.html",
            content_type='text/html',
            source='../index.html',
            depends_on=[s3_bucket])
        
        TerraformOutput(self, "bucket_name", value=s3_bucket.bucket)
        TerraformOutput(self, "bucket_arn", value=s3_bucket.arn)
        TerraformOutput(self, "website_url", value=s3_bucket.website_endpoint)


app = App()
MyStack(app, "demo")

app.synth()
