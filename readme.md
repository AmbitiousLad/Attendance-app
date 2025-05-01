# 🧑‍💼 Cloud-Based Attendance Tracking System

A fully cloud-hosted Python Flask web application to track and manage attendance, deployed using **AWS EC2**, **RDS (MySQL)**, **Launch Templates**, **Auto Scaling Groups**, and **Application Load Balancer (ALB)**. This setup ensures complete automation, scalability, and no reliance on any local development environment.

---

## 🚀 Features

- ✅ User registration and login system
- ✅ Attendance submission and viewing dashboard
- ✅ MySQL RDS backend
- ✅ Modern styled HTML templates
- ✅ Deployed entirely on AWS
- ✅ Auto-scaling with Load Balancer

---

## 🧱 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3
- **Database**: AWS RDS (MySQL)
- **Cloud Infrastructure**: EC2, AMI, Auto Scaling Group, Application Load Balancer

---

## 🗂️ Project Structure

```bash
# 🧑‍💼 Cloud-Based Attendance Tracking System

A fully cloud-hosted Python Flask web application to track and manage attendance, deployed using **AWS EC2**, **RDS (MySQL)**, **Launch Templates**, **Auto Scaling Groups**, and **Application Load Balancer (ALB)**. This setup ensures complete automation, scalability, and no reliance on any local development environment.

---

## 🚀 Features

- ✅ User registration and login system
- ✅ Attendance submission and viewing dashboard
- ✅ MySQL RDS backend
- ✅ Modern styled HTML templates
- ✅ Deployed entirely on AWS
- ✅ Auto-scaling with Load Balancer

---

## 🧱 Tech Stack

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3
- **Database**: AWS RDS (MySQL)
- **Cloud Infrastructure**: EC2, AMI, Auto Scaling Group, Application Load Balancer

---

## 🗂️ Project Structure

```bash
.
└── attendance-app
    ├── app.py
    └── templates
        ├── dashboard.html
        ├── login.html
        ├── register.html
        └── report.html

2 directories, 5 files
```
🛠️ Step-by-Step Setup Instructions
1. 📦 Create MySQL RDS Database
Go to AWS RDS → Create database

Select MySQL (Free tier eligible)

Enable Public access under Connectivity

Set DB name: attendance

Create master username and password

Click "Create database"

Once created, note your RDS endpoint, username, and password

Connect to your RDS instance using MySQL client and create tables:

```
CREATE DATABASE attendance;

USE attendance;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE attendance (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    date DATE DEFAULT CURRENT_DATE,
    status ENUM('present', 'absent') NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```
2. 💻 Launch EC2 Instance and Deploy App
Go to EC2 → Launch Instance

Select Amazon Linux 2 AMI (Free tier eligible)

Choose t2.micro instance type

Configure security group to allow:

SSH (port 22) - for initial setup

HTTP (port 80) - for web traffic

Launch instance with a new key pair

SSH into your instance:

```ssh -i your-key.pem ec2-user@<EC2_PUBLIC_IP>```
Install dependencies:

```
sudo yum update -y
sudo yum install python3 git -y
pip3 install flask pymysql
```
Clone or upload your app:

```
git clone https://github.com/AmbitiousLad/attendance-app.git
cd attendance-app
```

Configure your Flask app (app.py) with RDS details:

```
# Database configuration
app.config['MYSQL_HOST'] = 'your-rds-endpoint.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'your-password'
app.config['MYSQL_DB'] = 'attendance'
```
Run the app:
```
sudo python3 app.py 
```


## Verify it works by visiting http://<EC2_PUBLIC_IP>

3. 🪄 Create AMI
Go to EC2 → Instances

Select your running instance

Actions → Image and templates → Create Image

Name: flask-attendance-ami

Description: "AMI for attendance system"

Click "Create Image"

Wait for AMI to be ready (5-10 minutes)



📄 Create Launch Template
EC2 → Launch Templates → Create launch template

Name: flask-attendance-template

Use the AMI you created

Instance type: t2.micro

Key pair: Select your existing key pair

Security groups: Select the one with HTTP access

Advanced details → User data (paste this to auto-start Flask):

```
#!/bin/bash
cd /home/ec2-user/attendance-app
sudo python3 app.py 
```
Create launch template


5. 🔁 Create Auto Scaling Group (ASG)
EC2 → Auto Scaling Groups → Create

Name: attendance-asg

Select your launch template

Choose VPC and at least 2 subnets

Configure load balancing:

Select "Attach to an existing load balancer"

Choose "Application Load Balancer"

Create new target group

Set group size:

Minimum: 1

Desired: 2

Maximum: 4

Configure scaling policies (optional):

Target tracking policy: CPU utilization at 50%

Create ASG

6. 🌐 Create Application Load Balancer
EC2 → Load Balancers → Create

Choose "Application Load Balancer"

Name: attendance-alb

Scheme: internet-facing

Listeners: HTTP on port 80

Availability Zones: Select at least 2

Security group: Select HTTP-enabled group

Configure routing:

New target group: attendance-target-group

Health check path: /login

Register targets (will be done automatically by ASG)

Create load balancer



7. 🔗 Verify Connectivity
Wait for instances to launch (check EC2 console)

Check Target Group health status (should show healthy instances)

Get your ALB DNS name from Load Balancer description

Access your app at: http://<your-alb-dns-name>








