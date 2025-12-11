import boto3
import json
import time

def main():
    iam = boto3.client('iam')
    sts = boto3.client('sts')
    
    # Get current account ID
    account_id = sts.get_caller_identity()['Account']
    print(f"Current AWS Account ID: {account_id}")
    
    # Step 1: Create IAM user 'hacker'
    user_name = 'hacker'
    try:
        iam.create_user(UserName=user_name)
        print(f"✓ Created IAM user: {user_name}")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"! User {user_name} already exists")
    
    # Step 2: Create access key for the user
    try:
        access_key_response = iam.create_access_key(UserName=user_name)
        access_key = access_key_response['AccessKey']['AccessKeyId']
        secret_key = access_key_response['AccessKey']['SecretAccessKey']
        print(f"✓ Created access key for {user_name}")
        print(f"  Access Key: {access_key}")
        print(f"  Secret Key: {secret_key}")
    except Exception as e:
        print(f"✗ Error creating access key: {e}")
        return
    
    # Step 3: Create role 'compromised-cie-engineer'
    role_name = 'compromised-cie-engineer'
    
    # Trust policy with AWS:* (allows anyone to assume)
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }
    
    try:
        role_response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy),
            Description='Role with wildcard trust policy for demonstration'
        )
        role_arn = role_response['Role']['Arn']
        print(f"✓ Created role: {role_name}")
        print(f"  Role ARN: {role_arn}")
    except iam.exceptions.EntityAlreadyExistsException:
        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
        print(f"! Role {role_name} already exists")
        print(f"  Role ARN: {role_arn}")
    except Exception as e:
        print(f"✗ Error creating role: {e}")
        return
    
    # Wait for IAM propagation
    print("\n⏳ Waiting for IAM propagation (15 seconds)...")
    time.sleep(15)

    print(f"\n📋 Attempting to assume role with user '{user_name}' credentials...")
    
    max_retries = 5
    retry_delay = 10
    
    for attempt in range(1, max_retries + 1):
        try:
            # Create STS client with the IAM user credentials
            sts_user = boto3.client(
                'sts',
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key
            )
            
            # Assume the role
            assume_role_response = sts_user.assume_role(
                RoleArn=role_arn,
                RoleSessionName='hacker-session'
            )
            
            print(f"✓ Successfully assumed role: {role_name}")
            break
            
        except sts_user.exceptions.ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'InvalidClientTokenId' and attempt < max_retries:
                print(f"⏳ Attempt {attempt}/{max_retries}: Credentials not ready yet, waiting {retry_delay}s...")
                time.sleep(retry_delay)
                continue
            else:
                print(f"✗ Error assuming role: {e}")
                return
        except Exception as e:
            print(f"✗ Error assuming role: {e}")
            return
    else:
        print(f"✗ Failed to assume role after {max_retries} attempts")
        return
    
    try:
        
        # Extract temporary credentials
        temp_credentials = assume_role_response['Credentials']
        
        # Step 6: Get caller identity with assumed role credentials
        sts_assumed = boto3.client(
            'sts',
            aws_access_key_id=temp_credentials['AccessKeyId'],
            aws_secret_access_key=temp_credentials['SecretAccessKey'],
            aws_session_token=temp_credentials['SessionToken']
        )
        
        caller_identity = sts_assumed.get_caller_identity()
        
        print(f"\n✓ STS Get Caller Identity (as assumed role):")
        print(f"  User ID: {caller_identity['UserId']}")
        print(f"  Account: {caller_identity['Account']}")
        print(f"  ARN: {caller_identity['Arn']}")
        
    except Exception as e:
        print(f"✗ Error getting caller identity: {e}")
    
    print("\n" + "="*60)
    print("CLEANUP REMINDER:")
    print(f"  aws iam delete-access-key --user-name {user_name} --access-key-id {access_key}")
    print(f"  aws iam delete-user --user-name {user_name}")
    print(f"  aws iam delete-role --role-name {role_name}")
    print("="*60)

if __name__ == "__main__":
    main()
