#!/bin/bash

# Ensure the DST directory exists and fix permissions
if [ ! -d "${STEAMAPPDIR}" ]; then
    echo "ERROR: DST dedicated server directory at ${STEAMAPPDIR} is missing!"
    exit 1
fi

# Create the cluster_token.txt file using the environment variable
if [ -n "${CLUSTER_TOKEN}" ]; then
    echo "${CLUSTER_TOKEN}" > "${HOME}/.klei/DoNotStarveTogether/Cluster_1/cluster_token.txt"
    echo "Cluster token has been set."
else
    echo "ERROR: CLUSTER_TOKEN environment variable is not set!"
    exit 1
fi

# Change to the directory where the DST server binaries are located
cd "${STEAMAPPDIR}/bin"

# Launch the Master (Overworld) shard in a tmux session
tmux new-session -d -s DST-dedicated -n Master \
    "./dontstarve_dedicated_server_nullrenderer -cluster Cluster_1 -shard Master; bash -i"

# Launch the Cave shard in a separate tmux window
tmux new-window -d -n Caves -t DST-dedicated: \
    "./dontstarve_dedicated_server_nullrenderer -cluster Cluster_1 -shard Caves; bash -i"

# Attach to the tmux session (optional, can be useful for debugging)
#tmux attach-session -t DST-dedicated
