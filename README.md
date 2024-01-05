# KGPT
**KGPT**, or **Kubernetes General Purpose Tasker**, is a cutting-edge Kubernetes agent designed to simplify and streamline the management of complex and manual tasks within your Kubernetes cluster. In the dynamic world of container orchestration and cloud-native computing, KGPT emerges as a powerful ally, offering automation and intelligence to help you efficiently handle a wide range of tasks, from deployment and scaling to monitoring and troubleshooting. This innovative agent is engineered to alleviate the burden of manual interventions, enhancing the agility and reliability of your Kubernetes infrastructure. With KGPT at your side, you can confidently navigate the intricate landscape of Kubernetes, ensuring optimal performance and resource utilization while freeing up valuable time for more strategic endeavors.

### Install

#### Prerequisites
- You already setup an k8s cluster locally or on the cloud, and **kubectl** is working normally
- You need **Python** and **pip** installed
- openAI GPT-4 **API key** ready

#### Supported python version 3.8 | 3.9 | 3.10 | 3.11

```commandline 
pip install agentk8s
```

#### Install auto completion (optional)
```commandline
$ kgpt --install-completion
```

### Example
#### 1. call the setup command to enter your GPT-4 api-key
```commandline
kgpt setup
```

#### 2. Now try a few command, like setup an deployment and a service.
```commandline
kgpt chat "create an deployment called mynginx, image name is nginx, three replicas, expose port 80"
```
After a few seconds you should see the following output if everything is executed successfully.

```
user_proxy (to assistant):

exitcode: 0 (execution succeeded)
Code output: 
deployment.apps/mynginx created

service/mynginx exposed
```

#### 3. We can also modify a resource in the cluster, let's change the *mynginx* service target port to 8001

```commandline
kgpt chat "Change mynginx service's target port to 8001"
```

If everything is executed successfully, you should see the following output

```commandline
exitcode: 0 (execution succeeded)
Code output: 
service/mynginx patched
```

#### 4. Now let's delete the resource we just created.
```commandline
kgpt chat "delete mynginx deployment and service"
```
You should be able to see the following output, if everything is executed successfully.

```commandline
user_proxy (to assistant):

exitcode: 0 (execution succeeded)
Code output: 
deployment.apps "mynginx" deleted
service "mynginx" deleted
```
#### 5. You can also chat with a file, just use the *--doc [path or url]* option, let's find how weather there are vulnerability in a k8s yaml (Note you can't execute code when you supplied *--doc* option in RAG enabled mode)

```commandline
kgpt chat "find vulnerability in this k8s yaml file" --doc example_file/deployment1.yaml
```
you should be seeing the following output
```commandline
Intent: Code generation task (to find vulnerability in the provided k8s yaml file).

The provided YAML file has a few issues that could potentially be considered vulnerabilities or misconfigurations:

1. The `image` field does not specify a tag. Using the `latest` tag or not specifying a tag can lead to unpredictable deployments because it's not clear which version of the image is being used. It's better to use a specific version for reproducibility and to avoid accidentally pulling in an updated version with potential vulnerabilities.

2. There are no resource requests or limits specified for the container. This can lead to resource exhaustion on the node where the pod is running, potentially affecting other pods and the stability of the node itself.

3. There is no readiness probe defined. While not necessarily a vulnerability, a readiness probe is important for ensuring that traffic is not sent to a container that isn't ready to handle it.

4. The deployment does not define any security context. Without a security context, the container may run with default settings, which could include running as root, potentially leading to security risks if the container is compromised.

5. The YAML syntax is incorrect. The dashes before `name` and `containerPort` should not be indented.

Please note that the specific values for image version, resource requests, limits, and security context should be adjusted according to the actual requirements and best practices for the application and the organization's security policies.
```
You can also supply kgpt with multiply docs
```commandline
kgpt chat "combine these to yaml into one yaml" --doc example_file/deployment1.yaml --doc example_file/service1.yaml
```

### List of possible tasks
- "create an deployment called mynginx, image name is nginx, three replicas, expose port 80"
- "change mynginx service's target port to 8001"
- "delete mynginx deployment and service"
- "remove all deployment and service in namespace model"
- "watch the status of deployment nginx"
- "list all deployment and service"
- "list all running deployment with more than two replica"
- "create a namespace called test"
- "create a namespace called gpu and change the nginx deployment's namespace to gpu"
- "remove the namespace gpu if no deployment with the namespace gpu"
- "create a docker-registry secret called my-docker-secret, the docker server is mydocker.io usename is vurtne and the password is yqxzv193"

##### For more possible tasks that the agent can do please checkout [here](./Example_tasks.md)