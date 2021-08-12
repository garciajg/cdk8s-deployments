#!/usr/bin/env python
from constructs import Construct
from cdk8s import App, Chart
from imports import k8s
from config import (
    PG_ADMIN_EMAIL,
    PG_ADMIN_PASSWORD,
    PG_ADMIN_PORT,
    HELLO_KUB_PORT)
from webservice import WebService


class MyChart(Chart):
    def __init__(self, scope: Construct, id: str):
        super().__init__(scope, id)

        # Hello Kubernetes service
        WebService(
            self,
            "hello",
            image="paulbouwer/hello-kubernetes:1.7",
            replicas=2,
            port=HELLO_KUB_PORT,
            container_port=8000
        )

        # PGAdmin4 required variables
        pg_admin_variables = [
            k8s.EnvVar(
                name="PGADMIN_DEFAULT_EMAIL",
                value=PG_ADMIN_EMAIL    
            ),
            k8s.EnvVar(
                name="PGADMIN_DEFAULT_PASSWORD",
                value=PG_ADMIN_PASSWORD
            )
        ]

        # PGAdmin Kubernetes service
        WebService(
            self,
            "pgadmin4",
            image="dpage/pgadmin4",
            container_port=80,
            port=PG_ADMIN_PORT,
            variables=pg_admin_variables
        )


        


app = App()
MyChart(app, "cdk8s-app")

app.synth()
