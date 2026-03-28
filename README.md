🚀 3-Tier Scalable Web Application on AWS
📌 Overview

This project demonstrates the deployment of a highly available and scalable 3-tier architecture on AWS using best practices in cloud networking, security, and monitoring.

The application is designed with clear separation of layers:

Presentation Layer – Application Load Balancer (ALB)
Application Layer – EC2 instances (Auto Scaling Group with Nginx)
Data Layer – Amazon RDS (MySQL)
🏗️ Architecture Flow

Client → ALB → EC2 (Nginx + Application) → RDS (MySQL)

⚙️ Tech Stack
AWS Services: VPC, EC2, ALB, ASG, RDS, IAM, CloudWatch, SNS, NAT Gateway, Internet Gateway
Web Server: Nginx (Reverse Proxy)
Backend: (Add your stack: Python / Node.js / etc.)
Database: MySQL (Amazon RDS)
Version Control: GitHub
🌐 Key Features
Custom VPC with public & private subnets across multiple Availability Zones
Internet Gateway (IGW) for public access
NAT Gateway for secure outbound internet access from private subnets
Application Load Balancer (ALB) for traffic distribution
Auto Scaling Group (ASG) for high availability and fault tolerance
Target Tracking Scaling Policy (50% CPU) for automatic scaling
Amazon RDS (MySQL) deployed in private subnets
IAM Roles for secure access (no hardcoded credentials)
CloudWatch monitoring & alarms
SNS email notifications for alerts
🔐 Security
RDS is not publicly accessible
Database access allowed only from EC2 Security Group
Private subnets used for application and database layers
IAM roles used instead of access keys
📊 Monitoring & Scaling
CloudWatch used for monitoring system metrics
Alarm configured for CPU Utilization > 70%
Auto Scaling configured using Target Tracking (50% CPU)
SNS used for real-time email notifications
🚀 Deployment Steps (High-Level)
Create VPC with public & private subnets
Attach Internet Gateway and configure routing
Create NAT Gateway for private subnet access
Configure Security Groups and IAM roles
Launch Amazon RDS in private subnets
Deploy application on EC2 with Nginx
Create Launch Template / AMI
Configure ALB and Target Group
Create Auto Scaling Group
Set up CloudWatch alarms and SNS notifications
🎯 Learning Outcomes
Hands-on experience with AWS networking (VPC, subnets, routing)
Understanding of high availability and fault tolerance
Implementation of secure cloud architecture
Practical knowledge of Auto Scaling and Load Balancing
Experience with monitoring and alerting systems
🔮 Future Improvements
Add HTTPS using AWS Certificate Manager (ACM)
Implement CI/CD pipeline (GitHub Actions / CodePipeline)
Add caching layer (Redis / ElastiCache)
Improve logging and observability
