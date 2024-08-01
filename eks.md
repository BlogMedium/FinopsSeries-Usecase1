EKS_ADDITIONAL_USER
Create a IAM User in aws console
Make sure you have access key and secret key
image

Check the existing configmap kubectl -n kube-system get configmap aws-auth -o yaml
root@CLDBGDEVMGT0725:~# kubectl -n kube-system get configmap aws-auth -o yaml
apiVersion: v1
data:
  mapRoles: |
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::616259972398:role/eksctl-auth-dev-nodegroup-auth-de-NodeInstanceRole-IU7QZMNLEMOW
      username: system:node:{{EC2PrivateDNSName}}
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::616259972398:role/eksctl-auth-dev-nodegroup-auth-de-NodeInstanceRole-1UZ291L24NZR9
      username: system:node:{{EC2PrivateDNSName}}
kind: ConfigMap
metadata:
  creationTimestamp: "2023-05-09T11:19:27Z"
  name: aws-auth
  namespace: kube-system
  resourceVersion: "5626"
  uid: b739bc5d-fc43-4291-898d-d52ac1083fdf
kubectl -n kube-system edit configmap aws-auth
add

mapUsers: |
    - userarn: arn:aws:iam::616259972398:user/eks_test_user
      username: eks_test_user
      groups:
        - system:masters
Edit file looks like below
 Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: v1
data:
  mapRoles: |
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::616259972398:role/eksctl-auth-dev-nodegroup-auth-de-NodeInstanceRole-IU7QZMNLEMOW
      username: system:node:{{EC2PrivateDNSName}}
    - groups:
      - system:bootstrappers
      - system:nodes
      rolearn: arn:aws:iam::616259972398:role/eksctl-auth-dev-nodegroup-auth-de-NodeInstanceRole-1UZ291L24NZR9
      username: system:node:{{EC2PrivateDNSName}}
  mapUsers: "- userarn: arn:aws:iam::616259972398:user/eks_test_user\n  
  username:
    eks_test_user\n  groups:\n    - system:masters    \n"
kind: ConfigMap
metadata:
  creationTimestamp: "2023-05-09T11:19:27Z"
  name: aws-auth
  namespace: kube-system
  
aws configure --profile eks_test_user
export AWS_PROFILE="eks_test_user"
root@CLDBGDEVMGT0725:~# aws sts get-caller-identity { "UserId": "AIDAY667U5UXMOUYVHU3P", "Account": "616259972398", "Arn": "arn:aws:iam::616259972398:user/eks_test_user" }
Cluster is accessible

root@CLDBGDEVMGT0725:~# kubectl get nodes
NAME                                            STATUS   ROLES    AGE   VERSION
ip-192-168-136-241.us-west-2.compute.internal   Ready    <none>   36m   v1.22.17-eks-a59e1f0
ip-192-168-165-87.us-west-2.compute.internal    Ready    <none>   36m   v1.22.17-eks-a59e1f0
