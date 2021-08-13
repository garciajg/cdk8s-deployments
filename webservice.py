from constructs import Construct, Node
from imports import k8s
from typing import List, Optional


# Creating a webservice class used to create Kubernetes services
class WebService(Construct):
    def __init__(self, scope: Construct, id: str, *,
                image: str,
                replicas: int = 1,
                port: int = 80,
                container_port: int = 8080,
                variables: Optional[List] = None): # optional list of environment variables
        super().__init__(scope, id)

        label = {'app': Node.of(self).unique_id}

        # Creating the Service class that will be translated to a yaml Kube config file
        k8s.KubeService(self, 'service',
                        spec=k8s.ServiceSpec(
                            type='NodePort',
                            ports=[
                                k8s.ServicePort(port=port, node_port=30080, target_port=k8s.IntOrString.from_number(container_port))
                            ],
                            selector=label
                        )
        )

        # Creating the Deployment class that for Kubernetes
        k8s.KubeDeployment(self, 'deployment',
                          spec=k8s.DeploymentSpec(
                              replicas=replicas,
                              selector=k8s.LabelSelector(match_labels=label),
                              template=k8s.PodTemplateSpec(
                              metadata=k8s.ObjectMeta(labels=label),
                              spec=k8s.PodSpec(
                                containers=[
                                    k8s.Container(
                                        name='app',
                                        image=image,
                                        ports=[
                                            k8s.ContainerPort(container_port=container_port)
                                        ],
                                        env=variables
                                    )
                                ]
                            ))))