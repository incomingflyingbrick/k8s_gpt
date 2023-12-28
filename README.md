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
kgpt --install-completion
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

For more possible tasks that the agents can do please checkout [here](./Example_tasks.md)