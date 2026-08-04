## Task 1.2 — Pod-to-Component Mapping

| Pod Name (from my cluster)         | Kubernetes Component              | Control Plane or Worker Node |
|--------------------------------------|-------------------------------------|--------------------------------|
| kube-apiserver-minikube               | API Server                          | Control Plane                 |
| etcd-minikube                         | etcd                                 | Control Plane                 |
| kube-scheduler-minikube               | Scheduler                            | Control Plane                 |
| kube-controller-manager-minikube      | Controller Manager                   | Control Plane                 |
| kube-proxy-8t6qm                      | kube-proxy                           | Worker Node                   |
| coredns-7d764666f9-d6ld5              | Cluster DNS (supporting add-on)      | Control Plane (in this single-node setup) |
| storage-provisioner                   | Minikube storage add-on              | Not a lecture component        |

### Component NOT appearing as a pod: kubelet (and the container runtime)

The **kubelet** does not appear in this list because it is not itself a containerized workload — it's a 
background agent process that runs directly on the host OS, outside Kubernetes' own pod scheduling. In fact, 
kubelet is what starts every pod listed above, including the control-plane ones (which run as "static pods" 
defined by manifest files that kubelet reads directly from disk, not through the API server).

Similarly, the **container runtime** (Docker/containerd, whichever Minikube uses under the hood) also doesn't 
appear as a pod — it's the underlying engine kubelet calls to actually create and run containers. It's 
infrastructure that pods run on top of, not something Kubernetes itself schedules as a pod.

Note: `storage-provisioner` has restarted once (`RESTARTS: 1`) — this is normal for Minikube on startup and 
not something to worry about.
## Checkpoint Q1
The control plane makes cluster-wide decisions — it stores the desired state (etcd), exposes the API
(API Server), decides which node runs which pod (Scheduler), and detects/corrects drift between desired
and actual state (Controller Manager). Worker nodes are where the actual application pods run; each
worker's kubelet takes instructions from the control plane and starts/stops containers accordingly,
while kube-proxy manages that node's networking rules so traffic reaches the right pods.

## Checkpoint Q2
After deleting the frontend pod and recreating it from the same manifest, `kubectl get pods -o wide`
showed a new IP address different from the original. This happens because Pods are ephemeral —
deleting a Pod destroys that Pod object entirely, and Kubernetes does not "restart" or preserve it.
When the same manifest is applied again, a completely new Pod object is created from scratch, and the
cluster's CNI (container network interface) assigns it a new IP address from the available pool. There
is no guarantee of IP stability across a Pod's lifecycle, which is exactly why Services exist — to give
a stable, unchanging address in front of Pods whose underlying IPs are expected to change.

## Checkpoint Q3
Using the control-loop model: the Deployment's desired state was 3 replicas, stored via its ReplicaSet.
The ReplicaSet controller continuously watches the actual state of the cluster through the API server.
When I deleted one of the three running pods, the actual state dropped to 2 pods, creating a mismatch
against the desired state of 3. The controller detected this gap on its next reconciliation loop (which
runs continuously) and immediately created a new Pod object to close the gap, bringing actual state back
in line with desired state. This entire process took only a few seconds and required no manual
intervention on my part — it demonstrates Kubernetes' self-healing behavior driven entirely by continuous
reconciliation between desired and observed state.

## Checkpoint Q4
Once the database tier is deployed in Part 7, I will be able to scale the frontend without touching it
because each tier (frontend, API, cache, database) is deployed as its own independent Deployment or
StatefulSet, each with its own label selector and replica count. Scaling the frontend Deployment only
affects pods matching the `app: frontend` label — it has no dependency on, or coupling to, the database's
replica count, storage, or lifecycle. This is exactly what the lecture means by each service scaling
independently: the Deployment controller for frontend only manages frontend pods, so increasing or
decreasing its replica count leaves every other tier completely untouched.

## Checkpoint Q5
Port-forward (used in Part 2) creates a temporary tunnel directly to one specific Pod — if that pod is
deleted or replaced, the tunnel breaks immediately since it was bound to that exact Pod's identity. A
Service (used here in Part 5) instead has a stable virtual IP and DNS name, and uses a label selector to
dynamically route traffic to whichever pods currently match `app: frontend`, regardless of their
individual IP addresses. Since Pods are ephemeral and are assigned new IPs whenever they are replaced
(as observed in Checkpoint Q2), Services matter because they provide one stable, unchanging address that
clients can rely on — the Service transparently handles routing to whatever pods are currently healthy
and matching its selector, without clients ever needing to know or track individual pod IPs.

## Checkpoint Q6
Docker Compose has no built-in rolling update mechanism — updating an image typically requires running
`docker compose down` followed by `up`, which takes all replicas offline simultaneously rather than
replacing them gradually with health checks in between. There is no equivalent of Kubernetes'
pod-by-pod, health-checked rollout that keeps the application available throughout the update. Docker
Compose also keeps no revision history, so "rolling back" means manually re-specifying the old image tag
in the compose file and redeploying from scratch — there is no single command to revert to a previous
state the way `kubectl rollout undo` instantly does in Kubernetes, using the revision history it tracks
automatically for every Deployment.

## Checkpoint Q7
Frontend and API are stateless — every replica is interchangeable, pod names use random suffixes, and no
persistent identity or dedicated storage is needed, so a Deployment (which doesn't guarantee stable
naming or ordering) is sufficient and makes horizontal scaling simple. The database is stateful — it
needs a stable, predictable network identity (postgres-0), dedicated persistent storage that survives
pod rescheduling (via a PersistentVolumeClaim tied to that specific ordinal), and ordered, predictable
creation/deletion behavior — all of which only a StatefulSet provides. This matches the lecture's
Stateless vs Stateful comparison: Deployments give random pod names and interchangeable, ephemeral
storage, while StatefulSets give stable, indexed pod names (postgres-0, postgres-1, ...) each bound to
its own persistent volume that follows that specific pod identity across restarts.

## Checkpoint Q8
No — without a PersistentVolumeClaim, a plain Deployment's data lives only in the container's writable
layer, which is tied to that specific pod instance's filesystem. When the pod is deleted and a
replacement is scheduled, it starts with a completely fresh, empty filesystem — all data would be lost
immediately. The PVC decouples storage from the pod's lifecycle: it binds to a PersistentVolume that
exists independently and survives pod deletion, and gets re-attached to the new pod (which reuses the
same stable identity, postgres-0, because it's a StatefulSet). This is exactly what preserved the demo
row in this test — the storage outlived the pod that was deleted.

## Checkpoint Q9
The broken pod showed ErrImagePull, transitioning into ImagePullBackOff. This is not one of the exact
statuses in the lecture's basic Pod Status table (Running/Pending/CrashLoopBackOff/OOMKilled), but it is
the image-pull equivalent of CrashLoopBackOff — Kubernetes attempted to pull a non-existent image tag,
failed, and is now backing off and retrying with increasing delay rather than continuously hammering the
registry with requests. It follows the exact same backoff philosophy as CrashLoopBackOff applies to a
repeatedly crashing container, just triggered by an image-pull failure instead of a container crash.
