import time
import boto
import boto.ec2

COUNT = 1
INSTANCE_TYPE = 't1.micro'
EC2_ACCESS_ID = 'AKIAJCVQIOJ3SANYUC4Q'
EC2_SECRET_KEY = '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'
AMI_ID = 'ami-a4f87694'
RSA_PUB = open('~/.ssh/id_rsa.pub').read()

conn = boto.connect_ec2(EC2_ACCESS_ID, EC2_SECRET_KEY)
conn = boto.connect_ec2(EC2_ACCESS_ID, EC2_SECRET_KEY, region=conn.get_all_regions()[4])

# keypair
kp = conn.get_all_key_pairs()[0]
kp.save('gpg_keypair.pem')

sg = conn.get_all_security_groups()
sg_names = [ sg[0].name ]

# start instances
r = conn.run_instances(AMI_ID, min_count=COUNT, max_count=COUNT, key_name=kp.name, security_groups=sg_names, instance_type=INSTANCE_TYPE)

# wait for ready
for i in r.instances:
    while True:
        i.update()
        if i.state == 'running':
            break
            

dns_names = [ i.dns_name for i in r.instances ]

print dns_names, 'running'

# terminate all instances
for i in r.instances():
    i.terminate()
