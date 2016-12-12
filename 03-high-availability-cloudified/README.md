# Cloudify Mattermost

In other words, run mattermost on AWS using EC2 and RDS.

This Ansible playbook will provision EC2 and RDS instances to take care of web and database needs, and then deploy the Mattermost application onto that brand-new infrastructure environment.


## Control Machine Requirements

Just install the `python-boto` package on your control machine.


## Basic setup

Follow the AWS Setup guide for Ansible here: http://docs.ansible.com/ansible/guide_aws.html

- Set up an IAM user in AWS and securely store the Access Key ID and Secret.
- Create a SSH keypair in your AWS EC2 dashboard. Download that key, change its permissions to 700, and put it into your ~/.ssh/ directory. Remember the name for this keypair; you'll need it to connect to your EC2 instances after you create them.
- Set up authentication for the AWS API in your shell's rc file (probably ~/.bashrc)

    export AWS_ACCESS_KEY_ID='AK123'
    export AWS_SECRET_ACCESS_KEY='abc123'

- Open a new shell to continue in, or source your rc file from your current shell.



## Running the ec2-provisioning script

There are a few gotchas, since AWS is often incredibly slow.

- After provisioning the RDS master instance, the ansible run will fail with an error like "Failed to create replica instance: DB instance is not in the available state". Wait a few minutes until you see that RDS instance come up in your Amazon Console/Dashboard, and then just re-run the Ansible playbook.


## Notes on converting this from a single-machine playbook

- changed 'package' to 'apt', since we are no longer gathering facts for the 'web' playbook (to bootstrap it)
- 'register' sets a host variable. 'set_fact' gives you something you can use like a global variable


## Real-World Application

For larger infrastructure (50+ machines), it can be a pain to do Amazon infrastructure the way I'm doing it here with Ansible. Tying provisioning to deployment/automation can have some complicated failure modes, especially with an agentless system like Ansible. There are hacks that involve creating dynamic inventories using external scripts to look at your Cloud Infrastructure, but that's a slightly more advanced topic than this 'basics' course can cover.

This playbook just serves to show you that there's a way, without getting into prescribing how you should store the state of your infrastructure.

In real life, I'd recommend
- Terraform for provisioning
- Consul for service discovery (tying together your provisioning and your automation)
- Ansible for automation jobs, deployment, and ad-hoc changes (automating *processes for managing state*, not *storing state*)



## Additional Learning Ideas:

##### on your EC2 instance, check that you can connect to RDS (are on the same VPC/subnet) e.g.
psql -h your-postgres-name.az.rds.amazonaws.com -U $DBMASTERUSER $DBNAME


1. Create RDS security group (allow Postgres IN on tcp/5432)
2. Create RDS instance (small is fine)

2. Create a base AMI (mattermost-base) to spawn other images from
    -only install postgresql-client package; server no longer needed
    -create an image from your EC2 instance (name should indicate mattermost version)
    -copy to other Availability Zone

3. Set up ELB
    -round robin

4. Create an autoscaling group
    -launch mattermost ec2 instances (from your template) in both AZs
    -min 1 instance, max 3
    -scale when CPU load is >95% for more than 2 mins.


#### How do we update binaries? -- Blue/Green deployment

1. Create new template (new mattermost version #)
2. Create new autoscaling group with same # of EC2 instances, from new template, under the same load balancer as old one
3. Once the new instances have booted, modify OLD autoscaling group to have 0 instances running (drain traffic)

